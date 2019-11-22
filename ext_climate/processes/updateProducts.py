"""
  @author : acoto
  @since : 10/10/19
  @Description : 
"""
from .gen_maps_distritos import main as dist_m
from .gen_maps_cantones import main as cant_m
from .gen_maps_img import my_maps

from formshare.config.celery_class import CeleryTask
from formshare.config.celery_app import celeryApp
import shutil

@celeryApp.task(base=CeleryTask)
def updateProducts(settings, project):
    #try:
    #    shutil.rmtree(settings["repository.path"] +"/maps/"+project+"/")
    #except:
    #    pass
    #dist_m(settings, project)
    #cant_m(settings, project)
    my_maps(settings, project)




