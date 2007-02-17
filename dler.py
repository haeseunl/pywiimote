import urllib2
from time import sleep
filename = "ep012"

u = urllib2.urlopen('http://www.putfile.com/downloadfile/'+filename,{'Referer':'http://www.something.com/'})
file('tempfilefirstpage.html','w').write(u.read())
u.close()
for x in range (20):
    sleep(8)
    target = 'http://www.putfile.com/downloadfile/'+filename+'/'+str(x+1)
    print "RETREIVING "+target
    if x == 0:
        u = urllib.urlopen(target, {'Referer':'http://www.putfile.com/downloadfile/'+filename})
    else:
        u = urllib.urlopen(target, {'Referer':'http://www.putfile.com/downloadfile/'+filename+str(x)})
    file('tempfile'+str(x+1)+'.html','w').write(u.read())
    u.close()
