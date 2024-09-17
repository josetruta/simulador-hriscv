addi x5, x0, 4
addi x6, x0, 5
add x7, x5, x6
beq x5, x6, loop
sub x7, x6, x5
loop:
    nop
