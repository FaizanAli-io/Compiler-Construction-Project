# Float operations in loops
let n = 5.0;
let sum = 0.0;

repeat i in 1..10 {
    let fi = i * 1.0;
    let temp = sum + fi * 0.5;
    let sum = temp;
}

print sum;

# Float function
func square(x) {
    return x * x;
}

print square(2.5);
print square(3.0);

end;
