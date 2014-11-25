import re
import sys
import os.path

class Core(object):
    def __init__(self,quiet,filename,mode):
        self.memory = "."*1600#string that represents current state of memory
        self.framesPerLine = 80
        self.processes = parse_file(filename)#list of Process() instances
        self.quietmode = quiet #True = no interact, False = interact with user
        self.mode = mode#the algorithm to run

    def FreeMemory(self, procName):
        for i in range(1600):
            if self.memory[i] == procName:
                self.memory[i] = "."

    def PrintMemory(self):
        stringHolder = ""
        counter = 0
        for item in self.memory:
            stringHolder += item

            counter += 1
            if counter == self.framesPerLine:
                counter = 0
                print stringHolder
                stringHolder = ""


    def SwapMemoryLocations(self, index1, index2):
        memHolder = self.memory[index1]
        self.memory[index1] = self.memory[index2]
        self.memory[index2] = memHolder


    def Defrag(self):
        startFreeMem = 0
        startLock = False
        endFreeMem = 0
        endLock = False

        for i in range(1600):
            if self.memory[i] == "." && startLock == False:#set starting freespace location
                startFreeMem = i
                startLock = True
            if self.memory[i] == "." && startLock == True:#set ending freespace location
                endFreeMem = i
                endLock = True
            
            if startLock == True && endLock == True:#swapping loop
                for j in range(endFreeMem - startFreeMem):
                    if (j + (endFreeMem - startFreeMem) < 1600):#make sure we don't go out of bounds


                startLock = False
                endFreeMem = False


class Process(object):
    def __init__(self):
        self.uid = "." #the character that identifies the process
        self.frames = 0 #the number of memory frames the process uses
        self.times = [] #pairs of tuples of form: (arrival_time, exit_time)

def parse_file(filename):#parse the input file, return a list of Process() instances with data filled in
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


def main():
    args = sys.argv
    if not (len(args) == 3 or len(args) == 4):
        print "USAGE: memsim [-q] <input-file> { noncontig | first | best | next | worst }"
    else:
        quietmode = False
        if(args[1]) == "-q":
            quietmode = True
        filename = args[1 + quietmode]
        if not os.path.exists(filename):
            print "ERROR: Invalid file"
            return
        mode = str.lower(args[2 + quietmode])
        modes = ["first","best","next","worst","noncontig"]
        if mode not in modes:
            print "ERROR: Invalid mode"
            return
        c = Core(quietmode, filename, mode)

if __name__ == "__main__":
    main()
