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
-U USERNAME, --username USERNAME	cassandra database login with enough permissions to execute changes in files
-P PASSWORD, --password PASSWORD	user password
-S SERVERS, --servers SERVERS the key for the cluster list in the pickledb config file
-D DIRECTORY, --directory DIRECTORY	directory with files to apply
-C CONFIG, --config CONFIG	pickledb config file with db connections

python sling.py -U <user> -P <pw> -S <servers> -D <path to files>
Examples:
Successful execution of new scripts

::python sling.py -U <user> -P <pw> -S dev -D ..\..\ReleaseScripts\4_1\
[FILE]: 01__sling.cql
[RUNNING]: script has NOT been run already
[FILE]: 02_filestore.cql
[RUNNING]: script has NOT been run already
Execution of scripts already applied to database

::python sling.py -U <user> -P <pw> -S dev -D ..\..\ReleaseScripts\4_1\
[FILE]: 01__sling.cql
[PASS]: confirmed previously run script matches current verion under source control
[FILE]: 02_filestore.cql
[PASS]: confirmed previously run script matches current verion under source control
Execution of scripts previously applied, but source has changed

::python sling.py -U <user> -P <pw> -S dev -D ..\..\ReleaseScripts\4_1\
[FILE]: 01__sling.cql
[EXIT]: script has been run, but source has changed
Failed execution due to syntax

::python sling.py -U <user> -P <pw> -S dev -D ..\..\ReleaseScripts\4_1\
[FILE]: 01__sling.cql
[RUNNING]: script has NOT been run already
[FILE]: 02_filestore.cql
[RUNNING]: script has NOT been run already
[ERROR]: [STOPPING][CQL]: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:0 no viable alternative at input 'xCREATE'">
[ERROR]: [execute_file]: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:0 no viable alternative at input 'xCREATE'">
[ERROR]: [fling]: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:0 no viable alternative at input 'xCREATE'">
[ERROR]: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:0 no viable alternative at input 'xCREATE'">
Info only (-I True) - Prints the details and status information about scripts (applied and unapplied)
::python sling.py -I True -U <user> -P <pw> -S dev -D ..\..\ReleaseScripts\4_1\

+-----------+----------------------------------------+---------------------+----------+
| Release   | Filename                               | ApplyTime           | Status   |
+===========+========================================+=====================+==========+
| 7_2       | 7_2__000__sling.cql                    | 2015-03-11 20:58:12 | Success  |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__00_xxxxxxxxxxxxxxxxxxxxxxxxxx.cql | 2015-03-11 20:59:11 | Success  |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__01_xxxxxxxxx.cql                  | 2015-03-11 20:59:33 | Success  |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__xxxxxxxxxxxxxxxx.cql              | 2015-03-11 20:59:49 | Success  |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__001__sling_add_date_column.cql    | 2015-03-11 21:10:07 | Failed   |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__02_xxxxxxxxxxxxxxxxxxxxx.cql      | 2015-03-18 20:38:29 | Success  |
+-----------+----------------------------------------+---------------------+----------+
| 7_2       | 7_2__99__sling.cql                     |                     | Pending  |
+-----------+----------------------------------------+---------------------+----------+

