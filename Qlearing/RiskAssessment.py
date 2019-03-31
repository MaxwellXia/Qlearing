import math
class RiskAssessment(object):
    """description of class"""
    pi = 180
    #dcpa = d * sin(方向角)
    def GetDcpa(self,angle,d):
        return d * math.sin(angle)

    #UDCPA 参数
    D1 = 100
    D2 = 200
    def GetUdcpa(self,dcpa):
        if dcpa <= RiskAssessment.D1:
            return 1
        elif dcpa > RiskAssessment.D2:
            return 0
        else:
            value = 0.5 - 0.5 * math.sin( math.pi / (RiskAssessment.D2 - RiskAssessment.D1) * (dcpa - (RiskAssessment.D1 + RiskAssessment.D2 ) / 2) )
            return value

    #tcpa = dcpa / 相对速度
    def GetTcpa(self,angle,d,v):
        if 0 != v:
            return (d * math.cos(angle)) / v #不变
        else:
            return 1

    #UTCPA 参数
    t1 = 35
    t2 = 67
    def GetUtcpa(self,tcpa):
        if tcpa <= RiskAssessment.t1:
            return 1
        elif tcpa > RiskAssessment.t2:
            return 0
        else:
            value = math.pow( (RiskAssessment.t2 - abs(tcpa) ) / (RiskAssessment.t2 - RiskAssessment.t1) , 2 )
            return value

    #UD 参数
    uD1 = 200
    uD2 = 300
    def GetUd(self,d):
        if d >= 0 and d <= RiskAssessment.uD1:
            return 1
        elif d > RiskAssessment.uD2:
            return 0
        else:
            value = math.pow( (RiskAssessment.uD2 -d) / (RiskAssessment.uD2 - RiskAssessment.uD1) , 2)
            return value

    # r1为无人船距离航道边界的最小安全距离， 
    # r2为无人船与航道边界有足够的空间进行避碰操作的距离。
    #内河航道尺寸R
    #UR 参数
    r1 = 50
    r2 = 100

    def GetUr(self,r):
        if r <= RiskAssessment.r1:
            return 1
        elif r > RiskAssessment.r2:
            return 0
        else:
            value = 0.5 - 0.5 * math.sin( (RiskAssessment.pi / (RiskAssessment.r2 - RiskAssessment.r1) ) * (r - (RiskAssessment.r1 + RiskAssessment.r2) / 2 ) )
            return value

    #相对你方位角
    #v1 为本船的速度
    #v2 为障碍船的速度
    #p1 为本船的坐标
    #p2 为障碍船的坐标
    
    def GetAngle(self,v1,v2,p1,p2):
        Vxr = round(v2.value * math.sin(v2.angle * (math.pi / 180)) - v1.value * math.sin(v1.angle * (math.pi / 180)),5)
        Vyr = round(v2.value * math.cos(v2.angle * (math.pi / 180)) - v1.value * math.cos(v1.angle * (math.pi / 180)),5)
        quadrantAngle = 0
        if Vxr >= 0 and Vyr >= 0:
            quadrantAngle = 0
        elif Vxr < 0 and Vyr < 0:
            quadrantAngle = 180
        elif Vxr >= 0 and Vyr < 0:
            quadrantAngle = 180
        elif Vxr < 0 and Vyr >= 0:
            quadrantAngle = 360
        if 0 != Vyr:
            relativeVelocityDirection = math.atan(Vxr / Vyr) + quadrantAngle * (math.pi / RiskAssessment.pi)
        else:##################################################################
            relativeVelocityDirection = 0
        deviationX = p2.x - p1.x
        deviationY = p2.y - p1.y
        quadrantAngle2 = 0
        if deviationX >= 0 and deviationY >= 0:
            quadrantAngle2 = 0
        elif deviationX < 0 and deviationY < 0:
            quadrantAngle2 = 180
        elif deviationX >= 0 and deviationY < 0:
            quadrantAngle2 = 180
        elif deviationX < 0 and deviationY >= 0:
            quadrantAngle2 = 360
        temp = 0
        if 0 != deviationY:
            temp = math.atan(deviationX / deviationY ) + quadrantAngle2 * (math.pi / RiskAssessment.pi)
        else:
            temp = 0#######################

        return relativeVelocityDirection - temp - math.pi

    def GetDistance(self,p1,p2):
        return math.sqrt(math.pow(p1.x - p2.x,2) + math.pow(p1.y - p2.y,2))

    #UCR 参数
    w1 = 0.4
    w2 = 0.3
    w3 = 0.12
    w4 = 0.18

    #v1 为本船的速度
    #v2 为障碍船的速度
    #p1 为本船的坐标
    #p2 为障碍船的坐标
    #r为内河的尺寸
    def GetUcr(self,p1,p2,v1,v2,r):
        Vxr = v2.value * math.sin(v1.angle * (math.pi / 180)) - v1.value * math.sin(v2.angle * (math.pi / 180))
        Vyr = v2.value * math.cos(v1.angle  * (math.pi / 180)) - v1.value * math.cos(v2.angle * (math.pi / 180))
        speed = math.sqrt(math.pow(Vxr,2) + math.pow(Vyr,2))
        angle = self.GetAngle(v1,v2,p1,p2)
        distance = self.GetDistance(p1,p2)
        dcpa = self.GetDcpa(angle,distance)
        tcpa = self.GetTcpa(angle,distance,speed)
        udcpa = self.GetUdcpa(dcpa)
        utcpa = self.GetUtcpa(tcpa)
        ud = self.GetUd(distance)
        ur = self.GetUr(r)

        res = RiskAssessment.w1 * udcpa + RiskAssessment.w2 * utcpa + RiskAssessment.w3 * ud + RiskAssessment.w4 * ur
        return res

    #v1 为本船的速度
    #v2 为障碍船的速度
    #p1 为本船的坐标
    #p2 为障碍船的坐标
    def GetOrValue(self,p1,p2,v1,v2,speed,r):
        angle = self.GetAngle(v1,v2,p1,p2)
        distance = self.GetDistance(p1,p2)
        dcpa = self.GetDcpa(angle,distance)
        tcpa = self.GetTcpa(angle,distance,speed)
        udcpa = self.GetUdcpa(dcpa)
        utcpa = self.GetUtcpa(tcpa)
        ud = self.GetUd(distance)
        ur = self.GetUr(r)#应该为船到河岸的距离

        return udcpa or utcpa or ud or ur

    def GetRelativeAngle(v1,p1,p2):
        deviationX = p2.x - p1.x
        deviationY = p2.y - p1.y
        quadrantAngle2 = 0
        if deviationX >= 0 and deviationY >= 0:
            quadrantAngle = 0
        elif deviationX < 0 and deviationY < 0:
            quadrantAngle = 180
        elif deviationX >= 0 and deviationY < 0:
            quadrantAngle = 180
        elif deviationX < 0 and deviationY >= 0:
            quadrantAngle = 360
        temp = 0
        if 0 != deviationY:
            temp = math.atan(deviationX / deviationY ) * (180 / math.pi) + quadrantAngle2
        else:
            temp = 0######################

        angle = temp - v1.angle
        return angle


