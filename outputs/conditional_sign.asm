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
    sub rsp, 104  ; Allocate stack space for variables

func_sign:
    mov rax, [rbp - 16]
    mov [rbp - 24], rax
    mov rax, [rbp - 24]
    mov rbx, 0
    cmp rax, rbx
    setg al
    movzx rax, al
    mov [rbp - 32], rax
    mov rax, [rbp - 32]
    test rax, rax
    jz L0
    jmp positive
L0:
    mov rax, [rbp - 24]
    mov rbx, 0
    cmp rax, rbx
    setl al
    movzx rax, al
    mov [rbp - 48], rax
    mov rax, [rbp - 48]
    test rax, rax
    jz L1
    jmp negative
L1:
    ; Unknown operation: ret
positive:
    ; Unknown operation: ret
negative:
    mov rax, -1
    mov [rbp - 64], rax
    mov rax, [rbp - 64]
    mov [rbp - 72], rax
    ; Unknown operation: ret
    ; Unknown operation: ret
    ; Unknown operation: push
    ; call func_sign (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 80]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; call func_sign (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 88]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    mov rax, -17
    mov [rbp - 96], rax
    ; Unknown operation: push
    ; call func_sign (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 104]
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