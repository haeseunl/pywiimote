from pygame.locals import *
action = {
 K_LEFT:'rotateleft',
 K_RIGHT:'rotateright',
 K_UP:'moveforward',
 K_DOWN:'movebackward',
 K_w:'moveforward',
 K_s:'movebackward',
 K_a:'strafeleft',
 K_d:'straferight'}
actionstatus = {}
for item in action.values():
    actionstatus[item] = False
