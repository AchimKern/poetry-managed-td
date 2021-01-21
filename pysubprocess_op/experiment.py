import subprocess
def Run1(self, command, shell = False):
    # invoke process
    process = subprocess.Popen(shlex.split(command),shell=shell,stdout=subprocess.PIPE,bufsize=1,)

    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def Run2(self, command, shell = False):
    # invoke process
    process = subprocess.Popen(shlex.split(command),shell=shell,stdout=subprocess.PIPE,bufsize=1,)
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        print(line)
    process.stdout.close()


def Run3(self, command, shell = False):
    process = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace'
    )

    while True:
        realtime_output = process.stdout.readline()

        if realtime_output == '' and process.poll() is not None:
            break

        if realtime_output:
            print(realtime_output.strip(), flush=True)


def Run4(self, command, shell = False):
    with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, bufsize=1,universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')			


def Run2(self, command, shell = False):
    popen = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
