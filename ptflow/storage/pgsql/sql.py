from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import sql

EVENT = sql.Identifier('events')
""" events table """

STATE = sql.Identifier('states')
""" states table """

_pool = None
""" connection _pool """

@contextmanager
def cursor():
    """ cursor context helper """
    conn = _pool.getconn()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        _pool.putconn(conn)
        #_pool.closeall()

def _connect_crdb(**kwargs):
    """ create cockroachdb connection pool """
    return ThreadedConnectionPool( 2, 20,
        host=kwargs['pghost'],
        user=kwargs['pgusername'],
        dbname=kwargs['pgdatabase'],
        #password=kwargs['pgpassword'],
        port=26257,
        sslmode='disable',
    )

    return db_pool

def _connect_pgsql(**kwargs):
    """ create postgres connection pool """
    return ThreadedConnectionPool( 2, 20,
        host=kwargs['pghost'],
        user=kwargs['pgusername'],
        dbname=kwargs['pgdatabase'],
        password=kwargs['pgpassword'],
        port=5432,
    )

    return dbpool

def reconnect(dbtype='crdb'):
    """ recreate db connection pool """
    global _pool

    if dbtype == 'crdb':
        _pool = _connect_crdb(
            pghost='localhost',
            pgusername='root',
            pgdatabase='defaultdb'
        )
    else:
        _pool = _connect_pgsql(
            pghost='localhost',
            pgusername='pflow',
            pgpassword='pflow',
            pgdatabase='pflow'
        )

    return _pool

_drop = sql.SQL("""
DROP TABLE IF EXISTS {}
""")

drop_events = _drop.format(EVENT)
drop_states = _drop.format(STATE)

create_events = sql.SQL("""
CREATE TABLE IF NOT EXISTS {} (
    id UUID,
    schema VARCHAR DEFAULT '',
    action VARCHAR,
    multiple INT,
    payload JSONB NOT NULL,
    state INT[],
    ts TIMESTAMP DEFAULT now(),
    uuid UUID,
    parent UUID,
    PRIMARY KEY (id, schema, ts)
)
""").format(EVENT)

append_event = sql.SQL("""
INSERT INTO {}
    (uuid, id, schema, action, multiple, payload, state, parent, ts)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, now())
""").format(EVENT)

list_events = sql.SQL("""
SELECT * FROM {}
WHERE
    id = %s 
AND
    schema = %s 
""").format(EVENT)

get_event = sql.SQL("""
SELECT * FROM {}
WHERE
    uuid = %s 
AND
    schema = %s 
""").format(EVENT)

create_states = sql.SQL("""
CREATE TABLE IF NOT EXISTS {} (
    id UUID,
    schema VARCHAR DEFAULT '',
    state INT[],
    head UUID,
    created TIMESTAMP default now(),
    updated TIMESTAMP ,
    PRIMARY KEY (id, schema)
)
""").format(STATE)

set_state = sql.SQL("""
INSERT INTO {}
    (id, schema, state, head, updated)
VALUES (%s, %s, %s, %s, now())
ON CONFLICT(id, schema) DO
    UPDATE SET state = %s, head = %s
WHERE
    excluded.schema = %s 
AND
    excluded.id = %s 
""").format(STATE)

get_state = sql.SQL("""
SELECT * FROM {}
WHERE
    id = %s 
AND
    schema = %s 
""").format(STATE)
