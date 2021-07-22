class Axis:
    def __init__(self, unitVector):
        self.unitVector = unitVector

    def rotate(self, target, angle):
        pass


class Plane:
    def __init__(self, normalVector):
        self.normalVector = normalVector
        self.state = [[0 for i in range(cubeSize)] for i in range(cubeSize)]

    def printState(self):
        for column in range(cubeSize):
            for row in range(cubeSize):
                print("%d " % self.state[column][row], end='')
            print()
        print("Plane normal vector:", self.normalVector, "\n")


def printCubeState():
    pass


if __name__ == "__main__":
    cubeSize = 3
    axisX = Axis([1, 0, 0])
    axisY = Axis([0, 1, 0])
    axisZ = Axis([0, 0, 1])
    plane1 = Plane([1, 0,  0])
    plane2 = Plane([-1, 0, 0])
    plane3 = Plane([0, 1,  0])
    plane4 = Plane([0, -1, 0])
    plane5 = Plane([0, 0,  1])
    plane6 = Plane([0, 0, -1])
    planeList = [plane1, plane2, plane3, plane4, plane5, plane6]

    for plane in planeList:
        plane.printState()
