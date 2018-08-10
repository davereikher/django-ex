'''
Used to access an Oracle DB
'''
import cx_Oracle
from . import secret
import collections, datetime
import pandas as pd
ownerLog = 'ATLAS_MUON_NSW_MM_LOG'

class db:
        def __init__(self, tunnel=False, production=False):
                '''
                - Currently, only -t (tunnel) is supported, -w (server) is not supported
                - user 'ATLAS_MUON_NSW_STGC_QAQC_W', nswdb.library.secret.pwd_STGC_W_prod and nswdb.library.secret.pwd_STGC_W
                        coult be used, if the related pwds would be known.
                '''
                # All needed from the DB (equipment type related data) may be taken from the test DB
                self.MyDelimiter=';'
                self.lower_=False
                self.tunnel = tunnel
                isProduction = production
                params = self.dbParams(isProduction)
                self.connection = cx_Oracle.connect(params['user'], params['pwd'], self.cstring(params['host'],params['port'],params['domain']))
#                self.connection1 = cx_Oracle.connect(params['user1'], params['pwd1'], self.cstring(params['host'],params['port'],params['domain']))
                del params['pwd']
                #del params['pwd1']
                #utils.print_('Connected to '+str(params),2)
        def dbParams(self,isProduction): #tbd: take these details andthe con1 related stuff out, to make the code generic
                params={}
                params['user']='ATLAS_MUON_NSW_MM_LOG_W'
                params['user1']='ATLAS_MUON_NSW_STGC_QAQC' #tbd ATLAS_MUON_NSW_STGC_QAQC/sTGC7102_QAQC_MASTER@int8r or atlr
                if isProduction:
                        params['dbName']='productionDb'
                        params['domain'] = 'atlr.cern.ch'
                        params['port'] = '10121'
                        params['host'] = 'localhost'    if self.tunnel else 'atlr-s.cern.ch'
                        params['pwd'] = secret.pwd_LOG_W_Prod
                        #params['pwd1'] = secret.pwd_QAQC_Prod
                else:
                        params['dbName'] = 'testDb'
                        params['domain'] = 'int8r.cern.ch'
                        params['port'] = '10005'                if self.tunnel else '10121'
                        params['host'] = 'localhost'    if self.tunnel else 'int8r-s.cern.ch'
                        params['pwd'] = secret.pwd_LOG_W
                        #params['pwd1'] = secret.pwd_QAQC
                return params
        def cstring(self, host, port, domain):
                return "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = %s)(PORT = %s)) \
                        (LOAD_BALANCE = on)(CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = %s) ) )" % (host, port, domain)
        def descriptionToColumnNames(self,description): return map(lambda x:x[0],description)
        def addOrderBy(self,cmd,orderBy):
                rc=cmd if len(orderBy)==0 else cmd + ' ORDER BY '+orderBy
                return rc
        def cursor(self,con1=False):
                if con1:        return self.connection1.cursor()
                else:                   return self.connection.cursor()
        def cmd(self,cmd, verbose=0, clean=False, con1=False, commit=False, orderBy=''): #, fileName=''):
                cmd=cmd.strip() #Needed to ensure that cmd starts with select and not white space for queries
                cmd=self.addOrderBy(cmd,orderBy)
                if cmd==None:                                   raise Exception('db.cmd: bug: cmd==None')
                #utils.print_( 'db.cmd: '+ cmd, 2)
                isQuery= cmd.upper().startswith('SELECT')
                with self.cursor(con1) as cursor:
                    cursor = self.cursor(con1) # May be issue with repeated cursors
                    try:
                        cursor.execute(cmd)
                    except Exception as e:
                        raise(e)
                    if isQuery:
                        rc=[]
                        for r in cursor:
                            if clean:                               
                                rc.append(r[0])
                            else:                                   
                                rc.append(r)
                    elif commit:
                        self.commit(con1=con1)
                    if isQuery:
                        return pd.DataFrame(rc, columns=[x[0] for x in cursor.description])

        def bulkInsert(self,command, list, commit=True, con1=False):
            cursor = self.cursor(con1) # May be issue with repeated cursors
            cursor.prepare(command)
            #print cursor.bindnames()
            cursor.executemany(None, list)
            cursor.close()
            if commit: self.commit(con1=con1)
        def checkNulls(self,str):
                rc = ''
                and_ = ''
                for word in str.split(','):
                        rc += and_ + word + ' IS NOT NULL'
                        and_ = ' AND '
                return rc
        def dbMapList( self, tables, keyColumn, where, it, checkNull=True, valueColumn='', con1=False, orderBy=''):
                # Supports types dict/list/collections.defaultdict(set)
                if valueColumn!='':                     assert(type(it)==dict or type(it==collections.defaultdict))
                else:                                                   assert(type(it)==list)
                where_='where '
                if checkNull:
                        where_+=self.checkNulls(keyColumn)
                        if valueColumn != '': where_+ ' AND ' + self.checkNulls(valueColumn)
                        '''tbd" delete after debugging: if valueColumn!='':             where_+=keyColumn+' is not NULL and '+ valueColumn+' is not NULL'
                        else:                                           where_+=keyColumn+' is not NULL' '''
                if len(where)==0:                               where= where_
                else:
                        if not checkNull:                       where= where_+ where
                        else:                                           where= where_+ ' and '+ where
                valueColumnTerm= ','+valueColumn if valueColumn !='' else ''
                cmd='select '+keyColumn+valueColumnTerm+' from ' + ','.join(tables)+ ' ' + where
                cmd=self.addOrderBy(cmd,orderBy)
                dbResult=self.cmd(cmd, con1=con1)
                numKeyCols=len(keyColumn.split(','))
                for i in dbResult:
                        if valueColumn != '':
                                key = ','.join(i[:numKeyCols])  # key may have multiple columns
                                value = i[numKeyCols:numKeyCols + 1][0]  # TBD: value can only have one column
                                if type(it)==dict:              it[key]=value           # dict
                                elif type(it)==collections.defaultdict:
                                                                                it[key].add(value)      # collections.defaultdict(set)
                                else:                                   raise Exception('bug, unsupported type')
                        else:
                                if type(it) == list:
                                                                                key = i[:numKeyCols][0]
                                                                                it.append(key)
                                else:                                   raise Exception('bug, unsupported type')
                #utils.print_('len(it)'+str(len(it)),2)
        def fillDbIt(self, dataDict, itName, tables, keyColumn, where, checkNull=True, verboseBool=False, valueColumn=''
                                 , headers='', resultIsSet=False, con1=False, allowRepeat=False, kind='debug', orderBy=''):
                #bdd assert('project' in dataDict.keys())
                if 'project' in dataDict.keys():
                        project=dataDict['project']
                        (where,isProjectDependant)=specificDb.findProject(tables, project, where)
                        if not isProjectDependant and itName in dataDict['dbDictsFilled'] and not allowRepeat:
                                return #No need to repeat this query
                if valueColumn!='':
                        if resultIsSet: it=dataDict['dbDicts'][itName]=collections.defaultdict(set)
                        else:                   it=dataDict['dbDicts'][itName]={}
                else:                           it=dataDict['dbDicts'][itName]=[]
                self.dbMapList(tables=tables, keyColumn=keyColumn, valueColumn=valueColumn, where=where, it=it, checkNull=checkNull, con1=con1, orderBy='')
                dataDict['dbDictsFilled'].add(itName) # Memorize that this itName is filled
                #utils.printI(it, itName, maxLen=-1, headers=headers,   verbose=1, firstLineOnly=not verboseBool, kind=kind)
        '''def fillDbIts(self, dataDict, itNames, tables, keyColumns, where, checkNull=True, verboseBool=False, 
        valueColumns=list(), headers=list(), resultIsSet=False, con1=False, allowRepeat=False, orderBy=''):
                #Each fillDbIt must have a unique itName
                for n, itName in enumerate(itNames):
                        if len(keyColumns) == len(itNames):             keyColumn = keyColumns[n]               #keyColumns
                        elif len(keyColumns) == 1:                              keyColumn = keyColumns[0]
                        else:                                                                   raise Exception('Bug: fillDbIts: len(keyColumns) must be 1 or len(itNames)')
                        if len(valueColumns) == len(itNames):   valueColumn = valueColumns[n]   #valueColumns
                        elif len(valueColumns) == 1:                    valueColumn = valueColumns[0]
                        elif len(valueColumns) == 0:                    valueColumn = ''
                        else:                                                                   raise Exception('Bug: fillDbIts: len(valueColumns) must be 1 or len(itNames) or 0')
                        if len(headers) == len(itNames):                header = headers[n]                             #headers
                        elif len(headers) == 1:                                 header = headers[0]
                        elif len(headers) == 0:                                 header = ''
                        else:                                                                   raise Exception('Bug: fillDbIts: len(headers) must be 1 or len(itNames) or 0')
                        self.fillDbIt(dataDict, itName, tables, keyColumn, where, checkNull, verboseBool, valueColumn, header, 
                        resultIsSet, con1=con1, allowRepeat=allowRepeat, orderBy=orderBy) #The meat'''
        def count( self, table, where='', con1=False): # select count(*) from table where
                if where!='': where=' WHERE '+where
                rc=self.cmd('select count(*) from ' + table+ ' ' + where, clean=True, con1=con1)[0]
                assert (isinstance(rc, int))
                return rc
        def exists(self, table_, owner_, con1=False):
                rc=self.count(table='all_tables',where="OWNER = '"+owner_+"' AND table_name ='" + table_+ "'", con1=con1)
                return rc>0
        def update(self, table, column2set, values2set, columnWhere, valueWhere): #tbd, generalize also for numeric values
                cmd = 'UPDATE ' + table + ' SET ' + column2set + " ='" + values2set + "' WHERE " + columnWhere + "='" + valueWhere +"'"
                self.cmd(cmd)
        def commit(self, con1=False):   self.cmd('COMMIT',con1=con1)
        def dbIsInColumn( self, table, value, column): # select count(*) from table where column=key
                where=column+'='+ value
                return self.count(table, where)>0
        def __del__(self):
                self.connection.close()
                #utils.print_('Deleting DB obect',2)
        def cmdrc2list(self,rc):
                l = []
                for r in rc:    l.append(r[0])
                return l
        def cols(self,table, owner=ownerLog):
                cmd = "SELECT column_name FROM all_tab_cols WHERE table_name = '" + table + "' AND owner = '" + owner + "'"
                orderBy="COLUMN_ID"
                return self.cmdrc2list(self.cmd(cmd,orderBy))
        def q(self,cmd,indent_=5,con1=False,orderBy='', printIfNotEmpty=False, printIfNotZero=False):
                rc=self.cmd(cmd, withDescription=True,con1=con1,orderBy=orderBy)
                (headers, data)=rc
                if (not printIfNotEmpty or len(data)>0) \
                                and (not printIfNotZero or not ((len(data)==1) and len(data[0])==1 and data[0][0]==0)):
                        #utils.printTabulated(firstLine='cmd: ' + cmd, headers=headers, data=data, indent_=indent_, verbose=0
                                                                 #, level=5, firstLineOnly=False, enumerate=True)
                        pass
                return rc
        '''not in use (yet)
        def timestamp2linux(self, column): # column must be of type timestamp
                return "(cast ("+column+" at time zone 'UTC' as DATE) - to_date('1970-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')) * 86400" #secs/day: 60*60*24=86400'''
        def fromSecsFromEpochToTO_DATE(self, secsFromEpoch):
                return datetime.datetime.utcfromtimestamp(secsFromEpoch) #bad: "to_date('19700101', 'YYYYMMDD') + (1/86400)*"+str(secsFromEpoch)
#       def applyCommandsFromFile(self,fileName,commit=False):
#               '''Read file, apply each row as a command, commit if needed'''
#               found=False
#               for row in utils.file2list(fileName):
#                       self.cmd(row)
#                       found=True
#               if commit and found: self.commit()
#end: class db:
