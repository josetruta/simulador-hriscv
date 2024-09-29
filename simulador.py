import sys

class hsriscv:
    def __init__(self):
        # Inicializando os registradores (r0 a r7) e o PC
        self.registradores = [0] * 8
        self.pc = 0

        # Memória de instruções (128 endereços) e memória de dados (16 endereços)
        self.instruction_memory = ["00000000000000000000000000000000"] * 128
        self.data_memory = [0] * 16

    def load_instructions(self, instructions):
        # Carregar as instruções na memória de instruções
        for i, instruction in enumerate(instructions):
            if i < 128:
                self.instruction_memory[i] = instruction

    def decode_execute(self, instruction):
        # Decodificar e executar a instrução
        opcode = instruction[-7:] 

        # Mapeamento de opcodes para instruções
        if opcode == "0110011":  # Instruções do tipo R (add, sub, and, or)
            funct3 = instruction[17:20]
            funct7 = instruction[:7]
            rd = int(instruction[20:25], 2)  
            rs1 = int(instruction[12:17], 2) 
            rs2 = int(instruction[7:12], 2)  

            if funct3 == "000" and funct7 == "0000000":  # add
                self.registradores[rd] = self.registradores[rs1] + self.registradores[rs2]
            elif funct3 == "000" and funct7 == "0100000":  # sub
                self.registradores[rd] = self.registradores[rs1] - self.registradores[rs2]
            elif funct3 == "111":  # and
                self.registradores[rd] = self.registradores[rs1] & self.registradores[rs2]
            elif funct3 == "110":  # or
                self.registradores[rd] = self.registradores[rs1] | self.registradores[rs2]

        elif opcode == "0010011":  # Instruções do tipo I (addi, andi)
            funct3 = instruction[17:20]
            rd = int(instruction[20:25], 2)  
            rs1 = int(instruction[12:17], 2)  

            imm_bin = instruction[:12]
            imm = int(imm_bin, 2) if imm_bin[0] == '0' else int(imm_bin, 2) - (1 << 12)   

            if funct3 == "000":  # addi
                self.registradores[rd] = self.registradores[rs1] + imm
            elif funct3 == "111":  # andi
                self.registradores[rd] = self.registradores[rs1] & imm

        elif opcode == "1100011":  # Instruções de controle de fluxo (beq, bne)
            funct3 = instruction[17:20]
            rs1 = int(instruction[12:17], 2)  
            rs2 = int(instruction[7:12], 2)   
            imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24]
            offset = int(imm, 2)

            if funct3 == "000":  # beq
                if self.registradores[rs1] == self.registradores[rs2]:
                    self.pc = offset * 4
                    return  
            elif funct3 == "001":  # bne
                if self.registradores[rs1] != self.registradores[rs2]:
                    self.pc = offset * 4
                    return  

        elif opcode == "1101111":  # jal
            rd = int(instruction[20:25], 2)
            imm = int(instruction[:20], 2)     

            if rd != 0:
                self.registradores[rd] = self.pc
            self.pc = imm * 4
            return 

        elif opcode == "0000011":  # ld
            rd = int(instruction[20:25], 2)  
            rs1 = int(instruction[12:17], 2)  
            imm = int(instruction[:12], 2)   

            self.registradores[rd] = self.data_memory[rs1 + imm]

        elif opcode == "0100011":  # sd
            rs1 = int(instruction[12:17], 2)  
            rs2 = int(instruction[7:12], 2)   
            imm = int(instruction[:12], 2)   

            self.data_memory[rs1 + imm] = self.registradores[rs2]

        self.pc += 4

    def run(self):
        # Executar o código carregado até encontrar um NOP, fim das instruções ou sair da memória
        while self.pc < len(self.instruction_memory):
            instruction = self.instruction_memory[self.pc // 4]
            if instruction == "00000000000000000000000000000000":
                break
            if instruction == "00000000000000000000000000010011": 
                break
            self.decode_execute(instruction)

    def print_state(self):
        # Imprimir o estado atual dos registradores e do PC
        print(f"PC: {self.pc}")
        for i, reg in enumerate(self.registradores):
            print(f"r{i}: {reg}")

def load_from_file(filename):
    # Função para ler o arquivo de instruções
    with open(filename, 'r') as file:
        instructions = [line.strip() for line in file.readlines()]
    return instructions

if __name__ == "__main__":

    arquivo = sys.argv[1]
    instructions = load_from_file(arquivo)
    
    machine = hsriscv()
    
    machine.load_instructions(instructions)
    machine.run()
    machine.print_state()
