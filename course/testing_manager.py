import subprocess
import os
import shutil
from platform import system
import tempfile

class Executor:
    def runPython(container_name):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("docker run {0}".format(container_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(s)
        # decode s to a normal string
        return s

    def runGolang(container_name):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("docker run {0}".format(container_name).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # decode s to a normal string
        return s

    def runJavaScript(container_name):
    # create a pipe to a child process
        data, temp = os.pipe()
        # store output of the program as a byte string in s
        s = subprocess.run("docker run {0}".format(container_name).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)   
        # decode s to a normal string
        return s


class Manager:
    def jsTestFileCreator(code, test, dirname):
        dockerSrc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'js', 'testing', 'Dockerfile')
        testingDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'js', 'testing', dirname)
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        shutil.copyfile(dockerSrc, os.path.join(testingDir, 'Dockerfile'))
        testFile = os.path.join(testingDir, 'test.js')
        resFile = os.path.join(testingDir, 'task.js')
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        with open(testFile, 'a', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        subprocess.run("docker build -t {0} {1}".format(dirname, testingDir).split(' '))
        shutil.rmtree(testingDir)
        return dirname

    def pythonTestFileCreator(code, test, dirname):
        dockerSrc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'python', 'testing', 'Dockerfile')
        testingDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'python', 'testing', dirname)
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        shutil.copyfile(dockerSrc, os.path.join(testingDir, 'Dockerfile'))
        testFile = os.path.join(testingDir, 'test.py')
        resFile = os.path.join(testingDir, 'task.py')
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        subprocess.run("docker build -t {0} {1}".format(dirname, testingDir).split(' '))
        shutil.rmtree(testingDir)
        return dirname

    def goTestFileCreator(code, test, dirname):
        dockerSrc = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'go', 'testing', 'Dockerfile')
        testingDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'go', 'testing', dirname)
        if not os.path.exists(testingDir):
            os.mkdir(testingDir)
        shutil.copyfile(dockerSrc, os.path.join(testingDir, 'Dockerfile'))
        testFile = os.path.join(testingDir, 'test.go')
        resFile = os.path.join(testingDir, 'task.go')
        with open(testFile, 'w+', encoding='utf-8') as f:
            f.write(test)
        with open(resFile, 'w+', encoding='utf-8') as f:
            f.write(code)
        subprocess.run("docker build -t {0} {1}".format(dirname, testingDir).split(' '))
        shutil.rmtree(testingDir)
        return dirname


class CodeExecutor:
    def jsCodeExecute(code, test, dirname):
        val = Manager.jsTestFileCreator(code, test, dirname)
        res = Executor.runJavaScript(val)
        subprocess.run('''docker rm $(docker ps -a -f ancestor="{0}")'''.format(dirname).split(' '))
        subprocess.run('''docker rmi {0} --force'''.format(dirname).split(' '))
        if (res.returncode == 124):
            return {'output': res.stdout.decode("ISO-8859-1"), 'error': 'Time limit exceeded'}
        return {'output': res.stdout.decode("utf-8"), 'error': res.stderr.decode("utf-8")}

    def pythonCodeExecute(code, test, dirname):
        val = Manager.pythonTestFileCreator(code, test, dirname)
        res = Executor.runPython(val)
        subprocess.run('''docker rm $(docker ps -a -f ancestor="{0}")'''.format(dirname).split(' '))
        subprocess.run('''docker rmi {0} --force'''.format(dirname).split(' '))
        if (res.returncode == 124):
            return {'output': res.stdout.decode("ISO-8859-1"), 'error': 'Time limit exceeded'}
        return {'output': res.stdout.decode("ISO-8859-1"), 'error': res.stderr.decode("ISO-8859-1")}

    def goCodeExecute(code, test, dirname):
        val = Manager.goTestFileCreator(code, test, dirname)
        res = Executor.runGolang(val)
        subprocess.run('''docker rm $(docker ps -a -f ancestor="{0}")'''.format(dirname).split(' '))
        subprocess.run('''docker rmi {0} --force'''.format(dirname).split(' '))
        if (res.returncode == 124):
            return {'output': res.stdout.decode("ISO-8859-1"), 'error': 'Time limit exceeded'}
        return {'output': res.stdout.decode("ISO-8859-1"), 'error': res.stderr.decode("ISO-8859-1")}
