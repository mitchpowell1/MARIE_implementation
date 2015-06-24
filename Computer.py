__author__ = 'Mitchell Powell'

from ClassFile import *

def Boot():
## Instantiates registers and assigns some run control variables
    global Mem
    global Clock
    global IR
    global PC
    global MAR
    global MBR
    global AC
    global Run
    global Overflow
    global InReg
    global OutReg
    Mem = []
    for x in range(4096):
        Mem.append(Register(hex(x)[2:], 16, 0x0000))
    IR = Register('IR', 16, 0x0000)
    PC = Register('PC', 12, 0x000)
    MAR = Register('MAR', 12, 0x000)
    MBR = Register('MBR', 16, 0x0000)
    AC = Register('AC', 16, 0x0000)
    InReg = Register('InReg', 8, 0x00)
    OutReg = Register('OutReg',8,0x00)
    Clock = 0
    Run = 1
    Overflow = 0

def Initiate(input):
    x = open(input)
    PC.load(int(x.readline().split()[0],16))
#Read second line for number of iterations
    words = int(x.readline().split()[0])
    global RecentMod
    RecentMod = []
    global PCcount
    PCcount = 0

#Assign Values to memory cells based on input
    for i in range(words):
        Line = x.readline().split()
        value = int(Line[0],16)
        Mem[value].load(int(Line[1],16))
        RecentMod.append(int(Mem[value].name,16))
    WriteStatus()
    x.close()

def Status(MemAddress = None):
## Logs the status of the registers to the console
    print('\n{:10} {}'.format("Register","Contents"))
    print('\n{:6}{:20} {} \n'.format('',"Bin","Hex"))
    print('{:10} {:15} {}'.format(PC.name,PC.binDisplay(),PC.hexDisplay()))
    print('{:10} {:17} {}'.format(MAR.name,MAR.binDisplay(),MAR.hexDisplay()))
    print('{:5} {:20} {}'.format(IR.name,IR.binDisplay(),IR.hexDisplay()))
    if MemAddress != None:
        print('\nMem: \n')
        print('{:6}{:20}{}\n'.format('',"Bin","Hex"))
        for item in MemAddress:
            print('{:10} {:15} {}'.format(Mem[item].name, Mem[item].binDisplay(), Mem[item].hexDisplay()))

def WriteStatus():
## Logs the status of the registers to a text file
    global RecentMod
    a = './StatusRecord'
    x = open(a,'a')
    if Clock == 0:
        x.write('\nMitchell Powell\n')
    x.write('\nO Flag: '+str(Overflow)+'\n')
    x.write('\nR Flag: '+str(Run)+'\n')
    x.write('\nClock Cycle: '+str(Clock)+'\n')
    #x.write('\n{:10} {}\n'.format("Register","Contents"))
    x.write('\n{:6}{:20} {} \n'.format('',"Bin","Hex"))
    x.write('\n{:15} {:12} {}\n'.format(InReg.name,InReg.binDisplay(),InReg.hexDisplay()))
    x.write('{:15} {:12} {}\n'.format(OutReg.name,OutReg.binDisplay(),OutReg.hexDisplay()))
    x.write('{:10} {:16} {}\n'.format(PC.name,PC.binDisplay(),PC.hexDisplay()))
    x.write('{:10} {:16} {}\n'.format(MAR.name,MAR.binDisplay(),MAR.hexDisplay()))
    x.write('{:5} {:20} {}\n'.format(IR.name,IR.binDisplay(),IR.hexDisplay()))
    x.write('{:5} {:20} {}\n'.format(AC.name,AC.binDisplay(),AC.hexDisplay()))
    x.write('{:5} {:20} {}\n'.format(MBR.name,MBR.binDisplay(),MBR.hexDisplay()))
    x.write('\n{} Instruction'.format(DecodeName(IR.hexDisplay()[0])))
    x.write('\nMem: \n')
    if RecentMod != []:
        x.write('\n{:6}{:20}{}\n\n'.format('',"Bin","Hex"))
        for item in RecentMod:
            x.write('{:5} {:20} {}\n'.format(Mem[item].name, Mem[item].binDisplay(), Mem[item].hexDisplay()))
    else:
        x.write('\nNone Modified Since Last Write Out \n \n')
    x.write('...............................................')
    RecentMod = []

def Fetch():
## Loads PC to MAR and M[MAR] to IR, then increments PC
    global Clock
    MAR.load(PC.contents)
    IR.load(Mem[MAR.contents].contents)
    PC.contents += 1
    Clock += 2

