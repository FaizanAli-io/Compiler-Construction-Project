# Simple sum calculation
let n = 5;
let sum = 0;

repeat i in 1..n {
    let temp = sum + i;
    let sum = temp;
}

print sum;

end;
