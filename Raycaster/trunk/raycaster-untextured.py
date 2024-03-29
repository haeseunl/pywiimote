import math
import pygame
from pygame.locals import *
pygame.display.init()

#bugs
"""
walking past corners closely looks weird
might just have to do with movement speed, not sure yet.
will be easier to tell once texturing.
"""

#ideas
"""
1) way to generate a default keymap
2) positional audio
3) items have methods inside them' but all items have a universal attribute like queryobject
which will return something like this: object location: blah, object type: whatever
and given its type you can know what to call on it.
4)
Player starting area should be reserved by a map item.
--actually textures/walls data should be in a different file than the npc and player info.
5)
buffer texture scaling results (or preload them)
"""


def loadmap(path):
    f = file(path)
    tmp = f.readlines()
    the_map = []
    for line in tmp:
        #the_map.append([ord(c) for c in line.strip()])
        the_map.append([int(c) for c in line.strip()])
    f.close()
    return the_map

def drawmap(surf,the_map,gridsize):#should be a 2d list of ints
    for y,ydata in enumerate(the_map):
        for x,is_wall in enumerate(ydata):
            if is_wall:
                pygame.draw.rect(surf,(60,60,190), (x*gridsize,y*gridsize,gridsize-1,gridsize-1))
            else:
                pygame.draw.rect(surf,(255,0,0), (x*gridsize,y*gridsize,gridsize-1,gridsize-1),1)

def drawplayer(surf,location):
    pygame.draw.circle(surf,(190,190,0),location,3)


def drawray(surf,start,end,collisions):
    pygame.draw.line(surf,(3,227,252),start,end)
    for item in collisions:
        if item[1] == 1:#vertical collision
            pygame.draw.circle(surf,(149,0,149),item[0],2)
        elif item[1] == 2:#closest wall intersection            
            pygame.draw.circle(surf,(255,255,255),(int(item[0][0]),int(item[0][1])),2)
            
        else:
            pygame.draw.circle(surf,(0,0,149),(int(item[0][0]),int(item[0][1])),2)
pygame.font.init()
font = pygame.font.Font(None,16)

def screenoverlay(screen,position, text):
    screen.blit(font.render(text,0,(255,255,255)),position)
    


def castmap(the_map, playerpos, playerangle,gridsize,surf):
    plane = (320,200)
    planecenter = (160,100)
    FOV = 60
    planedist = (plane[0]/2) / math.tan(math.radians(FOV/2))
    rayincrement = FOV / float(plane[0])
    rayangle = playerangle + FOV / 2 #will this cast invertedly?
    #fix playerangle
    playerangle = playerangle % 360
    scaling = []#holds distances to walls
    wallvalues = []#what type of wall was at each location
    coltype = []#vert or horizontal collision? 1 = vertical
    collisionlocation = []
    for x in range(plane[0]):
        rayangle -= rayincrement
        horizint,vertint = castray(the_map,gridsize,playerpos,rayangle)
        closestpoint = None
        distance = None
        denom = abs(math.cos(math.radians(rayangle)))
        correction = math.cos(math.radians(playerangle-rayangle))
        #if denom 
        if horizint and not vertint:
            coltype.append(0)
            distance = abs(playerpos[1]-horizint[1]) / abs(math.sin(math.radians(rayangle))) * correction
            closestpoint = horizint

        elif vertint and not horizint:#this shouldnt cause a division by zero...
            coltype.append(1)
            distance = abs(playerpos[0]-vertint[0]) / abs(math.cos(math.radians(rayangle))) * correction
            closestpoint = vertint
        elif vertint and horizint:
            horizdist = abs(playerpos[0]-horizint[0]) / abs(math.cos(math.radians(rayangle))) * correction
            vertdist = abs(playerpos[0]-vertint[0]) / abs(math.cos(math.radians(rayangle))) * correction


            if abs(horizdist) < abs(vertdist):
                coltype.append(0)
                closestpoint = horizint
                distance = abs(horizdist)
            else:
                coltype.append(1)
                closestpoint = vertint
                distance = abs(vertdist)
        #no else necessary


        #if closestpoint and (x == 0 or x == plane[0]-1):
        if closestpoint:
            drawray(surf,playerpos,closestpoint,[(closestpoint,2)])
        wallvalues.append(the_map[int(closestpoint[1]) / gridsize][int(closestpoint[0]) / gridsize])
        collisionlocation.append(closestpoint)
        scaling.append(distance)

    return (wallvalues, (coltype,collisionlocation), scaling)


    
