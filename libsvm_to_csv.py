
import sys


print sys.argv
idx = open(sys.argv[1],"r")
libsvm=open(sys.argv[2],"r")
csv=open(sys.argv[3],"w+")




idxs = idx.readline()
idxs = idxs[1:]
idxs = idxs[:-1]
indexs = idxs.split(',')
ordered_indexs = {}
for index in indexs:
	value = index.split('=')
	ordered_indexs[int(value[1])]=value[0]
        
keys = ordered_indexs.keys()
keys.sort()

for key in keys:
	print str(key) + ordered_indexs[key]
	csv.write(ordered_indexs[key]+',')
csv.write('classification,')
csv.write('comment\n')

idx.close()


lines = libsvm.readlines()
for line in lines:
	data = line.split('#')
	comment = data[1]
	data = data[0]
	data = data.split()
	classification = data[0]
	data = data[1:]
	data_index={}
	for dataval in data:
		dat = dataval.split(':')
		data_index[int(dat[0])]=dat[1]

	print data_index
	for key in keys:
		if key not in data_index:
			csv.write(' ,')
		else:
			csv.write(data_index[key]+',')
	csv.write(classification+',')
	csv.write(comment)	

	








libsvm.close()
csv.close()






