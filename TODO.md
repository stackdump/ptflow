### WIP

support pflow import of petri-nets

WIP
---
- [ ] add travis

BACKLOG
--------
- [ ] run all unit tests
- [ ] default to postgres on travis

ICEBOX
------
- [ ] support leveldb
- [ ] support bigquery

COMPLETE
--------
- [x] always format uuids
- [x] add last event-id to state
- [x] role enforcement
- [x] change event stream to store new state as part of event
- [x] enforce guard conditions
- [x] load state machines python in-mem from pflow documents
- [x] role declarations w/ pflow
- [x] inhibitor support as guard declaration
- [x] change event stream to include schema + timestamp
- [x] create eventstore in cockroachdb
- [x] connect state machine w/ eventstore
- [x] try compatiblity w/ standard postgres (no multiple schemata)
- [x] finish pflow parser
