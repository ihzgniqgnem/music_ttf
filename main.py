import pyaudio
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
import worker
import pydub
now=0
class stream_(bytes):
    def read(self,size):
        global now
        size*=2
        now += size
        if now >= len(self):
            now = 0
        return self[now - size:now]
FROM_FILE="input.mp3"
OUTPUT=True
BUFFER_SIZE=4096
RATE=0
CHANNELS=1
pa=pyaudio.PyAudio()
if FROM_FILE:
    file = pydub.AudioSegment.from_file(FROM_FILE)
    if not RATE:RATE = file.frame_rate
    CHANNELS = file.channels
    stream = stream_(file.raw_data)
else:stream=pa.open(format=pyaudio.paInt16,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=BUFFER_SIZE)
if OUTPUT:stream_out=pa.open(format=pyaudio.paInt16,channels=CHANNELS if FROM_FILE else 1,rate=RATE,output=True)

def record():
    data_record=stream.read(BUFFER_SIZE)
    return data_record
def play():
    global data_record
    stream_out.write(data_record)
play_worker=worker.worker(play)
record_worker=worker.worker(record)
record_worker.run()
mpl.use("QtAgg")
fig, ax = plt.subplots(2,1)
line1, = ax[0].plot(np.arange(0, BUFFER_SIZE), np.random.rand(BUFFER_SIZE),linewidth=0.5)
ax[0].set_xlim(0, BUFFER_SIZE-1)
ax[0].set_ylim(-22768, 22768)
line2, = ax[1].plot(np.arange(0, BUFFER_SIZE//2), np.random.rand(BUFFER_SIZE//2),linewidth=0.5)
ax[1].set_xlim(20, 20000)
ax[1].set_ylim(100, 10000000)
ax[1].set_yscale('log', base=10)
ax[1].set_xscale('log', base=2)
ax[1].xaxis.set_major_formatter(LogFormatter(base=2))
plt.ion()
plt.show()
max_ = 0
ltime = time.time()
record_worker.run()
line2.set_xdata(np.fft.fftfreq(BUFFER_SIZE,1/RATE)[:BUFFER_SIZE//2])
while True:
    if OUTPUT:play_worker.get()
    data_record=record_worker.get()
    record_worker.run()
    if OUTPUT:play_worker.run()
    data=np.frombuffer(data_record,dtype=np.int16)
    data2y=np.abs(np.fft.fft(data)[:BUFFER_SIZE//2])
    line1.set_ydata(data)
    line2.set_ydata(data2y)
    fig.canvas.draw()
    fig.canvas.flush_events()
    now_time=time.time()
    if (BUFFER_SIZE / RATE/CHANNELS) - (now_time - ltime) > 0: time.sleep((BUFFER_SIZE / RATE/CHANNELS) - (now_time - ltime))
    print(1/(now_time - ltime))
    ltime = now_time