import math
import pygame, os
from pygame.locals import *
pygame.display.init()

#todo
"""
set a maximum view distance so big areas won't lag?
what happens if wall is so far away the height becomes 0?


let them set horis resolution, so they can have a 640x480 surf that has 320 rays, for example.
"""

#bugs
"""
Gridsize of 16 or 128 doesn't work when texture is 128x128, unsure if texture is 32x32, suspect it doesn't work either.

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
    def _drawStripe(self,wallvalues,collisions,xoffset,height, distances, isvertical):
        """Never returns bigger than the gridsize"""
        #print "THIS IS THE TEXTURE OFFSET: " + str(textureoffset)
        #print "Xoffset is:" + str(xoffset)
        #print "Wallvalues[%s] = %s" % (xoffset,wallvalues[xoffset])
        #print "LEN OF WALLVALUES:" + str(len(wallvalues))
        texture = self.textures[wallvalues[xoffset]-1]

        texheight = texture.get_height()
        texwidth = texture.get_width()

        
        if isvertical:
            slicex = int(collisions[xoffset][1] % texture.get_width())
        else:
            slicex = int(collisions[xoffset][0] % texture.get_width())
        
        sliceheight = height
        if height < 1: sliceheight = 1
        yoffset = (self.height - sliceheight) / 2 + 1
        end = self.height - yoffset - 1
        if end > self.height:
            end = self.height
        if height > self.height:
            yoffset = 0
        while yoffset <= end:
            d = yoffset * 256 - self.height * 128 + height * 128
            slicey = ((d * texheight) / height) / 256
            try:
                pix = texture.get_at((slicex,slicey))
                if self.darkenvertical:
                    if isvertical:
                        pass
                        #pix = (max(0,pix[0]-32),max(0,pix[1]-32),max(0,pix[2]-32))
                #print pix
            except:
                pix = (255,255,255)
                #print "Slicex: %s, Slicey: %s" % (slicex,slicey)
                pass
            self.display.set_at((xoffset,yoffset),pix)
            yoffset += 1
            #print offset


        """

        #--- start floorcasting below
        while yoffset < self.height:
            if sliceheight <= 1:
                return
            currentDist = self.height / (2.0 * yoffset - height)
            weight = currentDist / distances[xoffset]
            #currentFloorPos = weight * floorPosWall + (1.0 - weight) * playerPos
            currentFloorX = weight * collisions[xoffset][0] + (1.0 - weight) * 1
            currentFloorY = weight * collisions[xoffset][1] + (1.0 - weight) * 1
            #print "currentFloorX: %s, currentFloorY: %s" % (currentFloorX,currentFloorY)
            floorTexX = int(currentFloorX * texwidth) % texwidth
            floorTexY = int(currentFloorY * texheight) % texheight

            try:
                pix = self.floortexture.get_at((floorTexX,floorTexY))
            except:
                pix = (255,255,255)
            self.display.set_at((xoffset,yoffset),pix)
            yoffset += 1
            
        """

            #pass
        #return texture.subsurface((0,0,25,25))
        #return surf
        #print "You just called getcachedtexture!"
        pass
    def __init__(self, themap, gridsize, displaysurf, texturelist, floortexture,
                 ceilingtexture, camerapos, cameradir, FOV=60,cameradistance=None):
        self.map = themap
        self.gridsize = gridsize
        self.textures = texturelist
        self.flootexture = floortexture
        self.ceilingtexure = ceilingtexture
        self.camerapos = camerapos
        self.cameradir = cameradir
        
        self.display = displaysurf
        self.setDisplaySurface(self.display)
        self.FOV = FOV
        #self.FOVradians = math.radians(FOV)

        self.FPS = 0
        if not cameradistance:
            self.cameradistance = int(self.centerx / math.tan(math.radians(FOV / 2)))
        else:
            self.cameradistance = cameradistance

        #setup various caches to speed shit up
        #self.tancache = [math.tan(math.radians(x)) for x in range(360)]
        #self.coscache = [math.cos(math.radians(x)) for x in range(360)]
        #self.sincache = [math.sin(math.radians(x)) for x in range(360)]

        self.darkenvertical = True;
        #self.texturecache = []
        #for item in texturelist:
        #    self.texturecache.append([pygame.transform.scale(item,(self.gridsize,height)) for height in range(1,self.gridsize)])
       

    def setDisplaySurface(self, surface):
        """ setDisplaySurface (pygame.Surface new_surface) -> None """
        self.display = surface
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.centerx = self.width / 2
        self.centery = self.height / 2

    def ShowFPS(self, position, font, size): #size is font point size.
        """ MAKE THIS CALCULATE THE FPS!!!!"""
        self.display.blit(font.render(self.FPS,0,(255,255,255)),position)

    def _castDisplay(self):
        #plane = (320,200)
        #planecenter = (160,100)
        #planedist = (plane[0]/2) / math.tan(math.radians(FOV/2))
        rayincrement = self.FOV / float(self.width)
        rayangle = self.cameradir + self.FOV / 2 #will this cast invertedly?
        
        self.cameradir = self.cameradir % 360# is this necessary?
        
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
            correction = math.cos(math.radians(self.cameradir-rayangle))
            #if denom 
            if horizint and not vertint:
                coltype.append(0)
                distance = abs(self.camerapos[1]-horizint[1]) / abs(math.sin(rayrad)) * correction
                closestpoint = horizint

            elif vertint and not horizint:#this shouldnt cause a division by zero...
                coltype.append(1)
                distance = abs(self.camerapos[0]-vertint[0]) / abs(math.cos(rayrad)) * correction
                closestpoint = vertint
            elif vertint and horizint:
                horizdist = abs(self.camerapos[0]-horizint[0]) / abs(math.cos(rayrad)) * correction
                vertdist = abs(self.camerapos[0]-vertint[0]) / abs(math.cos(rayrad)) * correction


                if abs(horizdist) < abs(vertdist):
                    coltype.append(0)
                    closestpoint = horizint
                    distance = abs(horizdist)
                else:
                    coltype.append(1)
                    closestpoint = vertint
                    distance = abs(vertdist)

            #HERE we are assuming that they didn't make a map with holes in it,
            #because this would result in the closest point being infinity.

            #if closestpoint and (x == 0 or x == plane[0]-1):
            #if closestpoint:
                #drawray(surf,playerpos,closestpoint,[(closestpoint,2)])
            wallvalues.append(self.map[int(closestpoint[1]) / self.gridsize][int(closestpoint[0]) / self.gridsize])
            collisionlocation.append(closestpoint)
            scaling.append(distance)

        return (wallvalues,coltype,collisionlocation, scaling)
    
    def _castRay(self,rayangle):
        """ returns first horizontal & vertical intersections (or none for either or both)"""

        #todo: wrap angle values at 360? NO.
        #if rayangle >= 360:
        rayangle = rayangle % 360 #even wraps negative values correctly, (floats too i think)
        rayrad = math.radians(rayangle)
        #print rayangle
        horizint = None
        vertint = None
        
        #Horizontal intersections
        if rayangle < 180 and rayangle != 0 and rayangle != 90:#pointing up
            stepy = -self.gridsize
            pointy = (self.camerapos[1] / self.gridsize) * self.gridsize -.001
            stepx = self.gridsize/math.tan(rayrad)
        elif rayangle > 180 and rayangle != 270:#pointing down
            stepy = self.gridsize
            pointy = (self.camerapos[1] / self.gridsize) * self.gridsize + self.gridsize#i'm sure there's a better way to do this
            stepx = -(self.gridsize/math.tan(rayrad))

        elif rayangle == 90:        
            stepy = -self.gridsize
            pointy = (self.camerapos[1] / self.gridsize) * self.gridsize - .001#problem b/c of angle projection' makes walls stick out if angle of
            #ray is far off of FOV. may have something to do with not casting ray as integer or something?
            #fixed this way, anyway
            stepx = 0
            pointx = self.camerapos[0]
        elif rayangle == 270:
                    
            stepy = self.gridsize
            pointy = (self.camerapos[1] / self.gridsize) * self.gridsize + self.gridsize
            stepx = 0
            pointx = self.camerapos[0]

        else:
            pass#horizint will stay None

        if rayangle != 0 and rayangle != 180:
            if rayangle != 90 and rayangle != 270:
                #we have the y-coord of first intersection point to check
                #let's get the x coord (case: 90/270 pointx is just ray start b/c ray x-component = 0.)
                pointx = self.camerapos[0] + (self.camerapos[1] - pointy) / math.tan(rayrad)
                
            mapx = int(pointx)/self.gridsize
            mapy = int(pointy)/self.gridsize            
            while mapx >= 0 and mapx < len(self.map[0]) and mapy >= 0 and mapy < len(self.map):
                #should work for non-square maps, assuming rectangular
                if self.map[mapy][mapx]:#nonzero, therefore wall                    
                    horizint = (pointx,pointy)
                    break
                
                pointx += stepx
                pointy += stepy
                mapx = int(pointx)/self.gridsize
                mapy = int(pointy)/self.gridsize
        #------------------------------------

        #Vertical intersections
        if rayangle > 90 and rayangle < 270:#pointing left
            stepx = -self.gridsize
            pointx = (self.camerapos[0] / self.gridsize) * self.gridsize - .001
            stepy = self.gridsize * math.tan(rayrad)
        else:#pointing right
            stepx = self.gridsize
            pointx = (self.camerapos[0] / self.gridsize) * self.gridsize + self.gridsize#i'm sure there's a better way to do this
            stepy = -(self.gridsize*math.tan(rayrad))

        pointy = self.camerapos[1] + (self.camerapos[0] - pointx) * math.tan(rayrad)
        
        mapx = int(pointx)/self.gridsize
        mapy = int(pointy)/self.gridsize
        
        while mapx >= 0 and mapx < len(self.map[0]) and mapy >= 0 and mapy < len(self.map):
            #should work for non-square maps, assuming rectangular
            if self.map[mapy][mapx]:#nonzero, therefore wall
                vertint = (pointx,pointy)
                break
            pointx += stepx
            pointy += stepy
            mapx = int(pointx)/self.gridsize
            mapy = int(pointy)/self.gridsize
        return (horizint,vertint)




    def update(self):
        #WILL crash if no collision location ( == None)
        #print "running update now"
        wallvalues,collisiontype,collisionlocation, scaling = self._castDisplay()
        self.display.fill((20,20,190),(0,0,self.width,self.centery))
        self.display.fill((190,20,20),(0,self.centery,self.width,self.centery))
        #print self.cameradistance
        #print scaling[0]
        
        self.display.lock() 
        for x in range(self.width):
            if scaling[x]:
                sliceheight = int(self.gridsize / scaling[x] * self.cameradistance)
                #texture = pygame.transform.scale(textures[texturetype[x]-1],(sliceheight,sliceheight))
                self.display.lock()
                                                      
                if collisiontype[x]:#vertical collision
                    texturestrip = self._drawStripe(wallvalues,collisionlocation, x, sliceheight, scaling, True)
                    
                else:#horizontal collision
                    texturestrip = self._drawStripe(wallvalues,collisionlocation, x, sliceheight, scaling, False)
                    #sliceheight = min(sliceheight,self.gridsize)
                self.display.unlock()
                #sliceheight = min(sliceheight,self.height)
                #blitlocation = (x, self.centery - sliceheight / 2)
                #print blitlocation
                #self.display.blit(texturestrip,blitlocation)
                """
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
                """
        self.display.unlock()


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
    
def moveplayer(the_map,playerpos,movex, movey, playersize, gridsize):
    #checks that they don't move through a wall.  would be simple to implement a ray that is used to calculate
    #distance to closest wall on player's movement path and determine if they are walking through it;
    #currently this function merely checks for the dest square to see if it is occupied.
    #should be perfectly fine unless you plan on letting them move faster than gridsize.
    #DO THE ABOVE NOW, RETARD.
    destx = playerpos[0] + movex
    #if movex < 0:
    #    playersize = -playersize
        
    if int(destx/gridsize) < len(the_map[0]):
        if the_map[int(playerpos[1]/gridsize)][int((destx)/gridsize)]:
            destx = playerpos[0]
    else:
        destx = playerpos[0]
        
    
    desty = playerpos[1] + movey
        
    if int(desty/gridsize) < len(the_map):
        if the_map[int((desty)/gridsize)][int(playerpos[0]/gridsize)]:
            desty = playerpos[1]
    else:#keeps people from moving off map, probably
        desty = playerpos[1]
        

    """
    desty = playerpos[1] + move[1]
    """
    
    return [destx, desty]





screen = pygame.display.set_mode((320,240))
screen = screen.subsurface((0,20,320,200))
the_map = loadmap("the_map.txt")



playerpos = [300,300]
playerangle = 250
gridsize = 64
movespeed = 15
turnspeed = 6
texturelist = ["redbrick","eagle","purplestone","mossy","greystone"]
floortexturelist = ["bluestone","colorstone","wood"]
texturelist = [pygame.image.load('textures/'+s+'.bmp').convert() for s in texturelist]
floortexturelist = [pygame.image.load('textures/'+s+'.bmp').convert() for s in floortexturelist]
import keymap
print keymap.action


raycaster = Raycaster(the_map, gridsize, screen, texturelist, floortexturelist[0],
                 floortexturelist[1], playerpos, playerangle)
while 1:
    pygame.display.update()
    raycaster.update()
    raycaster.camerapos = playerpos
    raycaster.cameradir = playerangle

    if keymap.actionstatus['rotateright']: playerangle -= turnspeed
    if keymap.actionstatus['rotateleft']: playerangle += turnspeed
    movex,movey = 0,0
    if keymap.actionstatus['moveforward']:
        movex += int(math.cos(math.radians(playerangle)) * movespeed)
        movey -= int(math.sin(math.radians(playerangle)) * movespeed)
    if keymap.actionstatus['movebackward']:
        movex -= int(math.cos(math.radians(playerangle)) * movespeed)
        movey += int(math.sin(math.radians(playerangle)) * movespeed)
        
    if keymap.actionstatus['strafeleft']:
        movex -= int(math.cos(math.radians(playerangle-90)) * movespeed)
        movey += int(math.sin(math.radians(playerangle-90)) * movespeed)
    
    if keymap.actionstatus['straferight']:
        movex -= int(math.cos(math.radians(playerangle+90)) * movespeed)
        movey += int(math.sin(math.radians(playerangle+90)) * movespeed)
    playerpos = moveplayer(the_map, playerpos, movex,movey, 0,gridsize)
    #screen.fill((0,0,0))
    #drawmap(screen,the_map,gridsize)
    #drawplayer(screen,playerpos)
    #texturetype, collisioninfo, scaling = castmap(the_map, playerpos,playerangle,gridsize,screen)
    #castdisplay(screen, offset, [loadimg('wall.bmp')], texturetype, collisioninfo, scaling)
    
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
            
            
