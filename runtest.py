import subprocess
repos = ['git','jedit','jquery','puppet','scala','scipy']
timespans=['6m','1yr','2yr','all']
for repo in repos:

    cmd =  ' python combine_arffs.py --file1='+repo+'.test.arff --file2=data/'+repo+'.test.comment.arff --outfile=all/'+repo+'.all.test.arff'
    print cmd
    testOut = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=testOut.communicate()
    print out
    for timespan in timespans:
        
        cmd =  ' python combine_arffs.py --file1='+repo+'.train.'+timespan+'.arff --file2=data/'+repo+'.train.'+timespan+'.comment.arff --outfile=all/'+repo+'.all.train.'+timespan+'.arff '
        print cmd
        testOut = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=testOut.communicate()
        print out

        cmd =  ' python ensemble.py --classConfig=test3.config --test=all/'+repo+'.all.test.arff --train=all/'+repo+'.all.train.'+timespan+'.arff '
        print cmd
        testOut = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=testOut.communicate()
        print out+'\n\n\n'
