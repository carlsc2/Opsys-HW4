import re
import sys
import os.path

class Core(object):
    def __init__(self,quiet,filename,mode):
        self.memory = ["."]*1600#string that represents current state of memory
        self.framesPerLine = 80
        self.processes = parse_file(filename)#list of Process() instances
        self.quietmode = quiet #True = no interact, False = interact with user
        self.mode = mode#the algorithm to run
        self.time = 0

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

    def remove_process(self, process):
        #remove a process from memory
        for frame in self.memory:
            if frame == process.uid:
                frame = "."

    def add_process(self, process):
        #add a process to memory, return True if succeed, False if failed to add
        pass

    def run(self):
        #run the simulation -- if the quiet flag is specified, don't wait for user input
        done = False
        while not done:

            #move time forward to the next event
            for process in self.processes:#find the next event
                for i,k in enumerate(process.times):
                    s,e = k#get start and end times
                    if s == self.time:
                        if not add_process(process):
                            break
                    elif e == self.time:
                        remove_process(process)


            self.time += 1#increment time by 1 ms


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
