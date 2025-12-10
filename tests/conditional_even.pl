# Conditional: Print even numbers only
# Uses if-goto to skip odd numbers

let n = 10;

repeat i in 1..n {
    let mod = i % 2;
    let is_odd = mod == 1;

    if is_odd goto skip;
    print i;
    skip:
}

end;
