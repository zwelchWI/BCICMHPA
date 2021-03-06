import sys
import os
import getopt
from datetime import date
import _mysql



def usage():
    '''prints the acceptable list of command line options to the user'''
    print '''-------------------------------------------------------
        Usage
        -h  or --help           print list of commands
        -uY or --db-user Y      set database user to Y
        -pX or --db-passwd X    set password to X
        -dZ or --db-database Z  set db name to Z
        -Ha or --db-host a      set database host to a
        --start-date YYYY/MM/DD  ex: 1776/1/14
   	--end-date   YYYY/MM/DD
	-c  or --csv-file C	set csv filename
        --extensions		comma separated list of extensions
		LinesAdded
                LinesRemoved
		TimeHour
		TimeMin
		Day
		Month
		Year
		DayOfWeek
		User
		Comment
		CommentLength
		NumFiles
		
        def user         : root
        def password     : ""
        def db name      : cvsanaly
        def db host	 : localhost
	def csv name	 : out.csv
        -------------------------------------------------------'''
	



def main():
    pass


    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hu:p:d:H:c:',["help","db-user=","db-passwd=",
		"db-database=","db-host=","start-date=","end-date=",
		"csv-file=","extensions="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)


    User='root'
    Passwd=''
    db_name='cvsanaly'
    Host='localhost'
    csv_name = 'out.csv'
    start_date = None
    end_date = None
    extensions = [] 

    for opt, arg in options:
        
        if opt in ('-u','--db-user'):
            User = arg
        elif opt in ('-p','--db-passwd'):
            Passwd = arg
        elif opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('-d','--db-database'):
            db_name = arg
        elif opt in ('-H','--db-host'):
            Host = arg
        elif opt in ('--start-date'):
            sd = arg.split('/')
            start_date = date(int(sd[0]),int(sd[1]),int(sd[2]))
        elif opt in ('--end-date'):
            ed = arg.split('/')
            end_date = date(int(ed[0]),int(ed[1]),int(ed[2]))
        elif opt in ('-c','--csv-file'):
            csv_name = arg
        elif opt in ('--extensions'):
            extensions = arg.split(',')

        else:
            assert False, "unhandled option "+opt
    csv = open(csv_name,'w')
    
    db = _mysql.connect(host=Host,user=User,passwd=Passwd,db=db_name)

    #db.query("""SELECT spam, eggs, sausage FROM breakfast
    #     WHERE price < 5""")


    #we really aught to consider a streaming option if this gets too big

    time_query=""
    if start_date is not None and end_date is not None:
        time_query = "where commit_date BETWEEN '"+start_date.strftime("%y/%m/%d") +"' and '"+end_date.strftime("%y/%m/%d")+"'"
    elif start_date is not None:
        time_query = "where commit_date >= '"+start_date.strftime("%y/%m/%d")+"'"
    elif end_date is not None:
        time_query = "where commit_date <=  '"+end_date.strftime("%y/%m/%d")+"'"

    query_str=' select a.id,rev,commit_date,message,email,added,removed,file_count from scmlog a INNER JOIN people b ON a.author_id=b.id  INNER JOIN commits_lines c on a.id=c.commit_id INNER JOIN (select commit_id,count(commit_id) as file_count from actions group by commit_id) as d on a.id=d.commit_id'
    #get basic data
    db.query(query_str+" "+time_query)
    commits = db.use_result()
    #get all the rows as a tuple of dictionaries, where each key is the column name
    commit_data = commits.fetch_row(maxrows=0,how=1)

    #get list of buggy commits
    db.query("select DISTINCT bug_commit_id from Hunk_Blames;")
    buggy = db.use_result()
    buggy_data = buggy.fetch_row(maxrows=0,how=1)

    buggys=[]
    for b in buggy_data:
        buggys.append(b['bug_commit_id'])

    buggy=None
    buggy_data=None

    for ext in extensions:
        csv.write(ext+',')
    csv.write('buggy\n')
    for commit in commit_data:
        #print out the data
        date_time = commit['commit_date']
        cdate=date_time.split()[0]
        ctime=date_time.split()[1]
        cdates = cdate.split('-')
        ctimes = ctime.split(':')

        for ext in extensions:
            
            if ext == 'LinesAdded':
                csv.write(commit['added']+',')
            if ext == 'LinesRemoved':
                csv.write(commit['removed']+',')
            if ext == 'TimeHour':
                csv.write(ctimes[0]+',')
            if ext == 'TimeMin':
                csv.write(ctimes[1]+',')
            if ext == 'Day':
                csv.write(cdates[2]+',')
            if ext == 'Month':
                csv.write(cdates[1]+',')
            if ext == 'Year':
                csv.write(cdates[0]+',')
            if ext == 'DayOfWeek':
                dow = date(int(cdates[0]),int(cdates[1]),int(cdates[2])).weekday()
                d=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                csv.write(d[dow]+',')
            if ext == 'User':
                csv.write(commit['email']+',')
            if ext == 'Comment':
                lines = commit['message'].splitlines()
                messg = ''
                for line in lines:
                    messg = messg+' '+line.lstrip()
                messg = messg.replace(',','')
                messg = messg.replace('"','')
                csv.write('"'+messg.strip('"')+'",')
            if ext == 'CommentLength':
                csv.write(str(len(commit['message']))+',')
            if ext == 'NumFiles':
                csv.write(commit['file_count']+',')


        if commit['id'] in buggys:
            csv.write('buggy')
        else:
            csv.write('clean')
        csv.write('\n')

    csv.close()

if __name__ == "__main__":
    main()













