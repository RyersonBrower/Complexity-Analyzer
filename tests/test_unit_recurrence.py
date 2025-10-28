import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer.app import naive_detect_recurrence

def test_detect_simple_loop():
    result = naive_detect_recurrence("for i in range(n): print(i)")
    assert result["type"] == "loop"

def test_detect_divide_and_conquer():
    result = naive_detect_recurrence("T(n) = 2T(n/2) + n")
    assert result["type"] == "divide-and-conquer"
    assert result["a"] == 2
    assert result["b"] == 2
    assert result["f"] == "n"

def test_detect_unknown():
    result = naive_detect_recurrence("print('hi')")
    assert result["type"] == "unknown"