def Decode():
    global Clock
    Clock += 1
    MAR.load(int(IR.hexDisplay()[1:],16))
    if IR.hexDisplay()[0] == '0':
        JNS()
    elif IR.hexDisplay()[0] == '1':
        Load()
        return "Load"
    elif IR.hexDisplay()[0] == '2':
        Store()
        return('Store')
    elif IR.hexDisplay()[0] == '3':
        Add()
        return('Add')
    elif IR.hexDisplay()[0] == '4':
        Subtract()
        return('Subtract')
    elif IR.hexDisplay()[0] == '5':
        Input()
        return('Input')
    elif IR.hexDisplay()[0] == '6':
        Output()
        return('Output')
    elif IR.hexDisplay()[0] == '7':
        Halt()
        return('Halt')
    elif IR.hexDisplay()[0] == '8':
        SkipCond()
        return('SkipCond')
    elif IR.hexDisplay()[0] == '9':
        Jump()
        return('Jump')
    elif IR.hexDisplay()[0] == 'A':
        Clear()
        return('Clear')
    elif IR.hexDisplay()[0] == 'B':
        AddI()
        return('AddI')
    elif IR.hexDisplay()[0] == 'C':
        JumpI()
        return('JumpI')
    elif IR.hexDisplay()[0] == 'D':
        LoadI()
        return("LoadI")
    elif IR.hexDisplay()[0] == "E":
        StoreI()
        return('StoreI')
    elif IR.hexDisplay()[0] == "F":
        return None
def DecodeName(x):
    if x == '0':
        Name = 'JNS'
    elif x == '1':
        Name = 'Load'
    elif x == '2':
        Name = 'Store'
    elif x == '3':
        Name = 'Add'
    elif x == '4':
        Name = "Subtract"
    elif x == '5':
        Name = 'Input'
    elif x == '6':
        Name = 'Output'
    elif x == '7':
        Name = 'Halt'
    elif x == '8':
        Name = 'SkipCond'
    elif x == '9':
        Name = 'Jump X'
    elif x == 'A':
        Name = 'Clear'
    elif x == 'B':
        Name = 'Add (Indirect)'
    elif x == 'C':
        Name = 'Jump (Indirect)'
    elif x == 'D':
        Name = 'Load (Indirect)'
    elif x == 'E':
        Name = 'Store (Indirect)'
    else:
        Name = None
    return Name

def Add():
    global MBR
    global AC
    global Clock
    global Overflow
    MBR.load(Mem[MAR.contents].contents)
    AC.contents += MBR.contents
    if len(AC.hexDisplay()) > 4:
        Overflow = 1
        AC.contents = int(AC.hexDisplay()[1:],16)
    Clock +=2
def AddI():
    global Clock
    global Overflow
    global AC
    MAR.load(int(Mem[MAR.contents].hexDisplay()[1:],16))
    MBR.load(Mem[MAR.contents].contents)
    AC.contents += MBR.contents
    if AC.contents > 0xFFFF:
        Overflow = 1
        AC.load(int(AC.hexDisplay()[1:],16))
    Clock += 3
def Clear():
    global Clock
    global Overflow
    AC.dump()
    Clock += 1
    Overflow = 0
def Halt():
    global Run
    global Clock
    Run = 0
    Clock += 1
def Input():
    global Clock
    AC.load(InReg.contents)
    Clock += 1
def JNS():
    global MAR
    global Clock
    MBR.load(PC.contents)
    Mem[MAR.contents].load(MBR.contents)
    RecentMod.append(int(Mem[MAR.contents].name,16))
    MAR.contents += 1
    PC.load(MAR.contents)
    Clock += 3
def Jump():
    global Clock
    PC.load(int(IR.hexDisplay()[1:],16))
    Clock+= 1
def JumpI():
    global Clock
    PC.load(int(Mem[MAR.contents].hexDisplay()[1:],16))
    Clock += 1
def Load():
    global MBR
    global AC
    global Clock
    MBR.load(Mem[MAR.contents].contents)
    AC.load(MBR.contents)
    Clock +=2
def LoadI():
    global Clock
    MAR.load(int(Mem[MAR.contents].hexDisplay()[1:],16))
    MBR.load(Mem[MAR.contents].contents)
    AC.load(MBR.contents)
    Clock += 3
def Output():
    global Clock
    OutReg.load(AC.contents)
    Clock += 1
def SkipCond():
    global Clock
    if int(IR.hexDisplay()[1:2],16) == 0 and AC.contents < 0:
        PC.contents+=1
    elif int(IR.hexDisplay()[1:2],16) == 4 and AC.contents == 0 and Overflow != 1:
        PC.contents +=1
    elif int(IR.hexDisplay()[1:2],16) == 12 and AC.contents > 0:
       PC.contents += 1
    Clock += 1

def Store():
    global Clock
    global MBR
    global Mem
    MBR.load(AC.contents)
    Mem[MAR.contents].load(MBR.contents)
    RecentMod.append(int(Mem[MAR.contents].name,16))
    Clock +=2
def StoreI():
    global Clock
    MAR.load(int(Mem[MAR.contents].hexDisplay()[1:],16))
    MBR.load(AC.contents)
    Mem[MAR.contents].load(MBR.contents)
    RecentMod.append(int(Mem[MAR.contents].name,16))
    Clock += 3
def Subtract():
    global Clock
    global Overflow
    MBR.load(Mem[MAR.contents].contents)
    AC.load(AC.contents-MBR.contents)
    if AC.contents < 0:
        AC.contents = abs(AC.contents)
        Overflow = 1
    Clock += 2



def Main():
## Main Program Loop
    Boot()
    Initiate('./Fibonnacci')
    while Run == 1:
        Fetch()
        Decode()
        WriteStatus()
Main()
