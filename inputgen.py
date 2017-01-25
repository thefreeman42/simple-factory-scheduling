from Input import Task, Worker, Machine

inputLists = None

def genInput():
    """
    Generates random constraint environment for genetic algorithm.
    :return: lists of input variables as object instances
    """

    try:
        nTask = int(input('# of tasks to solve for: '))
        nType = int(input('# of task types: '))
        nWorker = int(input('# of workers available: '))
        nMach = int(input('# of machines available: '))
    except:
        raise Exception('Specifics of the environment must be given in integers.')

    print('-----')

    tasks, workers, machines = [], [], []
    with open('input.txt') as infile:
        for line in infile:
            if line.split(',')[0] == "task":
                tasks.append(Task(line.strip().split(',')[1:]))
            elif line.split(',')[0] == "worker":
                workers.append(Worker(line.strip().split(',')[1:]))
            elif line.split(',')[0] == "machine":
                machines.append(Machine(line.strip().split(',')[1:]))

    return (tasks, workers, machines)

if inputLists is None:
    inputLists = genInput()
# We make the lists of inputs global variables for simplicity's sake.
# It is used in generating genome strings, translating genome strings to genome objects, evaluation and breeding,
# and by making it global, we can avoid passing it in to multiple functions/methods in main, evolution and Schedule.
# It is a constant once genInput() generates it through main, therefore it will not cause unwanted side effects.