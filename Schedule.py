from random import random, randint, choice
from inputgen import inputLists
from Job import Job
import evolution as ev

class Schedule(object):
    '''A class representing an individual genome (or chromosome) of the generation, a particular schedule'''

    def __init__(self, genomeStr):

        self.genome = self.strToObj(genomeStr)
        self.idSortedGenome = sorted(self.genome, key=lambda x: x.task.id)

    def __iter__(self):
        return iter(self.genome)

    def __getitem__(self, index):
        return self.genome[index]

    def __len__(self):
        return len(self.genome)

    def __str__(self):

        s = ''
        for job in self.genome:
            s += '{0};'.format(str(job))
        return s[:-1]

    def strToObj(self, s):
        """
        Converts genome string to list of Job objects, sorted by the starting times of jobs.
        :param s: genome string
        :return: list of Job objects
        """

        taskList, workerList, machineList = inputLists

        genome = []
        for jobStr in s.split(';'):
            # Reminder for job string structure: 'jobID/startTime/worker1,worker2,.../mach1,mach2...'
            params = jobStr.split('/')
            task = taskList[int(params[0])]
            start = int(params[1])
            workers = [workerList[int(id)] for id in params[2].split(',') if id != '']
            machs = [machineList[int(id)] for id in params[3].split(',') if id != '']
            genome.append(Job(task, start, workers, machs))

        return sorted(genome, key=lambda j: j.start)

    def printAsSolution(self, nGen, fitness):

        shift = self.genome[0].start
        if shift > 0:
            for job in self.genome:
                job.start -= shift

        perfect = fitness > 0
        print('\n\nBest solution found within {0} generations:'.format(nGen))
        for job in self.genome:
            if perfect: job.inputEval()
            print('\nTask #{0} - Start: {1}m, end: {2}m'.format(job.task.id, job.start, job.getEnd()))
            print('--Workers assigned: {0}'.format([w.id for w in job.workers]))
            print('--Machines assigned: {0}'.format([m.id for m in job.machs]))

    def checkLength(self):
        end = sorted(self.genome, key=lambda j: j.getEnd())[-1].getEnd()
        return end - self.genome[0].start

    def evalGenome(self):
        """
        Evaluates genome schedule on a job-by-job basis in two phases. First checking their precedence fitness
        and correct input placements, then checking input availability.
        :return: genome fitness score
        """

        startList = []
        endList = []
        for job in self.genome:
            job.inputEval()
            job.precEval(endList)
            startList.append((job.task.id, job.start))
            endList.append((job.task.id, job.getEnd()))

        for job in self.genome:
            overlapIDs = []
            overlapJobs = []
            tempIDs = []

            for t in startList:
                if t[1] >= job.getEnd(): break
                elif t[1] >= job.start and t[0] != job.task.id:
                    overlapIDs.append(t[0])
                    overlapJobs.append(self.idSortedGenome[t[0]-1])
                else:
                    tempIDs.append(t[0])

            endList.sort(key=lambda x: x[1], reverse=True)
            for t in endList:
                if t[1] <= job.start: break
                elif t[0] != job.task.id and t[0] not in overlapIDs:
                    if t[1] <= job.getEnd():
                        overlapIDs.append(t[0])
                        overlapJobs.append(self.idSortedGenome[t[0]-1])
                    elif t[0] in tempIDs:
                        overlapIDs.append(t[0])
                        overlapJobs.append(self.idSortedGenome[t[0]-1])

            job.availEval(overlapJobs)

        length = self.checkLength()
        errorList = [job.getError() for job in self.genome]

        return -sum(errorList) + 1 / length

    def breedGenome(self, partner):

        childStr = ''

        for job in self.genome:
            while random() < job.budget:
                r = random()
                if r > 0.33: job = ev.chooseCrossover(job, partner)
                else: job = ev.chooseMutation(job)
            childStr += '{0};'.format(str(job))

        return childStr[:-1]
