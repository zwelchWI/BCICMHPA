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
    maxs=[]
    mins=[]
    for x in indata[1].split(','):
        try:
            val = float(x)
            mins.append(val)
            maxs.append(val)
        except:
            mins.append(None)
            maxs.append(None)
    for data in indata[2:]:
        vals = []
        for x in data.split(','):
            try:
                val = float(x)
                vals.append(val)
            except:
                vals.append(None)
        for ndx in range(len(vals)):
            if vals[ndx] is not None:
                if vals[ndx] < mins[ndx]:
                    mins[ndx]=vals[ndx]
                elif vals[ndx] > maxs[ndx]:
                    maxs[ndx] = vals[ndx]
    ranges = [0 for x in maxs]
    for ndx in range(len(maxs)):
        if vals[ndx] is not None:
            ranges[ndx] = (maxs[ndx]-mins[ndx])/float(numbins)
        else:
            ranges[ndx] = None

    for data in indata[1:]:
        vals = []
        for x in data.split(','):
            try:
                val = float(x)
                vals.append(val)
            except:
                vals.append(x)

        for ndx in range(len(vals)-1):
            if type(vals[ndx]) is str:
                outfile.write(vals[ndx]+',')
            else:
                print vals[ndx]
                for range_ndx in range(numbins):
                    low_bin = mins[ndx]+range_ndx*ranges[ndx]
                    high_bin= mins[ndx]+(range_ndx+1)*ranges[ndx]
                    if range_ndx < (numbins-1)/2.0:
                        something = 'low'+str(int(math.ceil((numbins-1)/2.0)-range_ndx))
                    elif range_ndx > (numbins-1)/2.0:
                        something = 'up'+str(int(range_ndx-math.ceil(numbins/2.0)+1))
                    else:
                        something ='mid'
                    if ranges[ndx] ==0:
                        something='only'
                    if (vals[ndx] >= low_bin and vals[ndx] < high_bin) or (ranges[ndx]==0):
                        print 'PRINT'
                        #in this bin
                        outfile.write(something+',')
                        if ranges[ndx] ==0:
                            break
                    elif vals[ndx] == maxs[ndx]:
                        outfile.write(something+',')
        outfile.write(vals[-1])    
    outfile.close()

    


if __name__ == "__main__":
    main()













