from datetime import date

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
