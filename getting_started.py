"""Set things up to get going for a live(ish) demo."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, Employee, Ssn, Team, Task


# Setup Engine
engine = create_engine('mysql://test:123@localhost:3306/sqlalchemy_demo')

# Create schema based on the models.
# This won't rewrite or remove any data. Old schemas won't be updated.
Base.metadata.create_all(engine)

# We can mess with out models without a DB connection
ateam = Team(name='The A-Team')
vee = Employee(name='Vebdev the Webdev')
dilly_dally = Task(name='Dilly Dally')
vee.team = ateam
vee.ssn = Ssn(value=123456789)
vee.tasks.append(dilly_dally)
# note id, create_at, and last_modified are currently empty


# Creating a session
Session = sessionmaker(bind=engine)
session = Session()
session.add(vee)
session.query(Employee).filter_by(name='Vebdev the Webdev').first()
# still no id and nothing in the db

session.commit()
# after the commit id, created_at, and last_modified are accessible

# session1 = Session()
# session2 = Session()
# vee1 = session1.query(Employee).filter_by(name='Vebdev the Webdev').first()
# vee2 = session2.query(Employee).filter_by(name='Vebdev the Webdev').first()
