import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

POINTS = 100
sin_list = [0] * POINTS
indx = 0
 
fig, ax = plt.subplots()
ax.set_ylim([0,100])
ax.set_xlim([0,100])
#ax.set_autoscale_on(False)
#ax.set_xticks(range(0, 100, 10))
#ax.set_yticks(range(-2, 3, 1))
#ax.grid(True)

x = []
y = []
x1 = []
y1 = []
line_sin, = ax.plot(x, y, label='正弦', color='cornflowerblue')
line_sin1, = ax.plot(x1, y1, label='正弦1', color='r')
ax.legend(loc='upper center', ncol=4, prop=font_manager.FontProperties(size=10))
 
 
countX = 0
countY = 0

def sin_output(ax):
    global indx, sin_list, line_sin,countX,countY,x,y
    if indx == 20:
        indx = 0
    indx += 1
 
    countX += 1
    countY += 1
    #sin_list = sin_list[1:] + [np.sin((indx / 10) * np.pi)]
    #line_sin.set_ydata(sin_list)
    x.append(countX)
    y.append(countY)
    x1.append(countX)
    y1.append(countY + 4)
    line_sin.set_xdata(x)
    line_sin.set_ydata(y)
    ax.draw_artist(line_sin)

    line_sin1.set_xdata(x1)
    line_sin1.set_ydata(y1)
    ax.draw_artist(line_sin1)
    ax.figure.canvas.draw()
 
 
timer = fig.canvas.new_timer(interval=100)
timer.add_callback(sin_output, ax)
timer.start()
plt.show()