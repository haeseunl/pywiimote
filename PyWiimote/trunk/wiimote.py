import hid
import sys
VENDORID = 0x057e
PRODUCTID = 0x0306



FEATURE_DISABLE = 0x00
FEATURE_ENABLE = 0x04

IR_MODE_OFF = 0
IR_MODE_STD = 1
IR_MODE_EXP = 3
IR_MODE_FULL = 5

CMD_SET_REPORT = 0x52

RID_LEDS = 0x11
RID_MODE = 0x12
RID_IR_EN = 0x13
RID_SPK_EN = 0x14
RID_STATUS = 0x15
RID_WMEM = 0x16
RID_RMEM = 0x17
RID_SPK = 0x18
RID_SPK_MUTE = 0x19
RID_IR_EN2 = 0x1A

MODE_BASIC = 0x30
MODE_ACC = 0x31
MODE_ACC_IR = 0x33
MODE_FULL = 0x3e

class Wiimote(object):
    """ currently only works on XP, but you can inherit and override the write method if you have some way of writing the reports on another platform."""
    def __init__(self, oparg):
        """oparg is an argument we pass to the hid operations.  We don't care
        what the """
        self.handle = handle
        self.overlapped = overlapped
        self.leds = [0,0,0,0]
        self.rumble = False
        self.continuous = False
        self.accel = [0,0,0]
        self.buttons = {'Two':False,'One':False,'B':False,'A':False,'-':False,'+':False,'Home':False,
                        'Left':False,'Right':False,'Up':False,'Down':False}
        
    def __del__(self):
        hid.Disconnect(self.handle)
    def connectWiimote(self):
        self.write([0x52,0x12, 0x00, 0x30])

    def write(self, data):
        hid.Write(self.handle, self.overlapped, data)
        
    def read(self):
        return hid.Read(self.handle, self.overlapped)
    def send(self,cmd,report,data):
        temp = [cmd]
        temp.append(report)
        temp.extend(data)
        self.write(temp)
        #Send cmd, report, data to Wiimote. If cmd is CMD_SET_REPORT, this amounts to sending data to the specified report.
        #Interface code to Wiimote goes here.

    def setMode(self,mode,cont):
        """ cont = whether you want input to be continuous or only on state changes."""
        aux = 0
        if self.rumble:
                aux |= 0x01
        if cont:
                aux |= 0x04
        self.continuous = cont
        self.send(CMD_SET_REPORT,RID_MODE,[aux,mode])

    # size here is redundant, since we can just use len(data) if we want.
    def sendData(self,data,offset): # see writing to data: [[#On-board Memory].
        of1 = offset >> 24 & 0xFF #extract offset bytes
        of2 = offset >> 16 & 0xFF
        of3 = offset >> 8 & 0xFF
        of4 = offset & 0xFF
        data2 = data + [0]*(16-len(data)) # append zeros to pad data if less than 16 bytes
        if len(data2) > 16:
                data2 = data2[:16] # crop data if we have too much
        # format is [OFFSET (BIGENDIAN),SIZE,DATA (16bytes)]
        self.send(CMD_SET_REPORT,RID_WMEM,[of1,of2,of3,of4,len(data)]+data2)        

    def updateLEDs(self):
        """also makes sure rumble is current, but updateRumble should be used
        in general for rumble updates, because if changes are too fast, calling this
        function too frequently will default out the remote, causing the LEDs to
        flash. On the contrary, it's an easy way to flash the LEDs if you have need for that.
        """
        temp = 0x00
        if self.rumble:
            temp = 0x01
        addvals = [0x10,0x20,0x40,0x80]
        for x in range(4):
            if self.leds[x] != 0:
                temp |= addvals[x]
        self.send(CMD_SET_REPORT, RID_LEDS, [temp])

    def updateRumble(self):
        if self.rumble:
            self.send(CMD_SET_REPORT, RID_STATUS, [0x01]) #RID_MODE used b/c it's different from RID_LEDS
        else:
            self.send(CMD_SET_REPORT, RID_STATUS, [0x00])
    
    def updateStatus(self):
    
        readresult = self.read()
        reporttype = readresult[0]
        #button status is supposedly included in all reports in first 2 bits (not counting reporttype)
        #so we'll trust that that's correct and use those values.

        #the extract table is: (buttonName, offset, value)
        extracttable = [('Two',2,0x01),('One',2,0x02),('B',2,0x04),('A',2,0x08),
                        ('-',2,0x10),('Home',2,0x80),('Left',1,0x01),
                        ('Right',1,0x02),('Down',1,0x04),('Up',1,0x08),
                        ('+',1,0x10)]
        for name,index,andval in extracttable:
            temp = readresult[index] & andval
            if temp != 0:
                self.buttons[name] = 1
            else:
                self.buttons[name] = 0
        if reporttype == 0x30:# buttons only
            pass
        #print "Number of bytes read: "+ str(len(readresult))
        #print "Buffer: "
        #for x in range(len(readresult)):
        #        sys.stdout.write(readresult[x])
        #sys.stdout.write('\n')
        self.printStatus()
        if self.buttons['A']:
            if not self.rumble:
                self.rumble = True
                self.updateRumble()
        else:
            if self.rumble:
                self.rumble = False
                self.updateRumble()
            
    def printStatus(self):
        line = ['A','B','-','+','Home']
        for item in line:
            sys.stdout.write(item + ": " + ['False','True'][self.buttons[item]]+", ")
        line = ['Left','Right','Up','Down','One','Two']
        sys.stdout.write('\n')
        for item in line:
            sys.stdout.write(item + ": " + ['False','True'][self.buttons[item]]+", ")
        sys.stdout.write('\n')
        print "LEDs: [%s,%s,%s,%s], Rumble: %s" % (self.leds[0],self.leds[1],
                                                   self.leds[2],self.leds[3],
                                                   self.rumble)
    
