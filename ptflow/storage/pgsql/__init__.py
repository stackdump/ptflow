import os
import json
import uuid
from ptflow.storage.pgsql import sql
from contextlib import contextmanager

class RoleFail(Exception):
    pass

SUPERUSER = '*'
""" role used to bypass all permission checks """

ROOT_UUID = '00000000-0000-0000-0000-000000000000'
""" parent UUID used to initialize a stream """

DEFAULT_SCHEMA = 'base'
""" event schema to use if not provided """

class Storage(object):

    SOURCE_HEADER = "from ptflow.storage.pgsql import Storage"
    """ import line used to include this class in generated code """

    EVENT = sql.EVENT
    """ event table """

    STATE = sql.STATE
    """ state table """

    SQL = sql.sql.SQL
    """ sql formatter """

    cursor = sql.cursor
    """ sql cursor """

    @staticmethod
    def reconnect(**kwargs):
        """ create connection pool """
        if 'dbtype' not in kwargs:
            #dbtype = 'crdb'
            dbtype = os.environ.get('PTFLOW_DB', 'psql')

        sql.reconnect(dbtype)

    @staticmethod
    def drop():
        """ drop evenstore tables """
        with sql.cursor() as cur:
            cur.execute(sql.drop_events)
            cur.execute(sql.drop_states)

    @staticmethod
    def migrate():
        """ create evenstore tables if missing """
        with sql.cursor() as cur:
            cur.execute(sql.create_states)
            cur.execute(sql.create_events)

    def __init__(self, oid=None, schema=None):
        """ set object uuid for storage instance """

        self.cursor = Storage.cursor

        if oid is None:
            self.oid = str(uuid.uuid4())
        else:
            self.oid = oid

        if schema is None:
            self.schema = DEFAULT_SCHEMA
        else:
            self.schema = schema

    def __call__(self, action, **kwargs):
        """ append a new event """

        event_id = str(uuid.uuid4())
        payload = None
        new_state = None
        err = None

        try:
            if 'multiple' in kwargs:
                multiple = int(kwargs['multiple'])
            else:
                multiple = 1

            if 'payload' in kwargs:
                if isinstance(kwargs['payload'], dict):
                    payload = json.dumps(kwargs['payload'])
                else:
                    # already json encoded string
                    payload = kwargs['payload']
            else:
                # cannot be null
                payload = "{}"

            with sql.cursor() as cur:
                cur.execute(sql.get_state, (self.oid, self.schema))
                previous = cur.fetchone()

                if not previous:
                    current_state = self.initial_vector()
                    parent = ROOT_UUID
                else:
                    current_state = previous[2]
                    parent = previous[3]

                new_state, role = self.transform(current_state, action, multiple)

                if role not in kwargs['roles'] and SUPERUSER not in kwargs['roles']:
                    raise RoleFail("Missing Required Role: " + role)

                cur.execute(sql.set_state,
                    (self.oid, self.schema, new_state, event_id, new_state, event_id, self.schema, self.oid)
                )

                cur.execute(sql.append_event,
                    (event_id, self.oid, self.schema, action, multiple, payload, new_state, parent)
                )

        except Exception as x:
            err = x

        return event_id, new_state, err

    def events(self):
        """ list all events """
        with sql.cursor() as cur:
            cur.execute(sql.list_events, (self.oid, self.schema))
            return cur.fetchall()

    def event(self, uuid):
        """ get a single event """
        with sql.cursor() as cur:
            cur.execute(sql.get_event, (uuid, self.schema))
            return cur.fetchone()

    def state(self):
        """ get state """
        with sql.cursor() as cur:
            cur.execute(sql.get_state, (self.oid, self.schema))
            return cur.fetchone()
