# Conditional: Range checker
# Demonstrates multiple conditions

func in_range(x, min, max) {
    if x < min goto outside;
    if x > max goto outside;
    return 1;
    
    outside:
    return 0;
}

print in_range(5, 1, 10);
print in_range(15, 1, 10);
print in_range(1, 1, 10);
print in_range(10, 1, 10);
print in_range(0, 1, 10);

end;
