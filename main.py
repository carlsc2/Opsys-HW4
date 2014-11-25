import re


class Process(object):
    def __init__(self):
        self.uid = "" #the character that identifies the process
        self.frames = 0 #the number of memeory frames the process uses
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
        p.times = zip(processdata[2::2], processdata[3::2])

    return ret


if(__name__ == "__main__"):
    for item in parse_file("inputFile.txt"):
        print item