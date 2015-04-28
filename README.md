# sling

A utility to apply schema changes to Cassandra

Modeled after flyway*, this is a tool to manage applying changes to Cassandra. Scripts are applied to the database and a hash of the script is saved to a table. This table is queried to see if the change has already been applied or if the source control version has changed.

*flyway does not currently support Cassandra

# Features
Validates applied scripts match source control scripts

Applies new changes to the cluster

Stops on exceptions and discrepancies between database and source control

Reruns failures on next execution by default

Source changes to previously applied changes need to be researched and rectified manually depending on the cause and impact


# Usage
command line 
python sling.py -h -U USERNAME -P PASSWORD -S SERVERS -D DIRECTORY -C CONFIG

-U USERNAME

-P PASSWORD

-S SERVERS key for the cluster list in the pickledb config file

-D DIRECTORY directory with files to apply

-C CONFIG pickledb config file with db connections

-I INFO_ONLY outputs applied and unapplied changes for build


