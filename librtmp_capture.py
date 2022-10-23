import librtmp

conn = librtmp.RTMP('rtmp://[RTMP Server IP]:[PORT]/live/testkey', live=True)
conn.connect()
stream = conn.create_stream()

cnt = 0
all_data = None
with open('out.flv', 'wb') as f:
    while cnt < 5000:
        cnt += 1
        data = stream.read(1024)
        if all_data is None:
            all_data = data
        else:
            all_data += data
        f.write(data)
print(all_data[:100])
print(all_data[-100:])
