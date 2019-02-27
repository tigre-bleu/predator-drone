#
# Joystick management for Syma X5C-1
#

from threading import Thread
import re, os
import time

from .ext_exec import do
from . import disp



# ===============
#    Constants
# ===============

# Remote hosts that can host the Gamepad with USBIP
USBIP_SERVER_LIST = ["172.20.1.2", "172.20.1.3"]



# ===========
#    Tools
# ===========

def exp(value, koef=1.01, maximum=255):
    if value < 10:
        return value
    tmp = 160*(koef**(value)) / (koef**maximum)
    tmp = int(tmp) & 0xff
    return int(tmp)



# ==============================
#    JoystickController class
# ==============================

class JoystickController(Thread):

    def __init__(self, controller):
        disp.debug("Initilizing joystick")
        path = '/dev/'

        init_joystick = True
        while (init_joystick):
            try:
                file_list = [f for f in os.listdir(path) if f.startswith('hidr')]
                if file_list == []:
                    disp.warn("No existing hidraw device. Trying to connect with USBIP.")
                    if not self.connect_usbip():
                        disp.die("Error: Couldn't connect USBIP device. No joystick available.")
                    time.sleep(1)
                else:
                    joystick_file = path + file_list[-1]
                    disp.info('Joystick detected:', joystick_file)
                    self.joystick = open(joystick_file, 'r')
                    init_joystick = False

            except:
                disp.die("Error while initilizing joystick")

        super(JoystickController, self).__init__()

        self.syma_controller = controller

        disp.info("Everything is ready. Press <START> to capture drone",
                str(self.syma_controller.address) + ". Press <SELECT> to exit predator tool.")



    # ============================
    #    USB over IP management
    # ============================

    def connect_usbip(self):
        found = False

        for ip in USBIP_SERVER_LIST:
            if (not found):
                output = do('usbip list --remote=' + ip, get_output=True)

                regex = r"([-0-9]+): GreenAsia Inc. : MaxFire Blaze2 \(0e8f:0003\)"
                match = re.findall(regex,output)
                if (match):
                    busid = match[0]
                    server = ip
                    found = True

        if found:
            disp.info("GreenAsia Gamepad detected on", server, "with bus-id=" + busid)
            do('modprobe usbip_host usbip_core')
            do('modprobe vhci_hcd')
            do('usbip attach --remote', server, '--busid=' + busid)
            return True
        else:
            disp.info("GreenAsia Gamepad not detected in", str(USBIP_SERVER_LIST))
            return False



    # =====================
    #    Threading stuff
    # =====================

    def stop(self):
        self.stopped = True


    def run(self):
        self.stopped = False
        start_pressed = False
        while not self.stopped:
            s = self.joystick.read(8)

            if (ord(s[6]) & 0x20):
                if not start_pressed:
                    if self.syma_controller.running:
                        self.syma_controller.release()
                    else:
                        self.syma_controller.capture()
                start_pressed = True
            else:
                start_pressed = False

            if (ord(s[6]) & 0x10):
                self.syma_controller.exit()

            t = 2*(127 - ord(s[3]))
            if t < 0:
                t = 0
            self.syma_controller.throttle = exp(value=t)

            if (ord(s[6]) & 0x3):
                self.syma_controller.throttle = 255

            t = ord(s[2])
            if t == 128:
                # Neutral
                self.syma_controller.rudder = 0
            elif t < 128:
                # Left Yaw
                self.syma_controller.rudder = 127 - t
            else:
                # Right Yaw
                self.syma_controller.rudder = t

            t = ord(s[1])
            if t == 128:
                # Neutral
                self.syma_controller.elevator = 0
            elif t < 128:
                # Backwards
                self.syma_controller.elevator = 127 - t
            else:
                # Frontwards
                self.syma_controller.elevator = t

            t = ord(s[0])
            if t == 128:
                # Neutral
                self.syma_controller.aileron = 0
            elif t < 128:
                # Roll right
                self.syma_controller.aileron = 127 - t
            else:
                # Roll left
                self.syma_controller.aileron = t

            time.sleep(0.0)
        disp.debug("End of joystick thread")

