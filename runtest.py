import subprocess
repos = ['jedit','jquery','puppet','scala','scipy']
timespans=['6m','1yr','2yr','all']
for repo in repos:
    for timespan in timespans:
        cmd =  ' python ensemble.py --classConfig=test.config --test='+repo+'.test.arff --train='+repo+'.train.'+timespan+'.arff'
        print cmd
        testOut = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=testOut.communicate()
        print out
