__author__ = 'Mitchell Powell'

class Register:
    def __init__(self,name,size,contents):
        self.name = name
        self.size = size
        self.contents = contents
        self.bin = str('{0:016b}'.format(contents))

#Returns a binary representation of the registers contents
#in a string format
    def binDisplay(self):
        if self.size == 16:
            A = str("{0:016b}".format(self.contents))
            B = '{} {} {} {}'.format(A[0:4],A[4:8],A[8:12],A[12:16])
        elif self.size == 12:
            A = str("{0:012b}".format(self.contents))
            B='{} {} {}'.format(A[0:4],A[4:8],A[8:12])
        elif self.size == 8:
            A = str("{0:08b}".format(self.contents))
            B = '{} {}'.format(A[0:4],A[4:8])
        return B
#Returns a decimal representation of the register's contents
#in a string format
    def decDisplay(self):
        return "Dec: " +str(self.contents)
    def hexDisplay(self):
        if self.size == 16:
            return str("{0:04X}".format(self.contents))
        elif self.size == 12:
            return str("{0:03X}".format(self.contents))
        elif self.size == 8:
            return str("{0:02X}".format(self.contents))

    def load(self,new):
        self.contents = new

    def dump(self):
        if self.size == 12:
            self.contents = 0x000
        elif self.size == 16:
            self.contents = 0x0000
#main()