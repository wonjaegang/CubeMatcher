from math import *
import copy


class Axis:
    def __init__(self, vector):
        self.unitVector = vector

    # 0 < depth < cubeSize
    # angle : pi/2, pi, -pi/2
    def rotate(self, depth, angle):
        for p in planeList:
            if p.normalVector == self.unitVector:
                p.rotate(angle)
            if p.upperVector == self.unitVector:
                pass
            if dotProduct(p.normalVector, p.upperVector) == self.unitVector:
                pass
            if list(map(lambda x: -x, p.upperVector)) == self.unitVector:
                pass
            if dotProduct(p.upperVector, p.normalVector) == self.unitVector:
                pass


class Plane:
    def __init__(self, normalVector, upperVector):
        self.normalVector = normalVector
        self.upperVector = upperVector
        # self.state = [[0 for i in range(cubeSize)] for i in range(cubeSize)]
        self.state = [[1, 1, 0, 0], [2, 2, 0, 0], [3, 3, 0, 0], [4, 4, 0, 0]]

    def rotate(self, angle):
        tempState = copy.deepcopy(self.state)
        trans = (cubeSize - 1) / 2
        for column in range(cubeSize):
            for row in range(cubeSize):
                rotated = rotateVector(row - trans, column - trans, angle)
                newRow = int(rotated[0] + trans + 0.5)
                newColumn = int(rotated[1] + trans + 0.5)
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


def dotProduct(v1, v2):
    return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]


def rotateVector(x, y, angle):
    return [x * cos(angle) + y * sin(angle), -x * sin(angle) + y * cos(angle)]


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
    axisX.rotate(1, pi / 2)
    plane1.printState()
