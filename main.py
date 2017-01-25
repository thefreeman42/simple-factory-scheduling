from random import sample, randint
from inputgen import inputLists
from Schedule import Schedule
from copy import deepcopy


def main():

    # Get parameters and generate input
    nInd, nSlc, nGen = setup()

    # Initialise first generation
    gen = initGeneration(nInd)

    # Run algorithm
    bestSchedule, bestFitness = runGeneticAlgorithm(gen, nGen, nInd, nSlc)

    # Print solution
    bestSchedule.printAsSolution(nGen, bestFitness)


def setup():
    """
    Sets up constant variables for algorithm iteration.
    :return: constant variables
    """

    # Ask user for algorithm parameters
    try:
        nInd = int(input('# of individuals per generation: '))
        nSlc = int(input('# of individuals to naturally select per generation: '))
        nGen = int(input('# of generations: '))
    except: raise Exception('Algorithm parameters must be integers.')
    try:
        for n in [nGen, nInd, nSlc]: assert n > 0
    except: raise Exception('Algorithm parameters must be larger than zero.')
    try: assert nInd > nSlc
    except: raise Exception('Number of individuals must be larger than number of individuals selected.')

    return nInd, nSlc, nGen


def initGeneration(nInd):
    """
    Initialises starting generation from input lists.
    :param nInd: number of individuals to create
    :return: list of genome strings
    """

    taskList, workerList, machineList = inputLists
    interval = sum([task.dur for task in taskList])*2

    gen = []
    for i in range(nInd):
        genomeStr = ''
        for task in taskList:
            t = str(randint(0, interval-task.dur))
            w, m = '', ''
            for x in sample(workerList, task.nWorkers):
                w += '{0},'.format(str(x.id))
            for y in sample(machineList, task.nMachs):
                m += '{0},'.format(str(y.id))
            # Job string structure: 'jobID/startTime/worker1,worker2,.../mach1,mach2...'
            # We remove the last elements of w and m, so that we do not include unwanted commas
            genomeStr += '{0}/{1}/{2}/{3};'.format(str(task.id), t, w[:-1], m[:-1])
        # Same as before, we remove the last element, to avoid returning an extra semicolon
        gen.append(genomeStr[:-1])

    return gen


def runGeneticAlgorithm(gen, nGen, nInd, nSlc):

    def evaluate(gen):
        """
        Evaluates current generation of genomes
        :param gen: current generation of genomes
        :return: list of fitness scores (same ordering as generation)
        """

        genFitness = []
        for genomeStr in gen:
            sch = Schedule(genomeStr)
            genFitness.append(sch.evalGenome())

        return genFitness

    def select(gen, fitness, nSlc):
        """
        Sorts generation based on fitness scores and selects the prescribed amount
        :param gen: current generation of genomes
        :param fitness: fitness scores of current generation
        :param nSlc: number of genomes to naturally select
        :return: list of genomes selected to move on to next generation
        """

        sortedGen = [genome for score, genome in sorted(zip(fitness, gen), reverse=True)]
        bestFitness = sorted(fitness, reverse=True)[0]

        return sortedGen[:nSlc], bestFitness

    def breed(slcGen, nInd):
        """
        Breeds a new generation, randomly using crossover and mutation on selected genomes
        :param slcGen: selected genomes from previous generation
        :param nInd: number of individuals to breed generation to
        :return: new generation of genomes
        """

        newGen = deepcopy(slcGen)
        for i in range(nInd-len(newGen)):
            parent1, parent2 = tuple(Schedule(p) for p in sample(slcGen, 2))
            newGen.append(parent1.breedGenome(parent2))

        return newGen

    # Begin loop
    for n in range(nGen):

        print('Generation #{0}'.format(n+1))

        # Evaluate current generation
        genFitness = evaluate(gen)

        # Select fittest genomes naturally
        slcGen, bestFitness = select(gen, genFitness, nSlc)

        print('-- Highest genome score: {0}'.format(bestFitness))

        # Breed new generation from selected individuals
        if n < nGen-1: gen = breed(slcGen, nInd)
        # Or, if it's the last iteration of the loop, return the fittest genome
        else: return Schedule(slcGen[0]), bestFitness


if __name__ == "__main__":
    main()
