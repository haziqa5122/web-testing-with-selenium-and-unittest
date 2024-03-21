import unittest
import multiprocessing

# Import your test classes here
from unittest_with_selenium import TestLoginPage,TestPlatform

# List of test classes to run
test_classes = [TestLoginPage, TestPlatform]

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    processes = []
    # for test_class in [MyTest, MyTest2]:  # Add more test classes here if needed
    for test_class in test_classes:  # Add more test classes here if needed
        process = multiprocessing.Process(target=run_tests, args=(test_class,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
