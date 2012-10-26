#!/usr/bin/python

import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import getopt
import sys
try:
    from configobj import ConfigObj
except:
    print "WARNING: no configuration is being saved"
    print "  - install the configobj python module to fix this."
    print "  - in fedora: su -c \"yum install python-configobj\""
    print

import os
import random

NM_DBUS_INTERFACE_DEVICES = "org.freedesktop.NetworkManager.Devices"
NM_DBUS_SERVICE = "org.freedesktop.NetworkManager"
NM_DBUS_INTERFACE = "org.freedesktop.NetworkManager"
NM_DBUS_PATH = "/org/freedesktop/NetworkManager"

NM_DBUS_PATH_VPN = "/org/freedesktop/NetworkManager/VPNConnections"
NM_DBUS_INTERFACE_VPN = "org.freedesktop.NetworkManager.VPNConnections"

#TODO: vpn, daemon, security (wpa, leap), test devices, dialup

#bus = dbus.SystemBus()
#nm = bus.get_object(NM_DBUS_SERVICE, NM_DBUS_PATH_VPN)
#a= nm.getVPNConnections()
#print a
#p= nm.getVPNConnectionProperties(a[0])
#print p[2], p[0]
#exit()


CHANNELS = {    #based on `wlist channels`
2.412:   1,
2.417:   2,
2.422:   3,
2.427:   4,
2.432:   5,
2.437:   6,
2.442:   7,
2.447:   8,
2.452:   9,
2.457:  10,
2.462:  11,

5.18:   36,
5.2:    40,
5.22:   44,
5.24:   48,
5.26:   52,
5.28:   56,
5.3:    60,
5.32:   64,

5.745: 149,
5.765: 153,
5.785: 157,
5.805: 161,
5.825: 165
}

#Types of NetworkManager devices
DEVICE_TYPE_UNKNOWN = 0
DEVICE_TYPE_802_3_ETHERNET = 1
DEVICE_TYPE_802_11_WIRELESS = 2

#Types of NetworkManager states

NM_STATE_UNKNOWN = 0
NM_STATE_ASLEEP = 1
NM_STATE_CONNECTING = 2
NM_STATE_CONNECTED = 3
NM_STATE_DISCONNECTED = 4


#Types of NetworkManager device states

NM_DEVICE_STATE_UNKNOWN = 0
NM_DEVICE_STATE_DOWN = 1
NM_DEVICE_STATE_DISCONNECTED = 2
NM_DEVICE_STATE_PREPARE = 3
NM_DEVICE_STATE_CONFIG = 4
NM_DEVICE_STATE_NEED_AUTH = 5
NM_DEVICE_STATE_IP_CONFIG = 6
NM_DEVICE_STATE_ACTIVATED = 7
NM_DEVICE_STATE_FAILED = 8
NM_DEVICE_STATE_CANCELLED = 9


#NM-supported Authentication Methods

NM_AUTH_TYPE_WPA_PSK_AUTO = 0x00000000
NM_AUTH_TYPE_NONE         = 0x00000001
NM_AUTH_TYPE_WEP40        = 0x00000002
NM_AUTH_TYPE_WPA_PSK_TKIP = 0x00000004
NM_AUTH_TYPE_WPA_PSK_CCMP = 0x00000008
NM_AUTH_TYPE_WEP104       = 0x00000010
NM_AUTH_TYPE_WPA_EAP      = 0x00000020
NM_AUTH_TYPE_LEAP         = 0x00000040


#General device capability bits

NM_DEVICE_CAP_NONE              = 0x00000000
NM_DEVICE_CAP_NM_SUPPORTED      = 0x00000001
NM_DEVICE_CAP_CARRIER_DETECT    = 0x00000002
NM_DEVICE_CAP_WIRELESS_SCAN     = 0x00000004

# 802.11 wireless-specific device capability bits
NM_802_11_CAP_NONE              = 0x00000000
NM_802_11_CAP_PROTO_NONE        = 0x00000001
NM_802_11_CAP_PROTO_WEP         = 0x00000002
NM_802_11_CAP_PROTO_WPA         = 0x00000004
NM_802_11_CAP_PROTO_WPA2        = 0x00000008
NM_802_11_CAP_RESERVED1         = 0x00000010
NM_802_11_CAP_RESERVED2         = 0x00000020
NM_802_11_CAP_KEY_MGMT_PSK      = 0x00000040
NM_802_11_CAP_KEY_MGMT_802_1X   = 0x00000080
NM_802_11_CAP_RESERVED3         = 0x00000100
NM_802_11_CAP_RESERVED4         = 0x00000200
NM_802_11_CAP_RESERVED5         = 0x00000400
NM_802_11_CAP_RESERVED6         = 0x00000800
NM_802_11_CAP_CIPHER_WEP40      = 0x00001000
NM_802_11_CAP_CIPHER_WEP104     = 0x00002000
NM_802_11_CAP_CIPHER_TKIP       = 0x00004000
NM_802_11_CAP_CIPHER_CCMP       = 0x00008000


