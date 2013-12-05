import subprocess
repos = ['one','cyclus','git','jedit','jquery','puppet','scala','scipy']
timespans=['6m','1yr','2yr','all']
for repo in repos:
    for timespan in timespans:
        val = 0.0
        for ndx in range(10):
            cmd =  ' python randomWeight.py --test='+repo+'.test.arff --train='+repo+'.train.'+timespan+'.arff'
            testOut = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err=testOut.communicate()
            val = val + float(out)
        print cmd
        print str(val/10)
