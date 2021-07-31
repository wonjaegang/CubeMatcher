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


def getPlaneArray():
    planeArray = []
    for direction in range(6):
        planeArray.append([piece.colorState[direction] for piece in pieces
                           if piece.location[direction % 3] == (cubeSize - 1) * (1 - direction // 3)])
    return planeArray


if __name__ == "__main__":
    cubeSize = 3

    pieces = [Piece([i, j, k]) for i in range(cubeSize) for j in range(cubeSize) for k in range(cubeSize)]
    for i in pieces:
        print("location:", i.location)
        print("color state:", i.colorState)
        print("=" * 50)
    print(getPlaneArray())
