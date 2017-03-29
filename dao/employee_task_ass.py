"""Hacky solution to implement a many to many relationship."""
# or a prime example of why we should use sqlalchemy

from __future__ import print_function

from collections import MutableSequence

from task import Task

from rhc.database.db import DB
from rhc.database.dao import DAO


class EmployeeTaskAss(DAO):

    TABLE = 'employee_task_ass'

    FIELDS = (
        'employee_id',
        'task_id',
    )

    FOREIGN = {
        'task':  'task.Task',
        'employee':  'employee.Employee'
    }

    @classmethod
    def get(cls, task_id, employee_id):
        where = 'task_id=%s AND employee_id=%s'
        return cls.query().\
            where(where).execute((task_id, employee_id), one=True)

    @classmethod
    def create(cls, employee, task):
        ass = cls()
        ass.employee_id = employee.id
        ass.task_id = task.id
        ass.save()
        return ass

    def delete(self):
        with DB as cur:
            cur.execute('DELETE from %s where `task_id`=%%s AND'
                        '`employee_id`=%%s' % self.TABLE,
                        (self.task_id, self.employee_id))


class SpecialList(MutableSequence):
    """Container so when we add/remove a we correctly update this ass table."""
    # See: http://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python

    def __init__(self, data=None, parent=None):
        super(SpecialList, self).__init__()
        self.parent = parent
        if (data is not None):
            self._list = list(data)
        else:
            self._list = list()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._list)

    def __len__(self):
            """List length"""
            return len(self._list)

    def __getitem__(self, ii):
        """Get a list item"""
        return self._list[ii]

    def __setitem__(self, ii, val):
        # optional: self._acl_check(val)
        return self._list[ii]

    def insert(self, ii, val):
        # optional: self._acl_check(val)
        self._list.insert(ii, val)

    def __delitem__(self, item):
        """Delete the association when we delete from this list."""
        if isinstance(self.parent, Task):
            ass = EmployeeTaskAss.get(self.parent.id, self._list[item].id)
        else:
            ass = EmployeeTaskAss.get(self._list[item].id, self.parent.id)
        ass.delete()
        del self._list[item]

    def append(self, val, is_co_guarantor=False):
        """Create the association when appending to this list.

        If the association already exist, we will not add to the table.
        """
        if isinstance(self.parent, Task):
            ass = EmployeeTaskAss.get(self.parent.id, val.id)
        else:
            ass = EmployeeTaskAss.get(val.id, self.parent.id)

        if ass is None:
            if isinstance(self.parent, Task):
                EmployeeTaskAss.create(self.parent, val)
            else:
                EmployeeTaskAss.create(val, self.parent)
            self.insert(len(self._list), val)
