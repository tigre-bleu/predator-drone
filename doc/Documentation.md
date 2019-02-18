# Documentation
## USRP

- [USRP Hardware Driver and USRP Manual](https://files.ettus.com/manual/index.html)

**Install USRP (Fedora):**
```
#dnf install uhd uhd-devel
#/usr/libexec/uhd/uhd_images_downloader.py
$ uhd_find_devices
[INFO] [UHD] linux; GNU C++ version 8.1.1 20180712 (Red Hat 8.1.1-5); Boost_106600; UHD_3.12.0.0
[INFO] [B200] Loading firmware image: /usr/share/uhd/images/usrp_b200_fw.hex...
--------------------------------------------------
-- UHD Device 0
--------------------------------------------------
Device Address:
    serial: 307038D
    name:
    product: B200
    type: b200
```

## RF Tools
### Baudline
**Install (Fedora):**
```
#dnf install xorg-x11-fonts-ISO8859-1-75dpi.noarch
```
Then run ./baudline from downloaded tar on official website

## Reverse Engineering RF 2.4 GHz
- [Reverse Engineering a Quadcopter RC, or: How to not miss the needle while throwing the haystack in the air](https://mmelchior.wordpress.com/2016/06/06/qc-360-a1-p1/)
- [Reverse Engineering Quadcopter Protocols](https://hackaday.com/2016/06/28/reverse-engineering-quadcopter-protocols/)
- [PHD VI: How They Stole Our Drone](https://blog.ptsecurity.com/2016/06/phd-vi-how-they-stole-our-drone.html)
- [Nullcon 2017: Drone Hijacking And Other IoT Hacking With GNU Radio And SDR](https://www.rtl-sdr.com/nullcon-2017-drone-hijacking-and-other-iot-hacking-with-gnu-radio-and-sdr/)
- [Furibee F36 protocol attempt](https://www.deviationtx.com/forum/protocol-development/6806-furibee-f36-protocol-attempt?start=120)
- [
Shmoocon 2017: A Simple Tool For Reverse Engineering RF](https://hackaday.com/2017/01/15/shmoocon-2017-a-simple-tool-for-reverse-engineering-rf/)
- [Universal Radio Hacker](https://github.com/jopohl/urh)
- [NRF Analyse](https://github.com/chopengauer/nrf_analyze)

## Share USB device over TCP:
On server side:
```
sudo modprobe usbip_core
sudo modprobe usbip_host
sudo usbip list --local
sudo usbip bind --busid=1-2
```

On client side:
```
sudo modprobe usbip_core
sudo modprobe usbip_host
sudo modprobe vhci-hcd
sudo usbip list --remote=192.168.2.2
sudo usbip attach --remote 192.168.2.2 --busid=1-2
```