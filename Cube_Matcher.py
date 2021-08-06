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
screen.fill(WHITE)


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
        pygame.display.update()

    def addText(self, displayText):
        text = font.render(displayText, True, BLACK)
        text_rect = text.get_rect(center=(self.left + self.width // 2, self.top + self.height // 2))
        screen.blit(text, text_rect)
        pygame.display.update()

    def changeColor(self):
        colorList = [RED, BLUE, WHITE, ORANGE, GREEN, YELLOW]
        self.color = colorList[colorList.index(self.color) - 1]
        self.show()


class AI:
    def __init__(self):
        pass

    def selectRotation(self):
        axis = [1, 0, 0]
        target = 0
        direction = 1
        return axis, target, direction


# Piece 객체 리스트의 객체들을 위치순서대로 정렬
def sortPieces():
    pieces.sort(key=lambda x:
                x.location[2] * cubeSize * cubeSize +
                x.location[1] * cubeSize +
                x.location[0])


# Piece 객체리스트로 부터 큐브의 면 색 배열 정보 추출
def getPlaneArray():
    planeArray = []
    for direction in range(6):
        planeArray.append([piece.colorState[direction] for piece in pieces
                           if piece.location[direction % 3] == (cubeSize - 1) * (1 - direction // 3)])
    return planeArray


# 큐브 회전함수
def rotate(axis, target, direction):
    for piece in pieces:
        if piece.location[axis.index(1)] == target:
            piece.rotateLocation(axis, direction)
            piece.rotateColorState(axis, direction)
    print("Rotation - Axis:", axis, "Target:", target, "Direction,", direction)


# 큐브를 무작위로 섞는 함수
def mixCube():
    mixCount = cubeSize * 20
    for _ in range(mixCount):
        axis = [0, 0]
        axis.insert(random.choice(range(3)), 1)
        rotate(axis, random.choice(range(cubeSize)), random.choice([1, -1]))
        displayGUI()
        pygame.time.wait(10)


# GUI 에 큐브의 색 배열 출력
def displayGUI():
    planeArray = getPlaneArray()
    for i, color in enumerate(planeArray[0]):
        start = [gridSize * 2, gridSize * 2]
        left = start[0] + (i % cubeSize) * pieceSize
        top = start[1] - (i // cubeSize - (cubeSize - 1)) * pieceSize
        if userInput:
            inputButtonArray[0].append(PushButton([left, top], [pieceSize, pieceSize], WHITE))
            inputButtonArray[0][i].show()
            inputButtonArray[0][i].allocatedPiece = pieces[cubeSize * (i + 1) - 1]
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
                pieces[(i // cubeSize + 1) * cubeSize * cubeSize - (cubeSize - i % cubeSize)]
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
            inputButtonArray[2][i].allocatedPiece = pieces[i + cubeSize * cubeSize * (cubeSize - 1)]
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
            inputButtonArray[3][i].allocatedPiece = pieces[i * cubeSize]
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
            inputButtonArray[4][i].allocatedPiece = pieces[(i // cubeSize) * cubeSize * cubeSize + i % cubeSize]
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
            inputButtonArray[5][i].allocatedPiece = pieces[i]
        else:
            pygame.draw.rect(screen, color, [[left, top], [pieceSize, pieceSize]])
            pygame.draw.rect(screen, BLACK, [[left, top], [pieceSize, pieceSize]], 1)

    pygame.display.update()


if __name__ == "__main__":
    # 큐브 초기화
    pieces = [Piece([i, j, k]) for k in range(cubeSize) for j in range(cubeSize) for i in range(cubeSize)]
    inputButtonArray = [[] for _ in range(6)]

    # 사용자 입력 관련 객체 및 GUI
    startingButtons = [PushButton([gridSize * 1, gridSize * 2], [gridSize * 2, gridSize], GREY),
                       PushButton([gridSize * 4, gridSize * 2], [gridSize * 2, gridSize], GREY)]
    startingButtons[0].show()
    startingButtons[0].addText("Mix Randomly")
    startingButtons[1].show()
    startingButtons[1].addText("User Input")

    rotationCountDisplay = PushButton([gridSize * 4, gridSize * 4], [gridSize * 2, gridSize // 2], WHITE)

    # 메인 루프
    running = True
    selecting = True
    userInput = False
    rotationCount = 0
    ai_1 = AI()
    while running:
        # 사용자 입력 루프
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Mix the cube randomly
                    if startingButtons[0].collidepoint(pygame.mouse.get_pos()):
                        screen.fill(WHITE)
                        mixCube()
                        selecting = False
                    # User directly set the cube color state
                    elif startingButtons[1].collidepoint(pygame.mouse.get_pos()):
                        screen.fill(WHITE)

                        confirmButton = PushButton([gridSize * 5, gridSize * 4], [gridSize, gridSize // 2], GREY)
                        confirmButton.show()
                        confirmButton.addText("Confirm")

                        # User input loop: User clicks the pieces to change its color
                        userInput = True
                        displayGUI()
                        while userInput:
                            for inputEvent in pygame.event.get():
                                if inputEvent.type == pygame.MOUSEBUTTONDOWN:
                                    for planeButton in inputButtonArray:
                                        for button in planeButton:
                                            if button.collidepoint(pygame.mouse.get_pos()):
                                                button.changeColor()
                                    if confirmButton.collidepoint(pygame.mouse.get_pos()):
                                        for i, planeButton in enumerate(inputButtonArray):
                                            for button in planeButton:
                                                button.allocatedPiece.colorState[i] = button.color
                                        userInput = False
                                        selecting = False
                                        screen.fill(WHITE)
                                        displayGUI()

        # AI 에게서 다음 회전정보를 받아서 큐브를 회전
        nextRotate = ai_1.selectRotation()
        rotate(*nextRotate)
        sortPieces()
        rotationCount += 1

        rotationCountDisplay.show()
        rotationCountDisplay.addText("Rotate: %d" % rotationCount)
        displayGUI()
        pygame.time.wait(500)
