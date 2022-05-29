import task
import unittest

class TestStringMethods(unittest.TestCase):

    def test_helloworld(self):
        self.assertEqual(task.getHelloWorld(), 'HelloWorld!')

if __name__ == '__main__':
    unittest.main()