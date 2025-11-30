# Conditional: Simple bounded loop counter
# Demonstrates loop with early exit condition

func count_to_limit(limit) {
    let i = 1;
    let result = 0;
    
    repeat step in 1..100 {
        if i > limit goto done;
        let result = i;
        let i = i + 1;
    }
    
    done:
    return result;
}

print count_to_limit(5);
print count_to_limit(10);
print count_to_limit(15);

end;
