import random
import pygame
pygame.init()

# 큐브의 크기
cubeSize = 2

# GUI 관련 변수
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 204, 0)
ORANGE = (255, 102, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

pieceSize = 50
gridSize = pieceSize * cubeSize
screen = pygame.display.set_mode((gridSize * 7, gridSize * 5))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 12 * cubeSize, True)


class Cube:
    def __init__(self):
        self.pieces = [Piece([i, j, k]) for k in range(cubeSize) for j in range(cubeSize) for i in range(cubeSize)]

    # Piece 객체 리스트의 객체들을 위치순서대로 정렬
    def sortPieces(self):
        self.pieces.sort(key=lambda x: x.location[2] * cubeSize * cubeSize + x.location[1] * cubeSize + x.location[0])

    # Piece 객체리스트로 부터 큐브의 면 색 배열 정보 추출
    def getPlaneArray(self):
        planeArray = []
        for direction in range(6):
            planeArray.append([piece.colorState[direction] for piece in self.pieces
                               if piece.location[direction % 3] == (cubeSize - 1) * (1 - direction // 3)])
        return planeArray

    # 맞춰지지 않은 색들의 수 계산
    def countUnmatched(self):
        colorList = [RED, BLUE, WHITE, ORANGE, GREEN, YELLOW]
        planArray = self.getPlaneArray()
        unmatched = 0
        for i, plane in enumerate(planArray):
            unmatched += len(plane) - plane.count(colorList[i])
        return unmatched

    # 큐브 회전함수
    def rotate(self, axis, target, direction):
        for piece in self.pieces:
            if piece.location[axis.index(1)] == target:
                piece.rotateLocation(axis, direction)
                piece.rotateColorState(axis, direction)

    # 큐브 역회전함수
    def inverseRotate(self, axis, target, direction):
        self.rotate(axis, target, -direction)

    # 큐브를 무작위로 섞는 함수
    def mixCube(self):
        mixCount = cubeSize * 20
        for _ in range(mixCount):
            axis = [0, 0]
            axis.insert(random.choice(range(3)), 1)
            self.rotate(axis, random.choice(range(cubeSize)), random.choice([1, -1]))
            self.displayCube()
            pygame.display.update()
            pygame.time.wait(10)

    # GUI 에 큐브의 색 배열 출력
    def displayCube(self, userInput=None, inputButtonArray=None):
        planeArray = self.getPlaneArray()
        for i, color in enumerate(planeArray[0]):
            start = [gridSize * 2, gridSize * 2]
            left = start[0] + (i % cubeSize) * pieceSize
            top = start[1] - (i // cubeSize - (cubeSize - 1)) * pieceSize
            if userInput:
                inputButtonArray[0].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[0][i].show()
                inputButtonArray[0][i].allocatedPiece = self.pieces[cubeSize * (i + 1) - 1]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)
        for i, color in enumerate(planeArray[1]):
            start = [gridSize * 3 + 5, gridSize * 2]
            left = start[0] + ((cubeSize - 1) - i % cubeSize) * pieceSize
            top = start[1] - (i // cubeSize - (cubeSize - 1)) * pieceSize
            if userInput:
                inputButtonArray[1].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[1][i].show()
                inputButtonArray[1][i].allocatedPiece = \
                    self.pieces[(i // cubeSize + 1) * cubeSize * cubeSize - (cubeSize - i % cubeSize)]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)
        for i, color in enumerate(planeArray[2]):
            start = [gridSize * 2, gridSize * 1 - 5]
            left = start[0] + (i // cubeSize) * pieceSize
            top = start[1] + (i % cubeSize) * pieceSize
            if userInput:
                inputButtonArray[2].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[2][i].show()
                inputButtonArray[2][i].allocatedPiece = self.pieces[i + cubeSize * cubeSize * (cubeSize - 1)]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)
        for i, color in enumerate(planeArray[3]):
            start = [gridSize * 4 + 10, gridSize * 2]
            left = start[0] + ((cubeSize - 1) - i % cubeSize) * pieceSize
            top = start[1] - (i // cubeSize - (cubeSize - 1)) * pieceSize
            if userInput:
                inputButtonArray[3].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[3][i].show()
                inputButtonArray[3][i].allocatedPiece = self.pieces[i * cubeSize]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)
        for i, color in enumerate(planeArray[4]):
            start = [gridSize * 1 - 5, gridSize * 2]
            left = start[0] + (i % cubeSize) * pieceSize
            top = start[1] - (i // cubeSize - (cubeSize - 1)) * pieceSize
            if userInput:
                inputButtonArray[4].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[4][i].show()
                inputButtonArray[4][i].allocatedPiece = \
                    self.pieces[(i // cubeSize) * cubeSize * cubeSize + i % cubeSize]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)
        for i, color in enumerate(planeArray[5]):
            start = [gridSize * 2, gridSize * 3 + 5]
            left = start[0] + (i // cubeSize) * pieceSize
            top = start[1] + ((cubeSize - 1) - i % cubeSize) * pieceSize
            if userInput:
                inputButtonArray[5].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
                inputButtonArray[5][i].show()
                inputButtonArray[5][i].allocatedPiece = self.pieces[i]
            else:
                pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
                pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)


class Piece:
    # location: [x, y, z], colorState = [x, y, z, -x, -y, -z]
    def __init__(self, location):
        self.location = location
        self.colorState = [RED if location[0] == cubeSize - 1 else 'E',
                           BLUE if location[1] == cubeSize - 1 else 'E',
                           WHITE if location[2] == cubeSize - 1 else 'E',
                           ORANGE if location[0] == 0 else 'E',
                           GREEN if location[1] == 0 else 'E',
                           YELLOW if location[2] == 0 else 'E']

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


class PushButton(pygame.Rect):
    def __init__(self, pos, size, color):
        super().__init__(pos, size)
        self.color = color
        self.allocatedPiece = 0

    def show(self):
        pygame.draw.rect(screen, self.color, [[self.left, self.top], [self.width, self.height]])
        pygame.draw.rect(screen, BLACK, [[self.left, self.top], [self.width, self.height]], 1)

    def addText(self, displayText):
        text = font.render(displayText, True, BLACK)
        text_rect = text.get_rect(center=(self.left + self.width // 2, self.top + self.height // 2))
        screen.blit(text, text_rect)

    def changeColor(self):
        colorList = [RED, BLUE, WHITE, ORANGE, GREEN, YELLOW]
        self.color = colorList[colorList.index(self.color) - 1]
        self.show()


class AI:
    def __init__(self):
        self.virtualCube = Cube()
        self.virtualCube.pieces = cube.pieces.copy()
        self.path = []

    def selectRotation(self):
        # A* 알고리즘으로 먼저 구현해보자. 이후에 헤더파일로 떼어내자.
        self.path.append(self.virtualCube.getPlaneArray())
        lowestCost = float('inf')
        bestRotation = 0
        for axis in range(3):
            for target in range(cubeSize):
                for direction in [-1, 1]:
                    rotation = [[1 if i == axis else 0 for i in range(3)], target, direction]
                    self.virtualCube.rotate(*rotation)
                    currentCost = self.calculateCost()
                    if lowestCost > currentCost:
                        lowestCost = currentCost
                        bestRotation = rotation
                    self.virtualCube.inverseRotate(*rotation)
        print("Best Rotation:", bestRotation)
        print("Cost: %d" % lowestCost)
        print("=" * 50)
        return bestRotation

    def calculateCost(self):
        if self.virtualCube.getPlaneArray() in self.path:
            return float('inf')
        rotation = 0
        unmatched = self.virtualCube.countUnmatched()
        return rotation + unmatched


# 사용자로부터 큐브의 초기상태를 입력받음
def getUserInput():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 큐브 무작위로 섞기
            if startingButtons[0].collidepoint(pygame.mouse.get_pos()):
                screen.fill(WHITE)
                cube.mixCube()
                return False
            # 큐브의 색 배열을 사용자가 직접 입력
            elif startingButtons[1].collidepoint(pygame.mouse.get_pos()):
                inputButtonArray = [[] for _ in range(6)]
                confirmButton = PushButton([gridSize * 5, gridSize * 4], [gridSize, gridSize // 2], GREY)

                screen.fill(WHITE)
                confirmButton.show()
                confirmButton.addText("Confirm")
                cube.displayCube(True, inputButtonArray)
                pygame.display.update()

                while True:
                    if userInputDone(inputButtonArray, confirmButton):
                        return False
    return True


# 클릭을 통해 사용자가 색 입력
def userInputDone(inputButtonArray, confirmButton):
    for inputEvent in pygame.event.get():
        if inputEvent.type == pygame.MOUSEBUTTONDOWN:
            for planeButton in inputButtonArray:
                for button in planeButton:
                    if button.collidepoint(pygame.mouse.get_pos()):
                        button.changeColor()
                        pygame.display.update()
            if confirmButton.collidepoint(pygame.mouse.get_pos()):
                for d, planeButton in enumerate(inputButtonArray):
                    for button in planeButton:
                        button.allocatedPiece.colorState[d] = button.color
                screen.fill(WHITE)
                cube.displayCube()
                pygame.display.update()
                return True
    return False


if __name__ == "__main__":
    # 큐브 초기화
    cube = Cube()

    # 사용자 입력 관련 객체 및 GUI 초기화
    startingButtons = [PushButton([gridSize * 1, gridSize * 2], [gridSize * 2, gridSize], GREY),
                       PushButton([gridSize * 4, gridSize * 2], [gridSize * 2, gridSize], GREY)]
    rotationCountDisplay = PushButton([gridSize * 4, gridSize * 4], [gridSize * 2, gridSize // 2], WHITE)

    screen.fill(WHITE)
    startingButtons[0].show()
    startingButtons[0].addText("Mix Randomly")
    startingButtons[1].show()
    startingButtons[1].addText("User Input")
    pygame.display.update()

    # 메인 루프
    running = True
    selecting = True
    rotationCount = 0
    ai_1 = AI()
    while running:
        # 사용자 입력 루프
        while selecting:
            selecting = getUserInput()

        # AI 에게서 다음 회전정보를 받아서 큐브를 회전
        nextRotate = ai_1.selectRotation()
        cube.rotate(*nextRotate)
        cube.sortPieces()
        rotationCount += 1

        # 현재 큐브 상태 GUI 디스플레이
        cube.displayCube()
        rotationCountDisplay.show()
        rotationCountDisplay.addText("Rotate: %d" % rotationCount)
        pygame.display.update()
        pygame.time.wait(50)

        # 큐브 맞추기 완료
        if not cube.countUnmatched():
            print("Cube Solved!!!")
            while True:
                pass