#Vendor ID, 0x057e. Product ID, 0x0306
wiimotes = []
x = 0
device = True
while device:
    handle = None
    try:
        handle, overlapped = hid.OpenDevice(x)
        attrib = hid.Connect(handle)
        print "VendorID: %s, Product ID: %s, Version: %s" % (attrib.VendorID, attrib.ProductID, attrib.VersionNumber)
        if PRODUCTID == attrib.ProductID and VENDORID == attrib.VendorID:
            print "Found a Wii Remote."
            wiimotes.append(Wiimote(handle,overlapped))
        else:
            print "That wasn't a remote."
        
    except AccessDeniedError:
        pass
    except PathNotFoundError: #reached the end of the device list, probably.
        device = False
    x += 1



# this is Cliff's version pythonified, probably more accurate as far as sensitivity. Works pretty much the same for me.
#wiimotes[0].send(0x52,0x12,[0x00,0x30])

"""
wiimotes[0].setmode(MODE_ACC_IR,0)
#wiimotes[0].send(CMD_SET_REPORT, RID_LEDS, [0x10])
wiimotes[0].send(CMD_SET_REPORT,RID_IR_EN,[FEATURE_ENABLE])
wiimotes[0].send(CMD_SET_REPORT,RID_IR_EN2,[FEATURE_ENABLE])
wiimotes[0].senddata([1],0x04B00030) # seems to enable the IR peripheral
wiimotes[0].senddata([0x02, 0x00, 0x00, 0x71, 0x01, 0x00, 0xaa, 0x00, 0x64],0x04B00000)
wiimotes[0].senddata([0x63, 0x03],0x04B0001A)
# this seems incorrect - for FULL IR mode, we must use FULL wiimote mode (0x3e).
# otherwise the data is probably garbled.
wiimotes[0].senddata([IR_MODE_FULL],0x04B00033) 
wiimotes[0].senddata([8],0x04B00030) # Enable data output. Can be specified first it seems, we don't really need to be in mode 1.
"""




