#TODO: instead of opening a KERNEL write in the functions, allow the user to pass
# an instance with a write() method.  THis way it'll be easy to debug (just pass in a screen-printing class'
#write method) as well as making it easier to make portable.  also it potentially provides an alternative
# (using HID report writing so that people with the XP stack will be okay)

#error types
class AccessDeniedError(Exception): pass
class PathNotFoundError(Exception): pass
class UnknownHandleError(Exception): pass

from ctypes import *

kernel = windll.kernel32
hid = windll.hid
setupapi = windll.setupapi

#define setupapi flags used
DIGCF_DEFAULT           = 0x00000001  # only valid with DIGCF_DEVICEINTERFACE
DIGCF_PRESENT           = 0x00000002#we care about this one
#DIGCF_ALLCLASSES        = 0x00000004
#DIGCF_PROFILE           = 0x00000008
DIGCF_DEVICEINTERFACE   = 0x00000010#and this one



#from winnt.h
#define GENERIC_READ                     (0x80000000L)
#define GENERIC_WRITE                    (0x40000000L)
#define GENERIC_EXECUTE                  (0x20000000L)
#define GENERIC_ALL                      (0x10000000L)
#define FILE_SHARE_READ                 0x00000001  
#define FILE_SHARE_WRITE                0x00000002  
#define FILE_SHARE_DELETE               0x00000004
#define FILE_FLAG_WRITE_THROUGH         0x80000000
#define FILE_FLAG_OVERLAPPED            0x40000000
#define FILE_FLAG_NO_BUFFERING          0x20000000
#define FILE_FLAG_RANDOM_ACCESS         0x10000000
#define FILE_FLAG_SEQUENTIAL_SCAN       0x08000000
#define FILE_FLAG_DELETE_ON_CLOSE       0x04000000
#define FILE_FLAG_BACKUP_SEMANTICS      0x02000000
#define FILE_FLAG_POSIX_SEMANTICS       0x01000000
#define FILE_FLAG_OPEN_REPARSE_POINT    0x00200000
#define FILE_FLAG_OPEN_NO_RECALL        0x00100000
#define FILE_FLAG_FIRST_PIPE_INSTANCE   0x00080000
#define CREATE_NEW          1
#define CREATE_ALWAYS       2
#define OPEN_EXISTING       3
#define OPEN_ALWAYS         4
#define TRUNCATE_EXISTING   5

#The ones we actually use:
GENERIC_READ = 0x80000000L
GENERIC_WRITE = 0x40000000L
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 0x000000003
FILE_FLAG_OVERLAPPED = 0x40000000
ERROR_ACCESS_DENIED = 5
ERROR_PATH_NOT_FOUND = 3

class GUID(Structure):
    _fields_ = [('Data1',c_ulong), ('Data2',c_ushort),
    ('Data3',c_ushort), ('Data4',c_ubyte*8)]
    def __repr__(self):
        out = '{'
        out += hex(self.Data1)[2:-1].zfill(8)
        out += '-'
        out += hex(self.Data2)[2:].zfill(4)
        out += '-'
        out += hex(self.Data3)[2:].zfill(4)
        out += '-'
        out += hex(self.Data4[0])[2:].zfill(1)
        out += hex(self.Data4[1])[2:].zfill(1)
        out += '-'
        items = [hex(self.Data4[x])[2:].zfill(1) for x in range(2,8)]
        for item in items:
            out += item
        out += '}'
        return out
class DeviceInterfaceData(Structure):
    _fields_ = [('cbSize',c_ulong), ('InterfaceClassGuid',GUID),('Flags',c_ulong),('Reserved',POINTER(c_ulong))]
    def __repr__(self):
        out = ''
        out += 'cBsize: ' + str(self.cbSize) + '\n'
        out += 'Interface Class: ' + repr(self.InterfaceClassGuid) + '\n'
        out += 'Flags: ' + repr(self.Flags) + '\n'
        out += 'Reserved: '+ repr(self.Reserved) + '\n'
        return out

#the following classes are defined so that we can create an OVERLAPPED structure.
class struct(Structure):
    _fields_ = [("Offset",c_ulong),("OffsetHigh",c_ulong)]
class union(Union):
    _fields_ = [("",struct),("Pointer",c_void_p)]
class OVERLAPPED(Structure):
    _fields_ = [("Internal",POINTER(c_ulong)), ("Internal_High",POINTER(c_ulong)),("",union),("hEvent",c_void_p)]



