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
        self.jumptime = 0

    def PrintMemory(self):
        print "Memory at time %d:"%self.time
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

    def run(self):
        #run the simulation -- if the quiet flag is specified, don't wait for user input
        while True:
            #move time forward to the next event
            ps = []#processes to start this frame
            pe = []#processes to end this frame
            for process in self.processes:#find the next event
                for i,k in enumerate(process.times):
                    s,e = k#get start and end times
                    if s == self.time:
                        ps.append(process)
                    elif e == self.time:
                        pe.append(process)
            for process in pe:#for each process to end this frame
                remove_process(process)#end it
                if self.quietmode:#if automatic, print event
                    self.PrintMemory()#print memory and time
            for process in ps:#for each process to start this frame
                if not add_process(process):#if the process failed to allocate memory, return
                    self.Defrag()
                    if not add_process(process):
                        print "ERROR: OUT-OF-MEMORY"
                        return
                if self.quietmode:#if automatic, print event
                    self.PrintMemory()#print memory and time

            if not self.quietmode and self.time >= self.jumptime:#if not quiet mode, wait for user input
                self.PrintMemory()#print memory and time
                done = False
                while not done:
                    tmp = int(raw_input("Enter an integer t: "))
                    if tmp == 0:
                        return
                    if tmp <= self.time:
                        print "ERROR: t must be greater than current time"
                    self.jumptime = tmp
            self.time += 1#increment time by 1 ms

    def Defrag(self):
        print "Performing defragmentation..."
        for i in range(1600):
            if self.memory[i] != ".":
                indexHolder = i
                #while there's room to push back and the previous area is free
                while indexHolder > 0 and self.memory[indexHolder - 1] == ".":
                    self.SwapMemoryLocations(indexHolder, indexHolder - 1)
                    indexHolder -= 1
        print "Defragmentation completed."

    def add_process(self, process):
        #FIRST - puts new prog in first contiguous chunk of mem where it fits.--------------------------
        if self.mode == 'first':
            startLock = False
            startPos = 0
            incrementAmount = 0
            addSuccessful = False
            for i in range(1600):
                if self.memory[i] == "." and startLock == False:#start of free space
                    startPos = i
                    startLock = True

                if startLock == True and self.memory[i] != ".":
                    startLock = False

                if startLock == True and i - startPos >= process.frames:#reach suitable amount of room
                    for i in range(startPos, i + 1):
                        self.memory[i] = process.uid
                    addSuccessful = True
                    break

            if addSuccessful == False:
                return False
            else:
                return True


    	#BEST - puts new prog in smallest fitting chunk of free mem-------------------------------------
        if self.mode == 'best':
            bestfree = 1601
            beststart = 0

            for i in range(1600):
                if self.memory[i] == "." and startLock == False:#start of free space
                    startPos = i
                    startLock = True

                if startLock == True and self.memory[i] != ".":
                    startLock = False
                    freelen = i - startLock
                    if freelen >= process.frames:
                        if freelen < bestfree:
                            bestfree = freelen
                            beststart = startPos

            if bestfree <= 1600:
                for i in range(startPos, i + 1):
                    self.memory[i] = process.uid
                return True
            else:
                return False


    	#NEXT - puts new prog after all current progs---------------------------------------------------
    	if self.mode == 'next':
            i = 1599
            while i >= 0:
                if self.memory[i] != ".":
                    break
                i-=1

            chunksize = 1599 - i

            if chunksize >= process.frames:
                i += 1
                for i in range(startPos, i + 1):
                    self.memory[i] = process.uid
                return True
            else:
                return False



    	#WORST - puts new prog in largest fitting chunk of free mem-------------------------------------
        if self.mode == 'worst':
            bestfree = -1
            beststart = 0

            for i in range(1600):
                if self.memory[i] == "." and startLock == False:#start of free space
                    startPos = i
                    startLock = True

                if startLock == True and self.memory[i] != ".":
                    startLock = False
                    freelen = i - startLock
                    if freelen >= process.frames:
                        if freelen > bestfree:
                            bestfree = freelen
                            beststart = startPos

            if bestfree >= 0:
                for i in range(startPos, i + 1):
                    self.memory[i] = process.uid
                return True
            else:
                return False

        #NONCONTIG - puts new prog in largest fitting chunk of free mem-------------------------------------
        if self.mode == "noncontig":
            counter = process.frames
            for i in range(1600):
                if self.memory[i]== ".":
                    self.memory[i] = procname
                    counter -= 1
                if counter == 0:
                    break
            if counter != 0:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()
            else:
                return True

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

        c.Defrag()
        c.PrintMemory()

if __name__ == "__main__":
    main()
