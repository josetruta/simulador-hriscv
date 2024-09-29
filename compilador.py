import sys

def ler_arquivo_asm(nome_arquivo):
    # Lê o conteúdo do arquivo .asm e retorna as linhas como uma lista de strings
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    print(f"Linhas lidas do arquivo {nome_arquivo}:")
    print(linhas)
    return linhas

def converter_registrador(registrador):
    # Converte o registrador (ex: x5) para seu número (5)
    return int(registrador.replace('x', '').strip())

def converter_para_binario(valor, bits):
    # Converte um valor inteiro para uma string binária com o número de bits especificado
    binario = bin(valor & int('1' * bits, 2))[2:] 
    return binario.zfill(bits)  # Adiciona zeros à esquerda para garantir o tamanho

def converter_instrucao_para_binario(instrucao, rotulos):
    # Divide a instrução em partes e remove espaços adicionais e vírgulas
    partes = [parte.strip().strip(',') for parte in instrucao.split()]
    instrucao_binaria = ''

    print(f"Convertendo instrução: {partes}")

    if partes[0] == 'add':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        rs2 = converter_registrador(partes[3])
        opcode = '0110011'
        funct3 = '000'
        funct7 = '0000000'
        instrucao_binaria = funct7 + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode
    
    elif partes[0] == 'sub':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        rs2 = converter_registrador(partes[3])
        opcode = '0110011'
        funct3 = '000'
        funct7 = '0100000'
        instrucao_binaria = funct7 + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode
    
    elif partes[0] == 'and':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        rs2 = converter_registrador(partes[3])
        opcode = '0110011'
        funct3 = '111'
        funct7 = '0000000'
        instrucao_binaria = funct7 + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'or':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        rs2 = converter_registrador(partes[3])
        opcode = '0110011'
        funct3 = '110'
        funct7 = '0000000'
        instrucao_binaria = funct7 + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'addi':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        imm = int(partes[3])
        imm = format((1 << 12) + imm, '012b') if imm < 0 else format(imm, '012b')
        opcode = '0010011'
        funct3 = '000'
        instrucao_binaria = imm + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'andi':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        imm = int(partes[3])
        imm = format((1 << 12) + imm, '012b') if imm < 0 else format(imm, '012b')
        opcode = '0010011'
        funct3 = '111'
        instrucao_binaria = imm + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'ld':
        rd = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        opcode = '0000011'
        funct3 = '011'
        instrucao_binaria = converter_para_binario(0, 12) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'sd':
        rs2 = converter_registrador(partes[1])
        rs1 = converter_registrador(partes[2])
        opcode = '0100011'
        funct3 = '011'
        instrucao_binaria = converter_para_binario(0, 7) + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + converter_para_binario(0, 5) + opcode

    elif partes[0] == 'beq':
        rs1 = converter_registrador(partes[1])
        rs2 = converter_registrador(partes[2])
        offset = rotulos[partes[3]]
        opcode = '1100011'
        funct3 = '000'
        imm = converter_para_binario(offset, 12)
        instrucao_binaria = imm[0] + imm[2:8] + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + imm[8:] + imm[1] + opcode

    elif partes[0] == 'bne':
        rs1 = converter_registrador(partes[1])
        rs2 = converter_registrador(partes[2])
        offset = rotulos[partes[3]]
        opcode = '1100011'
        funct3 = '001'
        imm = converter_para_binario(offset, 12)
        instrucao_binaria = imm[0] + imm[2:8] + converter_para_binario(rs2, 5) + converter_para_binario(rs1, 5) + funct3 + imm[8:] + imm[1] + opcode

    elif partes[0] == 'jal':
        rd = converter_registrador(partes[1])
        offset = rotulos[partes[2]]
        opcode = '1101111'
        instrucao_binaria = converter_para_binario(offset, 20) + converter_para_binario(rd, 5) + opcode

    elif partes[0] == 'nop':
        # A instrução NOP é representada por um valor específico em binário.
        # Na arquitetura RISC-V, NOP pode ser representado como '00000000000000000000000000010011'
        instrucao_binaria = '00000000000000000000000000010011'
    
    else:
        raise ValueError(f"Instrução desconhecida: {partes[0]}")

    print(f"Instrução binária: {instrucao_binaria}") 
    return instrucao_binaria

def compilar_asm_para_binario(nome_arquivo_asm):
    # Lê o arquivo .asm
    linhas = ler_arquivo_asm(nome_arquivo_asm)
    
    # Identifica os rótulos e mapeia-os para os números das linhas
    rotulos = {}
    instrucoes = []
    linha_atual = 0
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith('#'):  # Ignora linhas vazias e comentários
            continue

        linha = linha.split("#")[0]
        
        # Verifica se a linha é um rótulo (exemplo: loop:)
        if ':' in linha:
            rotulo = linha.replace(':', '').strip()
            rotulos[rotulo] = linha_atual
            print(f"Rótulo identificado: {rotulo} na linha {linha_atual}") 
        else:
            instrucoes.append(linha)
            linha_atual += 1

    # Converte as instruções para binário
    instrucoes_binarias = []
    for instrucao in instrucoes:
        print(f"Instrução a ser convertida: {instrucao}") 
        instrucao_binaria = converter_instrucao_para_binario(instrucao, rotulos)
        instrucoes_binarias.append(instrucao_binaria)

    # Escreve as instruções binárias em um arquivo .txt
    nome_arquivo_saida = nome_arquivo_asm.replace('.asm', '.txt')
    with open(nome_arquivo_saida, 'w') as arquivo:
        for binario in instrucoes_binarias:
            arquivo.write(f'{binario}\n')
    
    print(f'Instruções binárias salvas em {nome_arquivo_saida}')

    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python compilador.py <nome_arquivo.asm>")
    else:
        nome_arquivo_asm = sys.argv[1]
        compilar_asm_para_binario(nome_arquivo_asm)


