import subprocess
import os
import shutil
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
        print(testing_file)
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("go run {0}".format(testing_file), capture_output = True)
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
    def jsTestFileCreator(code, test, dirname):
        testingDir = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\js\\testing\\' + dirname
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        testFile = testingDir + '\\test.js'
        resFile = testingDir + '\\task.js'
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        # shutil.rmtree(testingDir)
        return '"' + testFile + '"'

    def pythonTestFileCreator(code, test, dirname):
        testingDir = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\python\\testing\\' + dirname
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        testFile = testingDir + '\\test.py'
        resFile = testingDir + '\\task.py'
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        # shutil.rmtree(testingDir)
        return '"' + testFile + '"'

    def goTestFileCreator(code, test, dirname):
        testingDir = os.path.abspath(os.path.dirname(__file__)) + '\\tests\\go\\testing\\' + dirname
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        testFile = testingDir + '\\test.go'
        resFile = testingDir + '\\task.go'
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        # shutil.rmtree(testingDir)
        return '"' + testFile + '"'


class CodeExecutor:
    def jsCodeExecute(code, test, dirname):
        val = Manager.jsTestFileCreator(code, test, dirname)
        res = Executor.runJavaScript(val)
        return {'output': res.stdout.decode("utf-8"), 'error': res.stderr.decode("utf-8")}

    def pythonCodeExecute(code, test, dirname):
        val = Manager.pythonTestFileCreator(code, test, dirname)
        res = Executor.runPython(val)
        return {'output': res.stdout.decode("ISO-8859-1"), 'error': res.stderr.decode("ISO-8859-1")}

    def goCodeExecute(code, test, dirname):
        val = Manager.goTestFileCreator(code, test, dirname)
        res = Executor.runGolang(val)
        return {'output': res.stdout.decode("ISO-8859-1"), 'error': res.stderr.decode("ISO-8859-1")}
