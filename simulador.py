import argparse

# Definição do simulador
class RiscVMachine:
    def __init__(self):
        # Inicializando os registradores (r0 a r7) e o PC
        self.registradores = [0] * 8
        self.pc = 0

        # Memória de instruções (128 endereços) e memória de dados (16 endereços)
        self.instruction_memory = ["00000000000000000000000000000000"] * 128
        self.data_memory = [0] * 16

    def load_instructions(self, instructions):
        """Carregar as instruções na memória de instruções"""
        for i, instruction in enumerate(instructions):
            if i < 128:
                self.instruction_memory[i] = instruction

    def decode_execute(self, instruction):
        """Decodificar e executar a instrução"""
        opcode = instruction[-7:]  # Últimos 7 bits para opcode
        rd = int(instruction[20:25], 2)  # Registrador destino (rd)
        rs1 = int(instruction[12:17], 2)  # Primeiro registrador de origem (rs1)
        rs2 = int(instruction[7:12], 2)   # Segundo registrador de origem (rs2)
        imm = int(instruction[:12], 2)    # Imediato de 12 bits

        # Mapeamento de opcodes para instruções
        if opcode == "0110011":  # Instruções do tipo R (add, sub, and, or)
            funct3 = instruction[17:20]
            funct7 = instruction[:7]

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
            if funct3 == "000":  # addi
                self.registradores[rd] = self.registradores[rs1] + imm
            elif funct3 == "111":  # andi
                self.registradores[rd] = self.registradores[rs1] & imm

        elif opcode == "1100011":  # Instruções de controle de fluxo (beq, bne)
            funct3 = instruction[17:20]
            offset = imm << 1
            if funct3 == "000":  # beq
                if self.registradores[rs1] == self.registradores[rs2]:
                    self.pc += offset
                    return  # Skip PC increment
            elif funct3 == "001":  # bne
                if self.registradores[rs1] != self.registradores[rs2]:
                    self.pc += offset
                    return  # Skip PC increment

        elif opcode == "1101111":  # jal
            self.registradores[rd] = self.pc + 4
            self.pc += imm
            return  # Skip PC increment

        elif opcode == "0000011":  # ld
            self.registradores[rd] = self.data_memory[rs1 + imm]

        elif opcode == "0100011":  # sd
            self.data_memory[rs1 + imm] = self.registradores[rs2]

        # Incrementando o PC para a próxima instrução
        self.pc += 4

    def run(self):
        """Executar o código carregado até encontrar um NOP ou sair da memória"""
        while self.pc < len(self.instruction_memory):
            instruction = self.instruction_memory[self.pc // 4]
            if instruction == "00000000000000000000000000010011":  # NOP
                break
            self.decode_execute(instruction)
            #self.print_state()

    def print_state(self):
        """Imprimir o estado atual dos registradores e do PC"""
        print(f"PC: {self.pc}")
        for i, reg in enumerate(self.registradores):
            print(f"r{i}: {reg}")

# Função para ler o arquivo de instruções
def load_from_file(filename):
    with open(filename, 'r') as file:
        instructions = [line.strip() for line in file.readlines()]
    return instructions

# Exemplo de uso
if __name__ == "__main__":

    # Configurando o argparse para receber o arquivo pela linha de comando
    parser = argparse.ArgumentParser(description="Simulador de uma máquina RISC-V hipotética.")
    parser.add_argument("arquivo", help="Caminho para o arquivo .txt com as instruções em binário.")
    args = parser.parse_args()
    
    # Criando a máquina
    machine = RiscVMachine()

    # Carregando as instruções de um arquivo .txt
    instructions = load_from_file(args.arquivo)

    # Carregando as instruções na memória da máquina
    machine.load_instructions(instructions)

    # Executando as instruções
    machine.run()

    # Imprimindo o estado final da máquina
    machine.print_state()
