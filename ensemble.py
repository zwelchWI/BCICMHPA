import sys
import os
import getopt
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
import subprocess
import time


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
        -------------------------------------------------------'''
	



def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'h',["help","train=","test=","classifiers=","classConfig="])
	#fix later
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)



    trainFile = None
    testFile  = None
    classifiers = []
    args = []
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
        elif opt in ('--args'):
            args = arg.split(',')
        elif opt in ('--classConfig'):
            configFile = open(arg,'r')
            lines = configFile.readlines()
            configFile.close()
            for ndx in range(len(lines)):
                data = lines[ndx].split('=')
                if len(data) > 1:
                    try:
                        if data[0].lower() == 'classifier':
                            classifiers.append(data[1].strip())
                            data = lines[ndx+1].split('=')
                            args.append(data[1].strip())
                    except:
                        print 'ERROR, INVALID configFile'
                        print 'classifier=<classifierName>'
                        print 'args=<possibly empty list of args for model building>'
                        sys.exit(1)
        else:
            usage()
            assert False, "unhandled option "+opt

    if len(args) == 0:
        for cl in classifiers:
            args.append('')
 

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
    og_cl = list(classifiers)
    for cl in og_cl:
        pred = []
        bldCmd='java -cp /usr/share/java/weka.jar:/usr/share/java/libsvm.jar '
        bldCmd=bldCmd+cl+' -t "'+trainFile+'" -T "'+trainFile+'" -d "test" '+args[classifiers.index(cl)]
        print bldCmd
        buildOut = subprocess.Popen(bldCmd,shell=True,stdout=subprocess.PIPE)

        time.sleep(1)
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
        if len(pred) > 0:
            predictions.append(pred)
        else:
            args.remove(args[classifiers.index(cl)])
            classifiers.remove(cl)
            

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

    print 'Number of classifiers used in Ensemble :'+str(len(classifiers)-1)+'/'+str(len(og_cl))
    print 'Classifiers input but not used :'+ str([str(X) for X in og_cl if X not in classifiers])
if __name__ == "__main__":
    main()







