CREATE KEYSPACE sling WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};
USE sling;
CREATE TABLE schema_version (
  release text,
  create_dt timestamp,
  filename text,
  hash text,
  hostname text,
  status int,
  username text,
  PRIMARY KEY ((release), create_dt)
) WITH CLUSTERING ORDER BY (create_dt DESC)
