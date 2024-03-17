import unittest
import multiprocessing

# Import your test classes here
from unittest_with_selenium import TestLoginPage,TestPlatform

# List of test classes to run
test_classes = [TestLoginPage,TestPlatform]

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    # Number of parallel processes
    num_processes = 4

    # Create a process pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Run tests in parallel
    pool.map(run_tests, test_classes)

    # Close the pool
    pool.close()
    pool.join()
