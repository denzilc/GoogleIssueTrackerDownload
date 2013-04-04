import urllib2
import json
import unicodedata
import time

from datetime import datetime
from MySQL import MySQL

class AndroidIssueTracker():
    """Methods and Data for Android Issue Tracker"""
    db_fields = set()
    issue_labels = set(['Restrict', 'Target', 'SecurityProblem', 'ReportedBy', 'component', 'Component', 'Cat', 'Priority', 'Version', 'SubcomponentOpenGL', 'version', 'Subcomponent', 'Type', 'Regression', 'target'])
    insertQuery = """ INSERT INTO issues(issue_id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, restricted, target, securityProblem, reportedBy, component, cat, priority, version, subcomponentopengl, subcomponent, bugtype, regression, num_comments) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )"""
    insertCommentsQuery = """ INSERT INTO comments(issue_id, comment_id, published, updated, title, content, author, issue_status) VALUES (%s,%s,%s,%s, %s,%s,%s,%s)"""

    

    ''' Initialize permanent variables while instantiating this class. '''
    def __init__(self):
        self.issue_tracker_api_url = 'http://code.google.com/feeds/issues/p/android/issues/full/'
        self.num_comments_feed_url = 'http://code.google.com/feeds/issues/p/android/issues/%s/comments/full?alt=json'
        self.comment_feed_url = 'http://code.google.com/feeds/issues/p/android/issues/%s/comments/full?alt=json&max-results=%s'


    ''' Retrieves the Issue Report given the Issue ID '''
    def get_issue_report(self, issue_id):
        query = self.issue_tracker_api_url + str(issue_id) + '?alt=json'
        request = urllib2.Request(query)
        response = urllib2.urlopen(request)
        text = response.read()
        issue_report = json.loads(text)
        return issue_report['entry']
    
    ''' Retrieves the Number of Comments given the Issue ID '''
    def get_num_comments(self, issue_id):
            query = self.num_comments_feed_url % issue_id
            try:
                request = urllib2.Request(query)
                response = urllib2.urlopen(request)
                text = response.read()
                comment_feed = json.loads(text)
                num_comments = comment_feed['feed']['openSearch$totalResults']['$t']
                return num_comments
            except Exception, e:
                #print query,e 
                pass

    ''' Downloads Android Issue Reports '''
    def download_android_issue_reports(self, start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):

        for issue_id in range(start_issue_id, end_issue_id + 1) :
            try:
                issue_report = self.get_issue_report(issue_id)

                try :
                    num_comments = self.get_num_comments(issue_id)
                except:
                    num_comments = None
                    #print 'No comments '  + str(issue_id)
                    pass
                        
                try:
                    id = issue_report['id']['$t'].strip('http://code.google.com/feeds/issues/p/android/issues/full/')
                    #print id
                except Exception, e:
                    #print 'ID not found' + str(id)
                    pass
            
                try:
                    title = unicodedata.normalize('NFKD', issue_report['title']['$t']).encode('ascii', 'ignore')
                    #print title
                except:
                    title = None
                    #print 'Title not found' + str(id)
                    pass
            
                try :
                    state = issue_report['issues$state']['$t']
                except:
                    state = None
                    #print 'State not foud' + str(id)
                    pass
            
                try :
                    content = unicodedata.normalize('NFKD', issue_report['content']['$t']).encode('ascii', 'ignore')
                    #print content
                except:
                    content = None
                    #print 'Content not found' + str(id)
                    pass
            
                try:
                    stars = issue_report['issues$stars']['$t']
                except:
                    stars = None
                    #print 'Stars not found ' + str(id)
                    pass
            
                try:
                    owner =  issue_report['issues$owner']['issues$username']['$t']
                    #print owner
                except:
                    #print 'Owner not found ' + str(id)
                    owner = None
                    pass
            
                try:
                    blocking = issue_report['issues$blocking'][0]['issue$id']['$t']
                    #print id, blocking
                except:
                    blocking = None
                    #print 'Blocking not found ' + str(id)
                    pass

                try:
                    blockedOn = issue_report['issues$blockedOn'][0]['issue$id']['$t']
                    #print id, blockedOn
                except:
                    blockedOn = None
                    #print 'Blocking not found ' + str(id)
                    pass           
            
                try:
                    updated = datetime.strptime(issue_report['updated']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print updated, type(updated)
                
                except:
                    updated = None
    #                print 'Updated not found ' + str(id)
                    pass
            
                try:
                    status = issue_report['issues$status']['$t']
                    #print status
                except:
                    status = None
                    print 'Status not found ' + str(id)
                    pass
            
                try:
                    closedDate = datetime.strptime(issue_report['issues$closedDate']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print closedDate, type(closedDate)
                except:
                    closedDate = None
                    #print 'Closed date not found ' + str(id)
                    pass
            
                try:
                    mergedInto = issue_report['issues$mergedInto']['issues$id']['$t']
                    #print mergedInto
                except:
                    mergedInto = None
                    #print 'MergedInto not found' + str(id)
                    pass
            
                try:
                    cc = str()
                    names = issue_report['issues$cc']
                    for name in names:
                        cc  = cc + name['issues$username']['$t'] + ','
                    #print cc
                except:
                    #print 'CC not found' + str(id)
                    pass
            
            
                try:
                    author =  issue_report['author'][0]['name']['$t']
                    #print author
                except:
                    author = None
                    #print 'author not found ' + str(id)
                    pass
            
                try:
                    published = datetime.strptime(issue_report['published']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print published, type(published)
                except:
                    published = None
                    #print 'Published date not found ' + str(id)
                    pass  
            
                try :
                    labels = issue_report['issues$label']
    #                print labels

                    restrict = None
                    target = None
                    bugtype = None
                    securityProblem = False
                    reportedBy = None
                    component = None
                    cat = None
                    priority = None
                    version = None
                    subcomponentopengl = None
                    subcomponent = None
                    regression = False
                
                
                    for label in labels:
                        value =  unicodedata.normalize('NFKD', label['$t'].split('-')[0]).encode('ascii', 'ignore')
                        #print value, type(value), value.lower() == 'type'
                    
                        if value.lower() == 'restrict':
                            restrict = label['$t'].split('-')[1]
    #                        print restrict

                    
                        if value.lower() == 'target':
                            target = label['$t'].split('-')[1]
                            #print target       

                        
                        if value.lower() == 'type':
                            bugtype = label['$t'].split('-')[1]
    #                        print type

                        
                        if value.lower() == 'securityproblem':
                            securityProblem  = True
    #                        print  securityProblem


                        if value.lower() == 'reportedby':
                            reportedBy = label['$t'].split('-')[1]
    #                        print reportedBy


                        if value.lower() == 'component':
                            component = label['$t'].split('-')[1]
    #                        print component
                        
                        
                        if value.lower() == 'cat':
                            cat = label['$t'].split('-')[1]
    #                        print cat        


                        if value.lower() == 'priority':
                            priority = label['$t'].split('-')[1]
    #                        print priority    

                        
                        if value.lower() == 'version':
                            version = label['$t'].split('-')[1]
    #                        print version                        


                        if value.lower() == 'subcomponentopengl':
                            subcomponentopengl = False
    #                        print subcomponentopengl
                        
                    
                        if value.lower() == 'subcomponent':
                            subcomponent = label['$t'].split('-')[1]
    #                        print subcomponent      
   

                        if value.lower() == 'regression':
                            regression = True
    #                        print regression'

                                      
                except:
                    #print 'No labels found ' + str(id)
                    pass            
               
        #        issue_query = insertQuery % (id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, restrict, target, securityProblem, reportedBy, component, cat, priority, version, subcomponentopengl, subcomponent, bugtype, regression)
                M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                #print M.host, M.username, M.passwd, M.db, M.port
                connection, cursor = M.create_connection() 
                result = cursor.execute(self.insertQuery, (issue_id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, restrict, target, securityProblem, reportedBy, component, cat, priority, version, subcomponentopengl, subcomponent, bugtype, regression, num_comments))
                M.close_connection(cursor, connection)
            
            except Exception, e:
                #print e
                #print 'Unprocessed - ' +str(issue_id)
                filename = 'android_issues_unprocessed.txt'
                fopen = open(filename, 'a')
                fopen.write(str(issue_id) + '\n')
                fopen.close()



    ''' Download Unprocessed Android Issue Reports '''
    def download_android_unprocessed_issue_reports(self, fptr, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
        lines = fptr.readlines() 
        filename = 'android_issues_unprocessed_' + str(int(time.time())) + '.txt'
        fopen = open(filename, 'a')

        for line in lines :
            issue_id = line.strip()

            try:
                issue_report = self.get_issue_report(issue_id)

                try :
                    num_comments = self.get_num_comments(issue_id)
                except:
                    num_comments = None
                    #print 'No comments '  + str(issue_id)
                    pass
                        
                try:
                    id = issue_report['id']['$t'].strip('http://code.google.com/feeds/issues/p/android/issues/full/')
                    #print id
                except Exception, e:
                    #print 'ID not found' + str(id)
                    pass
            
                try:
                    title = unicodedata.normalize('NFKD', issue_report['title']['$t']).encode('ascii', 'ignore')
                    #print title
                except:
                    title = None
                    #print 'Title not found' + str(id)
                    pass
            
                try :
                    state = issue_report['issues$state']['$t']
                except:
                    state = None
                    #print 'State not foud' + str(id)
                    pass
            
                try :
                    content = unicodedata.normalize('NFKD', issue_report['content']['$t']).encode('ascii', 'ignore')
                    #print content
                except:
                    content = None
                    #print 'Content not found' + str(id)
                    pass
            
                try:
                    stars = issue_report['issues$stars']['$t']
                except:
                    stars = None
                    #print 'Stars not found ' + str(id)
                    pass
            
                try:
                    owner =  issue_report['issues$owner']['issues$username']['$t']
                    #print owner
                except:
                    #print 'Owner not found ' + str(id)
                    owner = None
                    pass
            
                try:
                    blocking = issue_report['issues$blocking'][0]['issue$id']['$t']
                    #print id, blocking
                except:
                    blocking = None
                    #print 'Blocking not found ' + str(id)
                    pass

                try:
                    blockedOn = issue_report['issues$blockedOn'][0]['issue$id']['$t']
                    #print id, blockedOn
                except:
                    blockedOn = None
                    #print 'Blocking not found ' + str(id)
                    pass           
            
                try:
                    updated = datetime.strptime(issue_report['updated']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print updated, type(updated)
                
                except:
                    updated = None
    #                print 'Updated not found ' + str(id)
                    pass
            
                try:
                    status = issue_report['issues$status']['$t']
                    #print status
                except:
                    status = None
                    print 'Status not found ' + str(id)
                    pass
            
                try:
                    closedDate = datetime.strptime(issue_report['issues$closedDate']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print closedDate, type(closedDate)
                except:
                    closedDate = None
                    #print 'Closed date not found ' + str(id)
                    pass
            
                try:
                    mergedInto = issue_report['issues$mergedInto']['issues$id']['$t']
                    #print mergedInto
                except:
                    mergedInto = None
                    #print 'MergedInto not found' + str(id)
                    pass
            
                try:
                    cc = str()
                    names = issue_report['issues$cc']
                    for name in names:
                        cc  = cc + name['issues$username']['$t'] + ','
                    #print cc
                except:
                    #print 'CC not found' + str(id)
                    pass
            
            
                try:
                    author =  issue_report['author'][0]['name']['$t']
                    #print author
                except:
                    author = None
                    #print 'author not found ' + str(id)
                    pass
            
                try:
                    published = datetime.strptime(issue_report['published']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                    #print published, type(published)
                except:
                    published = None
                    #print 'Published date not found ' + str(id)
                    pass  
            
                try :
                    labels = issue_report['issues$label']
    #                print labels

                    restrict = None
                    target = None
                    bugtype = None
                    securityProblem = False
                    reportedBy = None
                    component = None
                    cat = None
                    priority = None
                    version = None
                    subcomponentopengl = None
                    subcomponent = None
                    regression = False
                
                
                    for label in labels:
                        value =  unicodedata.normalize('NFKD', label['$t'].split('-')[0]).encode('ascii', 'ignore')
                        #print value, type(value), value.lower() == 'type'
                    
                        if value.lower() == 'restrict':
                            restrict = label['$t'].split('-')[1]
    #                        print restrict

                    
                        if value.lower() == 'target':
                            target = label['$t'].split('-')[1]
                            #print target       

                        
                        if value.lower() == 'type':
                            bugtype = label['$t'].split('-')[1]
    #                        print type

                        
                        if value.lower() == 'securityproblem':
                            securityProblem  = True
    #                        print  securityProblem


                        if value.lower() == 'reportedby':
                            reportedBy = label['$t'].split('-')[1]
    #                        print reportedBy


                        if value.lower() == 'component':
                            component = label['$t'].split('-')[1]
    #                        print component
                        
                        
                        if value.lower() == 'cat':
                            cat = label['$t'].split('-')[1]
    #                        print cat        


                        if value.lower() == 'priority':
                            priority = label['$t'].split('-')[1]
    #                        print priority    

                        
                        if value.lower() == 'version':
                            version = label['$t'].split('-')[1]
    #                        print version                        


                        if value.lower() == 'subcomponentopengl':
                            subcomponentopengl = False
    #                        print subcomponentopengl
                        
                    
                        if value.lower() == 'subcomponent':
                            subcomponent = label['$t'].split('-')[1]
    #                        print subcomponent      
   

                        if value.lower() == 'regression':
                            regression = True
    #                        print regression'

                                      
                except:
                    #print 'No labels found ' + str(id)
                    pass            
               
        #        issue_query = insertQuery % (id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, restrict, target, securityProblem, reportedBy, component, cat, priority, version, subcomponentopengl, subcomponent, bugtype, regression)
                M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                #print M.host, M.username, M.passwd, M.db, M.port
                connection, cursor = M.create_connection() 
                result = cursor.execute(self.insertQuery, (issue_id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, restrict, target, securityProblem, reportedBy, component, cat, priority, version, subcomponentopengl, subcomponent, bugtype, regression, num_comments))
                M.close_connection(cursor, connection)
            
            except Exception, e:
                #print e
                #print 'Unprocessed - ' +str(issue_id)
                filename = 'android_issues_unprocessed_' + str(int(time.time())) +'.txt'
                fopen = open(filename, 'a')
                fopen.write(str(issue_id) + '\n')
                fopen.close()
        fptr.close()



    ''' Retrieves the comment feed given the issue id '''
    def download_android_comments(self,start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
    
        for issue_id in range(start_issue_id, end_issue_id + 1):
            try:
                num_comments = self.get_num_comments(issue_id)
            
                query = self.comment_feed_url % (issue_id, num_comments)
                request = urllib2.Request(query)
                response = urllib2.urlopen(request)
                text = response.read()
                comment_feed = json.loads(text)
            
                #print num_comments
                comment_entries = comment_feed['feed']['entry']
                for comment_entry in comment_entries:
                
                    try :                    
                        comment_id = comment_entry['id']['$t'].split('http://code.google.com/feeds/issues/p/android/issues/%s/comments/full/' % issue_id)[1]
                        #print issue_id, comment_id
                    except Exception, e:
                        #print e
                        print
                
                    try:
                        published = datetime.strptime(comment_entry['published']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                        #print published
                    except:
                        published = None
                        pass
                
                    try:
                        updated = datetime.strptime(comment_entry['updated']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                        #print updated
                    except:
                        updated = None
                        pass
                
                    try:
                        title = comment_entry['title']['$t']
                        #print title
                    except:
                        title = None
                    
                    
                    try:
                        content = unicodedata.normalize('NFKD', comment_entry['content']['$t']).encode('ascii', 'ignore')
                        #print content
                    except :
                        content = None
                
                    try:
                        author = comment_entry['author'][0]['name']['$t']
                    except:
                        author = None
                    
                    
                    try :
                        issue_status = comment_entry['issues$updates']['issues$status']['$t']
                        #print issue_status
                    except :
                        issue_status = None
                    
                
                    try :
                        M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                        #print M.host, M.username, M.passwd, M.db, M.port
                        connection, cursor = M.create_connection() 
                        result = cursor.execute(self.insertCommentsQuery, (issue_id, comment_id, published, updated, title, content, author, issue_status))
                        M.close_connection(cursor, connection)
                    
                    except Exception, e:
                        #print e
                        #print 'Unprocessed - ' +str(issue_id)
                        filename = 'android_commentsql_unprocessed.txt'
                        fopen = open(filename, 'a')
                        fopen.write(str(issue_id) + '\n')
                        fopen.close()    
                     
            except Exception, e:
                #print e           
                #print 'Unprocessed - ' +str(issue_id)
                filename = 'android_comments_unprocessed.txt'
                fopen = open(filename, 'a')
                fopen.write(str(issue_id) + '\n')
                fopen.close()     
        
    ''' Retrieves the comment feed given the issue id '''
    def download_unprocessed_android_comments(self,fptr, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
        lines = fptr.readlines() 
        filename = 'android_comments_unprocessed_' + str(int(time.time())) + '.txt'
        fopen = open(filename, 'a')
        android_sql_fopen = open('android_comments_sql_unprocessed_' + str(int(time.time())) + '.txt', 'a')


        for line in lines :
            issue_id = line.strip()
            try:
                num_comments = self.get_num_comments(issue_id)
            
                query = self.comment_feed_url % (issue_id, num_comments)
                request = urllib2.Request(query)
                response = urllib2.urlopen(request)
                text = response.read()
                comment_feed = json.loads(text)
            
                #print num_comments
                comment_entries = comment_feed['feed']['entry']
                for comment_entry in comment_entries:
                
                    try :                    
                        comment_id = comment_entry['id']['$t'].split('http://code.google.com/feeds/issues/p/android/issues/%s/comments/full/' % issue_id)[1]
                        #print issue_id, comment_id
                    except Exception, e:
                        #print e
                        print
                
                    try:
                        published = datetime.strptime(comment_entry['published']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                        #print published
                    except:
                        published = None
                        pass
                
                    try:
                        updated = datetime.strptime(comment_entry['updated']['$t'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                        #print updated
                    except:
                        updated = None
                        pass
                
                    try:
                        title = comment_entry['title']['$t']
                        #print title
                    except:
                        title = None
                    
                    
                    try:
                        content = unicodedata.normalize('NFKD', comment_entry['content']['$t']).encode('ascii', 'ignore')
                        #print content
                    except :
                        content = None
                
                    try:
                        author = comment_entry['author'][0]['name']['$t']
                    except:
                        author = None
                    
                    
                    try :
                        issue_status = comment_entry['issues$updates']['issues$status']['$t']
                        #print issue_status
                    except :
                        issue_status = None
                    
                
                    try :
                        M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                        #print M.host, M.username, M.passwd, M.db, M.port
                        connection, cursor = M.create_connection() 
                        result = cursor.execute(self.insertCommentsQuery, (issue_id, comment_id, published, updated, title, content, author, issue_status))
                        M.close_connection(cursor, connection)
                    
                    except Exception, e:
                        #print e
                        #print 'Unprocessed - ' +str(issue_id)
                        android_sql_fopen.write(str(issue_id) + '\n')    
                     
            except Exception, e:
                #print e           
                #print 'Unprocessed - ' +str(issue_id)
                fopen.write(str(issue_id) + '\n')

        fopen.close()  
        android_sql_fopen.close() 