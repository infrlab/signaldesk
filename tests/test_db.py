import sqlite3
from pathlib import Path
from backend import db


def test_database_persists_between_connections(tmp_path: Path):
    path=str(tmp_path/'durable.db')
    db.initialize(path,seed=False)
    created=db.insert_contact(path, {'outlet':'Sample Outlet','channel':'press','status':'sent','due_date':None,'notes':'Demo'})
    assert db.get_contact(path,created['id'])['status']=='sent'
    assert db.get_summary(path)['total']==1


def test_seeding_does_not_duplicate_records(tmp_path: Path):
    path=str(tmp_path/'seed.db')
    db.initialize(path,seed=True)
    db.initialize(path,seed=True)
    assert db.get_summary(path)['total']==4


def test_parameterized_sql_does_not_execute_injected_queries(tmp_path: Path):
    path=str(tmp_path/'inject.db')
    db.initialize(path,seed=False)
    dangerous="A'); DROP TABLE contacts; --"
    created=db.insert_contact(path, {'outlet':dangerous,'channel':'press','status':'planned','due_date':None,'notes':''})
    assert db.get_contact(path,created['id'])['outlet']==dangerous
    assert db.get_summary(path)['total']==1
