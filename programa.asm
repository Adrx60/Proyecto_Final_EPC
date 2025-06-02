section .data
discos db 3
msg db ’Mover disco de %c a %c’, 0xA, 0

section .text
global _start

_start:
movzx eax, byte [discos] ; 0F B6 05 [addr discos]
push ’C’ ; 68 43 00 00 00
push ’B’ ; 68 42 00 00 00
push ’A’ ; 68 41 00 00 00
push eax ; 50
call hanoi ; E8 0A 00 00 00
add esp, 16 ; 83 C4 10

int 0x80 ; CD 80

hanoi:
push ebp ; 55
mov ebp, esp ; 89 E5
mov eax, [ebp+8] ; 8B 45 08

cmp eax, 1 ; 83 F8 01
jne recursivo ; 75 0E

; Caso base (imprimir)
; Aquí iría código para imprimir
jmp fin_hanoi ; EB 1C

recursivo:
; Hanoi(n-1, origen, auxiliar, destino)
dec eax ; 48
push [ebp+20] ; FF 75 14
push [ebp+16] ; FF 75 10
push [ebp+12] ; FF 75 0C
push eax ; 50
call hanoi ; E8 xx xx xx xx
add esp, 16 ; 83 C4 10

; Imprimir movimiento
; Aquí iría código para imprimir

; Hanoi(n-1, auxiliar, destino, origen)
mov eax, [ebp+8] ; 8B 45 08
dec eax ; 48
push [ebp+12] ; FF 75 0C
push [ebp+20] ; FF 75 14
push [ebp+16] ; FF 75 10
push eax ; 50
call hanoi ; E8 xx xx xx xx
add esp, 16 ; 83 C4 10

fin_hanoi:
leave ; C9
ret ; C3
