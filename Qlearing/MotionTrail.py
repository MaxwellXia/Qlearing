import math
from copy import copy
from DataType import Point

class MotionTrail(object):
    """description of class"""
    """speed 为矢量，包含大小和方向""" 
    def Initialize(self,speed,startPoint,barrierSpeed,barrierStartPoint):
        self.speed = copy(speed)
        self.startSpeed = copy(speed)
        self.startPoint = copy(startPoint)
        self.currentLocation = copy(startPoint)
        self.lastLocation = copy(startPoint)

        self.barrierStartSpeed = copy(barrierSpeed)
        self.barrierSpeed = copy(barrierSpeed)
        self.barrierStartPoint = copy(barrierStartPoint)
        self.barrierCurrentLocation = copy(barrierStartPoint)
        self.barrierLastLocation = copy(barrierStartPoint)

    def Move(self,changeAngle,speedValue = -1): 
        if(-1 != speedValue):
            self.speed.value = copy(speedValue)

        self.lastLocation = copy(self.currentLocation)
        self.speed.angle = self.speed.angle + changeAngle
        if self.speed.angle > 360:
            self.speed.angle -= 360
        if self.speed.angle < 0:
            self.speed.angle += 360
        self.currentLocation.x = self.currentLocation.x + self.speed.value * math.sin(self.speed.angle * (math.pi / 180))
        self.currentLocation.y = self.currentLocation.y + self.speed.value * math.cos(self.speed.angle * (math.pi / 180))

        self.barrierLastLocation = copy(self.barrierCurrentLocation)
        self.barrierCurrentLocation.x = self.barrierCurrentLocation.x + self.barrierSpeed.value * math.sin(self.barrierSpeed.angle * (math.pi / 180))
        self.barrierCurrentLocation.y = self.barrierCurrentLocation.y + self.barrierSpeed.value * math.cos(self.barrierSpeed.angle * (math.pi / 180))

    #按照给定的角度运行但是不改变智能体和障碍物的坐标，并且返回以动后的坐标
    def PreMove(self,changeAngle):
        point = Point()
        point.x = self.currentLocation.x + self.speed.value * math.sin( (self.speed.angle + changeAngle) * (math.pi / 180))
        point.y = self.currentLocation.y + self.speed.value * math.cos( (self.speed.angle + changeAngle )* (math.pi / 180))
        return point


    def GetCurrentLocation(self):
        return self.currentLocation

    def GetLastLocation(self):
        return self.lastLocation

    def GetBarrierCurrentLocation(self):
        return self.barrierCurrentLocation

    def GetBarrierLastLocation(self):
        return self.barrierLastLocation

    def GetSpeed(self):
        return self.speed 

    def GetBarrierSpeed(self):
        return self.barrierSpeed

    def Reset(self):
        self.speed = copy(self.startSpeed)
        self.currentLocation = copy(self.startPoint)
        self.lastLocation = copy(self.startPoint)

        self.barrierSpeed =  copy(self.barrierStartSpeed)
        self.barrierCurrentLocation = copy(self.barrierStartPoint)
        self.barrierLastLocation = copy(self.barrierStartPoint)
