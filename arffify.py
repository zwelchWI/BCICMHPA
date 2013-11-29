import sys
import os
import getopt
from datetime import date
import _mysql
import math

def usage():
    '''prints the acceptable list of command line options to the user'''
    print '''-------------------------------------------------------
        Usage
        -h  or --help           print list of commands
        -i  or --infile		input csv file to binify
	-o  or --outfile	output filename to write to
       -------------------------------------------------------'''
	



def main():
    pass


    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hi:o:',["help","infile=","outfile="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)


    infile = None
    outfile= None
    for opt, arg in options:
        
        if opt in ('-i','--infile'):
            infile = arg
        elif opt in ('-o','--outfile'):
            outfile = arg
        elif opt in ('-h','--help'):
            usage()
            sys.exit(2)
        else:
            assert False, "unhandled option "+opt


    if outfile is None or infile is None:
        usage()
        print "Error Input and Output files not specified"
        sys.exit(2)

    inf = open(infile,'r')
    indata = inf.readlines()
    inf.close()


    attribs = indata[0].split(',')

    header = '% 1. Title : '+infile.rstrip('.csv')+'\n'
    header = header + '''%
%
% 2. Sources:
%    (a) Creator : Zach Welch
%    (b) Date 
@RELATION buggy
'''
    exData = indata[1].split(',')


    for ndx in range(len(attribs)):
        datatype = None
        try:
            hold = float(exData[ndx])
            datatype = 'NUMERIC'
        except:
            datatype = 'STRING'
        header = header + "@ATTRIBUTE "+attribs[ndx].strip()+" "+datatype+'\n'
        
    header = header + "@DATA \n"
    
    outfile= open(outfile,'w')
    outfile.write(header)
    for line in indata[1:]:
        outfile.write(line)
    outfile.close()

    


if __name__ == "__main__":
    main()













