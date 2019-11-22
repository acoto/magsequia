from formshare.plugins.utilities import FormSharePublicView, FormSharePrivateView

from pyramid.httpexceptions import HTTPNotFound

from .processes.getData import formSummary, FormsWithRepo,getSensiMaps
from .processes.updateProducts import updateProducts
from .orm.extTask import ExtTask
from .processes.processStatus import ProcessStatus
from .processes.evaluateForm import getFormId


class MyPublicView(FormSharePublicView):
    def process_view(self):
        return {}


class MyPrivateView(FormSharePrivateView):
    def process_view(self):
        self.set_active_menu("myCustomMenu")
        self.showWelcome = True
        fnames = FormsWithRepo(self)
        settings = {}
        project_details = self.activeProject

        for key, value in self.request.registry.settings.items():
            if isinstance(value, str):
                settings[key] = value
        if "update_products" in self.request.POST:
            task = updateProducts.apply_async(
                (
                    settings,
                    self.request.POST.get("current_proj")
                )
            )
            newExtTask = ExtTask(
                id_task=task.id,
                project=self.request.POST.get("current_proj")
            )

            try:
                self.request.dbsession.add(newExtTask)
                self.request.dbsession.flush()

            except Exception as e:
                self.request.dbsession.rollback()
                return HTTPNotFound

        if not fnames:
            return {"data": False}
        else:
            if "send_forms" in self.request.POST:
                return {"data": formSummary(self, self.request.POST.get("send_forms")), "fnames": fnames,
                        "cur_prj": self.request.POST.get("send_forms"),
                        "formid": getFormId(self,self.request.POST.get("send_forms")),
                        "status": ProcessStatus(self, self.request.POST.get("project_id")),
                        "projectDetails": project_details}
            else:
                return {"data": formSummary(self, fnames[0][1]), "fnames": fnames, "cur_prj": fnames[0][1],
                        "formid": getFormId(self,fnames[0][1]),
                        "status": ProcessStatus(self, self.request.POST.get("project_id")),
                        "projectDetails": project_details}


class PrjStatus(FormSharePrivateView):
    def __init__(self, request):
        FormSharePrivateView.__init__(self, request)
        self.checkCrossPost = False
        self.returnRawViewResult = True

    def process_view(self):

        return {"status": ProcessStatus(self, self.request.POST.get("project_id"))}


class SensiMap(FormSharePrivateView):
    def __init__(self, request):
        FormSharePrivateView.__init__(self, request)
        self.privateOnly = True
        self.checkCrossPost = False
        self.returnRawViewResult = True

    def process_view(self):
        div=self.request.matchdict["div"]
        prj = self.request.matchdict["prj"]
        return getSensiMaps(self, div, prj)