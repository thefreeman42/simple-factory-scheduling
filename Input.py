class Input(object):

    def __init__(self, params):
        self.id = int(params[0])
        self.type = params[1].split('/')

class Task(Input):
    """A class used to hold evaluation information of process tasks"""

    def __init__(self, params):
        super(Task, self).__init__(params)
        self.type = params[1]
        self.dur = int(params[2])
        self.nWorkers = int(params[3])
        self.nMachs = int(params[4])
        if params[5] == '-': self.plist = []
        else: self.plist = [int(p) for p in params[5].split('/')]

class Worker(Input):

    def __init__(self, params):
        super(Worker, self).__init__(params)
        if params[2] == '-': self.mach_id = []
        else: self.mach_id = [int(id) for id in params[2].split('/')]

class Machine(Input):

    def __init__(self, params):
        super(Machine, self).__init__(params)
        self.mltp = float(params[2])
