import sys
import os
import getopt
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
import subprocess


def usage():
    '''prints the acceptable list of command line options to the user'''
    print '''-------------------------------------------------------
        Usage
        -h  or --help           print list of commands
        --train=file		training file
	--test=file		testing file
        --classifiers		comma separated list of classifiers
        -------------------------------------------------------'''
	



def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'h',["help","train=","test=","classifiers="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)



    trainFile = None
    testFile  = None
    classifiers = []
    for opt, arg in options:
        if opt in ('-h','--help'):
            usage()
            sys.exit(2)
        elif opt in ('--train'):
            trainFile = arg
        elif opt in ('--test'):
            testFile = arg
        elif opt in ('--classifiers'):
            classifiers = arg.split(',')
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


    actual = []
    predictions = []
    #collect predictions
    for cl in classifiers:
        pred = []
        bldCmd='java -cp /usr/share/java/weka.jar:/usr/share/java/libsvm.jar '
        bldCmd=bldCmd+cl+' -t "'+trainFile+'" -T "'+trainFile+'" -d "test"'
        print bldCmd
        buildOut = subprocess.Popen(bldCmd,shell=True,stdout=subprocess.PIPE)


        testCmd= 'java -cp /usr/share/java/weka.jar:/usr/share/java/libsvm.jar '+cl+' -p 0'
        testCmd=testCmd+'  -l "test" -T "cyclus.test.numeric.arff"'
        print testCmd
        testOut = subprocess.Popen(testCmd,shell=True,stdout=subprocess.PIPE)
        out,err=testOut.communicate()
 
        outlines = out.split('\n')
        for line in outlines[5:-2]:
            vals = line.split()
            if len(outlines[5:-2]) > len(actual):
                actual.append(vals[1].split(':')[1])
            pred.append(vals[2].split(':')[1])
        predictions.append(pred)


    ens_pred = []
    for ndx in range(len(actual)):
        num_clean = 0
        for pred in predictions:
            if pred[ndx] == 'clean':
                num_clean = num_clean + 1
        if float(num_clean)/len(predictions) >= 0.5:
            ens_pred.append('clean')
        else:
            ens_pred.append('buggy')

    classifiers.append("Ensemble Methods")
    predictions.append(ens_pred)


    for clndx in range(len(classifiers)):         
        num_correct = 0
        num_actual_buggy = 0
        num_pred_buggy = 0
        for ndx in range(len(actual)):
            if actual[ndx] == 'buggy':
                num_actual_buggy = num_actual_buggy+1
            if predictions[clndx][ndx] == 'buggy':
                num_pred_buggy = num_pred_buggy+1
            if actual[ndx] == predictions[clndx][ndx]:
                num_correct = num_correct+ 1
        print 'CLASSIFIER: '+classifiers[clndx]
        print '-------------------------------'
        print 'Number predicted buggy '+str(num_pred_buggy)
        print 'Number actually buggy '+str(num_actual_buggy)
        print 'Number correct: '+str(num_correct)
        print 'Total data '+str(len(actual))
        print 'Accuracy '+str(float(num_correct)/len(actual))
        print ''



if __name__ == "__main__":
    main()







