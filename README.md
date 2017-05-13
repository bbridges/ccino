ccino
==

[![Build Status](https://travis-ci.com/bloof-bb/ccino.svg?token=i58uqsNTypCSHwaT2j4f&branch=master)](https://travis-ci.com/bloof-bb/ccino)

> A Python unit test framework based on Mocha

ccino aims to make Python unit testing much easier than the alternatives. Tests
are labelled instead of being found automatically. ccino test files are
readable as the structure of the test files looks like the output.

Python 2 and 3 compatible.

### Sample Test

```python
# test_math.py

import math

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
        @raises(ValueError)
        def test_sqrt_negative():
            return math.sqrt(-1)

    @test('should have a good value for pi')
    @returns(3.1415926535, approx=1e-10)
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

  4 passing (365µs)

```

## Installation

To install ccino from source run the following:

```sh
pip install git+ssh://git@github.com/bloof-bb/ccino.git
```

...and that's it!

## Usage

#### Tests

A test is the most basic piece of a testing framework. Making a test is simple:

```python
@test('Hello World')
def _():
    print('Hey guys!')
```

Note that you don't have to import `@test` from anywhere. By default ccino
decorators are added in as builtin functions.

As long as the test runs without error it passes!

Output of the above:

```

Hey guys!
  ✓ Hello World

  1 passing (181µs)

```

If tests print out data it will appear in the report unindented.

#### Suite

A suite can easily group similar tests together. Suites are just as simple to
use:

```python
my_list = [1, 4, 7, 8]

@suite('Indexing')
def _():
    @test('Index 0 returns first value')
    def _():
        assert my_list[0] == 1

    @test('Index -1 returns last value')
    def _():
        assert my_list[-1] == 8
```

For nested behavior, just put a suite inside another. Effectively suites act as
folders.

#### Hooks

Hooks are used for setting and tearing down stuff for tests so you don't have
to keep doing it again.

A setup hook will run before each test, and a teardown hook will run after.

```python
@suite('del')
def _():
    @setup()
    def _():
        global my_list
        my_list = [5, 77, 4, 3]

    @test('Deleting an element makes a list shorter')
    def _():
        assert len(my_list) == 4
        del my_list[0]
        assert len(my_list) == 3

    @test('Deleting two elements makes a list even shorter')
    def _():
        assert len(my_list) == 4
        del my_list[0]
        del my_list[1]
        assert len(my_list) == 2
```

A suite setup and suite teardown hook simply run before and after all tests in
a suite.

`@setup`, `@teardown`, `@suite_setup`, `@suite_teardown` are the valid hook
decorators.

#### Returns

To ensure a test returns a specific value use `@returns(value)` above a test.
For approximate numbers use `@returns(value, approx=1e-10)`.

#### Raises

To ensure a test raises a specific exception use `@raises(exception)` above a
test.

#### Skipping

To prevent a test from running for whatever reason, simply use `@skip` above.
To make this vary on a condition just use `@skip(condition)`.

#### Test failures

If a test throws an error they are printed gracefully. Exceptions are printed
like in node.js. The last calling frame is printed at the top, and for
readability, the line context is hidden to make them shorter (they can be
shown by an option in the CLI). The tests will keep running even if one fails
by default.

```

  Cool Suite
    ✓ This one works
    0) Pretty lame test

  1 passing (519µs)
  1 failing

  0) Pretty lame test
     AssertionError
      at _ (/Users/ccino/cool_test.py:9)
      at run (/Users/ccino/anaconda/lib/python3.6/site-packages/ccino/fixtures/test.py:69)

```

#### Command Line Interface

ccino comes packed with a command line interface for efficient test running.

Simply call the following in a and it will load in modules in the `test/`
directory.

```sh
ccino
```

You can specify a different directory, specific files, or a combination of the
two easily.

```sh
ccino test_files_dir run_this.py this/is/nested.py
```

Command line options:

```
Usage: ccino [options] [files]

Options:
  -b, --bail             Stop running after a test failure.
  -B, --no-bail          Don't stop running after a test failure.
  -R, --reporter <name>  Specify the reporter to use.
  -c, --color            Force color output.
  -C, --no-color         Force no color output.
  -r, --recursive        Load in subdirectories.
  --no-builtins          Don't add ccino functions to the builtins.
  --config <file>        Specify the config file.
  --no-config            Do not use a config file.
  --out <file>           Save the output to a file.
  --stdout <file>        Save the stdout output to a file.
  --exc-context          Show context in stack trace if possible.
  --cover                Output coverage information using coverage.py.
  --reporters            List available reporters and exit.
  -V, --version          Show the current version and exit.
  -h, --help             Show this message and exit.
```
