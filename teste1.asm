addi x1, x0, 5
addi x2, x0, 10
add x3, x1, x2
beq x1, x2, skip
addi x1, x1, 1
skip:
    nop