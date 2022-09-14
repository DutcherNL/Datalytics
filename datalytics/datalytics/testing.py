import os
import os.path, pkgutil
from traceback import print_exception, print_tb
import importlib

from datalytics import tests
from datalytics.tests import TestCase


def run_tests():
    pkgpath = os.path.dirname(tests.__file__)

    print("--- Start running tests ---")

    Tester().run_tests_in_pkg(pkgpath, 'datalytics.tests')



class Tester:
    def __init__(self):
        self.results = {}

    def run_tests_in_pkg(self, pkg_path, pkg_name):
        """ Runs all tests in a given pkg name """
        for path, name, ispkg in pkgutil.iter_modules([pkg_path], prefix=f'{pkg_name}.'):
            if ispkg:
                self.run_tests_in_pkg(path, name)
            elif name[name.rindex('.'):].__contains__('test'):
                try:
                    self.run_tests_in_module(importlib.import_module(name))
                except ImportError:
                    print(f"Error importing module {name}")

        self.print_results()

    def print_results(self):
        for name, value in self.results.items():
            print(f"tested {name}:\n Ran {value['tests_run']} tests \n Found {len(value['errors'])} errors")
            for (method, error) in value['errors']:
                print(f'failed {method}: {error}')

    def run_tests_in_module(self, module):
        """ Runs all testcases of a specific module """
        self.results[module.__name__] = {
            'errors': [],
            'tests_run': 0,
        }
        for name, cls in module.__dict__.items():
            if isinstance(cls, type):
                # Get all subclasses of the TestCase class, but not accidental imported copies of itself
                if issubclass(cls, TestCase) and cls != TestCase:
                    methods = [method for method in dir(cls) if method.startswith('test') is True]
                    for method_name in methods:
                        try:
                            # Run the test cases starting with test
                            test_obj = cls()
                            test_obj.setUp()
                            getattr(test_obj, method_name)()
                            test_obj.breakDown()
                        except AssertionError as e:
                            self.results[module.__name__]['errors'].append((f'{cls.__name__}.{method_name}', e))

                    self.results[module.__name__]['tests_run'] += len(methods)