import math
from RiskAssessment import RiskAssessment

class Rules(object):
    def Initialize(self,safetyThreshold ):
        self.safetyThreshold = safetyThreshold

    #返回值为当前状态下的有效动作空间
    #左转 返回 -1
    #右转 返回 1
    #保持 返回 2
    #无限制 0
    def GetRulesAct(self,v1,v2,p1,p2,currentUcr):
        angle = RiskAssessment.GetRelativeAngle(v1,p1,p2)

        if currentUcr > self.safetyThreshold:
            if angle < 0:
                angle = 360 + angle
            cT = math.pi -  abs(v2.angle - v1.angle)
            if (angle >= 355 and angle < 360 and cT <= 5) or\
                (angle >= 0 and angle < 5 ) or \
                (angle >= 5 and angle < 67.5 and cT <= 5):
                return 1
            elif (angle >= 67.5 and angle < 112.5 and cT > 5):
                return -1
            elif (angle >= 355 and angle < 360 and cT > 5) or\
                (angle >= 112.5 and angle < 274.5 ) or\
                (angle >= 247.5 and angle < 355 and cT > 5):
                return 2
       
        return 0
