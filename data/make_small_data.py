import random

fr = open('data.txt', 'r')
fr2 = open('data_small.txt', 'w')
lines = fr.readlines()

for line in lines:
    if random.randint(1, 200) % 100 == 0:
        fr2.write(line)