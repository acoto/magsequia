"""
  @author : acoto
  @since : 25/9/19
  @Description : 
"""

from formshare.models.formshare import Odkform
import numpy as np
from pprint import pprint as p
from glob import glob as g
import base64
import shapefile
from json import dumps


def FormsWithRepo(self):
    result = self.request.dbsession.query(Odkform.form_name, Odkform.form_schema).filter(
        Odkform.project_id == self.activeProject["project_id"]).filter(Odkform.form_schema.isnot(None)).all()
    forms_with_repo = []
    if result is not None:
        for i in result:
            if i.form_schema == self.request.POST.get("send_forms"):
                forms_with_repo.append([i.form_name, i.form_schema, True])
            else:
                forms_with_repo.append([i.form_name, i.form_schema, False])
    else:
        return False

    flag = False
    if forms_with_repo:
        for f in forms_with_repo:
            if f[2] is True:
                flag = True
        if not flag:
            forms_with_repo[0][2] = True
    else:
        return False

    return sorted(forms_with_repo, key=lambda x: int(x[2]), reverse=True)


def sdi(data):
    """ Given a hash { 'species': count } , returns the SDI

    >>> sdi({'a': 10, 'b': 20, 'c': 30,})
    1.0114042647073518"""

    from math import log as ln

    def p(n, N):
        """ Relative abundance """
        if n is 0:
            return 0
        else:
            return (float(n) / N) * ln(float(n) / N)

    N = sum(data.values())

    return -sum(p(n, N) for n in data.values() if n is not 0)


