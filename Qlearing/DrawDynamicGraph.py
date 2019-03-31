import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class DrawDynamicGraph(object):
    def Initialize(self,speed,xMin,xMax,yMin,yMax):
        self.speed = speed
        self.xLim = [xMin,xMax]
        self.yLim = [yMin,yMax]
        self.fig,self.ax = plt.subplots()
        self.ax.set_xlim(self.xLim)
        self.ax.set_ylim(self.yLim)

    def SetLineInfo(self,angenLineInfo,agentLable,agentColor,barrierLineInfo,barrierLable,barrierColor):
        self.agentIndex = 0
        self.agentMaxIndex = len(angenLineInfo)
        self.angenLineInfo = angenLineInfo
        self.agentShowBufferX = []
        self.agentShowBufferY = []
        self.agentLine, = self.ax.plot(self.agentShowBufferX,self.agentShowBufferY, label=agentLable, color='g')

        self.barrierIndex = 0
        self.barrierMaxIndex = len(barrierLineInfo)
        self.barrierLineInfo = barrierLineInfo
        self.barrierShowBufferX = []
        self.barrierShowBufferY = []
        self.barrierLine, = self.ax.plot(self.barrierShowBufferX,self.barrierShowBufferY, label=barrierLable, color='r')
        self.ax.legend(loc='upper center', ncol=4, prop=font_manager.FontProperties(size=10))

    def ShowThread(self):
        #更新本船的信息
        if self.agentIndex < self.agentMaxIndex:
            self.agentShowBufferX.append(self.angenLineInfo[self.agentIndex].x)
            self.agentShowBufferY.append(self.angenLineInfo[self.agentIndex].y)
            self.agentLine.set_xdata(self.agentShowBufferX)
            self.agentLine.set_ydata(self.agentShowBufferY)
            self.agentIndex += 1
            self.ax.draw_artist(self.agentLine)

        #更新障碍物的信息
        if self.barrierIndex < self.barrierMaxIndex:
            self.barrierShowBufferX.append(self.barrierLineInfo[self.barrierIndex].x)
            self.barrierShowBufferY.append(self.barrierLineInfo[self.barrierIndex].y)
            self.barrierLine.set_xdata(self.barrierShowBufferX)
            self.barrierLine.set_ydata(self.barrierShowBufferY)
            self.barrierIndex += 1
            self.ax.draw_artist(self.barrierLine)

        #更新绘图
        self.ax.figure.canvas.draw()

    def Start(self):
        timer = self.fig.canvas.new_timer(self.speed)
        timer.add_callback(self.ShowThread)
        timer.start()
        plt.show()
