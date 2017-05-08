ccino
==

[![Build Status](https://travis-ci.com/bloof-bb/ccino.svg?token=i58uqsNTypCSHwaT2j4f&branch=master)](https://travis-ci.com/bloof-bb/ccino)

> A Python unit test framework based on Mocha

### Sample Test

```python
# test_math.py

@suite('math')
def test_math():

    @suite('#sqrt()')
    def test_sqrt():

        @test('should return 1 with input 1')
        @returns(1)
        def test_sqrt_positive():
            return math.sqrt(1)

        @test('should return 0 with input 0')
        @returns(0)
        def test_sqrt_zero():
            return math.sqrt(0)

        @test('should raise a ValueError with input -1')
        @throws(ValueError, 'math domain error')
        def test_sqrt_negative():
            return math.sqrt(-1)

    @test('should have a good value for pi')
    @returns.approx(3.1415926535, 1e-10)
    def test_pi():
        return math.pi
```

To run the test file `test_math.py` run the following in the terminal:

```sh
ccino test_math.py
```

### Sample Output

```

  math
    #sqrt()
      ✓ should return 1 with input 1
      ✓ should return 0 with input 0
      ✓ should raise a ValueError with input -1
    ✓ should have a good value for pi

  4 passing (1ms)

```