def formSummary(self, fname):
    data = {}

    records = self.request.dbsession.execute("select count(*) as total from %s.maintable" % fname).fetchone()
    data["count"] = records.total  # total de encuestas

    if data["count"] is 0:
        return data

    records = self.request.dbsession.execute(
        "select count(DISTINCT provincia) as prov,count(DISTINCT canton) as cant,count(DISTINCT distrito) as dist  from %s.maintable" % fname).fetchone()
    # numero de cantones, distritos y provincias distintos
    data["prov"] = records.prov
    data["cant"] = records.cant
    data["dist"] = records.dist

    # porcentaje de hombres y de mujeres
    records = self.request.dbsession.execute(
        "select count(respondentsex) as c, respondentsex as s from %s.maintable group by respondentsex" % fname).fetchall()

    for r in records:
        if r.s == "F":
            data["F"] = "%.1f" % (100 / int(data["count"]) * r.c)
        else:
            data["M"] = "%.1f" % (100 / int(data["count"]) * r.c)

    # tipos de fincas
    records = self.request.dbsession.execute(
        "SELECT i_d as id,grow_crops as gc,livestock_owners as lo FROM %s.maintable;" % fname)

    fa = 0  # fincas agricolas
    fg = 0  # fincas ganaderas
    fm = 0  # fincas mixtas
    na = 0  # ninguna de las anteriores
    for r in records:
        if r.gc is "Y" and r.lo is "Y":
            fm += 1
        elif r.gc is "N" and r.lo is "Y":
            fg += 1
        elif r.gc is "Y" and r.lo is "N":
            fa += 1
        else:
            na += 1

    data["fincas"] = {"fm": "%.1f" % (100 / int(data["count"]) * fm), "fg": "%.1f" % (100 / int(data["count"]) * fg),
                      "fa": "%.1f" % (100 / int(data["count"]) * fa), "na": "%.1f" % (100 / int(data["count"]) * na)}

    # saber cuantas fincas son prestadas, alquiladas o propias
    records = self.request.dbsession.execute(
        "select count(m.land_tenure) as ln,l.land_tenure_des as des from %s.maintable as m, %s.lkpland_tenure as l where m.land_tenure = l.land_tenure_cod group by m.land_tenure;" % (
            fname, fname))
    rent = 0
    data["own"] = []

    for r in records:
        if "prestada" in r.des:
            data["own"].append(["Prestadas", "%.1f" % (100 / int(data["count"]) * r.ln)])
        elif "propia" in r.des:
            data["own"].append(["Propias", "%.1f" % (100 / int(data["count"]) * r.ln)])
        else:
            rent += r.ln
    data["own"].append(["Alquiladas", "%.1f" % (100 / int(data["count"]) * rent)])

    records = self.request.dbsession.execute(
        "select DATE(endtime_auto) mydate, count(*) as total from %s.maintable group by mydate order by mydate;" % fname)
    data["n_days"] = []
    data["days"] = []
    for r in records:
        data["n_days"].append(r.total)
        data["days"].append([r.mydate, r.total])
    data["max"] = max(data["n_days"])
    data["mean"] = "%.1f" % (np.mean(data["n_days"]))

    for m in data["days"]:
        if m[1] == data["max"]:
            data["max_date"] = m[0]

    # calc sdi
    records = self.request.dbsession.execute(
        "select m.distrito as d,dc.distrito_des as de, m.crops as c, m.livestock as l from %s.maintable as m, %s.lkpdistrito as dc where m.distrito = dc.distrito_cod;" % (
            fname, fname))

    sdiDict = {}  # sdi por distrito
    sdiGen = {"A": {}, "P": {}, "G": {}}  # sdi clasificado
    distD = {}  # distrito data
    for i in records:
        if i.d not in distD.keys():  # store code and name for each distrito
            distD[i.d] = i.de.title()

        if i.d not in sdiDict.keys():
            sdiDict[i.d] = {}
        if i.c is not None:
            vals = i.c.split(" ")
            for v in vals:
                if v not in sdiDict[i.d].keys():
                    sdiDict[i.d][v] = 0
                    sdiGen["A"][v] = 0
                sdiDict[i.d][v] += 1
                sdiGen["A"][v] += 1
        if i.l is not None:
            vals = i.l.split(" ")
            for v in vals:
                if v not in sdiDict[i.d].keys():
                    sdiDict[i.d][v] = 0
                    sdiGen["P"][v] = 0
                sdiDict[i.d][v] += 1
                sdiGen["P"][v] += 1

    data["sdi"] = []
    for sd in sdiDict:
        data["sdi"].append([distD[sd], sdi(sdiDict[sd])])
    data["sdi"] = sorted(data["sdi"], key=lambda x: int(x[1]), reverse=True)
    data["sdiA"] = "%.2f" % sdi(sdiGen["A"])
    data["sdiP"] = "%.2f" % sdi(sdiGen["P"])

    sdiGen["P"].update(sdiGen["A"])

    data["sdiG"] = "%.2f" % sdi(sdiGen["P"])

    records = self.request.dbsession.execute(
        "SELECT (SELECT COUNT(DISTINCT livestock) FROM %s.maintable_msel_livestock) + (SELECT COUNT(DISTINCT crops) FROM %s.maintable_msel_crops) AS tot, (SELECT COUNT(lkpc.crop_list_cod) FROM %s.lkpcrop_list AS lkpc)+(SELECT COUNT(lkp.livestock_list_cod) FROM %s.lkplivestock_list AS lkp) AS ind;" % (
            fname, fname, fname, fname)).fetchone()
    data["spc"] = "%s / %s" % (str(records.tot), str(records.ind))

    # sensibilidad por distrito data

    records = self.request.dbsession.execute(
        "SELECT idx.distrito AS cod,lkp.distrito_des AS des, idx.idxdist AS ind FROM %s.lkpdistrito as lkp,%s.idxdist_view as idx WHERE lkp.distrito_cod=idx.distrito ORDER BY ind ASC;" % (
            fname, fname))

    data["sensi"] = {}
    for row in records:
        data["sensi"][row.cod] = {"name": row.des, "ind": row.ind, "ndvi": row.ind}

    # p(data)

    data["maps_v"] = []
    data["maps_h"] = []


    imgs = g(self.request.registry.settings.get("repository.path", "") + "maps/%s/*jpg" % fname)
    for i_path in imgs:
        if "sensitivity" not in i_path:
            with open(i_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            title = ""
            tp, dt, yy, mm = "", "", "", ""
            shp_p = i_path.split("/")[-1]
            if "canton" in shp_p:
                dt = "Cantonal"
            elif "distrito" in shp_p:
                dt = "Distrital"

            if "hazard" in shp_p:
                tp = "Amenaza"
            elif "sensitivity" in shp_p:
                tp = "Sensibilidad"
            elif "vulnerability" in shp_p:
                tp = "Vulnerabilidad"

            yy = shp_p.split("-")[-1][:4]
            mm = shp_p.split("-")[-1][:-4][4:]

            months = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre",
                      "Octubre",
                      "Noviembre", "Diciembre"]
            title = "%s %s para %s del %s" % (tp, dt, months[int(mm)], yy)
            val = ["data:image/jpg;base64,%s" % encoded_string.decode("utf-8"), i_path.split("/")[-1], title]
            if tp == "Amenaza":
                data["maps_h"].append(val)
            if tp == "Vulnerabilidad":
                data["maps_v"].append(val)


    return data

def getSensiMaps(self, div, prj):
    if div =="c":
        i_path = self.request.registry.settings.get("repository.path", "") + "maps/%s/sensitivity-canton.shp" % prj
    elif div=="d":
        i_path = self.request.registry.settings.get("repository.path", "") + "maps/%s/sensitivity-distrito.shp" % prj


    reader = shapefile.Reader(i_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    return {"type": "FeatureCollection", "features": buffer}
