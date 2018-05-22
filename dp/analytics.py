from datetime import date
from dp.analytic_settings import *

class EVMTask:
    def __init__(self):
        self.ev = 0
        self.ac = 0
        self.pv = 0

    def calculate_for_task(self, tast_instance):
        task = tast_instance
        emps = task.assignedtask_set.count()

        if task.deadline and task.start_date and task.state=='2':
            days_plan = task.deadline - task.start_date
            days_plan = days_plan.days * emps

            today = date.today()
            days_past = today - task.start_date
            days_past = days_past.days * emps

            self.ev = (round(task.progress * days_plan, 0))
            self.ac = days_past
            self.pv = days_plan

    @staticmethod
    def new_instance(tast_instance):
        ins = EVMTask()
        ins.calculate_for_task(tast_instance)
        return ins





class EVM:
    def __init__(self):
        self.ev = 0
        self.ac = 0
        self.pv = 0

        self.cpi = 0
        self.spi = 0
        self.eac = 0
        self.etc = 0

    def calculate_for_project(self, project_instance):
        project = project_instance
        if project.deadline and project.start_date and project.state == '2':
            for task in project.task_set.all():
                self.ev = self.ev + task.evmtask().ev
                self.pv = self.pv + task.evmtask().pv
                self.ac = self.ac + task.evmtask().ac

            if self.ev is not 0:
                self.cpi = (round(self.ev / self.ac, 2))
                self.spi = (round(self.ev / self.pv, 2))
                self.eac = (round(project.plan_budget / self.cpi, 2))
                self.etc = self.eac - self.ac

    @staticmethod
    def new_instance(project_instance):
        ins = EVM()
        ins.calculate_for_project(project_instance)
        return ins

def optimization(project, org_strategy):
    result = 0

    result += COMPLEXITY_LOW_POINTS if project.complexity == '0' else COMPLEXITY_HIGH_POINTS
    is_strategic = check_if_strategic(project, org_strategy)
    result += IS_STRATEGIC_POINTS if is_strategic else ISNT_STRATEGIC_POINTS

    if project.progress >= PROGRESS_HIGH:
        result += PROGRESS_HIGH_POINTS
    elif project.progress <= PROGRESS_MODERATE:
        result += PROGRESS_LOW_POINTS
    else:
        result += PROGRESS_MODERATE_POINTS

    if project.state == '2' or project.state == '4':
        res_tmp = calculate_ongoing_proj_score(project)
        result += res_tmp
    return result


def calculate_ongoing_proj_score(project):
    result = 0
    if project.importance == '1':
        if project.urgency == '1':
            result += URG_IMP_POINTS
        else:
            result += NOT_URG_IMP_POINTS
    else:
        if project.urgency == '1':
            result += URG_NOT_IMP_POINTS
        else:
            result += NOT_URG_NOT_IMP_POINTS

    project_evm = project.evm()
    if project_evm.cpi >= 1:
        if project_evm.spi >= 1:
            result += CPI_SPI_POINTS
        elif project_evm.spi < 1:
            result += CPI_NOT_SPI_POINTS
    else:
        if project_evm.spi >= 1:
            result += NOT_CPI_SPI_POINTS
        elif project_evm.spi < 1:
            result += NOT_CPI_NOT_SPI_POINTS

    return result

def check_if_strategic(project, org_strategy):
    if not project.portfolio:
        for value in project.projectstrategy_set.all():
            res = org_strategy.filter(strategy=value.strategy.id).all()
            if res:
                return True
    else:
        for value in project.projectstrategy_set.all():
            res = project.portfolio.portfoliostrategy_set.filter(strategy=value.strategy.id).all()
            if res:
                return True
    return False


