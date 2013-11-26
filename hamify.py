import sys



arff = open(sys.argv[1],'r')
arfflines = arff.readlines()
arff.close()

ham = open(sys.argv[2],'w')
dataflag = 0
for line in arfflines:
    if dataflag:
        data = line.split(',')
        if 'clean' in data[-1]:
            ham.write('ham\t')
        else:
            ham.write('spam\t')
        ham.write(data[0].strip('"')+'\n')
    
    if '@DATA' in line:
        dataflag = 1


ham.close()


