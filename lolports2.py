import asyncio
import json
import socket
import subprocess
import sys
from datetime import datetime

remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)
checkedPorts = []
Ports = {}

print("▬" * 60)
print("Please wait, scanning remote host", remoteServerIP)
print("▬" * 60)

timeStart = datetime.now()


async def portcheck(portToCheck):
    returnVal = ""
    timeStartFunc = datetime.now()
    print("Scanning port: ", portToCheck)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, portToCheck))
    if result == 0:
        print("Port {}: 	 Open".format(portToCheck))
        returnVal += "Open"
    else:
        print("Port: ", portToCheck, " is closed.")
        returnVal += "Closed"
    sock.close()
    print("Scanned port: ", portToCheck, " in ", (datetime.now() - timeStartFunc))
    return returnVal


async def trier(startP, endP):
    try:
        for port in range(startP, endP):
            if port in checkedPorts:
                continue
            checkedPorts.append(port)
            result = await portcheck(port)
            Ports = {port : result}

    except KeyboardInterrupt:
        print("YOu pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()

    except socket.error:
        print("Couldn't connect to Server")
        sys.exit()

async def main():
    #The following doesn't actually work properly yet, still executing all requests in sequence rather than concurrently
    #TODO: Fix the trier() and the portChecker() to run concurrently and not block the event loop
    await asyncio.gather(
        trier(1,249),
        trier(250,499),
        trier(500,749),
        trier(750,1025)
    )
    file = open("portlog.txt",w)
    json.dump(Ports, file, indent=1)
    file.flush()
    file.close()

asyncio.run(main())

timeEnd = datetime.now()

timeTotal = timeEnd - timeStart

print("Scanning completed in: ", timeTotal)
