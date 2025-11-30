# Test constant folding optimization
# Shows how optimizer simplifies expressions

let x = 5 + 3;      # Should fold to: x = 8
let y = x * 1;      # Should simplify to: y = x
let z = y + 0;      # Should simplify to: z = y
let a = 2 * 4;      # Should fold to: a = 8

print x;
print y;
print z;
print a;

end;
