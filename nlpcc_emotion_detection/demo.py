import numpy as np

all_lines = []

with open('/home/wuyaqiang/myprojects/Corpus/glove.6B/glove.6B.100d.txt','r') as f:
    for line in f:
        values = line.split()
        all_lines.append(values)

print(all_lines[342][0])
print(all_lines[342][1:])