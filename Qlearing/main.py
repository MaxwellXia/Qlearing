from RewardFunc import RewardFunc
import pandas as pd
from DataType import *
import random
from Paint import Paint
import math
from copy import copy
import np
from Database import Database
import os
from DrawDynamicGraph import DrawDynamicGraph
from Common import *

def GetMaxValue(array):
    temp = array[0]
    for value in array:
        if temp < value:
            temp = value
    return temp

actionArea = [0,-30,-25,-20,-15,-10,-5,5,10,15,20,25,30]
q_table = [ [0] *  13 for i in range(512)]

def UpdateQtable(value,row,angle):
    q_table[row][actionArea.index(angle)] = value

#配置参数
rewardFunc = RewardFunc()
destination = Point()
destination.x = 0
destination.y = 900

speed = Speed()
speed.value = 1
speed.angle = 0

startPoint = Point()
startPoint.x = 0
startPoint.y = 100

barrierSpeed = Speed()
barrierSpeed.value = 0.5
barrierSpeed.angle = 180

barrierStartPoint = Point()
barrierStartPoint.x = 0
barrierStartPoint.y = 900

safetyThreshold = 0.5
rewardFunc.Initialize(destination,speed,startPoint,barrierSpeed,barrierStartPoint,safetyThreshold)
learningRate = 0.8
discountFactor = 0.9
MaxExporeCount = 1500

P = 0.9 #从q表中选取Q值大的动作的概率
def GetGetGreedAction(statusIndex):
    if random.random() > 1 - P:
        array = q_table[statusIndex]
        actionIndex = array.index(GetMaxValue(array))
        action = actionArea[actionIndex]
        return action
    else:
        return random.randrange(-30,35,5)

    #判断无人船方向和无人船与目标连线的夹角在正负90°以内,如果不在范围内，就要换动作   
def IfAimArrow(moveAngle):
    currentangle = rewardFunc.GetSpeed().angle + moveAngle
    aimarrow = GetAgent_AimArrow(destination,rewardFunc.GetAgentLocation(),currentangle)
    if aimarrow <= 90 or aimarrow >= 270:
        return True 
    else:
        return False 

#判断文件是否存在，若存在则从文件中获取Q_table
database = Database()
if os.path.exists(Database.fileName):
    database.Load(q_table)

for i in range(10000):#探索的次数
    #初始化本船的坐标和障碍物的坐标为原始状态
    rewardFunc.Reset()
    exporeCount = 0
    #以下内容重复执行，直到触发终止信号

    while (not rewardFunc.IsEnd()) and (exporeCount < MaxExporeCount):
        exporeCount = exporeCount + 1
        
        #随机选择一个动作
        #random.randrange(-30,35,5)

        #使用贪婪算法获取动作
        moveAngle = GetGetGreedAction(rewardFunc.GetState())
        #moveAngle = random.randrange(-30,35,5)

        #如果 y 坐标相等则结束档次探索
        if 0 == round(rewardFunc.GetAgentLocation().y - destination.y,2):
            break;
        #判断选取的动作是否合法 不合法则重新选取动作,直到动作合法
        while not IfAimArrow(moveAngle):
           if ( rewardFunc.IfLegalEffect() ):
            #获取合法动作
               legalAction = rewardFunc.GetLegalAct()
               if 2 == legalAction:
                  moveAngle = 0
               elif legalAction * moveAngle < 0:
                    if legalAction == 1:
                       moveAngle = random.randrange(5,35,5)
                    elif legalAction == -1:
                         moveAngle = random.randrange(-30,0,5)
               else:
                   moveAngle = GetGetGreedAction(rewardFunc.GetState())
           else:
               moveAngle = GetGetGreedAction(rewardFunc.GetState())
           moveAngle = GetGetGreedAction(rewardFunc.GetState())
            
        #moveAngle = 0
        currentQvalue = q_table[rewardFunc.GetState()][actionArea.index(moveAngle)]
        rewardValue = rewardFunc.GetReward(moveAngle)

        #####################
        correntLoc = rewardFunc.GetAgentLocation()
        barrierLocation = rewardFunc.GetBarrierLocation()
        #####################
        qValue = round(currentQvalue + learningRate * (rewardValue + discountFactor * GetMaxValue(q_table[rewardFunc.GetState()]) - currentQvalue),3)
        UpdateQtable(qValue,rewardFunc.GetState(),moveAngle)

