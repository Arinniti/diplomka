from datetime import date
from dp.analytic_settings import *

class EVM:
    def __init__(self):
        self.ev = None
        self.ac = None
        self.pv = None

        self.cpi = None
        self.spi = None
        self.eac = None
        self.etc = None

    def calculate_for_project(self, project_instance):
        project = project_instance
        plan_daily_cost = "Not set"
        actual_daily_cost = "Not set"
        days_past = "Not set"
        if project.deadline and project.start_date:
            days = project.deadline - project.start_date
            days = days.days

            plan_daily_cost = project.plan_budget / days
            plan_daily_cost = (round(plan_daily_cost, 2))

            today = date.today()
            days_past = today - project.start_date
            days_past = days_past.days

            self.ev = project.progress * project.plan_budget
            self.ac = project.used_budget
            self.pv = plan_daily_cost * days_past

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
    result += RISK_OK_POINTS if project.risk() < RISK_APPETITE else RISK_NOT_OK_POINTS
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
    if project_evm.cpi > CPI_POSITIVE_HIGH:
        result += CPI_POSITIVE_HIGH_POINTS
    elif project_evm.cpi > CPI_POSITIVE:
        result += CPI_POSITIVE_POINTS
    elif project_evm.cpi > CPI_NEGATIVE:
        result += CPI_NEGATIVE_POINTS
    else:
        result += CPI_NEGATIVE_HIGH_POINTS


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


