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
        --train=file		training file
	--test=file		testing file
        --classifiers		comma separated list of classifiers
	--args			Comma separated list of classifiers
        --classConfig		file
  	-v			verbose
        -------------------------------------------------------'''
	



def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'hv',["help","train=","test=","classifiers=","classConfig="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)



    trainFile = None
    testFile  = None
    classifiers = []
    args = []
    verb = False
    for opt, arg in options:
        if opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('--train'):
            trainFile = arg
        elif opt in ('--test'):
            testFile = arg
        else:
            usage()
            assert False, "unhandled option "+opt

 

    if trainFile is None:
        print 'Train File not specified'
        usage()
        sys.exit(1)
    if testFile is None:
        print 'Test File not specified'
        usage()
        sys.exit(1)

    trainF = open(trainFile,'r')
    train = trainF.readlines()
    trainF.close()

    testF = open(testFile,'r')
    test = testF.readlines()
    testF.close()


    trainData=False
    numTrainBuggy = 0.0
    valNdx = 0
    for ndx in range(len(train)):
        if trainData:
            data = train[ndx].split(',')
            if data[-1] == 'buggy\n':
                numTrainBuggy = numTrainBuggy + 1
        else:
            if '@DATA' in train[ndx]:
                trainData=True
                valNdx = ndx+1
    trainPercent= numTrainBuggy/len(train[valNdx:])

    testData=False
    numCorrect=0.0
    random.seed(None)
    for ndx in range(len(test)):
        if testData:
            data = test[ndx].split(',')
            rand = random.random()
            if rand <= trainPercent:
                guess = 'buggy'
            else:
                guess = 'clean'

            if guess in data[-1]:
                numCorrect = numCorrect+1 
        else:
            if '@DATA' in test[ndx]:
                testData=True
    accuracy=numCorrect/len(test[valNdx:])
    print str(accuracy)


if __name__ == "__main__":
    main()







