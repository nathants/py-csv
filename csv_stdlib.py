import csv
import sys

fields = [int(x) - 1 for x in sys.argv[1].split(',')]

for row in csv.reader(sys.stdin):
    val = []
    for field in fields:
        val.append(row[field])
    sys.stdout.write(','.join(val) + '\n')
