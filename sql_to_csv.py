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
        --start-date MO/DAY/YR  ex: 07/04/1776
   	--end-date   MO/DAY/YR
	-c  or --csv-file C	set csv filename
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
		"csv-file="])
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
            start_date = date(int(sd[2]),int(sd[0]),int(sd[1]))
        elif opt in ('--end-date'):
            ed = arg.split('/')
            end_date = date(int(ed[2]),int(ed[0]),int(ed[1]))
        elif opt in ('-c','--csv-file'):
            csv_name = arg

        else:
            assert False, "unhandled option "+opt

    csv = open(csv_name,'w')

    db = _mysql.connect(host=Host,user=User,passwd=Passwd,db=db_name)

    #db.query("""SELECT spam, eggs, sausage FROM breakfast
    #     WHERE price < 5""")


    time_query=""
    if start_date is not None and end_date is not None:
        time_query = "BETWEEN "+start_time.strftime("%m/%d/%y") +" and "+end_time.strftime("%m/%d/%y")
    elif start_date is not None:
        time_query = ""
    elif end_date is not None:
        time_query = ""


    db.query("select * from scmlog "+time_query)


    #assume 1 is clean and -1 is buggy
    db.query("select DISTINCT bug_commit_id from Hunk_Blames;")
    buggy = db.store_results()


    csv.close()

if __name__ == "__main__":
    main()













