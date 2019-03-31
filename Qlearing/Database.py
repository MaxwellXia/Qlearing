from Paint import Paint
from DataType import *
from copy import copy

class Database(object):
    """description of class"""
    fileName = "qtable.txt"

    def Load(self,qTable):
        file = open(Database.fileName, "r")
        qTable.clear()

        line = file.readline().strip('\n').split(' ')
        while line:
            array = []
            for value in line:
                array.append(float(value))
            qTable.append(copy(array))
            line = file.readline()
            if line:
                line = line.strip('\n').split(' ')
        file.close()


    def Save(self,qTable):
        file = open(Database.fileName, "w")
        length = len(qTable)
        for index in range(length):
            array = qTable[index]
            line = ''
            for arrayIndex in range(len(array)):
                line += str(array[arrayIndex])
                if arrayIndex < len(array) - 1:
                    line += ' '
            if index < length - 1:
                line += '\n'
            file.write(line)
        file.close()
        
