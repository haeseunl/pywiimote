import math
import pygame
from pygame.locals import *
pygame.display.init()

#todo
"""
set a maximum view distance so big areas won't lag?
what happens if wall is so far away the height becomes 0?
"""

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
6) in mapfile there should be a way to configure the player's offset within his square,
how big each map is, ad what direction the player is looking in.
"""
import math
class Raycaster(object):
    """ pass surf as a subsurface of the display, otherwise the raycasting will cover the whole screen. """
    def getCachedTexture(textureoffset,height,slicex):
        pause
    def __init__(self, themap, gridsize, displaysurf, texturelist, floortexture, ceilingtexture, camerapos, cameradir, FOV=60,
                 cameradistance=None):
        self.map = themap
        self.gridsize = gridsize
        self.textures = texturelist
        self.flootexture = floortexture
        self.ceilingtexure = ceilingtexture
        self.camerapos = camerapos
        self.cameradir = cameradir
        
        self.display = displaysurf
        self.centerx = self.displaysurf.get_width() / 2
        self.width = self.displaysurf.get_width() / 2
        self.setDisplaySurface(displaysurf)
        self.FOV = FOV
        self.FOVradians = math.radians(FOV)

        self.FPS = 0
        if not cameradistance:
            self.cameradistance = self.centerx / math.tan(FOVradians)
        else:
            self.cameradistance = cameradistance
        #self.tancache = [math.tan(math.radians(x)) for x in range(360)]
        #self.coscache = [math.cos(math.radians(x)) for x in range(360)]
        #self.sincache = [math.sin(math.radians(x)) for x in range(360)]

    def setDisplaySurface(self, surface):
        """ setDisplaySurface (pygame.Surface new_surface) -> None """
        self.display = surface
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.centerx = self.width / 2
        self.centery = self.height / 2
        


    def ShowFPS(self, position, font, size): #size is font point size.
        """ MAKE THIS CALCULATE THE FPS!!!!"""
        self.display.blit(font.render(self.FPS,0,(255,255,255)),position)

    def _castDisplay():
        #plane = (320,200)
        #planecenter = (160,100)
        #planedist = (plane[0]/2) / math.tan(math.radians(FOV/2))
        rayincrement = self.FOV / float(plane[0])
        rayangle = playerangle + FOV / 2 #will this cast invertedly?
        
        playerangle = playerangle % 360
        
        scaling = []#holds distances to walls
        wallvalues = []#what type of wall was at each location
        coltype = []#vert or horizontal collision? 1 = vertical
        collisionlocation = []
        for x in xrange(self.width):
            rayangle -= rayincrement
            rayrad = math.radians(rayangle)
            horizint,vertint = self._castRay(rayangle)
            closestpoint = None
            distance = None
            denom = abs(math.cos(rayrad))
            correction = math.cos(math.radians(playerangle-rayangle))
            #if denom 
            if horizint and not vertint:
                coltype.append(0)
                distance = abs(playerpos[1]-horizint[1]) / abs(math.sin(rayrad)) * correction
                closestpoint = horizint

            elif vertint and not horizint:#this shouldnt cause a division by zero...
                coltype.append(1)
                distance = abs(playerpos[0]-vertint[0]) / abs(math.cos(rayrad)) * correction
                closestpoint = vertint
            elif vertint and horizint:
                horizdist = abs(playerpos[0]-horizint[0]) / abs(math.cos(rayrad)) * correction
                vertdist = abs(playerpos[0]-vertint[0]) / abs(math.cos(rayrad)) * correction


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
    
    def _castRay(self,rayangle):
        """ returns first horizontal & vertical intersections (or none for either or both)"""

        #todo: wrap angle values at 360?
        
        #if rayangle >= 360:
        rayangle = rayangle % 360 #even wraps negative values correctly, (floats too i think)
        rayrad = math.radians(rayangle)
        #print rayangle
        horizint = None
        vertint = None
        
        #Horizontal intersections
        if rayangle < 180 and rayangle != 0 and rayangle != 90:#pointing up
            stepy = -self.gridsize
            pointy = (self.camerapos[1] / gridsize) * gridsize -.001
            stepx = gridsize/math.tan(rayrad)
        elif rayangle > 180 and rayangle != 270:#pointing down
            stepy = gridsize
            pointy = (self.camerapos[1] / gridsize) * gridsize + gridsize#i'm sure there's a better way to do this
            stepx = -(gridsize/math.tan(rayrad))

        elif rayangle == 90:        
            stepy = -gridsize
            pointy = (self.camerapos[1] / gridsize) * gridsize - .001#problem b/c of angle projection' makes walls stick out if angle of
            #ray is far off of FOV. may have something to do with not casting ray as integer or something?
            #fixed this way, anyway
            stepx = 0
            pointx = self.camerapos[0]
        elif rayangle == 270:
                    
            stepy = gridsize
            pointy = (self.camerapos[1] / gridsize) * gridsize + gridsize
            stepx = 0
            pointx = self.camerapos[0]

        else:
            pass#horizint will stay None

        
        

        if rayangle != 0 and rayangle != 180:
            if rayangle != 90 and rayangle != 270:
                #we have the y-coord of first intersection point to check
                #let's get the x coord (case: 90/270 pointx is just ray start b/c ray x-component = 0.)
                pointx = self.camerapos[0] + (self.camerapos[1] - pointy) / math.tan(rayrad)
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
        if rayangle > 90 and rayangle < 270:#pointing left
            stepx = -gridsize
            pointx = (self.camerapos[0] / gridsize) * gridsize - .001
            stepy = gridsize*math.tan(rayrad)
        else:#pointing right
            stepx = gridsize
            pointx = (self.camerapos[0] / gridsize) * gridsize + gridsize#i'm sure there's a better way to do this
            stepy = -(gridsize*math.tan(rayrad))

        pointy = self.camerapos[1] + (self.camerapos[0] - pointx) * math.tan(rayrad)
        
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
            #texture = pygame.transform.scale(textures[texturetype[x]-1],(sliceheight,sliceheight))
            texturestrip = 
            heightoffset = sliceheight - height
            if heightoffset > 0:
                heightoffset /= 2
            else:
                heightoffset = 0
            if collisiontype[x]:#vertical collision
                slicerect = [int(collisionlocation[x][1]) % 32, heightoffset,1, sliceheight-heightoffset]
                blitlocation = (offset + x, mid - sliceheight / 2)
            else:#horizontal collision
                slicerect = [int(collisionlocation[x][0]) % 32, heightoffset,1, sliceheight-heightoffset]
                blitlocation = (offset + x, mid - sliceheight / 2)
            screen.blit(texture,blitlocation,slicerect)





class RaycasterMap(object):
    pass


def loadimg(path):
    return pygame.image.load(path).convert()

def loadmap(path):
    f = file(path)
    tmp = f.readlines()
    the_map = []
    for line in tmp:
        #the_map.append([ord(c) for c in line.strip()])
        the_map.append([int(c) for c in line.strip()])
    f.close()
    return the_map

"""
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
"""


    



    
    
    

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
    castdisplay(screen, offset, [loadimg('wall.bmp')], texturetype, collisioninfo, scaling)
    
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
            
            
