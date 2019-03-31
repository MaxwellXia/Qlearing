import math
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from matplotlib import pyplot
import matplotlib.pyplot as plt
from RewardFunc import RewardFunc
from DataType import *
from interval import Interval

#状态转移函数

#避碰规则
#0: 对驶相遇
#1: 右舷小角度交叉相遇
#2: 右舷大角度交叉相遇
#3: 追越
#4: 左舷交叉相遇
meet = [ 0, 1 ,2 ,3, 4]
func = [ 'left','right','none']

#p1为本船的坐标 p2为障碍物的坐标
#A:tan(-5)~tan(5)
#B:tan(5)~tan(67.5)
#C:tan(67.5)~tan(112.5)
#D:tan(112.5)~tan(247.5)
#E:tan(247.5)~tan(355)

rewardFunc = RewardFunc()
destination = Point()
destination.x = 100
destination.y = 100

speed = Speed()
speed.value = 10
speed.angle = 10

startPoint = Point()
startPoint.x = 0
startPoint.y = 0

barrierSpeed = Speed()
barrierSpeed.value = 10
barrierSpeed.angle = -10

barrierStartPoint = Point()
barrierStartPoint.x = 50
barrierStartPoint.y = 50


rewardFunc.Initialize(10,destination,speed,startPoint,barrierSpeed,barrierStartPoint)
value = rewardFunc.GetReward(10)

from Paint import Paint
#point = [[1,1],[2,2],[3,3],[4,4]]
#p = Paint()
#p.PaintLine(point,'*','测试','b')
#x = [0,1,2,3,4,5]
#y = [0,1,2,3,4,5]
#p.SetScale(x,y)
#p.show()
