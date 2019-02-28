sudo modprobe usbip_core
sudo modprobe usbip_host
sudo usbip list --local
sudo firewall-cmd --add-port=3240/tcp
usbipd&
echo "start with: sudo usbip bind --busid=X-X"
