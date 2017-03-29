'''Define all models for this little example.

Things to read
    Tutorial: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
    Relationships: http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    MySQL Dialect: http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
    Testing: http://alextechrants.blogspot.com/2014/01/unit-testing-sqlalchemy-apps-part-2.html
'''

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func

Base = declarative_base()


# Ass Tables
employee_task_association = Table('employee_task_ass', Base.metadata,
    Column('employee_id', INTEGER(unsigned=True), ForeignKey('employee.id')),
    Column('task_id', INTEGER(unsigned=True), ForeignKey('task.id'))
)


class Employee(Base):
    '''Minion.'''
    __tablename__ = 'employee'

    # Columns
    id = Column(INTEGER(unsigned=True), primary_key=True)
    created_at = Column(DATETIME, default=func.now())
    last_modified = Column(DATETIME, onupdate=func.utc_timestamp())
    name = Column(VARCHAR(255, collation='utf8mb4_unicode_ci'))
    team_id = Column(INTEGER(unsigned=True), ForeignKey('team.id'))

    # Relationships
    # relationship(ClassName, attribute of that class to update)
    ssn = relationship('Ssn', back_populates='employee', uselist=False)  # 1-1
    team = relationship('Team', back_populates='members')  # many-1
    tasks = relationship('Task',
                         secondary=employee_task_association,
                         back_populates='employees')  # many-many

    def __repr__(self):
        return '<Employee(name=%s)>' % self.name


class Ssn(Base):
    '''Minion.'''
    __tablename__ = 'ssn'

    # Columns
    id = Column(INTEGER(unsigned=True), primary_key=True)  # autoincrements by default
    created_at = Column(DATETIME, default=func.now())
    last_modified = Column(DATETIME, onupdate=func.utc_timestamp())
    value = Column(INTEGER(unsigned=True))
    employee_id = Column(INTEGER(unsigned=True), ForeignKey('employee.id'))

    # Relationships 1-1
    employee = relationship('Employee', back_populates='ssn', uselist=False)

    def __repr__(self):
        return '<Ssn(value=%s)>' % self.value


class Team(Base):
    '''Group of minions.'''
    __tablename__ = 'team'

    # Columns
    id = Column(INTEGER(unsigned=True), primary_key=True)
    created_at = Column(DATETIME, default=func.now())
    last_modified = Column(DATETIME, onupdate=func.utc_timestamp())
    name = Column(VARCHAR(255, collation='utf8mb4_unicode_ci'))

    # Relationships
    members = relationship('Employee', back_populates='team')  # 1-many

    def __repr__(self):
        return '<Team(name=%s)>' % self.name


class Task(Base):
    '''Stuff to do.'''
    __tablename__ = 'task'

    # Columns
    id = Column(INTEGER(unsigned=True), primary_key=True)
    created_at = Column(DATETIME, default=func.now())
    last_modified = Column(DATETIME, onupdate=func.utc_timestamp())
    name = Column(VARCHAR(255, collation='utf8mb4_unicode_ci'))

    # Relationships
    employees = relationship('Employee',
                             secondary=employee_task_association,
                             back_populates='tasks')  # many-many

    def __repr__(self):
        return '<Task(name=%s)>' % self.name
