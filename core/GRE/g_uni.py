class CellUnion:
    def __init__(self, cells):
        self.__cells = cells
        self.__stat = [int(''.join(map(str, cell.read())), 2) for cell in cells]
        self.__unionLen = len(cells)

    def getUnionLength(self):
        return self.__unionLen
    
    def clear(self):
        for cell in self.__cells:
            cell.clear()

    def __fixOverflow(self):
        for i in range(len(self.__stat)-1,0,-1):
            if self.__stat[i] > 255:
                self.__stat[i-1] += (self.__stat[i] - 255)
                self.__stat[i] -= 255
        if self.__stat[0] > 255:
            self.clear()
            
        


    