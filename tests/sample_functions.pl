# Functions in PatternLang
# Define a function to compute sum of two numbers and use it

func add(a, b) {
    return a + b;
}

let x = 10;
let y = 32;
let z = add(x, y);
print z;

# Function for nth triangular number via loop
func tri(n) {
    let sum = 0;
    repeat i in 1..n {
        let sum = sum + i;
    }
    return sum;
}

print tri(10);

end;
