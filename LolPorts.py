import asyncio
import socket
import subprocess
import sys
from datetime import datetime

remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

print("▬" * 60)
print("Please wait, scanning remote host", remoteServerIP)
print("▬" * 60)

t1 = datetime.now()


async def portcheck(portToCheck):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, portToCheck))
    if result == 0:
        print("Port {}: 	 Open".format(portToCheck))
        sock.close()
        return 1
    else:
        sock.close()
        return 0


async def main():
    try:
        checkedPorts = []
        for port in range(1, 1025):
            if port in checkedPorts:
                continue
            checkedPorts.append(port)
            await portcheck(port)

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    t2 = datetime.now()

    total = t2 - t1

    print('Scanning Completed in: ', total)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())