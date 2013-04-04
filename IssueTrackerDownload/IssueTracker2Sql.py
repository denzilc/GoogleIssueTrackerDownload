'''
Created on April 4, 2013

@author: denzilcorrea
'''

import argparse
from ChromiumIssueTracker import ChromiumIssueTracker
from AndroidIssueTracker import AndroidIssueTracker


''' Return the arguments passed from command line while script execution '''
def get_cmdline_args():
    parser = argparse.ArgumentParser(description='Google Issue Tracker to MySQL database.')
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('--host', help = 'The host on which your MySQL database is located. Default Value = localhost', default ='localhost')
    parser.add_argument('--username', help = 'The username of your MySQL database.', required=True)
    parser.add_argument('--password', help = 'The password to your MySQL database.', required=True)
    parser.add_argument('--port', help = 'The port on which your MySQL database is available. Defalut Value = 3306', default = 3306)
    parser.add_argument('--database', choices = ['chrome', 'android'], help = 'Name of the MySQL database', required=True)
    parser.add_argument('--meta', choices = ['issues', 'comments'], help = 'Meta-data you would want to download : issues OR comments.', required = True)
    group.add_argument('--range',metavar=('START', 'END'), nargs = 2, type= int, help = 'You can specify a range of contiguous issue IDs you want to download.')
    group.add_argument('--file', metavar = 'FILENAME', type=argparse.FileType('r'), help = 'Text File containing a list of Issue IDs, one per line.')
    #parser.print_help()
    #parser.print_usage()
    args = parser.parse_args()
    return args
    #parser.parse_args(['-h'])


''' Main Function '''
if __name__ == "__main__":
    args = get_cmdline_args()
    vals = vars(args)
    #print vals

    CT = ChromiumIssueTracker()
    AT = AndroidIssueTracker()

    mysql_host = vals['host']
    mysql_username = vals['username']
    mysql_password = vals['password']
    mysql_port = int(vals['port'])

    metadata = vals['meta']
  

    if vals['database'] == 'chrome':
        mysql_database = 'chromium'
        print 'Welcome to Chromium Issue Tracker Download!'

        if vals['file'] is None:
            #print metadata, mysql_database, mysql_host, mysql_password, mysql_username, start_issue_id, end_issue_id
            start_issue_id = vals['range'][0]
            end_issue_id = vals['range'][1] 

            if metadata == 'issues' :
                ''' Download Chromium Issue Reports'''
                CT.download_chromium_issue_reports(start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

            elif metadata == 'comments':
                ''' Download comments for the Chromium Issue Reports '''
                CT.download_chromium_comments(start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

        else :
            filename = vals['file']
            if metadata == 'issues' :
                CT.download_chromium_unprocessed_issue_reports(filename,mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
            
            elif metadata == 'comments':
                CT.download_unprocessed_chromium_comments(filename,mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

    elif vals['database'] == 'android':
        mysql_database = 'android'
        print 'Welcome to Android Issue Tracker Download!'

        if vals['file'] is None:
            #print metadata, mysql_database, mysql_host, mysql_password, mysql_username, start_issue_id, end_issue_id
            start_issue_id = vals['range'][0]
            end_issue_id = vals['range'][1] 

            if metadata == 'issues' :
                ''' Download Android Issue Reports'''
                AT.download_android_issue_reports(start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

            elif metadata == 'comments':
                ''' Download comments for the Android Issue Reports '''
                AT.download_android_comments(start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

        else :
            filename = vals['file']
            if metadata == 'issues' :
                AT.download_android_unprocessed_issue_reports(filename,mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
            
            elif metadata == 'comments':
                AT.download_unprocessed_android_comments(filename,mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)

           
    else:
        'Uh oh! This is not possible. Please report a bug on the issue tracker.'