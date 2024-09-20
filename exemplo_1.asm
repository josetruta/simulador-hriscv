# Verifica se um determinado número é par.
addi x1, x0, 30 # Adiciona o número a ser verificado em x1.
addi x7, x0, 1 # Adiciona o valor 1 em x7.
addi x6, x0, 2 # Adiciona o valor 2 em x6.
add x2, x0, x1 # Faz cópia do número a ser verificado em x2, para iteração.
loop: 
    beq x2, x0, true # Se o número resultante for igual à 0, é par.
    beq x2, x7, false # Se o número resultante for igual à 1, é ímpar.
    sub x2, x2, x6 # Subtrai 2 do número em verificação.
    jal x0, loop  # Retorna ao ínicio do loop.
true:
    addi x3, x0, 1 # Caso seja par, adiciona 1 em x3.
    nop # Encerra execução.
false:
    nop # Encerra execução.