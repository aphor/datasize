def value_equivalence_check(a,b):
    assert a == b

def string_format_check(a,b,c):
    assert a.format(b) == c

def test_true_is_not_false():
    assert True != False
