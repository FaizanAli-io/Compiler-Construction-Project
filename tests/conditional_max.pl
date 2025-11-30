# Conditional: Maximum of two numbers
# Demonstrates comparison and conditional branching

func max(a, b) {
    let diff = a - b;
    if diff >= 0 goto return_a;
    return b;
    return_a:
    return a;
}

print max(15, 23);
print max(42, 17);
print max(10, 10);

end;
