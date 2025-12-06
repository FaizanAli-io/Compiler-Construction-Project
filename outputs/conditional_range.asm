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
    sub rsp, 120  ; Allocate stack space for variables

func_in_range:
    mov rax, [rbp - 16]
    mov [rbp - 24], rax
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 48]
    mov [rbp - 56], rax
    mov rax, [rbp - 24]
    mov rbx, [rbp - 40]
    cmp rax, rbx
    setl al
    movzx rax, al
    mov [rbp - 64], rax
    mov rax, [rbp - 64]
    test rax, rax
    jz L0
    jmp outside
L0:
    mov rax, [rbp - 24]
    mov rbx, [rbp - 56]
    cmp rax, rbx
    setg al
    movzx rax, al
    mov [rbp - 80], rax
    mov rax, [rbp - 80]
    test rax, rax
    jz L1
    jmp outside
L1:
    ; Unknown operation: ret
outside:
    ; Unknown operation: ret
    ; Unknown operation: ret
    ; Unknown operation: push
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_in_range (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 88]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_in_range (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 96]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_in_range (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 104]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_in_range (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 112]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; Unknown operation: push
    ; Unknown operation: push
    ; call func_in_range (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 120]
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