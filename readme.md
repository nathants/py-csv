## why

it should be possible to process well formed csv in pure python with decent performance.

## what

a code template of boilerplate to copy/paste and then modify row handling code.

## how

python doesn't have inlining or macros, so far maximum performance we have to manually inline code into the body of the parsing loop.

for input we minimize allocations and syscalls by reading large chunks into a buffer and only allocating meta data about the start and end offset of each column in a row.

for output we mutate a byte buffer and only call write when the buffer would overflow.

this parsing is only for well formed csv, and is only aware of comma and newline. if you need to parse that is not well formed, use the standard library parser.

if you need to go faster than this, look into using similar techniques to minimize allocations and syscalls with [native code](https://github.com/nathants/bsv/tree/master/experiments/cut)

## demo

```
>> time pypy3 gen_csv.py 8 15000000 > /tmp/large.csv
real    0m9.075s
```

```
>> ls -lh /tmp/large.csv
-rw-r--r-- 1 nathants nathants 1.1G Jul  1 13:24 /tmp/large.csv
```

```
>> time pypy3 csv_stdlib.py 3,7 </tmp/large.csv >/dev/null
real    0m17.199s
```

```
>> time pypy3 csv_faster.py 3,7 </tmp/large.csv >/dev/null
real    0m6.636s
```

```
>> time pypy3 csv_fastest.py 3,7 </tmp/large.csv >/dev/null
real    0m4.259s
```

```
>> time python3 csv_stdlib.py 3,7 </tmp/large.csv >/dev/null
real    0m21.720s
```

```
>> time python3 csv_faster.py 3,7 </tmp/large.csv >/dev/null
real    0m11.531s
```

```
>> pypy3 csv_stdlib.py 3,7 </tmp/large.csv | md5sum
b64f540b7a1713bcc9f509ff3f9062a5  -

>> pypy3 csv_faster.py 3,7 </tmp/large.csv | md5sum
b64f540b7a1713bcc9f509ff3f9062a5  -

>> pypy3 csv_fastest.py 3,7 </tmp/large.csv | md5sum
b64f540b7a1713bcc9f509ff3f9062a5  -
```