#将Q_table存放在文件中
database.Save(q_table)

#绘图
paint = Paint()
rewardFunc.Reset()
agentLine = []
barrierLine = []


minX = 0
maxX = 0
minY = 0
maxY = 0
count = 0
MaxCount = 2000

def Align(num):
    szie = 5
    inStr = str(num)
    spaceNum = szie - len(inStr)
    spaceStr = ' ' * spaceNum
    res = inStr + spaceStr
    return res

isFirstTime = True
while (not rewardFunc.IsGotDestination()) and (count < MaxCount):
    count = count + 1
    barrierPoint = copy(rewardFunc.GetBarrierLocation())
    barrierPoint.x = round(barrierPoint.x,2)
    barrierPoint.y = round(barrierPoint.y,2)
    agentPoint = copy(rewardFunc.GetAgentLocation())
    agentPoint.x = round(agentPoint.x,2)
    agentPoint.y = round(agentPoint.y,2)

    barrierLine.append(barrierPoint)
    agentLine.append(agentPoint)
    state = rewardFunc.GetState()
    array = q_table[state]
    maxQvalue = GetMaxValue(array)
    actionIndex = array.index(maxQvalue)
    action = actionArea[actionIndex]

    ###
    ctRes = state & 0b1
    angleRes = state &0b1110
    distanceRes = state & 0b110000
    aimarrowRes = state & 0b111000000

    print('state:' + Align(state) + ' aimarrowRes: ' + Align(aimarrowRes) + ' distanceRes: '+ Align(distanceRes) + ' angleRes: ' \
        + Align(angleRes) + ' Ct: ' + Align(ctRes) + ' angle: ' + Align(action))

    #获取x y 的刻度
    if isFirstTime:
        minX = rewardFunc.GetAgentLocation().x
        maxX = minX
        minY = rewardFunc.GetBarrierLocation().y
        maxY = minY
        isFirstTime = False
    #改变状态
    rewardFunc.GetReward(action)
    if rewardFunc.IsGotDestination():
        agentLine.append(copy(rewardFunc.GetAgentLocation()))
        barrierLine.append(copy(rewardFunc.GetBarrierLocation()))

    if rewardFunc.GetAgentLocation().x > maxX:
        maxX =round(rewardFunc.GetAgentLocation().x,0)
    if rewardFunc.GetBarrierLocation().x > maxX:
        maxX = round(rewardFunc.GetBarrierLocation().x,0)
    if rewardFunc.GetAgentLocation().x < minX:
        minX = round(rewardFunc.GetAgentLocation().x,0)
    if rewardFunc.GetBarrierLocation().x < minX:
        minX = round(rewardFunc.GetBarrierLocation().x,0)

    if rewardFunc.GetAgentLocation().y > maxY:
        maxY = round(rewardFunc.GetAgentLocation().y,0)
    if rewardFunc.GetBarrierLocation().y > maxY:
        maxY = round(rewardFunc.GetBarrierLocation().y,0)
    if rewardFunc.GetAgentLocation().y < minY:
        minY = round(rewardFunc.GetAgentLocation().y,0)
    if rewardFunc.GetBarrierLocation().y < minY:
        minY = round(rewardFunc.GetBarrierLocation().y,0)

drawDynamicGraph = DrawDynamicGraph()
drawDynamicGraph.Initialize(20,minX - 1,maxX + 1,minY - 1,maxY + 1)
drawDynamicGraph.SetLineInfo(agentLine,"本船",'r',barrierLine,'障碍船','y')
drawDynamicGraph.Start()

while True:
    i = 0
    i = i + 1
