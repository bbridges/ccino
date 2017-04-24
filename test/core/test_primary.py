from __future__ import print_function

import sys
import re


PYTHON_3 = sys.version_info[0] == 3


if PYTHON_3:
    from io import StringIO
else:
    from StringIO import StringIO


from ccino.runner import Runner


@suite
def test_suite():

    @test
    def test_test_no_args():
        runner = Runner()

        @runner.test
        def test_without_args():
            print('in test_without_args()')

        report_io = StringIO()
        stdout_io = StringIO()

        runner.output(report_io)
        runner.stdout(stdout_io)

        runner.reporter('debug')

        runner.run_tests()

        string = (
            'starting tests\n\n'
            'entering suite \'root\'\n'
            '  test \'test_without_args\' passed\n'
            'exiting suite \'root\'\n\n'
            'stopped running tests, took \d\d\d\d\d.\d\d\d\d\d\d seconds\n'
        )

        assert re.match(string, report_io.getvalue())
        assert stdout_io.getvalue() == 'in test_without_args()\n'

    @test
    def test_test_double_no_args():
        runner = Runner()

        @runner.test()
        def test_double_without_args():
            print('in test_double_without_args()')

        report_io = StringIO()
        stdout_io = StringIO()

        runner.output(report_io)
        runner.stdout(stdout_io)

        runner.reporter('debug')

        runner.run_tests()

        string = (
            'starting tests\n\n'
            'entering suite \'root\'\n'
            '  test \'test_double_without_args\' passed\n'
            'exiting suite \'root\'\n\n'
            'stopped running tests, took \d\d\d\d\d.\d\d\d\d\d\d seconds\n'
        )

        assert re.match(string, report_io.getvalue())
        assert stdout_io.getvalue() == 'in test_double_without_args()\n'

    @test
    def test_test_desc():
        runner = Runner()

        @runner.test('desc')
        def test_desc():
            print('in test_desc()')

        report_io = StringIO()
        stdout_io = StringIO()

        runner.output(report_io)
        runner.stdout(stdout_io)

        runner.reporter('debug')

        runner.run_tests()

        string = (
            'starting tests\n\n'
            'entering suite \'root\'\n'
            '  test \'desc\' passed\n'
            'exiting suite \'root\'\n\n'
            'stopped running tests, took \d\d\d\d\d.\d\d\d\d\d\d seconds\n'
        )

        assert re.match(string, report_io.getvalue())
        assert stdout_io.getvalue() == 'in test_desc()\n'

    @test
    def test_it():
        assert not it == test

@suite
def suite_suite():
    @test
    def test_describe():
        assert describe == suite

@suite
def suite_setup_suite():
    pass

@suite
def suite_teardown_suite():
    pass

@suite
def setup_suite():
    pass

@suite
def teardown_suite():
    pass

@suite
def debug_reporter_suite():
    pass
