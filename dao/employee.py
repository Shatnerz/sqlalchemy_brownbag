from rhc.database.dao import DAO

from employee_task_ass import SpecialList


# Look at vesuvius application and guarantors.
# Many-to-many is a bit of a mess.
# One to one is just a hack on the CHILDREN field

class Employee(DAO):

    TABLE = 'employee'

    FIELDS = (
        'id',
        'name'
        'team_id'
    )

    CHILDREN = {
        'employee_asses': 'employee_task_ass.EmployeeTaskAss'
    }

    def __repr__(self):
        return "<EmployeeDAO(%s)>" % (self.name)

    def _get_task_list(self):
        try:
            self = self.load(self.id)  # refresh
            task_list = self._task_list
            if len(task_list) != len(self.employee_asses):
                raise Exception('Gets me to the except statement')
            else:
                return task_list
        except:
            self._task_list = SpecialList(parent=self)
            self._task_list._list = [ass.task for ass in self.employee_asses]
            return self._app_list

    @property
    def tasks(self):
        return self._get_task_list()
