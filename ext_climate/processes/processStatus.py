"""
  @author : acoto
  @since : 16/10/19
  @Description : 
"""
from formshare.models.formshare import FinishedTask
from ..orm.extTask import ExtTask


def ProcessStatus(self, project_id):
    """

    :param self:
    :param project_id:
    :return: 1 error, 0 termino, 2 en proceso, 4 no existe
    """

    result = self.request.dbsession.query(ExtTask).filter(ExtTask.project == project_id).first()

    if result:
        resultB = self.request.dbsession.query(FinishedTask.task_enumber).filter(FinishedTask.task_id==result.id_task).first()
        if resultB is None:
            return 2
        else:
            if resultB.task_enumber == 1:
                return 1
            elif resultB.task_enumber == 0:
                return 0
    else:
        return 4
