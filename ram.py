class Ram:
    def __init__(self, size):
        self.mem = [0] * size
    
    def read(self, mar):
        return self.mem[mar]

    def write(self, mar, mdr):
        self.mem[mar] = mdr
    
    def load_program(self, filename):
        address = 0
        with open(filename) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '':  # ignore blanks
                    continue
                val = int(num, 2)

                self.mem[address] = val
                # print(self.mem[address])
                address += 1
        return address
