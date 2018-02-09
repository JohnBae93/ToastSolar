from konlpy.tag import Twitter
from konlpy.utils import pprint

fr = open('../data.txt', 'r')
fw = open('../data_noun.txt', 'w')

lines = fr.readlines()
twiter = Twitter()
print(len(lines))
for line in lines:
    fw.write(" ".join(twiter.nouns(line)) + '\n')


