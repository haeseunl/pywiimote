from wiimote import *
wiimotes = get_wiimotes()
print "You have the following wiimotes connected to the system:"
print wiimotes
inp = raw_input("Which would you like to access? ")
player_1 = wiimotes[int(inp)]
player_1.connectWiimote()

#import time
def hex2bin(item):
    bin = [[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],
           [1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]
    return bin[item % 16]
offset = 0
ledstatus = 1
player_1.updateLEDs(hex2bin(ledstatus))
while 1:
    player_1.updateStatus()
    player_1.printStatus()
    if player_1.buttons['+']:
        ledstatus += 1
        player_1.updateLEDs(hex2bin(ledstatus))
        
    if player_1.buttons['-']:
        ledstatus -= 1
        #if ledstatus <= 0: ledstatus = 0
        player_1.updateLEDs(hex2bin(ledstatus))
        
    if player_1.buttons['A']:
        if not player_1.rumble:
            player_1.rumble = True
            player_1.updateRumble()
    else:
        if player_1.rumble:
            player_1.rumble = False
            player_1.updateRumble()
