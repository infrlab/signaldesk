"""SignalDesk: an API-first, single-origin outreach tracking application."""
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from . import db
from .models import ContactCreate, ContactPatch, Status

BASE = Path(__file__).resolve().parent.parent


def create_app(database_path: str | None = None, read_only: bool | None = None, seed: bool | None = None) -> FastAPI:
    database_path = database_path or os.getenv('DATABASE_PATH', str(BASE / 'data' / 'signaldesk.db'))
    read_only = read_only if read_only is not None else os.getenv('READ_ONLY', 'false').lower() == 'true'
    seed = seed if seed is not None else os.getenv('DEMO_SEED', 'true').lower() == 'true'

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db.initialize(database_path, seed=seed)
        yield

    app=FastAPI(title='SignalDesk API', version='1.0.0', lifespan=lifespan,
                description='Demo outreach tracking for independent music releases. No authentication: do not store real contact data.')
    started=time.monotonic()

    def ensure_writable():
        if read_only:
            raise HTTPException(status_code=403, detail='Public demo is read-only')

    @app.get('/health', tags=['Operations'])
    def health():
        return {'status':'ok', 'service':'signaldesk'}

    @app.get('/ops/metrics', tags=['Operations'])
    def metrics():
        summary=db.get_summary(database_path)
        return {'uptime_seconds':round(time.monotonic()-started,2), 'contacts_total':summary['total'], 'contacts_overdue':summary['overdue']}

    @app.get('/api/contacts', tags=['Contacts'])
    def contacts(status: Status | None = None, q: str = Query('', max_length=120), limit: int = Query(100, ge=1, le=100),offset: int = Query(0, ge=0)):
        return db.list_contacts(database_path,status,q,limit,offset)

    @app.get('/api/contacts/{contact_id}', tags=['Contacts'])
    def contact(contact_id: int):
        existing=db.get_contact(database_path,contact_id)
        if existing is None:
            raise HTTPException(status_code=404,detail='Contact not found')
        return existing

    @app.post('/api/contacts', status_code=201, tags=['Contacts'])
    def create_contact(item: ContactCreate):
        ensure_writable()
        return db.insert_contact(database_path,item.model_dump(mode='json'))

    @app.patch('/api/contacts/{contact_id}', tags=['Contacts'])
    def update_contact(contact_id: int, item: ContactPatch):
        ensure_writable()
        changes=item.model_dump(mode='json',exclude_unset=True)
        if any(val is None for key,val in changes.items() if key != 'due_date'):
            raise HTTPException(status_code=422,detail='Fields except due_date cannot be null')
        result=db.patch_contact(database_path,contact_id,changes)
        if result is None:
            raise HTTPException(status_code=404,detail='Contact not found')
        return result

    @app.delete('/api/contacts/{contact_id}', status_code=204, tags=['Contacts'])
    def remove_contact(contact_id: int):
        ensure_writable()
        if not db.delete_contact(database_path,contact_id):
            raise HTTPException(status_code=404,detail='Contact not found')
        return Response(status_code=204)

    @app.get('/api/summary',tags=['Contacts'])
    def summary():
        return db.get_summary(database_path)

    @app.get('/api/config', tags=['Operations'])
    def config():
        return {'read_only': read_only, 'demo_seed': seed}

    app.mount('/assets',StaticFiles(directory=BASE/'frontend'),name='assets')

    @app.get('/',include_in_schema=False)
    def index():
        return FileResponse(BASE/'frontend'/'index.html')

    return app


app=create_app()
