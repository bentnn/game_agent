import subprocess
import os

class Executor:
    def runPython(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.check_output("py {0}".format(testing_file), stdin = data, shell = True)
        # decode s to a normal string
        print(s.decode("utf-8"))

    def runGolang(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.check_output("g++ {0}".format(testing_file), stdin = data, shell = True)
        # decode s to a normal string
        print(s.decode("utf-8"))

    def runJavaScript(testing_file):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.check_output("node {0}".format(testing_file), stdin = data, shell = True)
        # decode s to a normal string
        print(s.decode("utf-8"))

class Manager:
    def jsTestFileCreator(code):
        includeFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\include.js'
        testFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\test.js'
        resFile = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\testing\\test.js'
        print(testFile)
        print(includeFile)
        str = ''
        with open(includeFile, 'r', encoding='utf-8') as f:
            str += f.read()
        str += '\n' + code + '\n'
        with open(testFile, 'r', encoding='utf-8') as f:
            str += f.read()
        with open(resFile, 'a+', encoding='utf-8') as f:
            f.write(str)