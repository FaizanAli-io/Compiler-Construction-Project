# Error Test: Function Call with Wrong Arity
func add(a, b) {
    return a + b;
}

let x = add(5.0);  # add() expects 2 arguments, got 1

print x;

end;
