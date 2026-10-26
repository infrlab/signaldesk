"""Small SQLite persistence layer, with parameterized SQL and no network I/O."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

STATUS = ('planned', 'sent', 'replied', 'confirmed', 'closed')
SEED = [
    ('Independent Radio', 'radio', 'planned', '2026-11-02', 'Demo record — not a real contact'),
    ('Northern Culture Magazine', 'press', 'sent', '2026-11-04', 'Demo outreach sent'),
    ('Night Shift Playlist', 'playlist', 'replied', '2026-11-09', 'Demo reply pending'),
    ('Small Room Sessions', 'venue', 'confirmed', None, 'Demo booking confirmed'),
]


def connection(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA busy_timeout=5000')
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA foreign_keys=ON')
    return conn


def initialize(path: str, seed: bool = False) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connection(path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outlet TEXT NOT NULL,
            channel TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            notes TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )""")
        db.execute('CREATE INDEX IF NOT EXISTS ix_contacts_status ON contacts(status)')
        if seed and db.execute('SELECT COUNT(*) FROM contacts').fetchone()[0] == 0:
            now = utc_now()
            db.executemany("""INSERT INTO contacts
                (outlet,channel,status,due_date,notes,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?)""", [(a,b,c,d,e,now,now) for a,b,c,d,e in SEED])


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def get_contact(path: str, contact_id: int) -> dict | None:
    with connection(path) as db:
        row = db.execute('SELECT * FROM contacts WHERE id=?', (contact_id,)).fetchone()
    return dict(row) if row else None


def list_contacts(path: str, status: str | None, q: str, limit: int, offset: int) -> list[dict]:
    filters, args = [], []
    if status:
        filters.append('status=?')
        args.append(status)
    if q:
        filters.append("lower(outlet) LIKE ? ESCAPE '\\'")
        escaped = q.lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        args.append('%'+escaped+'%')
    clause = ' WHERE ' + ' AND '.join(filters) if filters else ''
    with connection(path) as db:
        rows = db.execute('SELECT * FROM contacts' + clause + ' ORDER BY updated_at DESC, id DESC LIMIT ? OFFSET ?', [*args,limit,offset]).fetchall()
    return [dict(row) for row in rows]


def insert_contact(path: str, payload: dict) -> dict:
    now = utc_now()
    with connection(path) as db:
        cur = db.execute("""INSERT INTO contacts (outlet,channel,status,due_date,notes,created_at,updated_at)
            VALUES(?,?,?,?,?,?,?)""", (payload['outlet'].strip(),payload['channel'],payload['status'],payload.get('due_date'),payload['notes'],now,now))
        new_id = cur.lastrowid
    return get_contact(path, new_id)


def patch_contact(path: str, contact_id: int, changes: dict) -> dict | None:
    old = get_contact(path, contact_id)
    if old is None:
        return None
    if not changes:
        return old
    values = {key: (val.strip() if key == 'outlet' else val) for key,val in changes.items()}
    values['updated_at'] = utc_now()
    keys = list(values)
    with connection(path) as db:
        db.execute('UPDATE contacts SET ' + ','.join(key+'=?' for key in keys)+' WHERE id=?', [*(values[key] for key in keys),contact_id])
    return get_contact(path,contact_id)


def delete_contact(path: str, contact_id: int) -> bool:
    with connection(path) as db:
        cur=db.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
    return cur.rowcount>0


def get_summary(path: str) -> dict:
    with connection(path) as db:
        total=db.execute('SELECT COUNT(*) FROM contacts').fetchone()[0]
        counts=dict(db.execute('SELECT status,COUNT(*) FROM contacts GROUP BY status').fetchall())
        overdue=db.execute("SELECT COUNT(*) FROM contacts WHERE due_date < date('now') AND status NOT IN ('confirmed','closed')").fetchone()[0]
    return {'total': total,'by_status':{status:counts.get(status,0) for status in STATUS}, 'overdue': overdue}
