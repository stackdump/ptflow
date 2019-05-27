# Ptflow 

A state-machine eventstore constructed 'blockchain style'.

Construct Markov chains backed by CockroachDB or PostgreSQL databases.

Uses Petri-Nets as state machines to validate events before appending to a eventstore.

Read the original description of this format in the [bitwrap-io whitepaper](https://github.com/bitwrap/bitwrap-io/blob/master/whitepaper.md)

## Why use this library?

Using an eventstore that ensures only valid events are stored is a distinct style choice
that can simplify the design of many types of applications where ledger-driven audits are desirable.

Petri-nets are well explored data structures that have mathematically verifiable properties.

States and transitions are computed as a [Vector addition System with State](https://en.wikipedia.org/wiki/Vector_addition_system)
This vector format makes machine learning analysis of event logs very trivial.

This library is compatible with `.pflow` files produced with a [visual editor](http://www.pneditor.org/)
Once a user is familiar with the basic semantics of a Petri-Net, new process flows can be developed rapidly.

## Status

[![Build Status](https://travis-ci.org/stackdump/ptflow.svg?branch=master)](https://travis-ci.org/stackdump/ptflow)

This eventstore tested in a *development environment only*

* indexes or partitioning should likely be applied when used with PostgreSQL.
* sql is compatible with CockroachDB but again not tested at scale.

## Features

- [x] Creates db schema for PostgreSQL or CockroachDB
- [x] Loads state machines as python classes from source pflow xml documents
- [x] Enforces role declarations w/ pflow
- [x] Enforce inhibitor arcs as guard conditions
- [x] Persists witness sequence of valid events to database
- [x] Stores output state after applying each valid event

### Development

#### pre-reqs

* docker
* docker-compose
* python3

#### Cockroach DB

start
```
docker-compose -f crdb/docker-compose.yml  up -d
```

stop
```
docker-compose -f crdb/docker-compose.yml down
```

connect
```
docker-compose exec roach1 bash -c '/cockroach/cockroach sql --insecure'
```

#### PostgreSQL

```
docker-compose -f pgsql/docker-compose.yml  up -d
```

stop
```
docker-compose -f pgsql/docker-compose.yml down
```

connect
```
docker-compose -f pgsql/docker-compose.yml exec pgsql1 bash -c 'psql -U pflow'
```
