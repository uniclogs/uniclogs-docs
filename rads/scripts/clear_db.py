import sys
sys.path.insert(0, '..')
from models import Request, Pass, PassRequest, Session

session = Session()

result = session.query(PassRequest).all()

for r in result:
    session.delete(r)

result = session.query(Request).all()

for r in result:
    session.delete(r)

result = session.query(Pass).all()

for r in result:
    session.delete(r)

session.commit()
session.close()
