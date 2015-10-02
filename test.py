from Bio.pairwise2 import format_alignment
from Bio import pairwise2

b1 = "ri167955X22Z03Q5Z86g0Y10y5096Y39Q09gQY5Q54767"
b2 = "ri167955X22Z01Q5Z06g0Y10y5086Y31Q08gQY5Q54767"

b1str = ""
middle = ""
b2str = ""

for i in range(len(b1)):
    b1str += b1[i]
    if b1[i] is not b2[i]:
        middle += "X"
    else:
        middle += "|"

    b2str += b2[i]


print b1str
print middle
print b2str