IW_AUTH_ALG_OPEN_SYSTEM = 0x1
IW_AUTH_ALG_SHARED_KEY = 0x2
IW_AUTH_ALG_LEAP = 0x4

class NMCLI:
    # Network device activated
    def nm_device_active_cb(self,path,*args,**kwds):
        print "%s is now active" % path
        self.get_devices()

    # Network device deactivated
    def nm_device_notactive_cb(self,path):
        print "%s in no longer active" % path
        self.get_devices()

    # Network device activating
    def nm_device_activating_cb(self,path):
        print "%s is about to become active" % path
        self.get_devices()

    # Network devices changed
    def nm_devices_changed_cb(self,path):
        #TODO: check self._devices to see if the device was added or removed
        print "%s has been added or removed" % path
        self.get_devices()

    def __init__(self):

        #setup dbus connection stuff to nm manager, and get a list of devices (and networks)
        self.bus = dbus.SystemBus()
        self.nm = self.bus.get_object(NM_DBUS_SERVICE, NM_DBUS_PATH)

        self.bus.add_signal_receiver(handler_function=self.nm_device_active_cb,
                signal_name="DeviceNowActive", path=NM_DBUS_PATH, dbus_interface=NM_DBUS_INTERFACE)
        self.bus.add_signal_receiver(handler_function=self.nm_device_notactive_cb,
                signal_name="DeviceNoLongerActive", path=NM_DBUS_PATH, dbus_interface=NM_DBUS_INTERFACE)
        self.bus.add_signal_receiver(handler_function=self.nm_device_activating_cb,
                signal_name="DeviceActivating", path=NM_DBUS_PATH, dbus_interface=NM_DBUS_INTERFACE)
        self.bus.add_signal_receiver(handler_function=self.nm_devices_changed_cb,
                signal_name="DevicesChanged", path=NM_DBUS_PATH, dbus_interface=NM_DBUS_INTERFACE)

        self.get_devices()

        self._device = None
        self._verbose = False
        self._networks = False
        self._essid = None
        self._wep_open = False
        self._key = None
        self._daemon = False
        self._create = False
        self._list = False
        self._set = False
        self._boot = False

        for a in sys.argv[1:]:
            if a in self.__devices:
                self._device = a

            elif a in self.__hw_devices:
                self._device = self.__hw_devices[a]

            elif a in self.__networks:
                self._essid = a

            elif a in self.__hw_networks:
                self._essid = self.__hw_networks[a]

            elif a[:2] == '-n':
                self._essid = a[2:]

            elif a in ('help','-h','--help'):
                self.usage()
                sys.exit()

            elif a in ('daemon','-d','--daemon'):
                self._daemon = True

            elif a in ('open','-o','--open'):
                self._wep_open = True

            elif a in ('shared','--shared'):
                self._wep_open = False

            elif len(a) == 10 or len(a) == 26:
                try:
                    int(a, 16)  # a hex number of 104 or 40 bits... hmmm maybe a wep key
                    self._key = a
                except:
                    pass

            elif a in ('sleep','--sleep'):
                self.sleep()

            elif a in ('wake','--wake'):
                self.wake()

            elif a in ('verbose','--verbose','-v'):
                self._verbose = True

            elif a in ('set','--set','use','--use'):
                self._set = True

            elif a in ('start','boot'):
                self._boot = True

            elif a[:6] == '--key=':
                self._key = a[6:]
            elif a[:2] == '-k':
                self._key = a[2:]
                if self._key == "":
                    pass    #TODO: get the next item? so -k KEY works... not just -kKEY

        if self._boot:  #check to see if we are connected, and if not, try
            pass

        if self._essid and not self._key:

            hw_address = None

            for dev in self.devices:
                if self.devices[dev].has_key('networks'):
                    for net in self.devices[dev]['networks']:
                        if net['name'] == self._essid:
                            hw_address = net['hwaddress']

            try:
                if hw_address:
                    self._key = config[hw_address]['key']
                    self._wep_open = bool(config[hw_address]['open'])

                else:
                    for hwa in config:
                        if config[hwa]['name'] == self._essid:
                            self._key = config[hwa]['key']
                            self._wep_open = bool(config[hwa]['open'])
            except:
                pass

        if self._key:
            hw_address = str(random.randint(1,1000000))    #in case there is no hardware...

            for dev in self.devices:
                if self.devices[dev].has_key('networks'):
                    for net in self.devices[dev]['networks']:
                        if net['name'] == self._essid:
                            hw_address = net['hwaddress']

            try:
                config[hw_address] = {}
                config[hw_address]['name'] = self._essid
                config[hw_address]['key'] = self._key
                config[hw_address]['open'] = str(self._wep_open)
            except:
                pass

            self.set_wep_interface(self._device, self._essid, self._key, self._wep_open)

        elif self._set:
            if self._essid:
                self.set_interface(self._device, self._essid)
            else:
                self.set_interface(self._device)

        elif self._create:
            self.create_wireless_network(self._device, self._essid)

        elif self._list:
            self.print_list()

        elif self._networks:
            self.print_networks()

        elif self._device:
            self.print_device(self._device)

        else:
            self._networks = True   #eh, might as well...
            self.print_list()       #no commmand arguments entered, just list devices

        if self._daemon:
            loop = gobject.MainLoop()
            loop.run()

    """
    Lists out each device using print_device
    """
    def print_list(self):
        for iface_name in self.devices:
            self.print_device(iface_name)

    """
    Prints out information about a device based on
    the interface's name (i.e. eth0)
    """
    def print_device(self, name):

        device = self.devices[name]

        if device['active']:
            active = '*'
        else:
            active = ' '
        if self._verbose:
            print "%6s%c   NM Path:           %s" % (name, active, device['path'])
            print "          HW Address:        %s" % device['hwaddress']
        else:
            print "%6s%c   HW Address:        %s" % (name, active, device['hwaddress'])

        state = self.get_device_state_string(name)
        if state:
            print "          Status:            %s" % state

        if device["type"] == DEVICE_TYPE_802_3_ETHERNET:
            print "          Type:              Wired"
        elif device["type"] == DEVICE_TYPE_802_11_WIRELESS:
            print "          Type:              802.11 Wireless"

        if self._verbose:
            print "          Driver:            %s" % device['driver']

        if device['active']:
            print "          IP Address:        %s" % device['address']

            if self._verbose:

                print "          Netmask:           %s" % device['subnetmask']
                print "          Broadcast:         %s" % device['broadcast']
                print "          Gateway:           %s" % device['route']
                print "          Primary DNS:       %s" % device['primary_dns']
                print "          Secondary DNS:     %s" % device['secondary_dns']

        if self._verbose:
            print "          Capabilities:"
            self.print_capabilities(name)

        if self._networks:
            self.print_networks(name)

        print

    """
    Print out a listing of capabilities
    """
    def print_capabilities(self, name):

        cap = self.devices[name]['capabilities']

        if cap & NM_DEVICE_CAP_NONE:
            print "            No Capabilities"

        if cap & NM_DEVICE_CAP_NM_SUPPORTED:
            print "            Supported"

        if cap & NM_DEVICE_CAP_CARRIER_DETECT:
            print "            Carrier Detect"

        if cap & NM_DEVICE_CAP_WIRELESS_SCAN:
            print "            Wireless Scan"

