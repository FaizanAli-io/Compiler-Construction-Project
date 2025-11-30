# Conditional: Sign function
# Returns -1, 0, or 1 based on sign of input

func sign(x) {
    if x > 0 goto positive;
    if x < 0 goto negative;
    return 0;
    
    positive:
    return 1;
    
    negative:
    let neg = 0 - 1;
    return neg;
}

print sign(42);
print sign(0);
print sign(0 - 17);

end;
