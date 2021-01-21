print(f"--- import {__name__}")
import shlex
import sys
import subprocess
import os
import uuid
from threading import Thread
from queue import Queue, Empty
from types import SimpleNamespace
from td import op

# handle MOCKS for sphinx documentatio
try:
    op
except NameError:
    from td import op

TDF = op.TDModules.mod.TDFunctions


class Task(SimpleNamespace):
    """ A simpleNamespace based class used to transfer all args to/from the subprocess/queue"""

    pass


class Ext1:
    """Class Doc missin
    """

    def __init__(self, ownerComp):
        print(f"----- init {__name__} @ {ownerComp}")
        self.ownerComp = ownerComp
        self.baseColor = ownerComp.color
        self.Queue = Queue()
        self.Tasks = []
        self.prefix_start = "thread >>> "
        self.prefix_run = "thread === "
        self.prefix_done = "thread <<< "
        # TDF generated  properties dont make it to docstring generators
        TDF.createProperty(
            self, "ActiveProcesses", value=0, dependable=True, readOnly=False,
        )

        """The numer off active processes, if this is 0 we stop polling the queue"""

    def Add(
        self,
        cmd: str = "",
        id: str = None,
        verbose: int = None,
        cb=None,
        shell: bool = None,
        continue_on_error: bool = False,
    ):
        """This will add the supplied process/command to the task queue. Use Start() to trigger
        Args:
            cmd: The command to be executed
            id: Is attached to the subprocess to identify it's stdout in the thread safe queue, uses the full command if None
            verbose: 0 = off, 1 = Started/Finished events, 2 = all stdout and stderr 
            cb: takes an optional callback function object 
            shell: start process in shell
            continue_on_error: if a sequence of tasks should continue if a task exits with returncode > 0
        """
        # handle defaults
        if verbose == None:
            verbose = int(self.ownerComp.par.Verbosity)
        if shell == None:
            shell = int(self.ownerComp.par.Shell.val)

        task = Task(
            cmd=cmd,
            id=id,
            verbose=verbose,
            cb=cb,
            shell=shell,
            message=None,
            stdout=[],
            stderr=[],
            rc=None,
            continue_on_error=continue_on_error,
        )
        self.Tasks.append(task)

    def Start(
        self,
        cmd: str = None,
        id: str = None,
        verbose: int = None,
        cb=None,
        shell: bool = None,
        continue_on_error: bool = False,
    ):
        """This will add the supplied process/command to the task queue and execute all tasks in the queue. 
        
        Use without any args to execute taks previously added via Add()

        Args:
            cmd: The command to be executed
            id: Is attached to the subprocess to identify it's stdout in the thread safe queue, uses the full command if None
            verbose: 0 = off, 1 = Started/Finished events, 2 = all stdout and stderr 
            cb: takes an optional callback function object 
            shell: start process in shell
        """
        if verbose == None:
            verbose = int(self.ownerComp.par.Verbosity)
        if shell == None:
            shell = int(self.ownerComp.par.Shell.val)

        if cmd:
            self.Tasks.append(
                Task(
                    cmd=cmd,
                    id=id,
                    verbose=verbose,
                    cb=cb,
                    shell=shell,
                    message=None,
                    stdout=[],
                    stderr=[],
                    rc=None,
                    continue_on_error=continue_on_error,
                )
            )
        tasks = self.Tasks.copy()
        self.Tasks = []
        self.execute(tasks)

    def execute(self, tasks):
        """ An interal function to execute a task/process and start a thread to query its results
        
        Args:
            tasks: a list of task objects
        
        """
        if len(tasks):
            task = tasks.pop(0)
            task.next_tasks = tasks
            if task.verbose:
                if task.id == None:
                    print(f"{self.prefix_start}{task.cmd}")
                else:
                    print(f"{self.prefix_start}{task.id} ({task.cmd})")

            if task.id == None:
                task.id = task.cmd

            process = subprocess.Popen(
                shlex.split(task.cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                shell=task.shell,
                # text = True  # DONT as this will keep the thread alive
            )

            t = Thread(
                target=self.enqueue_output, args=(process, self.Queue, task,),
            )
            t.daemon = True  # thread dies with the program
            t.start()
            self.ActiveProcesses = self.ActiveProcesses + 1
            self.ownerComp.color = (1, 0, 0)

    def enqueue_output(self, process, queue, task):
        """ An interal function started in a new thread. It will read from the process.stdout whenever a new line is available 
        and dumps it into our Queue. When the child exits (empty bytestring received) the thread stops """
        for line in iter(process.stdout.readline, b""):
            line = line.decode("utf-8").strip()
            if len(line):
                task.stdout.append(line)
                if task.verbose == 2:
                    print(f"{self.prefix_run}{task.id}: {line}")
        process.stdout.close()
        task.stderr = process.stderr.read().decode("utf-8").strip()
        task.message = "PYSUBPROC.FINISHED"
        task.rc = process.poll()
        if task.rc == None:
            print("{self.prefix_end}  !!!  TASK RC IS NONE !!!")
        queue.put(task)

    def read_queue(self):
        """
        While any managed subprocesses are active this is internally called every frame to check the return status of all sub processes.
        """
        while not self.Queue.empty():
            try:
                task = self.Queue.get_nowait()
                if task.message == "PYSUBPROC.FINISHED":
                    if task.verbose:
                        if task.rc == 0 or task.rc == None:
                            print(f"{self.prefix_done}{task.id}")
                        else:
                            print(f"{self.prefix_done}{task.id} ({task.rc})")
                    # if it has a callback execute it
                    if task.cb:
                        task.cb(task)

                    # handle the active process
                    self.ActiveProcesses = self.ActiveProcesses - 1
                    if self.ActiveProcesses == 0:
                        self.ownerComp.color = self.baseColor

                    # handle next task in tasks
                    if task.continue_on_error or (
                        task.rc == 0 or task.rc == None
                    ):
                        self.execute(task.next_tasks)
            except Empty:
                continue

    '''
    def Run(self, cmd, shell = False):
        """This will run (blocking) the supplied process/cmd and return the result.

        Args:
            cmd: The command to be executed
            shell: enable shell mode
        """
        return subprocess.run(shlex.split(cmd), capture_output = True, shell=shell, text = True) 

    # call it via
    command = 'poetry add sphinx'
    r = op("pySubprocess_op").Run( command , shell = True)
    print(r.stdout)
    #print(r.stderr)

    command = 'poetry add sphinx_rtd_theme'
    r = op("pySubprocess_op").Run( command , shell = True)
    print(r.stdout)
    #print(r.stderr)
    '''
