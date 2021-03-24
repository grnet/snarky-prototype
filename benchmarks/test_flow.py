import time
def something(duration=0.000001):
    time.sleep(duration)
    return 123

def test_my_stuff(benchmark):
    result = benchmark(something)
    assert result == 123
