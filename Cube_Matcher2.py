import pygame
pygame.init()


class Piece:
    # location: [x, y, z], colorState = [x, y, z, -x, -y, -z]
    def __init__(self, location):
        self.location = location
        self.colorState = ['R' if location[0] == cubeSize - 1 else 'E',
                           'B' if location[1] == cubeSize - 1 else 'E',
                           'W' if location[2] == cubeSize - 1 else 'E',
                           'O' if location[0] == 0 else 'E',
                           'G' if location[1] == 0 else 'E',
                           'Y' if location[2] == 0 else 'E']

    # 큐브 회전 시 조각의 위치변환
    # 회전 축과 평행한 요소는 고정, 나머지 요소들을 회전축이 원점이 오도록 이동, 회전변환 후 다시 원위치로 이동
    def rotateLocation(self, rotateAxis, direction):
        def rotate90Matrix(x, y, z):
            newX = rotateAxis[0] * x + rotateAxis[1] * (direction * z) + rotateAxis[2] * (-direction * y)
            newY = rotateAxis[0] * (-direction * z) + rotateAxis[1] * y + rotateAxis[2] * (direction * x)
            newZ = rotateAxis[0] * (direction * y) + rotateAxis[1] * (-direction * x) + rotateAxis[2] * z
            return [newX, newY, newZ]

        trans = (cubeSize - 1) / 2
        temp = list(map(lambda x: x - trans, self.location))
        self.location = list(map(lambda x: int(x + trans), rotate90Matrix(temp[0], temp[1], temp[2])))

    # 큐브 회전 시 조각의 색 방향 변환
    # 회전 축과 평행한 요소는 고정, 나머지 요소는 리스트 내에서 한 칸씩 이동
    # X, Z 축회전은 + 방향이면 정방향 이동, Y축은 - 방향이면 정방향 이동
    def rotateColorState(self, rotateAxis, direction):
        temp = self.colorState

        axisFactor = [[i, j] for i, j in enumerate(self.colorState) if i % 3 == rotateAxis.index(1)]
        for i, factor in enumerate(axisFactor):
            del(temp[factor[0] - i])
        temp = list(map(lambda x: temp[(x - direction + rotateAxis[1] * 2) % 4], range(4)))
        for factor in axisFactor:
            temp.insert(factor[0], factor[1])
        self.colorState = temp


# Piece 객체리스트로 부터 큐브의 면 정도 추출
def getPlaneArray():
    planeArray = []
    for direction in range(6):
        planeArray.append([piece.colorState[direction] for piece in pieces
                           if piece.location[direction % 3] == (cubeSize - 1) * (1 - direction // 3)])
    return planeArray


def rotate(axis, target, direction):
    for piece in pieces:
        if piece.location[axis.index(1)] in target:
            piece.rotateLocation(axis, direction)
            piece.rotateColorState(axis, direction)


if __name__ == "__main__":
    cubeSize = 3

    pieces = [Piece([i, j, k]) for i in range(cubeSize) for j in range(cubeSize) for k in range(cubeSize)]
    for i in pieces:
        print("location:", i.location)
        print("color state:", i.colorState)
        print("=" * 50)

    print(getPlaneArray())
    rotate([1, 0, 0], [0], 1)
    print(getPlaneArray())

    # print(getPlaneArray())
    # print(pieces[0].location, pieces[0].colorState)
    # pieces[0].rotateLocation([1, 0, 0], 1)
    # pieces[0].rotateColorState([1, 0, 0], 1)
    # print(pieces[0].location, pieces[0].colorState)
