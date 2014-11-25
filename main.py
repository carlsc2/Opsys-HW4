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
        for i in range(1600):
            if self.memory[i] != ".":
                indexHolder = i
                #while there's room to push back and the previous area is free
                while indexHolder > 0 and self.memory[indexHolder - 1] == ".":
                    self.SwapMemoryLocations(indexHolder, indexHolder - 1)
                    indexHolder -= 1

<<<<<<< HEAD
                startLock = False
                endFreeMem = False
				
	def AddProc(self):
	"""	
	#FIRST - puts new prog in first contiguous chunk of mem where it fits.--------------------------
	if mode == 'first'
		increment through mem
			if '.' found, 
				remember that location
				keep incrementingas long as still '.', keeping track of how far youve incremented
					if amount of '.' incremented through  == size of proc
						enter it in mem starting at where '.' was first found.
						no need to keep incrementing, break
		if proc not inserted
			defrag and run again
			if already degragged and still not added
				exit simulation with 'out of memory' error


	#BEST - puts new prog in smallest fitting chunk of free mem-------------------------------------
	if mode == 'best'
		increment through mem
			if '.' found
				remember that location
				increment as long as still '.', keeping track of how far youve incremented
					keep incrementing until not '.'
				if amount of '.' incremented though >= size of proc
					if first time getting this far, simply store first '.' location and length of free space.
					else if an area already stored, overright if this has a smaller free space.
		insert prog at the stored '.' location

		if proc not inserted
			need to defrag and run again
			if already degragged and still not added
				exit simulation with 'out of memory' error
 
	#NEXT - puts new prog after all current progs---------------------------------------------------
	if mode == 'next'
		decrement through mem from end
			keep counter of how far you have decremented
			if something other than '.' found
				break
		if counter is >= prog size
			increment once (to be in empty mem again) and insert prog

		if proc not inserted
			need to defrag and run again
			if already degragged and still not added
				exit simulation with 'out of memory' error

	#WORST - puts new prog in largest fitting chunk of free mem-------------------------------------
	if mode == 'worst'
		increment through mem
			if '.' found
				remember that location
				increment as long as still '.', keeping track of how far youve incremented
					keep incrementing until not '.'
				if amount of '.' incremented though >= size of proc
					if first time getting this far, simply store first '.' location and length of free space.
					else if an area already stored, overright if this has a larger free space.
		insert prog at the stored '.' location

		if proc not inserted
			need to defrag and run again
			if already degragged and still not added
				exit simulation with 'out of memory' error
	"""

	
	""" # NONCONTIG - self explanatory
	if mode == 'noncontig':
		counter = """PROCSIZE"""
		for i in range(1600):
            if self.memory[i] == ".":
                self.memory[i] = "procName"
				counter -= 1
				if counter == 0:
					break
		if counter != 0:
			exit simulation with 'out of memory' error
	"""
=======

>>>>>>> 48c3b52e2c3c5c581a8cf6d3e1cc452bd7723c0f

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