def castray(the_map,gridsize,raystart,rayangle):
    """ returns first horizontal & vertical intersections (or none for either or both)"""
    #todo: wrap angle values at 360?
    #this will be made into a class later
    


    #if rayfixed >= 360:
    rayfixed = rayangle % 360 #even wraps negative values correctly, (floats too i think)
    #print rayfixed
    horizint = None
    vertint = None
    #Horizontal intersections
    
    if rayfixed < 180 and rayfixed != 0 and rayfixed != 90:#pointing up
        stepy = -gridsize
        pointy = (raystart[1] / gridsize) * gridsize -.001
        stepx = gridsize/math.tan(math.radians(rayfixed))
    elif rayfixed > 180 and rayfixed != 270:#pointing down
        stepy = gridsize
        pointy = (raystart[1] / gridsize) * gridsize + gridsize#i'm sure there's a better way to do this
        stepx = -(gridsize/math.tan(math.radians(rayfixed)))

    elif rayfixed == 90:        
        stepy = -gridsize
        pointy = (raystart[1] / gridsize) * gridsize - .001#problem b/c of angle projection' makes walls stick out if angle of
        #ray is far off of FOV. may have something to do with not casting ray as integer or something?
        #fixed this way, anyway
        stepx = 0
        pointx = raystart[0]
    elif rayfixed == 270:
                
        stepy = gridsize
        pointy = (raystart[1] / gridsize) * gridsize + gridsize
        stepx = 0
        pointx = raystart[0]

    else:
        pass#horizint will stay None

    
    

    if rayfixed != 0 and rayfixed != 180:
        if rayfixed != 90 and rayfixed != 270:
            #we have the y-coord of first intersection point to check
            #let's get the x coord (case: 90/270 pointx is just ray start b/c ray x-component = 0.)
            pointx = raystart[0] + (raystart[1] - pointy) / math.tan(math.radians(rayfixed))
        mapx = int(pointx)/gridsize
        mapy = int(pointy)/gridsize
        
        
        while mapx >= 0 and mapx < len(the_map[0]) and mapy >= 0 and mapy < len(the_map):
            #should work for non-square maps, assuming rectangular
            if the_map[mapy][mapx]:#nonzero, therefore wall
                
                horizint = (pointx,pointy)
                break
            
            pointx += stepx
            pointy += stepy
            mapx = int(pointx)/gridsize
            mapy = int(pointy)/gridsize
    #------------------------------------

    #Vertical intersections
    if rayfixed > 90 and rayfixed < 270:#pointing left
        stepx = -gridsize
        pointx = (raystart[0] / gridsize) * gridsize - .001
        stepy = gridsize*math.tan(math.radians(rayfixed))
    else:#pointing right
        stepx = gridsize
        pointx = (raystart[0] / gridsize) * gridsize + gridsize#i'm sure there's a better way to do this
        stepy = -(gridsize*math.tan(math.radians(rayfixed)))

    pointy = raystart[1] + (raystart[0] - pointx) * math.tan(math.radians(rayfixed))
    
    mapx = int(pointx)/gridsize
    mapy = int(pointy)/gridsize
    
    while mapx >= 0 and mapx < len(the_map[0]) and mapy >= 0 and mapy < len(the_map):
        #should work for non-square maps, assuming rectangular
        if the_map[mapy][mapx]:#nonzero, therefore wall
            vertint = (pointx,pointy)
            break
        pointx += stepx
        pointy += stepy
        mapx = int(pointx)/gridsize
        mapy = int(pointy)/gridsize
    return (horizint,vertint)

    
    
    

