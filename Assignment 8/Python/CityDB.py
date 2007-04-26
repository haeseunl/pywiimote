class BinTree(object):
    def __init__(self):
        self.data = 0
        self.left = None
        self.right = None
        self.isleaf = True
    def setdata(self,data):
        self.data = data
    def setleft(self,left):
        self.left=left
    def setright(self,right):
        self.right=right
    def __str__(self):
        if self.data:
            return str(self.data.citycode)
        return ""
    
    
class CityRecord(object):
    def __init__(self, a,b,c):
        self.citycode = a
        self.x = b
        self.y = c
    def __str__(self):
        return "City Code: %s, X,Y: (%s,%s)" % (self.citycode,self.x,self.y)
    def xyIdentical(self, x,y):
        if self.x == x and self.y == y:
            return True
        return False

class CityDB(object):
    def __init__(self):
        self.rootptr = None

    def search(self,rootptr, item1,item2=None):
        if rootptr == None:
            return False
        if item2: #city coords
            if rootptr.data.xyIdentical(item1,item2):
                return True
        else:
            if rootptr.data.citycode == item1:
                return True
        if self.search(rootptr.left,item1,item2):
            return True
        if self.search(rootptr.right,item1,item2):
            return True
        return False

    
    def insert(self,cityRecord):
        if self.rootptr == None:
            self.rootptr = BinTree()
            self.rootptr.data = cityRecord
        else:
            self.insertRecursive(cityRecord,self.rootptr)
            
    def insertRecursive(self,cityRecord,rootptr):
        if rootptr == 0: #this should never happen.
            raise OSError
        if cityRecord.citycode <= rootptr.data.citycode:
            if rootptr.left == None:
                rootptr.left = BinTree()
                rootptr.left.data = cityRecord
                rootptr.isleaf = False
            else:
                self.insertRecursive(cityRecord,rootptr.left)
        else:
            if rootptr.right == None:
                rootptr.right = BinTree()
                rootptr.right.data = cityRecord
                rootptr.isleaf = False
            else:
                self.insertRecursive(cityRecord,rootptr.right)

    def remove(rootptr, city):
        if rootptr.data == city:
            
        pass
    def remove_max(

    def __str__(self):
        self.printData(self.rootptr)
        #self.printNode(self.rootptr,0)
        return ""
    def __repr__(self):
        return self.__str__()
    def printData(self,root):
        if root.left != None:
            self.printData(root.left)
        print root.data
        if root.right != None:
            self.printData(root.right)
        

    def printTree(self,root,level):
        if root.right != None:
            self.printTree(root.right,level+1)
        print " "*level*4+str(root) + "  "
        if root.left != None:
            self.printTree(root.left,level+1)



y = CityDB()
tmp = [[5000, (5067, 765)],
[1700, (1789, 7981)],
[1800, (1890, 8091)],
[2000, (2012, 212)],
[1900, (1901, 9101)],
[3000, (3012, 213)],
[8000, (8012, 218)],
[7500, (7567, 5767)],
[7600, (7678, 6877)],
[2500, (2567, 5762)],
[7800, (7890, 8097)],
[7700, (7789, 7987)],
[1500, (1567, 5761)],
[9000, (9012, 219)]]
for item in tmp:
    x = CityRecord(item[0], item[1][0],item[1][1])
    y.insert(x)
#print y
while 1:
    print y
    #print y.search(y.rootptr,int(raw_input("item1? ")),int(raw_input("item 2? ")))
    print y.remove(y.rootptr,int(raw_input("city code? ")))


