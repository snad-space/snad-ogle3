ARG PSQL_VERSION=17
FROM postgres:${PSQL_VERSION}
ARG PSQL_VERSION=17

RUN apt-get update &&\
    apt-get install -y postgresql-server-dev-${PSQL_VERSION} tar bzip2 gzip make gcc

ADD https://github.com/postgrespro/pgsphere/archive/master.tar.gz pgsphere-master.tar.gz
RUN tar -zxf pgsphere-master.tar.gz && \
	cd pgsphere-master && \
	make USE_HEALPIX=0 USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config && \
	make USE_HEALPIX=0 USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config install && \
	cd .. && \
	rm -rf pgsphere-master pgsphere-master.tar.gz

COPY ogle.sql.bz2 /ogle.sql.bz2

COPY docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/

ENV POSTGRES_HOST_AUTH_METHOD trust
