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
	--attrib=attrib		attrib

        --outfile=combine.arff
  	-v			verbose
        -------------------------------------------------------'''
	



def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hv',["help","file1=","attrib=","outfile=","classConfig="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)



    file1 = None
    attrib  = None
    classifiers = []
    args = []
    combine='removed.arff'
    verb = False
    for opt, arg in options:
        if opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('--file1'):
            file1 = arg
        elif opt in ('--attrib'):
            attrib = arg
        elif opt in ('--outfile'):
            combine=arg
        else:
            usage()
            assert False, "unhandled option "+opt

 

    if file1 is None:
        print 'File 1 not specified'
        usage()
        sys.exit(1)
    if attrib is None:
        print 'Attrib not specified'
        usage()
        sys.exit(1)


    f1 = open(file1,'r')
    f1Lines=f1.read()
    f1.close()


    outFile=open(combine,'w')
    startAttribLine=1
    header1  = f1Lines.split('@DATA\n')[0]
    header1Lines = header1.split('\n')
    for ndx in range(len(header1Lines[:-1])):
        if attrib not in header1Lines[ndx]:
            outFile.write(header1Lines[ndx].strip()+'\n')
        else:
            attribNdx=ndx-startAttribLine

        if 'RELATION' in header1Lines[ndx]:
            startAttribLine=ndx+1

    outFile.write('@DATA\n')
    
    print attribNdx


    data1 = f1Lines.split('@DATA\n')[1]
    data1Lines = data1.split('\n')


    for ndx in range(len(data1Lines)):
        line1 = data1Lines[ndx].split(',')
        for  linendx in range(len(line1[:-1])):
            if linendx != attribNdx:
                outFile.write(line1[linendx]+',')
        outFile.write(line1[-1]+'\n')
    outFile.close()
    

if __name__ == "__main__":
    main()







