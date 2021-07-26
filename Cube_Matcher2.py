class Piece:
    def __init__(self, location):
        self.colorState = {'x': 0, 'y': 0, 'z': 0, '-x': 0, '-y': 0, '-z': 0}
        self.location = {'x': location[0], 'y': location[1], 'z': location[2]}


if __name__ == "__main__":
    cubeSize = 3
    pieces = [Piece([i, j, k]) for i in range(cubeSize) for j in range(cubeSize) for k in range(cubeSize)]
    for i in pieces:
        print(i.location)