#	if (nm_access_point_is_encrypted (ap))
#		g_string_append (str, ", Encrypted: ");
        print "           Encrypted: ",
        if cap & NM_802_11_CAP_PROTO_WEP:
            print "WEP",
        if cap & NM_802_11_CAP_PROTO_WPA:
            print "WPA",
        if cap & NM_802_11_CAP_PROTO_WPA2:
            print "WPA2",
        if cap & NM_802_11_CAP_KEY_MGMT_802_1X:
            print "Enterprise",
        print
#	if (capabilities & NM_802_11_CAP_PROTO_WEP)
#		g_string_append (str, " WEP");
#	if (capabilities & NM_802_11_CAP_PROTO_WPA)
#		g_string_append (str, " WPA");
#	if (capabilities & NM_802_11_CAP_PROTO_WPA2)
#		g_string_append (str, " WPA2");
#	if (capabilities & NM_802_11_CAP_KEY_MGMT_802_1X)
#		g_string_append (str, " Enterprise");

    """
    print out a list of networks detected from a device, or all.
    """
    def print_networks(self, name=None):
        if name:

            device = self.devices[name]

            if device.has_key('networks'):

                print "          Networks:"

                for net in device['networks']:
                    #net['name']
                    active = ' '
                    if net['active']:
                        active = '*'
                    print "       %17s%s  chan%3s   freq%6s Ghz  strength%3s%%  rate %d Mb/s" % \
                        (net['name'], active, net['channel'], net['frequency'], net['strength'], net['rate']/1024)
                print

        else:
            print "Networks:"
            for iface in self.devices:

                device = self.devices[iface]

                if device.has_key('networks'):
                    print '',iface,'-'
                    for net in device['networks']:
                        net['name']
                        print " %17s:  chan%3s  freq%6s Ghz  strength %3s%%  rate %d Mb/s" % \
                            (net['name'], net['channel'], net['frequency'], net['strength'], net['rate']/1024)
            print

    """
    The command line usage printout
    """
    def usage(self):
        print
        print "  nm-cli [options]"
        print
        print "  options:"
        print "   -h       This help menu"
        print "   -l       List device(s) info"
        print "   -n       List networks"
        print "   -ddev    use device 'dev'"
