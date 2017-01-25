from Input import Machine

class Job(object):
    '''A class representing a scheduled task, i.e. a job; a set of which is a genetic individual or genome'''

    def __init__(self, task, s, w, m):
        self.task = task
        self.length = task.dur
        self.start = s
        self.workers = w
        self.machs = m
        self.evalScore = {
            'prec': 1000 * len(self.task.plist),
            'availW': 0,
            'availM': 0,
            'inputW': 10 * self.task.nWorkers,
            'inputM': 10 * self.task.nMachs
        }
        self.budget = 1

    def __str__(self):

        w, m = '', ''
        for worker in self.workers:
            w += '{0},'.format(str(worker.id))
        for mach in self.machs:
            m += '{0},'.format(str(mach.id))
        return '{0}/{1}/{2}/{3}'.format(str(self.task.id), str(self.start), w[:-1], m[:-1])

    def getEnd(self):
        return self.start + self.length

    def getError(self):
        return sum(val**2 for key, val in self.evalScore.items())

    def inputEval(self):
        correctMachs = []
        machIDs = []
        for w in self.workers:
            if self.task.type in w.type:
                self.evalScore['inputW'] -= 10
                for id in w.mach_id:
                    machIDs.append(id)
        for m in self.machs:
            if self.task.type in m.type:
                self.evalScore['inputM'] -= 10
                if m.id in machIDs:
                    correctMachs.append(m)
        if self.evalScore['inputW'] == 0 and len(correctMachs) > 0:
            self.length *= min([m.mltp for m in correctMachs])

    def precEval(self, doneJobs):
        for job in doneJobs:
            if job[0] in self.task.plist and job[1] <= self.start:
                self.evalScore['prec'] -= 1000

    def availEval(self, overlapJobs):
        for j in overlapJobs:
            for w in self.workers:
                if w in j.workers: self.evalScore['availW'] += 100
            for m in self.machs:
                if m in j.machs: self.evalScore['availM'] += 100
        if len(set([w.id for w in self.workers])) < len(self.workers) or\
            len(set([m.id for m in self.machs])) < len(self.machs): self.evalScore['availW'] += 200