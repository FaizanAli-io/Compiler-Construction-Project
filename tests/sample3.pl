# Factorial-style pattern in PatternLang
# Demonstrates multiplication and accumulation

let n = 5;
let result = 1;

repeat i in 1..n {
    let result = result * i;
    print result;
}

end;
