import subprocess
import os
from platform import system

class Executor:
    def runPython(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("py {0}".format(testing_file), capture_output = True)
        # decode s to a normal string
        return s

    def runGolang(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("g++ {0}".format(testing_file), capture_output = True)
        # decode s to a normal string
        return s

    def runJavaScript(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("node {0}".format(testing_file), capture_output = True)
        # decode s to a normal string
        return s

class Manager:
    def jsTestFileCreator(code):
        includeFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\include.js'
        testFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\test.js'
        resFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\testing\\test.js'
        str = ''
        with open(includeFile, 'r', encoding='utf-8') as f:
            str += f.read()
        str += '\n' + code + '\n'
        with open(testFile, 'r', encoding='utf-8') as f:
            str += f.read()
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(str)
        return '"' + resFile + '"'

    def pythonTestFileCreator(code):
        if system() == "Linux":
            includeFile = 'tests/python/testing/test.py'
            testFile = 'tests/python/test.py'
            resFile = 'tests/python/testing/test.py'
        else:
            includeFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\python\\include.py'
            testFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\python\\test.py'
            resFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\python\\testing\\test.py'

        str = ''
        with open(includeFile, 'r', encoding='utf-8') as f:
            str += f.read()
        str += '\n' + code + '\n'
        with open(testFile, 'r', encoding='utf-8') as f:
            str += f.read()
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(str)
        return '"' + resFile + '"'

class CodeExecutor:
    def jsCodeExecute(code):
        val = Manager.jsTestFileCreator(code)
        return Executor.runJavaScript(val)

    def pythonCodeExecute(code):
        val = Manager.pythonTestFileCreator(code)
        return Executor.runPython(val)