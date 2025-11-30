# Triangular numbers in PatternLang
# Prints the first 10 triangular numbers (1, 3, 6, 10, 15, ...)

let n = 10;
let sum = 0;

repeat i in 1..n {
    let sum = sum + i;
    print sum;
}

end;