#todo: directional sound
    
def moveplayer(the_map,playerpos,move, gridsize):
    #checks that they don't move through a wall.  would be simple to implement a ray that is used to calculate
    #distance to closest wall on player's movement path and determine if they are walking through it;
    #currently this function merely checks for the dest square to see if it is occupied.
    #should be perfectly fine unless you plan on letting them move faster than gridsize.
    destx = playerpos[0] + move[0]
    if destx >= 0 and int(destx/gridsize) < len(the_map[0]):
        if the_map[int(playerpos[1]/gridsize)][int(destx/gridsize)]:
            destx = playerpos[0]
    else:
        destx = playerpos[0]

    desty = playerpos[1] + move[1]
    if desty >= 0 and int(desty/gridsize) < len(the_map):
        if the_map[int(desty/gridsize)][int(playerpos[0]/gridsize)]:
            desty = playerpos[1]
    else:#keeps people from moving off map, probably
        desty = playerpos[1]
        

    """
    desty = playerpos[1] + move[1]
    """
    
    return [destx, desty]


def castdisplay(screen, offset, textures, texturetype, collisioninfo, scaling):
    #WILL crash if no collision location ( == None)
    #assumes offset is an int
    width = 320
    height = 200
    mid = height / 2
    collisiontype,collisionlocation = collisioninfo
    screen.fill((20,20,190),(offset,0,width,mid))
    screen.fill((190,20,20),(offset,mid,width,mid))
    
    #print scaling[0]
    for x in range(320):
        if scaling[x]:
            sliceheight = 32 / scaling[x] * 277
            pygame.draw.line(screen,(0,0,0),(offset + x, mid - sliceheight / 2),(offset + x, mid + sliceheight / 2))


screen = pygame.display.set_mode((1024,768))

the_map = loadmap("the_map.txt")



playerpos = [100,100]
playerangle = 60
gridsize = 32
movespeed = 4
turnspeed = 3
offset = 700


import keymap
print keymap.action



while 1:
    pygame.display.update()

    if keymap.actionstatus['rotateright']: playerangle -= turnspeed
    if keymap.actionstatus['rotateleft']: playerangle += turnspeed
    move = [0,0]
    if keymap.actionstatus['moveforward']:
        move[0] += int(math.cos(math.radians(playerangle)) * movespeed)
        move[1] -= int(math.sin(math.radians(playerangle)) * movespeed)
    if keymap.actionstatus['movebackward']:
        move[0] -= int(math.cos(math.radians(playerangle)) * movespeed)
        move[1] += int(math.sin(math.radians(playerangle)) * movespeed)
        
    if keymap.actionstatus['strafeleft']:
        move[0] -= int(math.cos(math.radians(playerangle-90)) * movespeed)
        move[1] += int(math.sin(math.radians(playerangle-90)) * movespeed)
    
    if keymap.actionstatus['straferight']:
        move[0] -= int(math.cos(math.radians(playerangle+90)) * movespeed)
        move[1] += int(math.sin(math.radians(playerangle+90)) * movespeed)
        
    playerpos = moveplayer(the_map, playerpos, move, gridsize)
    screen.fill((0,0,0))
    drawmap(screen,the_map,gridsize)
    drawplayer(screen,playerpos)
    texturetype, collisioninfo, scaling = castmap(the_map, playerpos,playerangle,gridsize,screen)
    castdisplay(screen, offset, [], texturetype, collisioninfo, scaling)
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit
            else:
                try:
                    keymap.actionstatus[keymap.action[event.key]] = True
                except KeyError: pass
        elif event.type == KEYUP:
            try:
                keymap.actionstatus[keymap.action[event.key]] = False
            except KeyError: pass
            
            
