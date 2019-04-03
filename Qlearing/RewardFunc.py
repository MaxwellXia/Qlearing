from RiskAssessment import RiskAssessment
from MotionTrail import MotionTrail
from rules import Rules
from State import State
import math

class RewardFunc(object):
    """description of class"""
    #uA 为常量
    #destination 为目的地的坐标
    #safetyThreshold  当Ucr大于此值时将会采取避碰措施
    D1 = 200
    D2 = 300
    AgentRadius = 5
    revierWride = 400

    def Initialize(self,destination,speed,startPoint,barrierSpeed,barrierStartPoint,safetyThreshold,langTa = 0.8):
        self.riskAssessment = RiskAssessment()
        self.motionTrail = MotionTrail()
        self.motionTrail.Initialize(speed,startPoint,barrierSpeed,barrierStartPoint)
        self.uA = safetyThreshold
        self.langTa = langTa
        self.destination = destination
        self.rules = Rules()
        self.rules.Initialize(safetyThreshold)
        self.state = State()
        self.state.Initialize(RewardFunc.D1,RewardFunc.D2,destination)

    #r为河道宽度 可以设置为定值
    def  GetRc(self):
        p1 = self.motionTrail.GetCurrentLocation()
        p2 = self.motionTrail.GetBarrierCurrentLocation()
        v1 = self.motionTrail.speed
        v2 = self.motionTrail.barrierSpeed
        ucr = self.riskAssessment.GetUcr(p1,p2,v1,v2,RewardFunc.revierWride)
        orValue = self.riskAssessment.GetOrValue(p1,p2,v1,v2,abs(self.motionTrail.speed.value - self.motionTrail.barrierSpeed.value),RewardFunc.revierWride)
        lastUcr = self.riskAssessment.GetUcr(self.motionTrail.GetLastLocation(),self.motionTrail.GetBarrierLastLocation(),self.motionTrail.speed,self.motionTrail.barrierSpeed,RewardFunc.revierWride)

        if self.uA <= ucr and ucr < 1:
            if ucr < lastUcr:
                self.langTa = 0.8
                return 1   
            else:
                return -5
        elif ucr < self.uA:
            self.langTa = 0
            return 0           
        elif orValue == 1:
            return -10

    def GetRd(self):
        currentLocation = self.motionTrail.GetCurrentLocation()
        lastLocation = self.motionTrail.GetLastLocation()
        currentDistance = math.sqrt(math.pow(currentLocation.x - self.destination.x,2) + math.pow(currentLocation.y - self.destination.y,2))
        lastDistance = math.sqrt(math.pow(lastLocation.x - self.destination.x,2) + math.pow(lastLocation.y - self.destination.y,2))

        if currentDistance <= RewardFunc.AgentRadius:
            return 1000
        elif currentDistance < lastDistance:
            return 5
        elif currentDistance >= lastDistance:
            return -3

    SafeDistanceMin = 10
    SafeDistanceMax = 50
    def ObstacleAvoidance(self):
        currentDistanceWithBarrier = self.riskAssessment.GetDistance(self.motionTrail.GetCurrentLocation(),self.motionTrail.GetBarrierCurrentLocation())
        lastDistanceWithBarrier = self.riskAssessment.GetDistance(self.motionTrail.GetLastLocation(),self.motionTrail.GetBarrierLastLocation())
        if currentDistanceWithBarrier == 0:
            return -1000
        elif currentDistanceWithBarrier < RewardFunc.SafeDistanceMin:
            return -10
        elif currentDistanceWithBarrier > RewardFunc.SafeDistanceMin and currentDistanceWithBarrier < RewardFunc.SafeDistanceMax and currentDistanceWithBarrier < lastDistanceWithBarrier:
            return -5
        elif currentDistanceWithBarrier > RewardFunc.SafeDistanceMin and currentDistanceWithBarrier < RewardFunc.SafeDistanceMax and currentDistanceWithBarrier > lastDistanceWithBarrier:
            return 1
        elif currentDistanceWithBarrier > RewardFunc.SafeDistanceMax:
            return 0
        else:
            return 0


    def GetReward(self,angle):
        self.motionTrail.Move(angle)
        #rc = self.GetRc()
        rd = self.GetRd()
        obstacleAvoidance = self.ObstacleAvoidance()
        #value = self.langTa  * rc + (1 - self.langTa ) * rd
        value = self.langTa  * obstacleAvoidance + (1 - self.langTa ) * rd
        return value

    def Reset(self):
        self.motionTrail.Reset()

    def GetCurrentUcr(self):
        p1 = self.motionTrail.GetCurrentLocation()
        p2 = self.motionTrail.GetBarrierCurrentLocation()
        v1 = self.motionTrail.speed 
        v2 = self.motionTrail.barrierSpeed
        ucr = self.riskAssessment.GetUcr(p1,p2,v1,v2,RewardFunc.revierWride)
        return ucr

    #获取合法动作
    def GetLegalAct(self):
        ucr = self.GetCurrentUcr()
        speed = self.motionTrail.GetSpeed()
        barrierSpeed = self.motionTrail.GetBarrierSpeed()
        location = self.motionTrail.GetCurrentLocation()
        barrierLocation = self.motionTrail.GetBarrierCurrentLocation()

        res = self.rules.GetRulesAct(speed,barrierSpeed,location,barrierLocation,ucr)
        return res

    #判断给定的动作是否符合规则
    def IsActLegal(self,angle):
        if self.IfLegalEffect():
            legalFlag = self.GetLegalAct()
            if legalFlag == 0:
                return True
            elif angle * legalFlag > 0:
                return True
            elif legalFlag == 2 and angle == 0:
                return True
            else:
                return False
        else:
            return True

    def IfLegalEffect(self):
        if self.GetCurrentUcr() > self.rules.safetyThreshold:
            return True
        else:
            return False

    #判断探测是否触发终止条件
    def IsEnd(self):
        p1 = self.motionTrail.GetCurrentLocation()
        p2 = self.motionTrail.GetBarrierCurrentLocation()
        distanceWithAssessment = self.riskAssessment.GetDistance(p1,p2)
        isGotDestination = self.IsGotDestination()

        if 0 == distanceWithAssessment or isGotDestination:
            return True
        else:
            return False

    def IsGotDestination(self):
        distance = self.riskAssessment.GetDistance(self.destination,self.motionTrail.GetCurrentLocation())
        if distance <= RewardFunc.AgentRadius:
            return True
        else:
            return False

    def GetState(self):
        speed = self.motionTrail.GetSpeed()
        barrierSpeed = self.motionTrail.GetBarrierSpeed()
        location = self.motionTrail.GetCurrentLocation()
        barrierLocation = self.motionTrail.GetBarrierCurrentLocation()
        return self.state.GetState(location,barrierLocation,speed,barrierSpeed)

    def GetAgentLocation(self):
        return self.motionTrail.GetCurrentLocation()

    def GetBarrierLocation(self):
        return  self.motionTrail.GetBarrierCurrentLocation()

    def GetSpeed(self):
        return self.motionTrail.GetSpeed()
