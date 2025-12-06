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
    sub rsp, 144  ; Allocate stack space for variables

func_add:
    mov rax, [rbp - 16]
    mov [rbp - 24], rax
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 24]
    mov rbx, [rbp - 40]
    add rax, rbx
    mov [rbp - 48], rax
    ; Unknown operation: ret
    ; Unknown operation: ret
    mov rax, 10
    mov [rbp - 56], rax
    mov rax, 32
    mov [rbp - 64], rax
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_add (function calls not fully implemented)
    ; Unknown operation: getret
    mov rax, [rbp - 72]
    mov [rbp - 80], rax
    mov rsi, [rbp - 80]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
func_tri:
    mov rax, [rbp - 16]
    mov [rbp - 96], rax
    mov rax, 0
    mov [rbp - 104], rax
    mov rax, 1
    mov [rbp - 112], rax
L0:
    mov rax, [rbp - 112]
    mov rbx, [rbp - 96]
    cmp rax, rbx
    setle al
    movzx rax, al
    mov [rbp - 120], rax
    mov rax, [rbp - 120]
    test rax, rax
    jz L1
    mov rax, [rbp - 104]
    mov rbx, [rbp - 112]
    add rax, rbx
    mov [rbp - 128], rax
    mov rax, [rbp - 128]
    mov [rbp - 104], rax
    mov rax, [rbp - 112]
    mov rbx, 1
    add rax, rbx
    mov [rbp - 136], rax
    mov rax, [rbp - 136]
    mov [rbp - 112], rax
    jmp L0
L1:
    ; Unknown operation: ret
    ; Unknown operation: ret
    ; Unknown operation: push
    ; call func_tri (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 144]
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