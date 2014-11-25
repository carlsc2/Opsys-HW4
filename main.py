import re
import sys
import os.path

class Core(object):
    def __init__(self,quiet,filename,mode):
        self.isContiguous = True
        self.memory = "."*1600
        self.framesPerLine = 80
        self.processes = parse_file(filename)
        self.quietmode = quiet
        self.mode = mode

    def PrintMemory(self):
        stringHolder = ""
        counter = 0
        for item in self.memory:
            stringHolder += item.uid

            counter += 1
            if counter == self.framesPerLine:
                counter = 0
                print stringHolder
                stringHolder = ""
<<<<<<< HEAD
                

=======
>>>>>>> 9cb6e7e5d2b644b9b83cdaaef136d31157dce4b0

    def SwapMemoryLocations(self, index1, index2):
        memHolder = self.memory[index1]
        self.memory[index1] = self.memory[index2]
        self.memory[index2] = memHolder


    def Defrag(self):
        memSection = []
        for i in range(1600):
            print self.memory[i].uid


class Process(object):
    def __init__(self):
        self.uid = "." #the character that identifies the process
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


<<<<<<< HEAD
if(__name__ == "__main__"):
    for item in parse_file("inputFile.txt"):
        print item.uid, item.frames, item.times

    c = Core()
    #c.PrintMemory()
    c.Defrag()
=======
def main():
    args = sys.argv
    if not (len(args) == 3 or len(args) == 4):
        print "USAGE: main.py [-q] <input-file> { first | best | next | worst }"
    else:
        quietmode = False
        if(args[1]) == "-q":
            quietmode = True
        filename = args[1 + quietmode]
        if not os.path.exists(filename):
            print "ERROR: Invalid file"
            return
        mode = str.lower(args[2 + quietmode])
        modes = ["first","best","next","worst"]
        if mode not in modes:
            print "ERROR: Invalid mode"
            return
        c = Core(quietmode, filename, mode)

if __name__ == "__main__":
    main()
>>>>>>> 9cb6e7e5d2b644b9b83cdaaef136d31157dce4b0
