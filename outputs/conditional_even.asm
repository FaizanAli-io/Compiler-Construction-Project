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
    sub rsp, 88  ; Allocate stack space for variables

    mov rax, 10
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
    mov rbx, 2
    idiv rbx
    mov [rbp - 32], rax
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 40]
    mov rbx, 2
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
    test rax, rax
    jz L2
    jmp skip
L2:
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
    mov [rbp - 88], rax
    mov rax, [rbp - 88]
    mov [rbp - 16], rax
    jmp L0
L1:

_exit:
    mov rsp, rbp
    pop rbp
    mov rax, 60      ; sys_exit
    xor rdi, rdi     ; exit code 0
    syscall