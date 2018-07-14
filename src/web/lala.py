import sys

file_name = sys.argv[1]
sentence = sys.argv[2]
num = sys.argv[3]

def demo(file_name, sentence, num):
	print(file_name, sentence, num)
	ret = [file_name, sentence, num]
	return ret