#        print "   -D       daemonize"
        print "   -a       activate use device/network"
        print "   -eessid  use network name 'essid'"
        print "   -s       put NetworkManager to sleep"
        print "   -w       wake NetworkManager up"
        print "   -kkey    use network key 'key' (WEP shared default)"
        print "   -o       use open WEP key"
        print "   -v       verbose info"
        print "   -V       version info"
#        print "   -cconf   store network keys to 'conf' (unencryped)" #perhaps a place to store network keys (until nm 0.7 has universal conf)
        print "   -m       make an ad-hoc network"
#        print "   -t       create a test device"
        print

    """
    Print out version info
    """
    def version(self):
        print
        print "  nm-cli - version 0.1"
        print
        print "    built for NetworkManager 0.6.5 dbus interface"
        print "    created by Robert Frank (admin@bobfrank.org)"
        print

    """
    Get the device state as a string
    """
    def get_device_state_string(self, name):

        status = self.devices[name]["act_stage"]

        state = False
        if status == NM_DEVICE_STATE_UNKNOWN:
            state = "Unknown"

        elif status == NM_DEVICE_STATE_DOWN:
            state = "Down"

        elif status == NM_DEVICE_STATE_DISCONNECTED:
            state = "Disconnected"

        elif status == NM_DEVICE_STATE_PREPARE:
            state = "Prepare"

        elif status == NM_DEVICE_STATE_CONFIG:
            state = "Config"

        elif status == NM_DEVICE_STATE_NEED_AUTH:
            state = "Need Auth"

        elif status == NM_DEVICE_STATE_IP_CONFIG:
            state = "IP Config"

        elif status == NM_DEVICE_STATE_ACTIVATED:
            state = "Activated"

        elif status == NM_DEVICE_STATE_FAILED:
            state = "Failed"

        elif status == NM_DEVICE_STATE_CANCELLED:
            state = "Cancelled"

        return state     

    """
    Get NetworkManager state as a string
    """
    def get_state_string(self):
        status = self.nm.state()
        state = False
        if status == NM_STATE_UNKNOWN:
            state = "Unknown"

        if status == NM_STATE_ASLEEP:
            state = "Sleeping"

        if status == NM_STATE_CONNECTING:
            state = "Connecting"

        if status == NM_STATE_CONNECTED:
            state = "Connected"

        if status == NM_STATE_DISCONNECTED:
            state = "Disconnected"

        return state

    """
    Tell NetworkManager which network to use, and what wep parameters
    """
    def set_wep_interface(self, iface="eth0", essid="", key="", open=True):
        try:
            device = self.devices[iface]

        except KeyError:
            print "Unknown device %s" % iface
            return

        if open:
            alg = IW_AUTH_ALG_OPEN_SYSTEM
        else:
            alg = IW_AUTH_ALG_SHARED_KEY

        if len(key) == 26:  #26 characters long...
            wep_type = NM_AUTH_TYPE_WEP104
        else:               #10 characters long...
            wep_type = NM_AUTH_TYPE_WEP40

        self.nm.setActiveDevice(device['path'], essid, wep_type, key, alg)

    """
    Tell NetworkManager to go into offline mode mode
    """
    def sleep(self):
        self.nm.sleep(ignore_reply=True)

    """
    Tell NetworkManager to come back from offline mode
    """
    def wake(self):
        self.nm.wake(ignore_reply=True)

    """
    Tell NetworkManager to create an ad-hoc wireless network
    """
    def create_wireless_network(self, iface, essid):
        print iface, essid, self.devices[iface]['path']
        self.nm.createWirelessNetwork(self.devices[iface]['path'], essid)

    """
    Tell NetworkManager to enable or disable all wireless devices
    """
    def enable_wireless(self, enabled):
        self.nm.setWirelessEnabled(enabled, ignore_reply=True)

    """
    Similar to selecting a device and network on the systray,
    this function tells NetworkManager to try to get that network
    """
    def set_interface(self, iface, essid=None):
        try:
            #self.get_devices()  #get/update devices

            device = self.devices[iface]

            if device['type'] == DEVICE_TYPE_802_11_WIRELESS:
                yay = False
                if device.has_key('networks'):
                    for net in device['networks']:
                        if net['name'] == essid:
                            yay = True
                            break
                    if yay:
                        self.nm.setActiveDevice(device['path'], essid)
                    else:
                        print "Error: invalid network essid %s" % essid
            else:
                self.nm.setActiveDevice(device['path'])

        except KeyError,e:

            print "Error: invalid device %s" % iface

    """
    Sets up a list of devices in self.devices, and
    if there are already devices, then it updates the list
    """
    def get_devices(self):

        devices = self.nm.getDevices(dbus_interface=NM_DBUS_INTERFACE_DEVICES)

        self.devices = {}

        self.__devices = []
        self.__networks = []

        self.__hw_devices = {}
        self.__hw_networks = {}

        for device in devices:
            dev = self.bus.get_object(NM_DBUS_SERVICE, device)
            do = {}

            do['path'] = device
            do['name'] = str(dev.getName())
            do['type'] = int(dev.getType())
            #do['address'] = int(dev.getIP4Address())
            do['active'] = bool(dev.getLinkActive())
            do['hwaddress'] = str(dev.getHWAddress())
            do['capabilities'] = dev.getCapabilities()
            do['driver'] = str(dev.getDriver())

            props = dev.getProperties()     #look at the source of networkmanager for the order...
            do['udi'] = str(props[3])
            do['act_stage'] = int(props[5])  #device status
            #print props[5]
            do['address'] = str(props[6])    #used instead of above, because its already string format
            do['subnetmask'] = str(props[7])
            do['broadcast'] = str(props[8])
            do['route'] = str(props[10])
            do['primary_dns'] = str(props[11])
            do['secondary_dns'] = str(props[12])

            #print do

            if do['type'] == DEVICE_TYPE_802_11_WIRELESS:

                #print "mode:",dev.getMode()

                do['active_network'] = ''
                try:
                    if do['active']:
                        do['active_network'] = str(dev.getActiveNetwork())
                except:
                    pass

                do['networks'] = []
                try:
                    networks = dev.getNetworks()
                except:
                    #there are no networks...
                    continue

                for network in networks:
                    net = self.bus.get_object(NM_DBUS_SERVICE, network)
                    #print net.getProperties()

                    no = {}
                    no['name'] = str(net.getName())
                    props = net.getProperties()  #check nm for order (and what we get...)
                    no['hwaddress'] = str(props[2])
                    no['strength'] = int(net.getStrength())
                    no['frequency'] = 0
                    try:
                        no['frequency'] = int(net.getFrequency())/1000000000.0
                        no['channel'] = CHANNELS[ no['frequency'] ]
                    except:
                        no['channel'] = -1
                    no['rate'] = int(net.getRate())
                    no['encrypted'] = bool(net.getEncrypted())

                    do['networks'].append(no)
                    if network == do['active_network']:
                        no['active'] = True
                        do['active_network'] = no
                    else:
                        no['active'] = False
                    self.__hw_networks[ no['hwaddress'] ] = no['name']
                    self.__networks.append( no['name'] )

            self.devices[ do['name'] ] = do
            self.__devices.append( do['name'] )
            self.__hw_devices[ do['hwaddress'] ] = do['name']

DBusGMainLoop(set_as_default=True)

#make sure we keep old config info...
try:
    config = ConfigObj()
    config.filename =  "%s/.nm-cli" % os.environ['HOME']

    read_config = ConfigObj("%s/.nm-cli" % os.environ['HOME'])

    for a in read_config:
        config[a] = read_config[a]
except:
    pass

#start the program
if __name__ == "__main__":
    nm = NMCLI()

#save configuration data
try:
    config.write()
except:
    pass
