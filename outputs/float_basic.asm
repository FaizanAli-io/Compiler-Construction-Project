; PatternLang Compiler Output
; x86-64 NASM Assembly

global _start
extern printf

section .data
    fmt_float: db '%.6g', 10, 0  ; Float format with newline

section .text

_start:
    push rbp
    mov rbp, rsp
    sub rsp, 32  ; Allocate stack space for variables

    mov rax, 3140000
    cvtsi2sd xmm0, rax
    movsd [rbp - 8], xmm0
    mov rax, 2000000
    cvtsi2sd xmm0, rax
    movsd [rbp - 16], xmm0
    movsd xmm0, [rbp - 8]
    movsd xmm1, [rbp - 16]
    addsd xmm0, xmm1
    movsd [rbp - 24], xmm0
    movsd xmm0, [rbp - 24]
    movsd [rbp - 32], xmm0
    movsd xmm0, [rbp - 8]
    lea rdi, [rel fmt_float]  ; First argument: format string
    mov rax, 1              ; 1 floating-point arg
    push rbp                ; Align stack
    call printf
    pop rbp
    movsd xmm0, [rbp - 16]
    lea rdi, [rel fmt_float]  ; First argument: format string
    mov rax, 1              ; 1 floating-point arg
    push rbp                ; Align stack
    call printf
    pop rbp
    movsd xmm0, [rbp - 32]
    lea rdi, [rel fmt_float]  ; First argument: format string
    mov rax, 1              ; 1 floating-point arg
    push rbp                ; Align stack
    call printf
    pop rbp

_exit:
    mov rsp, rbp
    pop rbp
    mov rax, 60      ; sys_exit
    xor rdi, rdi     ; exit code 0
    syscall