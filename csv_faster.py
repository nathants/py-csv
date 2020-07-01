import sys

fields = [int(x) - 1 for x in sys.argv[1].split(',')]

for line in sys.stdin:
    parts = line.split(',')
    val = []
    for field in fields:
        val.append(parts[field])
    sys.stdout.write(','.join(val) + '\n')
