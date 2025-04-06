import keyboard
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
times=[time.time()]
datay1=[]
datay2=[]
datax=[]
mpl.use('QtAgg')
fig, ax = plt.subplots()
line1,line2=ax.plot([i for i in range(300)], [0 for i in range(300)],[i for i in range(300)], [0 for i in range(300)],linewidth=0.5)
ax.set_xlim(0, 300)
ax.set_ylim(0,1200)
plt.ion()
[plt.rcParams.__setitem__(i,[]) for i in plt.rcParams.keys() if i.startswith('keymap.')]
def on_press(e):
    if e.event_type == 'down':
        times.append(e.time)
        datay1.append(60/(times[-1]-times[-2]))
        datay2.append((times[-1]-times[-2])*2000)
        datax.append(times[-1]-times[0])
        line1.set_data(datax,datay1)
        #line2.set_data(datax, datay2)
keyboard.hook(on_press)
plt.show()
while True:
    fig.canvas.draw()
    fig.canvas.flush_events()