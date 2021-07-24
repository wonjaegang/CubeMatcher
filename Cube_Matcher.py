class Axis:
    def __init__(self, vector):
        self.unitVector = vector

    def rotate(self, target, angle):
        pass


class Plane:
    def __init__(self, normalVector, upperVector):
        self.normalVector = normalVector
        self.upperVector = upperVector
        self.state = [[0 for i in range(cubeSize)] for i in range(cubeSize)]

    def initializeState(self):
        pass

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
    cubeSize = 3
    unitVector = UnitVector()
    axisX = Axis(unitVector.x)
    axisY = Axis(unitVector.y)
    axisZ = Axis(unitVector.z)

    plane1 = Plane(unitVector.x, unitVector.z)
    plane2 = Plane(unitVector.mx, unitVector.z)
    plane3 = Plane(unitVector.y, unitVector.z)
    plane4 = Plane(unitVector.my, unitVector.x)
    plane5 = Plane(unitVector.z, unitVector.mx)
    plane6 = Plane(unitVector.mz, unitVector.mx)
    planeList = [plane1, plane2, plane3, plane4, plane5, plane6]

    for plane in planeList:
        plane.printState()
