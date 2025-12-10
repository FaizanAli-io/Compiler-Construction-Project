# Error Test: Mismatched Braces
let x = 5.0;

repeat i in 1..10 {
    print i;
    # Missing closing brace
;

end;
