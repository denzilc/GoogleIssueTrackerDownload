from MySQL import MySQL

import urllib2
import json
import unicodedata
from datetime import datetime
import time


''' This class defines all the required methods and data for Chromium Issue Tracker download. '''
class ChromiumIssueTracker() :
    insertCommentsQuery = """ INSERT INTO comments(issue_id, comment_id, published, updated, title, content, author, issue_status, owner_update) VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s)"""
    insertIssueQuery = ''' INSERT INTO `issues`
    (`issue_id`,
    `title`,
    `state`,
    `content`,
    `stars`,
    `owner`,
    `blocking`,
    `blockedOn`,
    `updated`,
    `status`,
    `closedDate`,
    `mergedInto`,
    `cc`,
    `author`,
    `published`,
    `bugtype`,
    `priority`,
    `pri`,
    `os`,
    `area`,
    `feature`,
    `mstone`,
    `releaseBlock`,
    `regression`,
    `performance`,
    `cleanup`,
    `polish`,
    `stability`,
    `crash`,
    `security`,
    `secSeverity`,
    `webkit`,
    `hotlist`,
    `internals`,
    `sev`,
    `secImpacts`,
    `notLabel`,
    `action`,
    `numComments`)
    VALUES
    (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    );
    '''  

    ''' Initialize permanent variables while instantiating this class. '''
    def __init__(self):
        self.issue_tracker_api_url = 'http://code.google.com/feeds/issues/p/chromium/issues/full/'
        self.num_comments_feed_url = 'http://code.google.com/feeds/issues/p/chromium/issues/%s/comments/full?alt=json'
        self.comment_feed_url = 'http://code.google.com/feeds/issues/p/chromium/issues/%s/comments/full?alt=json&max-results=%s'

    ''' Retrieves the Issue Report given the Issue ID '''
    def get_issue_report(self, issue_id):
        query = self.issue_tracker_api_url + str(issue_id) + '?alt=json'
        #print query
        request = urllib2.Request(query)
        response = urllib2.urlopen(request)
        text = response.read()
        issue_report = json.loads(text)
        return issue_report['entry']


    ''' Retrieve the number of comments given the Issue ID '''
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


    ''' Download all issue reports '''        
    def download_chromium_issue_reports(self,start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):        
        
        for issue_id in range(start_issue_id, end_issue_id + 1) :
            try:
                issue_report = self.get_issue_report(issue_id)
                #print issue_report
            
                try :
                    num_comments = self.get_num_comments(issue_id)
                except:
                    num_comments = None
                    print 'No comments '  + str(issue_id)
                    pass
            
                try:
                    id = issue_report['id']['$t'].strip('http://code.google.com/feeds/issues/p/android/issues/full/')
                
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
                    #print state
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
                    #print stars
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
                    #print 'Status not found ' + str(id)
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
                                           
                                           
                try:
                    labels = issue_report['issues$label']
                    feature = str()
                    os = str()
                    webkit = str()
                    notLabel = str()
                    action = str()
                
                    bugtype = None
                    priority = None
                    pri = None
                    area = None
                    mstone = None
                    releaseBlock = None
                    secSeverity = None
                    hotlist = None
                    internals = None
                    sev = None
                    secImpacts = None
                
                    regression = False
                    performance = False
                    cleanup = False
                    polish = False
                    usability = False
                    crash = False
                    security = False
                
                    #print labels
                
                    for label in labels:
                        value =  unicodedata.normalize('NFKD', label['$t'].split('-')[0]).encode('ascii', 'ignore')

                    
                        if value.lower() == 'type':
                            bugtype = label['$t'].split('-')[1]
                            #print bugtype
                  

                        if value.lower() == 'priority':
                            priority = label['$t'].split('-')[1]
                            #print priority    
             

                        if value.lower() == 'pri':
                            pri = label['$t'].split('-')[1]
                            #print pri    
                        

                        if value.lower() == 'os':
                            if os:
                                os = os + ',' + label['$t'].split('-')[1]
                            else:
                                os = label['$t'].split('-')[1]


                        if value.lower() == 'area':
                            area = label['$t'].split('-')[1]
                            #print area, type(area)   

                    
                        if value.lower() == 'feature':
                            if feature:
                                feature = feature + ',' + label['$t'].lower().split('feature-')[1]                                                    
                            else:
                                feature = label['$t'].lower().split('feature-')[1]
                                                

                        if value.lower() == 'mstone':
                            mstone = label['$t'].split('-')[1]
                            #print mstone, type(mstone)   
                        
                    
                        if value.lower() == 'releaseblock':
                            releaseBlock = label['$t'].split('-')[1]
                            #print releaseBlock

                        
                        
                        mod_label = unicodedata.normalize('NFKD', label['$t']).encode('ascii', 'ignore')
                    
                        if mod_label.lower()  == 'type-regression' or mod_label.lower() == "regression":
                            regression = True
                    
                        if mod_label.lower() == "performance" or mod_label.lower() == "type-performance" or mod_label.lower() == "stability-performance":
                            performance = True
                        
                        if mod_label.lower() == "cleanup" or mod_label.lower() == "type-cleanup":
                            cleanup = True
                        
                        if mod_label.lower() == "polish" or mod_label.lower() == "type-polish" or mod_label.lower() == "stability-polish":
                            polish = True
                    
                        if mod_label.lower() == "usability" or mod_label.lower() == "type-usability " or mod_label.lower() == "stability-usability":
                            usability =  True
                        
                        if mod_label.lower() == "crash" or mod_label.lower() == "type-crash" or mod_label.lower() == "stability-crash":
                            crash = True
                        
                        if mod_label.lower() == "security" or mod_label.lower() == "type-security":
                            security = True
            

                        if value.lower() == 'secseverity':
                            secSeverity = label['$t'].split('-')[1]
                            #print issue_id, secSeverity, type(secSeverity)   
                        
                                        
                        if value.lower() == 'webkit':                           
                            if webkit:   
                                webkit = webkit + ',' +  label['$t'].lower().split('webkit-')[1]
                            else:
                                webkit =  label['$t'].lower().split('webkit-')[1]
                    
                        if value.lower() == 'hotlist':
                            hotlist = label['$t'].lower().split('hotlist-')[1]
                    
                        if value.lower() == 'internals':
                            internals = label['$t'].split('Internals-')[1]                    
 
                        if value.lower() == 'sev':
                            sev = label['$t'].split('Sev-')[1]   

                        if value.lower() == 'secimpacts':
                            secImpacts = label['$t'].split('SecImpacts-')[1]   

                        if value.lower() == 'not':                           
                            if notLabel:   
                                notLabel = notLabel + ',' +  label['$t'].lower().split('not-')[1]
                            else:
                                notLabel =  label['$t'].lower().split('not-')[1]                    

                        if value.lower() == 'action':                           
                            if action:   
                                action = action + ',' +  label['$t'].lower().split('action-')[1]
                            else:
                                action =  label['$t'].lower().split('action-')[1] 

                except Exception, e:
                    #print e
                    #print 'No labels found ' + str(id)
                    pass
            

                #print issue_id, action
                M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                #print M.host, M.username, M.passwd, M.db, M.port
                connection, cursor = M.create_connection() 
                result = cursor.execute(self.insertIssueQuery,(issue_id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, bugtype, priority, pri, os, area, feature, mstone, releaseBlock, regression, performance, cleanup, polish, usability, crash, security, secSeverity, webkit, hotlist, internals, sev, secImpacts, notLabel, action, num_comments))
                M.close_connection(cursor, connection)
                
            except Exception, e:
                #print e           
                #print 'Unprocessed - ' +str(issue_id)
                filename = 'chromium_issues_unprocessed.txt'
                fopen = open(filename, 'a')
                fopen.write(str(issue_id) + '\n')
                fopen.close()


    ''' Retrieves the comment feed given the issue id '''
    def download_chromium_comments(self,start_issue_id, end_issue_id, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
    
        for issue_id in range(start_issue_id, end_issue_id + 1):
            time.sleep(2)
            try:
            
                num_comments = self.get_num_comments(issue_id)
                #print type(num_comments)
            
                if num_comments != 0 :
                    query = self.comment_feed_url % (issue_id, num_comments)
                    request = urllib2.Request(query)
                    response = urllib2.urlopen(request)
                    text = response.read()
                    comment_feed = json.loads(text)
                
                    #print num_comments
                    comment_entries = comment_feed['feed']['entry']
                    for comment_entry in comment_entries:
                    
                        try :                    
                            comment_id = comment_entry['id']['$t'].split('http://code.google.com/feeds/issues/p/chromium/issues/%s/comments/full/' % issue_id)[1]
                            #print issue_id, comment_id
                        except Exception, e:
                            print e

                    
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
                            owner_update = comment_entry['issues$updates']['issues$ownerUpdate']['$t']
                            #print owner_update
                        except :
                            owner_update = None
                        
                    
                        try :

                            M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                            #print M.host, M.username, M.passwd, M.db, M.port
                            connection, cursor = M.create_connection() 
                            result = cursor.execute(self.insertCommentsQuery, (issue_id, comment_id, published, updated, title, content, author, issue_status, owner_update))
                            M.close_connection(cursor, connection)
                        
                        except Exception, e:
                            #print e
                            #print 'Unprocessed - ' +str(issue_id)
                            filename = 'chromium_comments_sql_unprocessed.txt'
                            fopen = open(filename, 'a')
                            fopen.write(str(issue_id) + '\n')
                            fopen.close()    
                     
            except Exception, e:
                #print e           
                #print 'Unprocessed - ' +str(issue_id)
                filename = 'chromium_comments_unprocessed.txt'
                fopen = open(filename, 'a')
                fopen.write(str(issue_id) + '\n')
                fopen.close()


    ''' Download unprocessed chromium issue reports '''
    def download_chromium_unprocessed_issue_reports(self, fptr, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
        lines = fptr.readlines() 
        filename = 'chromium_issues_unprocessed_' + str(int(time.time())) + '.txt'
        fopen = open(filename, 'a')

        for line in lines:
            issue_id = line.strip()

            try:
                issue_report = self.get_issue_report(issue_id)
                #print issue_report
            
                try :
                    num_comments = self.get_num_comments(issue_id)
                except:
                    num_comments = None
                    print 'No comments '  + str(issue_id)
                    pass
            
                try:
                    id = issue_report['id']['$t'].strip('http://code.google.com/feeds/issues/p/android/issues/full/')
                
                except Exception, e:
                    print 'ID not found' + str(id)
                    pass
            
                        
                try:
                    title = unicodedata.normalize('NFKD', issue_report['title']['$t']).encode('ascii', 'ignore')
                    #print title
                except:
                    title = None
                    print 'Title not found' + str(id)
                    pass
            
                try :
                    state = issue_report['issues$state']['$t']
                    #print state
                except:
                    state = None
                    print 'State not foud' + str(id)
                    pass
            
                try :
                    content = unicodedata.normalize('NFKD', issue_report['content']['$t']).encode('ascii', 'ignore')
                    #print content
                except:
                    content = None
                    print 'Content not found' + str(id)
                    pass

                try:
                    stars = issue_report['issues$stars']['$t']
                    #print stars
                except:
                    stars = None
                    print 'Stars not found ' + str(id)
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
                    #print 'Status not found ' + str(id)
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
                                           
                                           
                try:
                    labels = issue_report['issues$label']
                    feature = str()
                    os = str()
                    webkit = str()
                    notLabel = str()
                    action = str()
                
                    bugtype = None
                    priority = None
                    pri = None
                    area = None
                    mstone = None
                    releaseBlock = None
                    secSeverity = None
                    hotlist = None
                    internals = None
                    sev = None
                    secImpacts = None
                
                    regression = False
                    performance = False
                    cleanup = False
                    polish = False
                    usability = False
                    crash = False
                    security = False
                
                    print labels
                
                    for label in labels:
                        value =  unicodedata.normalize('NFKD', label['$t'].split('-')[0]).encode('ascii', 'ignore')

                    
                        if value.lower() == 'type':
                            bugtype = label['$t'].split('-')[1]
                            #print bugtype
                  

                        if value.lower() == 'priority':
                            priority = label['$t'].split('-')[1]
                            #print priority    
             

                        if value.lower() == 'pri':
                            pri = label['$t'].split('-')[1]
                            #print pri    
                        

                        if value.lower() == 'os':
                            if os:
                                os = os + ',' + label['$t'].split('-')[1]
                            else:
                                os = label['$t'].split('-')[1]


                        if value.lower() == 'area':
                            area = label['$t'].split('-')[1]
                            #print area, type(area)   

                    
                        if value.lower() == 'feature':
                            if feature:
                                feature = feature + ',' + label['$t'].lower().split('feature-')[1]                                                    
                            else:
                                feature = label['$t'].lower().split('feature-')[1]
                                                

                        if value.lower() == 'mstone':
                            mstone = label['$t'].split('-')[1]
                            #print mstone, type(mstone)   
                        
                    
                        if value.lower() == 'releaseblock':
                            releaseBlock = label['$t'].split('-')[1]
                            #print releaseBlock

                        
                        
                        mod_label = unicodedata.normalize('NFKD', label['$t']).encode('ascii', 'ignore')
                    
                        if mod_label.lower()  == 'type-regression' or mod_label.lower() == "regression":
                            regression = True
                    
                        if mod_label.lower() == "performance" or mod_label.lower() == "type-performance" or mod_label.lower() == "stability-performance":
                            performance = True
                        
                        if mod_label.lower() == "cleanup" or mod_label.lower() == "type-cleanup":
                            cleanup = True
                        
                        if mod_label.lower() == "polish" or mod_label.lower() == "type-polish" or mod_label.lower() == "stability-polish":
                            polish = True
                    
                        if mod_label.lower() == "usability" or mod_label.lower() == "type-usability " or mod_label.lower() == "stability-usability":
                            usability =  True
                        
                        if mod_label.lower() == "crash" or mod_label.lower() == "type-crash" or mod_label.lower() == "stability-crash":
                            crash = True
                        
                        if mod_label.lower() == "security" or mod_label.lower() == "type-security":
                            security = True
            

                        if value.lower() == 'secseverity':
                            secSeverity = label['$t'].split('-')[1]
                            #print issue_id, secSeverity, type(secSeverity)   
                        
                                        
                        if value.lower() == 'webkit':                           
                            if webkit:   
                                webkit = webkit + ',' +  label['$t'].lower().split('webkit-')[1]
                            else:
                                webkit =  label['$t'].lower().split('webkit-')[1]
                    
                        if value.lower() == 'hotlist':
                            hotlist = label['$t'].lower().split('hotlist-')[1]
                    
                        if value.lower() == 'internals':
                            internals = label['$t'].split('Internals-')[1]                    
 
                        if value.lower() == 'sev':
                            sev = label['$t'].split('Sev-')[1]   

                        if value.lower() == 'secimpacts':
                            secImpacts = label['$t'].split('SecImpacts-')[1]   

                        if value.lower() == 'not':                           
                            if notLabel:   
                                notLabel = notLabel + ',' +  label['$t'].lower().split('not-')[1]
                            else:
                                notLabel =  label['$t'].lower().split('not-')[1]                    

                        if value.lower() == 'action':                           
                            if action:   
                                action = action + ',' +  label['$t'].lower().split('action-')[1]
                            else:
                                action =  label['$t'].lower().split('action-')[1] 

                except Exception, e:
                    print e
                    print 'No labels found ' + str(id)
                    pass
            
                print issue_id, action
    
                M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                connection, cursor = M.create_connection() 
                result = cursor.execute(self.insertIssueQuery,(issue_id, title, state, content, stars, owner, blocking, blockedOn, updated, status, closedDate, mergedInto, cc, author, published, bugtype, priority, pri, os, area, feature, mstone, releaseBlock, regression, performance, cleanup, polish, usability, crash, security, secSeverity, webkit, hotlist, internals, sev, secImpacts, notLabel, action, num_comments))
                M.close_connection(cursor, connection)

            except Exception, e:
                print e           
                print 'Unprocessed - ' +str(issue_id)

                fopen.write(str(issue_id) + '\n')
            
        fopen.close()                                               
        fptr.close()


    ''' Downloads the unprocessed chromium comments given the filename '''
    def download_unprocessed_chromium_comments(self,fptr, mysql_host, mysql_username, mysql_password, mysql_database, mysql_port):
       lines = fptr.readlines()
       filename = 'chromium_comments_unprocessed_' + str(int(time.time())) + '.txt'
       fopen = open(filename, 'a')
       chrome_sql_fopen = open('chromium_comments_sql_unprocessed_' + str(int(time.time())) + '.txt', 'a')

       for line in lines:
            issue_id = line.strip()
            time.sleep(2)

            try:
            
                num_comments = self.get_num_comments(issue_id)
                #print type(num_comments)
            
                if num_comments != 0 :
                    query = self.comment_feed_url % (issue_id, num_comments)
                    request = urllib2.Request(query)
                    response = urllib2.urlopen(request)
                    text = response.read()
                    comment_feed = json.loads(text)
                
                    #print num_comments
                    comment_entries = comment_feed['feed']['entry']
                    for comment_entry in comment_entries:
                    
                        try :                    
                            comment_id = comment_entry['id']['$t'].split('http://code.google.com/feeds/issues/p/chromium/issues/%s/comments/full/' % issue_id)[1]
                            #print issue_id, comment_id
                        except Exception, e:
                            print e

                    
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
                            owner_update = comment_entry['issues$updates']['issues$ownerUpdate']['$t']
                            #print owner_update
                        except :
                            owner_update = None
                        
                    
                        try :

                            M = MySQL(mysql_host, mysql_username, mysql_password, mysql_database, mysql_port)
                            #print M.host, M.username, M.passwd, M.db, M.port
                            connection, cursor = M.create_connection() 
                            result = cursor.execute(self.insertCommentsQuery, (issue_id, comment_id, published, updated, title, content, author, issue_status, owner_update))
                            M.close_connection(cursor, connection)
                        
                        except Exception, e:
                            #print e
                            #print 'Unprocessed - ' +str(issue_id)                       
                            chrome_sql_fopen.write(str(issue_id) + '\n')
                                
                     
            except Exception, e:
                #print e           
                #print 'Unprocessed - ' +str(issue_id)
                fopen.write(str(issue_id) + '\n')

       chrome_sql_fopen.close()
       fopen.close()
       fptr.close()
