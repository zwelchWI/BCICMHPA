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
 	-b  or --numbins	number of bins to split to (2)
       -------------------------------------------------------'''
	



def main():
    pass


    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hi:o:b:',["help","infile=","outfile=",
		"numbins="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)


    infile = None
    outfile= None
    numbins = 2
    for opt, arg in options:
        
        if opt in ('-i','--infile'):
            infile = arg
        elif opt in ('-o','--outfile'):
            outfile = arg
        elif opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('-b','--numbins'):
            numbins = int(arg)
        else:
            assert False, "unhandled option "+opt


    if outfile is None and infile is None:
        usage()
        print "Error Input and Output files not specified"
        sys.exit(2)

    infile = open(infile,'r')
    indata = infile.readlines()
    
    infile.close()

    outfile= open(outfile,'w')
    outfile.write(indata[0])
    num_cols = len(indata[0].split(',')) 
    mins = [float(x) for x in indata[1].split(',')]
    maxs = [float(x) for x in indata[1].split(',')]
    
    for data in indata[2:]:
        vals = [float(x) for x in data.split(',')]
        for ndx in range(len(vals)):
            if vals[ndx] < mins[ndx]:
                mins[ndx]=vals[ndx]
            elif vals[ndx] > maxs[ndx]:
                maxs[ndx] = vals[ndx]
    print mins
    print maxs
    ranges = [0 for x in maxs]
    for ndx in range(len(maxs)):
        ranges[ndx] = (maxs[ndx]-mins[ndx])/float(numbins)
        

    for data in indata[1:]:
        vals = [float(x) for x in data.split(',')]
        for ndx in range(len(vals)):
            for range_ndx in range(numbins):
                print range_ndx," ",numbins/2.0
                low_bin = mins[ndx]+range_ndx*ranges[ndx]
                high_bin= mins[ndx]+(range_ndx+1)*ranges[ndx]
                if range_ndx < numbins/2.0:
                    something = 'low'+str(int(math.ceil(numbins/2.0)-range_ndx))
                elif range_ndx > numbins/2.0:
                    something = 'up'+str(int(range_ndx-math.ceil(numbins/2.0)))
                else:
                    something ='mid'  
                if vals[ndx] >= low_bin and vals[ndx] <= high_bin:
                    #in this bin
                    outfile.write(something+',')
                    
        outfile.write('\n')
    outfile.close()

    


if __name__ == "__main__":
    main()













