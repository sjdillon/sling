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

# Using It
Run it as a command line application with the following arguments:

# Usage
usage: python sling.py -h -U USERNAME -P PASSWORD -S SERVERS -D DIRECTORY -C CONFIG

-h, --help show this help message and exit
-U USERNAME, --username USERNAME
-P PASSWORD, --password PASSWORD
-S SERVERS, --servers SERVERS 
key for the cluster list in the pickledb config file
-D DIRECTORY, --directory DIRECTORY	
directory with files to apply
-C CONFIG, --config CONFIG	
pickledb config file with db connections

python sling.py -U <user> -P <pw> -S <servers> -D <path to files>