class HIDDevice(object):
    def __init__(self):
        pass
    
    def OpenDevice(self, index):
        guid = GUID()
        hid.HidD_GetHidGuid(byref(guid))
        setupapi.SetupDiGetClassDevsA.restype = c_void_p
        #classdevices = c_void_p(setupapi.SetupDiGetClassDevsA(byref(guid),None,None,(DIGCF_PRESENT|DIGCF_DEVICEINTERFACE)))
        classdevices = setupapi.SetupDiGetClassDevsA(byref(guid),None,None,(DIGCF_PRESENT|DIGCF_DEVICEINTERFACE))

        #setupapi.SetupDiGetClassDevsA(byref(guid),None,None,(DIGCF_PRESENT|DIGCF_DEVICEINTERFACE))

        deviceinterfacedata = DeviceInterfaceData()

        deviceinterfacedata.cbSize = sizeof(deviceinterfacedata)#16+4+4+4
        deviceinterfacedata.InterfaceClassGuid = guid
        deviceinterfacedata.Flags = 0
        deviceinterfacedata.Reserved = None

        device = setupapi.SetupDiEnumDeviceInterfaces(classdevices,None,byref(guid),index,byref(deviceinterfacedata))
        buflen = c_ulong()
        setupapi.SetupDiGetDeviceInterfaceDetailA(classdevices,byref(deviceinterfacedata),None,0,byref(buflen),0)

        class DeviceInterfaceDetailData(Structure):
            _fields_ = [('cbSize',c_ulong), ('DevicePath',c_char * (buflen.value+1))]
        device = setupapi.SetupDiEnumDeviceInterfaces(classdevices,None,byref(guid),index,byref(deviceinterfacedata))
        detail = DeviceInterfaceDetailData()
        detail.cbSize = sizeof(c_ulong)+1 # Size of cbSize itself plus size of a null string.
        setupapi.SetupDiGetDeviceInterfaceDetailA(classdevices,byref(deviceinterfacedata),byref(detail),buflen,None,None)

        if setupapi.SetupDiDestroyDeviceInfoList(classdevices):
            pass
            #return detail.DevicePath
        else:
            print "Unable to delete device list."
            raise OSError


        kernel.CreateFileA.restype = c_void_p
        #devicepath = '\\\\.\\' + devicepath[4:]
    
        #tmp = create_string_buffer(devicepath)#,len(devicepath)+1)
        #tmp[-1] = '\0'
        #print "The device's address is: " + devicepath
        #devicepath = '\\\\.\\' + devicepath[4:]
        handle = kernel.CreateFileA(detail.DevicePath,GENERIC_READ | GENERIC_WRITE,
                                FILE_SHARE_READ | FILE_SHARE_WRITE, None,
                                OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
        #print kernel.GetLastError()
        if handle == -1:
            error = kernel.GetLastError() 
            if error == ERROR_ACCESS_DENIED:
                raise AccessDeniedError
            elif error == ERROR_PATH_NOT_FOUND:
                raise PathNotFoundError
            else:
                raise UnknownHandleError# we should give people some way of accessing the error code in this case.
            
            kernel.CloseHandle(handle)
            #return error
        #else:
            #print "THE ADDRESS OF THE DEVICE'S INPUT STREAM IS: "+str(self.handle)
        #pass
        kernel.CreateEventA.restype = c_void_p
        event = kernel.CreateEventA(None, True, True, "")
        overlapped = OVERLAPPED()
	overlapped.Offset = 0
	overlapped.OffsetHigh = 0
	overlapped.hEvent = event
	
        return (handle, overlapped)


    def Connect(self, handle):
        class HidAttributes(Structure):
            _fields_ = [('Size',c_ulong),('VendorID',c_ushort),('ProductID',c_ushort),('VersionNumber',c_ushort)]

        attrib = HidAttributes()
        attrib.Size = sizeof(attrib)
        hid.HidD_GetAttributes(handle,byref(attrib))# add a try here
        return attrib
        #print "|VendorID: %s, Product ID: %s, Version: %s" % (attrib.VendorID, attrib.ProductID, attrib.VersionNumber)


    def Disconnect(self, handle):
        #if self.connected:
        if kernel.CloseHandleA(handle):# and kernel.CloseHandleA(self.event):
            #self.connected = False
            return True
        return False

    def Write(self, handle, data):
        """ data should be a pointer to a ctypes byte array."""
        temp = c_byte * len(data)
        temp = temp()
        #temp.value = data
        #print temp
        #print "The data is: "
        #print data
        #print "Here is each item individually"
        for x,item in enumerate(temp):
            #print data[x]
            temp[x] = data[x]
        #print type(temp)

        hid.HidD_SetOutputReport(handle, temp, len(data))

    def Read(self, handle, overlapped, timeout=1000,bufsize=0xff):
        temp = c_byte * bufsize
        temp = temp()
        bytes_read = c_int(10)
        #print type(overlapped)
        kernel.ReadFile(handle, byref(temp),bufsize,byref(bytes_read),byref(overlapped))
        result = kernel.WaitForSingleObject(overlapped.hEvent, timeout)
        #print overlapped
        print "Number of bytes read: "+ str(bytes_read.value)
        print "Buffer: ", temp[0], temp[1], temp[2], temp[3], temp[4]
        print "Result: ", result
        if result == 0:#WAIT_OBJECT_0 which is STATUS_WAIT_0 (which is 0) + 0
            kernel.ResetEvent(overlapped.hEvent)
            return temp
        print "Read Timed Out"
        #something unexpected happened (implicit else)
        kernel.CancelIo(handle)
        kernel.ResetEvent(overlapped.hEvent)

