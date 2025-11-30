# Conditional: Absolute value function
# Returns positive version of number

func abs(x) {
    if x >= 0 goto positive;
    let neg = 0 - x;
    return neg;
    positive:
    return x;
}

let a = 5;
let b = 0 - 12;
let c = 0;

print abs(a);
print abs(b);
print abs(c);

end;
