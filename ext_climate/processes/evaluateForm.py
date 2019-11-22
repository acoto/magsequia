"""
  @author : acoto
  @since : 18/9/19
  @Description : eval forms for climate
"""
from lxml import etree
from formshare.models.formshare import Odkform

def requiredFields():
    fields = {
        "livestock_repeat": {
            "fields": {
                "livestock_repeat_rowid": {"odktype": ""},
                "live_rep_number": {"odktype": "calculate"},
                "live_name": {"odktype": "select one"},
                "live_label": {"odktype": "calculate"},
                "live_number": {"odktype": "integer"},
                "bee_number": {"odktype": "integer"},
                "tipo_ganaderia": {"odktype": "select one"},
                "tipo_aves": {"odktype": "select one"},
                "tiene_pastos": {"odktype": "select one"},
                "pasto_total": {"odktype": "decimal"},
                "pasto_total_unit": {"odktype": "select one"},
                "pasto_piso": {"odktype": "decimal"},
                "pasto_piso_unit": {"odktype": "select one"},
                "pasto_mejorado": {"odktype": "decimal"},
                "pasto_mejorado_unit": {"odktype": "select one"},
                "pasto_corte": {"odktype": "decimal"},
                "pasto_corte_unit": {"odktype": "select one"},
                "ensilaje": {"odktype": "decimal"},
                "ensilaje_unit": {"odktype": "select one"},
                "fecha_pasto": {"odktype": "date"},
                "rowuuid": {"odktype": ""}

            }
        }, "crop_repeat": {
            "fields": {
                "crop_repeat_rowid": {"odktype": ""},
                "crop_rep_number": {"odktype": "calculate"},
                "crop_name": {"odktype": "select one"},
                "crop_label": {"odktype": "calculate"},
                "crop_planted": {"odktype": "decimal"},
                "crop_yield_units": {"odktype": "select one"},
                "crop_irrigated": {"odktype": "select one"},
                "fecha_siembra": {"odktype": "date"},
                "rowuuid": {"odktype": ""}
            }
        }, "maintable": {
            "fields": {
                "surveyid": {"odktype": ""},
                "originid": {"odktype": ""},
                "_submitted_by": {"odktype": "text"},
                "_xform_id_string": {"odktype": "text"},
                "_submitted_date": {"odktype": "datetime"},
                "_geopoint": {"odktype": "geopoint"},
                "_dummy": {"odktype": "text"},
                "interviewername": {"odktype": "text"},
                "deviceid": {"odktype": "deviceid"},
                "starttime_auto": {"odktype": "start"},
                "starttime_calculated": {"odktype": "calculate"},
                "participation": {"odktype": "select one"},
                "provincia": {"odktype": "select one"},
                "canton": {"odktype": "select one"},
                "distrito": {"odktype": "select one"},
                "caserio_nombre": {"odktype": "text"},
                "respondentname": {"odktype": "text"},
                "i_d": {"odktype": "text"},
                "respondentsex": {"odktype": "select one"},
                "respondent_is_head": {"odktype": "select one"},
                "household_position": {"odktype": "select one"},
                "household_type": {"odktype": "select one"},
                "casa_productor": {"odktype": "select one"},
                "direccion_de_la_casa": {"odktype": "text"},
                "numero_casa": {"odktype": "integer"},
                "numero_movil": {"odktype": "integer"},
                "work_away": {"odktype": "select one"},
                "children_under_4": {"odktype": "integer"},
                "children_4to10": {"odktype": "integer"},
                "children_4to10_educacion": {"odktype": "select one"},
                "males11to24": {"odktype": "integer"},
                "females11to24": {"odktype": "integer"},
                "males25to50": {"odktype": "integer"},
                "females25to50": {"odktype": "integer"},
                "malesover50": {"odktype": "integer"},
                "femalesover50": {"odktype": "integer"},
                "adultsover65": {"odktype": "integer"},
                "adultsover65_pension": {"odktype": "select one"},
                "land_tenure": {"odktype": "select all that apply"},
                "landowned": {"odktype": "decimal"},
                "unitland_owned": {"odktype": "select one"},
                "land_ownership": {"odktype": "select all that apply"},
                "landrentin": {"odktype": "decimal"},
                "unitland_rentin": {"odktype": "select one"},
                "landrentout": {"odktype": "decimal"},
                "unitland_rentout": {"odktype": "select one"},
                "landcultivated": {"odktype": "decimal"},
                "unitland": {"odktype": "select one"},
                "areaunits_other": {"odktype": "text"},
                "agua_finca": {"odktype": "select one"},
                "agua_disponible": {"odktype": "select one"},
                "grow_crops": {"odktype": "select one"},
                "crops": {"odktype": "select all that apply"},
                "crop_count": {"odktype": "calculate"},
                "crops_other1": {"odktype": "text"},
                "crops_other2": {"odktype": "text"},
                "crops_other3": {"odktype": "text"},
                "livestock_owners": {"odktype": "select one"},
                "livestock": {"odktype": "select all that apply"},
                "livestock_count": {"odktype": "calculate"},
                "tiene_ensilaje": {"odktype": "select one"},
                "ensilaje": {"odktype": "decimal"},
                "ensilaje_unit": {"odktype": "select one"},
                "offfarm_incomes_any": {"odktype": "select one"},
                "offfarm_income_ag": {"odktype": "select one"},
                "prop_onfarm": {"odktype": "select one"},
                "prop_crops": {"odktype": "select one"},
                "gps": {"odktype": "geopoint"},
                "endtime_auto": {"odktype": "end"},
                "endtime_calculated": {"odktype": "calculate"},
                "rowuuid": {"odktype": ""}
            }
        }
    }
    return fields


def getFormId(self,schema):
    result=self.request.dbsession.query(Odkform.form_id).filter(Odkform.form_schema==schema).first()

    return result.form_id

def validateForm(create_file):
    myTables = requiredFields()
    tree = etree.parse(create_file)
    root = tree.getroot()

    err = []

    if root.find(".//table[@name='crop_repeat']") is None and root.find(".//table[@name='livestock_repeat']") is None:
        return False, "Este usuario solo puede subir formularios aptos para sequia"

    for k in myTables.keys():
        table = root.find(".//table[@name='" + k + "']")
        if table is not None:
            t_fields = list(myTables[k]["fields"].keys())
            for i in table.iterchildren():
                if i.tag == "field":
                    if i.attrib["name"] in t_fields:
                        t_fields.remove(i.attrib["name"])
                        odktype = myTables[k]["fields"][i.attrib["name"]]["odktype"]
                        if str(i.attrib["odktype"]) != str(odktype):
                            err.append("En el campo %s el tipo de dato debe ser: %s\n" % (i.attrib["name"], odktype))
            if len(t_fields) is not 0:
                err.append("En la tabla %s faltan los siguientes campos: %s\n" % (k, ", ".join(t_fields)))
        else:
            err.append("No se encuentra la tabla: %s\n" % k)

    if len(err) is 0:
        return True, ""
    else:
        return False, " - ".join(err)
