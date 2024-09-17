andi x1, x0, 7
andi x2, x0, 3
or x3, x1, x2
bne x1, x3, done
addi x1, x1, 2
done:
    nop