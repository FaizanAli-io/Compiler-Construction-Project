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
    sub rsp, 64  ; Allocate stack space for variables

    mov rax, 8
    mov [rbp - 8], rax
    mov rax, [rbp - 8]
    mov [rbp - 16], rax
    mov rax, [rbp - 16]
    mov [rbp - 24], rax
    mov rax, [rbp - 24]
    mov [rbp - 32], rax
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 40]
    mov [rbp - 48], rax
    mov rax, 8
    mov [rbp - 56], rax
    mov rax, [rbp - 56]
    mov [rbp - 64], rax
    mov rsi, [rbp - 16]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    mov rsi, [rbp - 32]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    mov rsi, [rbp - 48]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    mov rsi, [rbp - 64]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp

_exit:
    mov rsp, rbp
    pop rbp
    mov rax, 60      ; sys_exit
    xor rdi, rdi     ; exit code 0
    syscall