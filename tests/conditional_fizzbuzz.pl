# Conditional: FizzBuzz-style pattern
# Print number, but skip multiples of 3 and 5

let n = 20;

repeat i in 1..n {
    # Check if divisible by 3
    let div3 = i / 3;
    let mult3 = div3 * 3;
    let rem3 = i - mult3;
    
    if rem3 == 0 goto skip;
    
    # Check if divisible by 5
    let div5 = i / 5;
    let mult5 = div5 * 5;
    let rem5 = i - mult5;
    
    if rem5 == 0 goto skip;
    
    # Not divisible by 3 or 5, print it
    print i;
    
    skip:
}

end;
