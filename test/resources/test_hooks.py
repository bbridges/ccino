from __future__ import print_function

# Expected Output
# 1
# 2
# 3
# 2
# 4
# 5
# 6
# 2
# 7
# 8
# 9
# 2
# 7
# 8
# 10
# 2
# 11


@suite('Hooks')
def hooks_suite():
    @suite_setup
    def before_hooks():
        print('1')

    @setup
    def before_each_hooks():
        print('2')

    @test('print 3')
    def test_print_3():
        print('3')

    @test('print 4')
    def test_print_4():
        print('4')

    @suite('Nested 1')
    def nested_1_suite():
        @suite_setup
        def before_nested_1():
            print('5')

        @suite_setup
        def before_nested_1_2():
            print('6')

        @setup
        def before_each_nested_1():
            print('7')

        @setup
        def before_each_nested_1_2():
            print('8')

        @test('print 9')
        def test_print_9():
            print('9')

        @suite('Nested 2')
        def nested_2_suite():
            pass

        @suite('Nested 3')
        def nested_3_suite():
            @test('print 10')
            def test_print_10():
                print('10')

    @test('print 11')
    def test_print_11():
        print('11')
