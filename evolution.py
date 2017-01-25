from random import randint, choice, sample
from inputgen import inputLists
from copy import deepcopy


def chooseCrossover(self, partnerGenome):

    partner = choice(partnerGenome)

    if partner.task.id == self.task.id:
        r = randint(1, 3)
        if r == 1:
            return co_same_startTime(self, partner)
        elif r == 2:
            return co_same_workers(self, partner)
        else:
            return co_same_machines(self, partner)
    else:
        r = randint(1, 5)
        if r == 1:
            return co_diff_startTime(self, partner)
        elif r == 2:
            return co_diff_singleWorker(self, partner)
        elif r == 3:
            return co_diff_singleMachine(self, partner)
        elif r == 4:
            return co_diff_allWorker(self, partner)
        else:
            return co_diff_allMachine(self, partner)


def chooseMutation(self):

    taskList, workerList, machineList = inputLists

    r = randint(1, 6)
    if r == 1:
        return mt_startTimeMove(self)
    elif r == 2:
        return mt_startTimeReplace(self, taskList)
    elif r == 3:
        return mt_singleWorker(self, deepcopy(workerList))
    elif r == 4:
        return mt_singleMachine(self, deepcopy(machineList))
    elif r == 5:
        return mt_allWorker(self, deepcopy(workerList))
    else:
        return mt_allMachine(self, deepcopy(machineList))


def mt_startTimeMove(parent):

    child = deepcopy(parent)
    d = int(parent.length/4)
    child.start += randint(-d, d)
    child.budget -= 0.3

    return child


def mt_startTimeReplace(parent, taskList):

    child = deepcopy(parent)
    interval = sum([task.dur for task in taskList])*2
    child.start = randint(0, interval-child.task.dur)
    child.budget -= 0.4

    return child


def mt_singleWorker(parent, workerList):

    if parent.task.nWorkers == 0 or set(parent.workers) == set(workerList): return parent
    else:
        child = deepcopy(parent)
        if parent.task.nWorkers == 1: i = 0
        else: i = randint(0,parent.task.nWorkers-1)
        while True:
            new = choice(workerList)
            if new not in child.workers:
                child.workers[i] = new
                break
        child.budget -= 0.25

        return child


def mt_allWorker(parent, workerList):

    if parent.task.nWorkers == 0 or set(parent.workers) == set(workerList): return parent
    else:
        child = deepcopy(parent)
        while True:
            new = sample(workerList, child.task.nWorkers)
            if set(new) != set(child.workers):
                diff = len(set(child.workers)-set(new))
                child.workers = new
                break
        child.budget -= (0.2 * diff)

        return child


def mt_singleMachine(parent, machineList):

    if parent.task.nMachs == 0 or set(parent.machs) == set(machineList): return parent
    else:
        child = deepcopy(parent)
        if parent.task.nMachs == 1: i = 0
        else: i = randint(0,parent.task.nMachs-1)
        while True:
            new = choice(machineList)
            if new not in child.machs:
                child.machs[i] = new
                break
        child.budget -= 0.25

        return child


def mt_allMachine(parent, machineList):

    if parent.task.nMachs == 0 or set(parent.machs) == set(machineList): return parent
    else:
        child = deepcopy(parent)
        while True:
            new = sample(machineList, child.task.nMachs)
            if set(new) != set(child.machs):
                diff = len(set(child.machs)-set(new))
                child.machs = new
                break
        child.budget -= (0.2 * diff)

        return child


def co_same_startTime(parentSelf, partner):

    if parentSelf.start == partner.start: return parentSelf
    else:
        child = deepcopy(parentSelf)
        child.start = partner.start
        child.budget -= 0.1

        return child


def co_same_workers(parentSelf, partner):

    if parentSelf.task.nWorkers == 0 or set(parentSelf.workers) == set(partner.workers): return parentSelf
    else:
        child = deepcopy(parentSelf)
        child.workers = partner.workers
        child.budget -= 0.2
        return child


def co_same_machines(parentSelf, partner):

    if parentSelf.task.nMachs == 0 or set(parentSelf.machs) == set(partner.machs): return parentSelf
    else:
        child = deepcopy(parentSelf)
        child.machs = partner.machs
        child.budget -= 0.2
        return child


def co_diff_startTime(parentSelf, partner):

    if parentSelf.start == partner.start: return parentSelf
    else:
        child = deepcopy(parentSelf)
        child.start = partner.start
        child.budget -= 0.15

        return child


def co_diff_singleWorker(parentSelf, partner):

    if parentSelf.task.nWorkers == 0 or partner.task.nWorkers == 0 or set(parentSelf.workers) == set(partner.workers):
        return parentSelf
    else:
        child = deepcopy(parentSelf)
        while True:
            new = sample(child.workers, child.task.nWorkers - 1) + [choice(partner.workers)]
            if len(set(new)) == len(new):
                child.workers = new
                break
        child.budget -= 0.2

        return child


def co_diff_allWorker(parentSelf, partner):

    if parentSelf.task.nWorkers == 0 or partner.task.nWorkers == 0 or set(parentSelf.workers) == set(partner.workers):
        return parentSelf
    else:
        child = deepcopy(parentSelf)
        if child.task.nWorkers > partner.task.nWorkers:
            while True:
                new = sample(child.workers, child.task.nWorkers - partner.task.nWorkers) + partner.workers
                if len(set(new)) == len(new):
                    diff = len(set(child.workers) - set(new))
                    child.workers = new
                    break
        elif child.task.nWorkers < partner.task.nWorkers:
            while True:
                new = sample(partner.workers, child.task.nWorkers)
                if set(new) != set(child.workers):
                    diff = len(set(child.workers) - set(new))
                    child.workers = new
                    break
        else:
            diff = len(set(child.workers) - set(partner.workers))
            child.workers = partner.workers
        child.budget -= (0.15 * diff)

        return child


def co_diff_singleMachine(parentSelf, partner):

    if parentSelf.task.nMachs == 0 or partner.task.nMachs == 0 or set(parentSelf.machs) == set(partner.machs):
        return parentSelf
    else:
        child = deepcopy(parentSelf)
        while True:
            new = sample(child.machs, child.task.nMachs - 1) + [choice(partner.machs)]
            if len(set(new)) == len(new):
                child.machs = new
                break
        child.budget -= 0.2

        return child



def co_diff_allMachine(parentSelf, partner):

    if parentSelf.task.nMachs == 0 or partner.task.nMachs == 0 or set(parentSelf.machs) == set(partner.machs):
        return parentSelf
    else:
        child = deepcopy(parentSelf)
        if child.task.nMachs > partner.task.nMachs:
            while True:
                new = sample(child.machs, child.task.nMachs- partner.task.nMachs) + partner.machs
                if len(set(new)) == len(new):
                    diff = len(set(child.machs) - set(new))
                    child.machs = new
                    break
        elif child.task.nMachs < partner.task.nMachs:
            while True:
                new = sample(partner.machs, child.task.nMachs)
                if set(new) != set(child.machs):
                    diff = len(set(child.machs) - set(new))
                    child.machs = new
                    break
        else:
            diff = len(set(child.machs) - set(partner.machs))
            child.machs = partner.machs
        child.budget -= (0.15 * diff)

        return child
