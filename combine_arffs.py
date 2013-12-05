import sys
import os
import getopt
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
import subprocess
import time
from datetime import datetime
import random

def usage():
    '''prints the acceptable list of command line options to the user'''
    print '''-------------------------------------------------------
        Usage
        -h  or --help           print list of commands
        --file1=file		file1
	--file2=file		file2

        --outfile=combine.arff
  	-v			verbose
        -------------------------------------------------------'''
	



def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hv',["help","file1=","file2=","classifiers=","classConfig="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)



    file1 = None
    file2  = None
    classifiers = []
    args = []
    combine='combine.arff'
    verb = False
    for opt, arg in options:
        if opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('--file1'):
            file1 = arg
        elif opt in ('--file2'):
            file2 = arg
        else:
            usage()
            assert False, "unhandled option "+opt

 

    if file1 is None:
        print 'File 1 not specified'
        usage()
        sys.exit(1)
    if file2 is None:
        print 'File 2 not specified'
        usage()
        sys.exit(1)


    f1 = open(file1,'r')
    f1Lines=f1.read()
    f1.close()
    f2 = open(file2,'r')
    f2Lines = f2.read()
    f2.close()


    outFile=open(combine,'w')

    header1  = f1Lines.split('@DATA\n')[0]
    header1Lines = header1.split('\n')
    for line in header1Lines[:-3]:
        outFile.write(line+'\n')

    

    header2 = f2Lines.split('@DATA')[0]
    header2 = header2.split('@RELATION BUGGY\n')[1]

    outFile.write(header2+'@DATA\n')

    data1 = f1Lines.split('@DATA\n')[1]
    data1Lines = data1.split('\n')
    data2 = f2Lines.split('@DATA\n')[1]
    data2Lines = data2.split('\n')


    for ndx in range(len(data1Lines)):
        line1 = data1Lines[ndx].split(',')
        line2 = data2Lines[ndx].split(',')
        if line1[-1] != line2[-1]:
            print 'Question Yo data'
        for datum in line1[:-1]:
            outFile.write(datum+',')
        outFile.write(data2Lines[ndx]+'\n')
    outFile.close()
    

if __name__ == "__main__":
    main()







