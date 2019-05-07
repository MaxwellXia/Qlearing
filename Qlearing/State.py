from DataType import *
from RiskAssessment import RiskAssessment
import math
from Common import *

class State(object):
    def Initialize(self,d1,d2,destination):
        self.d1 = d1
        self.d2 = d2
        self.aimarrowOffset =6
        self.distanceOffset = 4
        self.angleOffset = 1
        self.cTOffset = 0
        self.destination = destination
       
    #0   CT
    #1~3 Angle
    #4~5 Distance
    #6~8 aimarrow
    def GetState(self,p1,p2,v1,v2):
        distance = math.sqrt(math.pow(p1.x - p2.x,2) + math.pow(p1.y - p2.y,2))
        distanceRes = 0
        if distance <= self.d1:
            distanceRes= 0
        elif distance >= self.d2:
            distanceRes = 2
        else:
            distanceRes = 1

        angle = RiskAssessment.GetRelativeAngle(v1,p1,p2)
        if angle > 360:
            angle = angle - 360
        elif angle < 0:
            angle = angle + 360

        angleRes = 0
        if angle >= 355 and angle < 360:
            angleRes = 0
        elif angle >= 0 and angle < 5:
            angleRes = 1
        elif angle >= 5 and angle < 67.5:
            angleRes = 2
        elif angle >= 67.5 and angle < 112.5:
            angleRes = 3
        elif angle >= 112.5 and angle < 247.5:
            angleRes = 4
        else: 
            angleRes = 5
        
        ctRes = 0
        deviation = abs(v2.angle - v1.angle)
        cT = abs(180 -  deviation)
        if cT <= 5:
            ctRes = 0
        else:
            ctRes = 1

        aimarrowRes = 0
        aimarrow = GetAgent_AimArrow(self.destination,p1,v1.angle)
        if aimarrow < 30:
           aimarrowRes = 0
        elif aimarrow >= 30 and aimarrow < 60:
           aimarrowRes = 1
        elif aimarrow >= 60 and aimarrow < 90:
           aimarrowRes = 2
        elif aimarrow > 270 and aimarrow <= 300:
           aimarrowRes = 3
        elif aimarrow > 300 and aimarrow <= 330:
           aimarrowRes = 4
        elif aimarrow > 330 and aimarrow <= 360:
           aimarrowRes = 5
        else:
           aimarrowRes = 6
          
        res = (aimarrowRes << self.aimarrowOffset)|(distanceRes << self.distanceOffset)|(angleRes <<  self.angleOffset) | (ctRes << self.cTOffset)
        return res
