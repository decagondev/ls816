import instructions
import sys

class CPU:
    """
    CPU Class with instruction set run etc
    """
    def __init__(self, ram):
        self.SP = 7
        self.ram = ram
        self.reg = [0] * 16
        self.reg[self.SP] = 0xfff4
        self.ir = 0
        self.pc = 0
        self.fl = 0
        self.ie = 1

        self.inst_set_pc = False



        self.running = True

    def alu(self, inst, opa, opb):
        if inst == "ADD":
            self.reg[opa] += self.reg[opb]

        elif inst == "SUB":
            self.reg[opa] -= self.reg[opb]

        elif inst == "MUL":
            self.reg[opa] *= self.reg[opb]

        elif inst == "DIV":
            self.reg[opa] /= self.reg[opb]
        
        elif inst == "AND":
            self.reg[opa] &= self.reg[opb]

        elif inst == "OR":
            self.reg[opa] &= self.reg[opb]

        elif inst == "NOT":
            self.reg[opa] = ~self.reg[opa]
        
        elif inst == "XOR":
            self.reg[opa] ^= self.reg[opb]

        elif inst == "SHL":
            self.reg[opa] <<= self.reg[opb]
        
        elif inst == "SHR":
            self.reg[opa] >>= self.reg[opb]
        
        

    
    def run(self, screen):
        if self.running:
            # Fetch instruction and operands
            self.ir = self.ram.read(self.pc)
            opa = self.ram.read(self.pc + 1)
            opb = self.ram.read(self.pc + 2)
            print(f"{self.ir}: {opa}, {opb}")
            inst_size = ((self.ir >> 6) & 0b11) + 1

            # Decode
            if self.ir == instructions.op["HLT"]:
                self.running = False
                # sys.exit()

            
            elif self.ir == instructions.op["PRN"]:
                print(self.reg[opa])
                self.pc += 2
                return self.reg[opa]
            
            elif self.ir == instructions.op["LDI"]:
                self.reg[opb] = opa
            
            elif self.ir == instructions.op["PRA"]:
                print(chr(self.reg[opa]))
                return chr(self.reg[opa])
            
            elif self.ir == instructions.op["ADD"]:
                self.alu("ADD", opa, opb)

            elif self.ir == instructions.op["SUB"]:
                self.alu("SUB", opa, opb)

            elif self.ir == instructions.op["MUL"]:
                self.alu("MUL", opa, opb)

            elif self.ir == instructions.op["DIV"]:
                self.alu("DIV", opa, opb)

            elif self.ir == instructions.op["PUSH"]:
                self.reg[self.SP] -= 1
                self.ram.write(self.reg[self.SP], self.reg[opa])

            elif self.ir == instructions.op["POP"]:
                data = self.ram.read(self.reg[self.SP])
                self.reg[opa] = data


            self.pc += inst_size






