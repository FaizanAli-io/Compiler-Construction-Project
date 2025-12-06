; PatternLang Compiler Output
; x86-64 NASM Assembly

global _start
extern printf

section .data
    fmt_int: db '%d', 10, 0  ; Integer format with newline

section .text

_start:
    push rbp
    mov rbp, rsp
    sub rsp, 152  ; Allocate stack space for variables

    mov rax, 20
    mov [rbp - 8], rax
    mov rax, 1
    mov [rbp - 16], rax
L0:
    mov rax, [rbp - 16]
    mov rbx, [rbp - 8]
    cmp rax, rbx
    setle al
    movzx rax, al
    mov [rbp - 24], rax
    mov rax, [rbp - 24]
    test rax, rax
    jz L1
    mov rax, [rbp - 16]
    cqo
    mov rbx, 3
    idiv rbx
    mov [rbp - 32], rax
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 40]
    mov rbx, 3
    imul rax, rbx
    mov [rbp - 48], rax
    mov rax, [rbp - 48]
    mov [rbp - 56], rax
    mov rax, [rbp - 16]
    mov rbx, [rbp - 56]
    sub rax, rbx
    mov [rbp - 64], rax
    mov rax, [rbp - 64]
    mov [rbp - 72], rax
    mov rax, [rbp - 72]
    mov rbx, 0
    cmp rax, rbx
    sete al
    movzx rax, al
    mov [rbp - 80], rax
    mov rax, [rbp - 80]
    test rax, rax
    jz L2
    jmp skip
L2:
    mov rax, [rbp - 16]
    cqo
    mov rbx, 5
    idiv rbx
    mov [rbp - 96], rax
    mov rax, [rbp - 96]
    mov [rbp - 104], rax
    mov rax, [rbp - 104]
    mov rbx, 5
    imul rax, rbx
    mov [rbp - 112], rax
    mov rax, [rbp - 112]
    mov [rbp - 120], rax
    mov rax, [rbp - 16]
    mov rbx, [rbp - 120]
    sub rax, rbx
    mov [rbp - 128], rax
    mov rax, [rbp - 128]
    mov [rbp - 136], rax
    mov rax, [rbp - 136]
    mov rbx, 0
    cmp rax, rbx
    sete al
    movzx rax, al
    mov [rbp - 144], rax
    mov rax, [rbp - 144]
    test rax, rax
    jz L3
    jmp skip
L3:
    mov rsi, [rbp - 16]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
skip:
    mov rax, [rbp - 16]
    mov rbx, 1
    add rax, rbx
    mov [rbp - 152], rax
    mov rax, [rbp - 152]
    mov [rbp - 16], rax
    jmp L0
L1:

_exit:
    mov rsp, rbp
    pop rbp
    mov rax, 60      ; sys_exit
    xor rdi, rdi     ; exit code 0
    syscall