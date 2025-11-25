# Powers of 2 pattern in PatternLang
# Demonstrates doubling with arithmetic

let n = 8;
let power = 1;

repeat i in 1..n {
    print power;
    let power = power * 2;
}

end;
