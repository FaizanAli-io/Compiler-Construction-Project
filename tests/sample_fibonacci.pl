# Fibonacci sequence in PatternLang
# Prints the first 10 Fibonacci numbers

let n = 10;
let a = 0;
let b = 1;

repeat i in 1..n {
    print a;
    let t = a + b;
    let a = b;
    let b = t;
}

end;
