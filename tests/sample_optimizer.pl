# Test optimizer: constant folding, algebraic simplification, dead code elimination
# Demonstrates all three optimization techniques

# Constant Folding: compile-time arithmetic evaluation
# 5 + 3 → 8, 5 - 3 → 2, 5 * 3 → 15, 8 / 4 → 2.0
let a = 5 + 3;
let b = 5 - 3;
let e = 5 * 3;
let g = 8 / 4;

# Algebraic Simplification: eliminate identity operations
# x + 0 → x, x - 0 → x, x * 1 → x, x / 1 → x
let c = a + 0;
let d = b - 0;
let f = e * 1;
let h = g / 1;

# Dead Code Elimination: remove unused temporaries
# These intermediate values are computed but never used
let unused1 = 10 + 20;
let unused2 = 100 * 2;

# Print optimized results
print a;
print b;
print c;
print d;
print e;
print f;
print g;
print h;

end;
