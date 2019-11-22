import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from glob import glob as g


def pltcolor(lst, type):
    cols = []

    if type is "hazard":
        for l in lst:
            l = str(l)
            if l in ["1"]:
                cols.append('red')
            elif l in ["2"]:
                cols.append('orange')
            elif l in ["3"]:
                cols.append('yellow')
            else:
                cols.append('green')
    elif type is "vulnerability":
        for l in lst:
            l = str(l)
            if l in ["11", "12", "13"]:
                cols.append('red')
            elif l in ["14", "20", "21"]:
                cols.append('orange')
            elif l in ["22", "23", "24"]:
                cols.append('yellow')
            else:
                cols.append('green')
    elif type is "sensitivity":
        for l in lst:
            l = str(l)
            if l in ["10"]:
                cols.append('green')
            elif l in ["20"]:
                cols.append('yellow')
            elif l in ["30"]:
                cols.append('orange')
            else:
                cols.append('#CCCCCC')

    return cols
# Create the colors list using the function above


def genMaps(shp, out, title, field,ptype):
    can = gpd.GeoDataFrame.from_file(shp)

    base2 = gpd.GeoDataFrame.from_file(
        "/home/acoto/Dropbox/Bioversity/MAG/extensions/ext_climate/ext_climate/processes/base/CRI_adm0.shp")

    keys = list(can[field].unique())


    cols = pltcolor(keys,ptype)
    cmap = ListedColormap(cols, name='allred')

    base = can.plot(column=field, cmap=cmap)
    base2.plot(ax=base, color='gray', alpha=0.4)

    legend_elements = [Line2D([0], [0], marker='.', color='w', label='Alta', markerfacecolor='r', markersize=15),
                       Line2D([0], [0], marker='.', color='w', label='Media', markerfacecolor='orange', markersize=15),
                       Line2D([0], [0], marker='.', color='w', label='Baja', markerfacecolor='y', markersize=15),
                       Line2D([0], [0], marker='.', color='w', label='Nula', markerfacecolor='g', markersize=15), ]

    plt.legend(handles=legend_elements, loc='lower left')

    plt.grid(True)
    plt.title(title)
    plt.axis('off')

    # plt.show()

    plt.savefig(out)
    print(out)


def my_maps(settings, project):
    shpDir = settings["repository.path"] + "/maps/" + project + "/"
    shapefiles = g(shpDir + "*.shp")
    for shp in shapefiles:
        # try:
        field = ""
        tp, dt, yy, mm = "", "", "", ""
        shp_p = shp.split("/")[-1]
        print(">>>>>>>>"+shp_p)

        if "canton" in shp_p:
            dt = "Cantonal"
        elif "distrito" in shp_p:
            dt = "Distrital"

        if "hazard" in shp_p:
            tp = "Amenaza"
            ptype="hazard"
            field = "classCode"
        elif "sensitivity" in shp_p:
            tp = "Sensibilidad"
            ptype = "sensitivity"
            field = "classCode"
        elif "vulnerability" in shp_p:
            tp = "Vulnerabilidad"
            ptype = "vulnerability"
            field = "comCode"

        if "vulnerability" in shp_p or "hazard" in shp_p:
            yy = shp_p.split("-")[-1][:4]
            mm = shp_p.split("-")[-1][:-4][4:]

            months = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre",
                      "Octubre",
                      "Noviembre", "Diciembre"]
            title = "%s %s para %s del %s" % (tp, dt, months[int(mm)], yy)
        elif "sensitivity" in shp_p:
            title="Sensibilidad %s"%dt
        genMaps(shp, shp[:-3] + "jpg", title, field,ptype )

        # except:
        #    print("erre: "+title)
