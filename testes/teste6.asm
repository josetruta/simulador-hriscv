addi x1, x0, 3
addi x2, x0, 2
add x3, x1, x2
beq x3, x0, skip
nop
skip:
    addi x4, x0, 7