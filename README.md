Google Issue Tracker Download Tool
==========================

GoogleIssueTrackerDownload is straight forward to use. It downloads the issues from the Issue Tracker into your 
local MySQL database. 

**Pre-Requisites**
+ Python 2.7.3 (will mostly work on other versions, please report if it doesnot work on other versions)
+ argparse
+ mysqldb
+ urllib2

**Features**
+ Takes input from command line as well as files
+ Takes MySQL parameters as command line input
+ Downloads all available information from the Issue Tracker Systems
+ SQL scripts to generate `Chromium` and `Android` issue tracking systems schemas(more support coming soon)
+ Tolerant to Internet Connectivity issues viz. issues not downloaded due to Internet are stored in a file which can later be given as an input 
+ Separates haphazardly available information into neat RDBMS For ex. Chrome does not make readily available the 
"Type of Bug" (regression, stability crash etc.) but available in our tool.

**Usage**

Before using the tool you need to have the database present in the target machine. The SQL scripts to generate the databases are provided in the
repository viz. `chromium_schema.sql` and `android_schema.sql`. Please run these SQL scripts to generate the databases and then run the command-line
tool.

Type `python IssueTracker2Sql.py -h` on your command line for help. 



    python IssueTracker2Sql.py -h
    usage: IssueTracker2Sql.py [-h] [--host HOST] --username USERNAME --password
                           PASSWORD [--port PORT] --database {chrome,android}
                           --meta {issues,comments}
                           (--range START END | --file FILENAME)

    Google Issue Tracker to MySQL database.

    optional arguments:
    -h, --help            show this help message and exit
    --host HOST           The host on which your MySQL database is located.
                        Default Value = localhost
    --username USERNAME   The username of your MySQL database.
    --password PASSWORD   The password to your MySQL database.
    --port PORT           The port on which your MySQL database is available.
                        Defalut Value = 3306
    --database {chrome,android}
                        Name of the MySQL database
    --meta {issues,comments}
                        Meta-data you would want to download : issues OR
                        comments.
    --range START END     You can specify a range of contiguous issue IDs you
                        want to download.
    --file FILENAME       Text File containing a list of Issue IDs, one per
                        line.
