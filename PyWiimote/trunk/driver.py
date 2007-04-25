VENDORID = 0x057e
PRODUCTID = 0x0306

def rbin(value):
    """ returns binary of value % 16 in reverse order (LSB -> MSB)"""
    table = {0:[0,0,0,0],1:[0,0,0,1],2:[0,0,1,0],3:[0,0,1,1],
             4:[0,1,0,0],5:[0,1,0,1],6:[0,1,1,0],7:[0,1,1,1],
             8:[1,0,0,0],9:[1,0,0,1],10:[1,0,1,0],11:[1,0,1,1],             
             12:[1,1,0,0],13:[1,1,0,1],14:[1,1,1,0],15:[1,1,1,1]}
    value %= 0x10
    temp = table[value]
    temp.reverse()
    return temp
    

import wiimote
from HID import HIDDevice, AccessDeniedError, PathNotFoundError
hid = HIDDevice()
wiimotes = []
x = 0
device = True
while device:
    handle = None
    try:
        print "HI"
        handle, overlapped = hid.OpenDevice(x)
        print "HO"
        attrib = hid.Connect(handle)
        print "VendorID: %s, Product ID: %s, Version: %s" % (attrib.VendorID, attrib.ProductID, attrib.VersionNumber)
        if PRODUCTID == attrib.ProductID and VENDORID == attrib.VendorID:
            print "Found a Wii Remote."
            wiimotes.append(wiimote.Wiimote(handle,overlapped))
        else:
            print "That wasn't a remote."
        
    except wiimote.AccessDeniedError:
        print "ACCESSDENIED"
        pass
    except wiimote.PathNotFoundError: #reached the end of the device list, probably.
        device = False
    x += 1
    
leds = 1
for x in range(len(wiimotes)):
    wiimotes[x].connectWiimote()
    wiimotes[x].leds = rbin(leds)
    wiimotes[x].rumble = False
    wiimotes[x].updateLEDs()
    #wiimotes[x].updateRumble() # updateLEDs does same thing in this case.
added = 0
subtracted = 0
while 1:
    for x in range(len(wiimotes)):
        wiimotes[0].updateStatus()
        
        if wiimotes[0].buttons['+'] == True:
            if not added:
                added = True
                leds += 1
                wiimotes[0].leds = rbin(leds)
                wiimotes[0].updateLEDs()
        else:
            if added:
                added = False
        if wiimotes[0].buttons['-'] == True:
            if not subtracted:
                subtracted = True
                leds -= 1
                wiimotes[0].leds = rbin(leds)
                wiimotes[0].updateLEDs()
        else:
            if subtracted:
                subtracted = False
