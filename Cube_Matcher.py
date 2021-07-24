from math import *
import copy


class Axis:
    def __init__(self, vector):
        self.unitVector = vector

    def rotate(self, depth, angle):
        for p in planeList:
            if p.normalVector == self.unitVector:
                p.rotate(angle)
        pass


class Plane:
    def __init__(self, normalVector, upperVector):
        self.normalVector = normalVector
        self.upperVector = upperVector
        # self.state = [[0 for i in range(cubeSize)] for i in range(cubeSize)]
        self.state = [[1, 0, 0, 0], [2, 0, 0, 0], [3, 0, 0, 0], [4, 0, 0, 0]]

    def rotate(self, angle):
        tempState = copy.deepcopy(self.state)
        trans = (cubeSize - 1) / 2
        for column in range(cubeSize):
            for row in range(cubeSize):
                newRow = int((row - trans) * cos(angle) + (column - trans) * sin(angle) + trans + 0.5)
                newColumn = int(-(row - trans) * sin(angle) + (column - trans) * cos(angle) + trans + 0.5)
                self.state[newColumn][newRow] = tempState[column][row]

    def printState(self):
        for column in range(cubeSize):
            for row in range(cubeSize):
                print("%d " % self.state[column][row], end='')
            print()
        print("Plane normal vector:", self.normalVector)
        print("Plane upper vector:", self.upperVector, "\n")


class UnitVector:
    def __init__(self):
        self.x = [1, 0, 0]
        self.mx = [-1, 0, 0]
        self.y = [0, 1, 0]
        self.my = [0, -1, 0]
        self.z = [0, 0, 1]
        self.mz = [0, 0, -1]


def printCubeState():
    pass


if __name__ == "__main__":
    cubeSize = 4
    unitVector = UnitVector()
    axisX = Axis(unitVector.x)
    axisY = Axis(unitVector.y)
    axisZ = Axis(unitVector.z)
    axisMX = Axis(unitVector.mx)
    axisMY = Axis(unitVector.my)
    axisMZ = Axis(unitVector.mz)

    plane1 = Plane(unitVector.x, unitVector.z)
    plane2 = Plane(unitVector.mx, unitVector.z)
    plane3 = Plane(unitVector.y, unitVector.z)
    plane4 = Plane(unitVector.my, unitVector.x)
    plane5 = Plane(unitVector.z, unitVector.mx)
    plane6 = Plane(unitVector.mz, unitVector.mx)
    planeList = [plane1, plane2, plane3, plane4, plane5, plane6]

    for plane in planeList:
        plane.printState()

    plane1.rotate(pi/2)
    plane1.printState()
