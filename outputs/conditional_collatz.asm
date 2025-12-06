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
    sub rsp, 112  ; Allocate stack space for variables

func_count_to_limit:
    mov rax, [rbp - 16]
    mov [rbp - 24], rax
    mov rax, 1
    mov [rbp - 32], rax
    mov rax, 0
    mov [rbp - 40], rax
    mov rax, 1
    mov [rbp - 48], rax
L0:
    mov rax, [rbp - 48]
    mov rbx, 100
    cmp rax, rbx
    setle al
    movzx rax, al
    mov [rbp - 56], rax
    mov rax, [rbp - 56]
    test rax, rax
    jz L1
    mov rax, [rbp - 32]
    mov rbx, [rbp - 24]
    cmp rax, rbx
    setg al
    movzx rax, al
    mov [rbp - 64], rax
    mov rax, [rbp - 64]
    test rax, rax
    jz L2
    jmp done
L2:
    mov rax, [rbp - 32]
    mov [rbp - 40], rax
    mov rax, [rbp - 32]
    mov rbx, 1
    add rax, rbx
    mov [rbp - 80], rax
    mov rax, [rbp - 80]
    mov [rbp - 32], rax
    mov rax, [rbp - 48]
    mov rbx, 1
    add rax, rbx
    mov [rbp - 88], rax
    mov rax, [rbp - 88]
    mov [rbp - 48], rax
    jmp L0
L1:
done:
    ; Unknown operation: ret
    ; Unknown operation: ret
    ; Unknown operation: push
    ; call func_count_to_limit (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 96]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; call func_count_to_limit (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 104]
    lea rdi, [rel fmt_int]  ; First argument: format string
    xor rax, rax            ; No floating-point args
    push rbp                ; Align stack
    call printf
    pop rbp
    ; Unknown operation: push
    ; call func_count_to_limit (function calls not fully implemented)
    ; Unknown operation: getret
    mov rsi, [rbp - 112]
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