import math
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
from matplotlib import pyplot
import matplotlib.pyplot as plt

class Paint(object):
    """description of class"""
    #首先调用此函数添加想要绘制的曲线，pointInfo为坐标数组，marker为节点要显示的形状
    #label为图列要显的文字
    def PaintLine(self,pointInfo,marker,label,color):
        xArray = [0]
        yArray = [0]
        for point in pointInfo:
            xArray.append(point.x)
            yArray.append(point.y)
        plt.plot(xArray,yArray,color = color,label = label)


    """ 设置坐标轴的标度 """ 
    def SetScale(self,xScale,yScale):
        pyplot.xticks(xScale)
        pyplot.yticks(yScale)

    """ 显示图像 """ 
    def show(self):
        #设置显示图列
        plt.legend()
        plt.show()