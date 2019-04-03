from copy import copy
import math

#获取无人船与目标点的连线的方位角
def GetAimAngle(agentPoint1,aimPoint):
    agentPoint = copy(agentPoint1)
    agentPoint.x = round(agentPoint.x,2)
    agentPoint.y = round(agentPoint.y,2)
    aimPoint.x = round(aimPoint.x,2)
    aimPoint.y = round(aimPoint.y,2)
    deviationX1 = aimPoint.x - agentPoint.x
    deviationY1 = aimPoint.y - agentPoint.y

    quadrantAngle3 = 0
    if deviationX1 >= 0 and deviationY1 >= 0:
       quadrantAngle3 = 0
    elif deviationX1 < 0 and deviationY1 < 0:
       quadrantAngle3 = 180
    elif deviationX1 >= 0 and deviationY1 < 0:
       quadrantAngle3 = 180
    elif deviationX1 < 0 and deviationY1 >= 0:
       quadrantAngle3 = 360

    if deviationY1 == 0:
        if agentPoint.x < aimPoint.x:
            return 90
        else:
            return 270

    aimAngle = math.atan (deviationX1/deviationY1)*(180/math.pi)+quadrantAngle3
    return aimAngle


def GetAgent_AimArrow(aimPoint,agentPoint,agentDirection):
    aimAngle = GetAimAngle(agentPoint,aimPoint)
    aimarrow = agentDirection - aimAngle
    if aimarrow < 0:
       aimarrow += 360
    return aimarrow


