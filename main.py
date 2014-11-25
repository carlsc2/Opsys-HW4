import re


class Core(object):
    def __init__(self):
        self.isContiguous = True
        self.memory = []

        for i in range(1600):

            self.memory.append(Process())

    def SwapMemoryLocations(self, index1, index2):
        memHolder = self.memory[index1]
        self.memory[index1] = self.memory[index2]
        self.memory[index2] = memHolder



class Process(object):
    def __init__(self):
        self.uid = "" #the character that identifies the process
        self.frames = 0 #the number of memory frames the process uses
        self.times = [] #pairs of tuples of form: (arrival_time, exit_time)




def parse_file(filename):
    ret = []
    f = open(filename)
    num_processes = int(f.readline().rstrip())#get first line

    for line in f.readlines():
        p = Process()
        ret.append(p)
        processdata = re.split(r'[ \t]+', line.rstrip())
        p.uid = processdata[0]
        p.frames = int(processdata[1])
        p.times = zip([int(x) for x in processdata[2::2]], [int(x) for x in processdata[3::2]])

    return ret


if(__name__ == "__main__"):
    for item in parse_file("inputFile.txt"):
<<<<<<< HEAD
        print item

    c = Core()
=======
        print item.uid, item.frames, item.times
>>>>>>> b4eae02ac35ebb005976204d6a029c14eb2fab94
