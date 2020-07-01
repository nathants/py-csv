import sys

fields = [int(x) - 1 for x in sys.argv[1].split(',')]

### START BOILERPLATE ###
buffer_size = 1024 * 1024
starts = [0 for _ in range(1 << 16)]
ends   = [0 for _ in range(1 << 16)]
comma = bytearray(b',')[0]
newline = bytearray(b'\n')[0]
write_buffer = bytearray(buffer_size)
while True:
    read_buffer = sys.stdin.buffer.read(buffer_size) # type: ignore
    stop = len(read_buffer) != buffer_size
    if len(read_buffer) == buffer_size: # on a full read, extend with the next full line so the read_buffer always ends with a newline
        read_buffer += sys.stdin.buffer.readline()
    read_offset = 0
    write_offset = 0
    max = 0
    for i in range(len(read_buffer)): # process read_buffer byte by byte
        if read_buffer[i] == comma: # found the next column
            starts[max] = read_offset
            ends[max] = i
            read_offset = i + 1
            max += 1
        elif read_buffer[i] == newline: # found the row end
            starts[max] = read_offset
            ends[max] = i
            read_offset = i

            # start handle row
            val = b''
            ### START CUSTOM CODE ###
            for i, f in enumerate(fields):
                val += read_buffer[starts[f]:ends[f]]
                if i != len(fields) - 1:
                    val += b','
            ### END CUSTOM CODE ###
            val += b'\n'
            # end handle row

            if len(val) > len(write_buffer) - write_offset: # write and maybe flush
                sys.stdout.buffer.write(write_buffer[:write_offset])
                write_offset = 0
            write_buffer[write_offset:write_offset + len(val)] = val
            write_offset += len(val)
            max = 0 # reset for next row
    sys.stdout.buffer.write(write_buffer[:write_offset])
    if stop:
        break
### END BOILERPLATE ###
