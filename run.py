import monitor
import threading
from prox_import import proxy

def useragent():
    useragentss = []
    userr = open('agent.txt', 'r')

    for x in userr:
        useragentss.append(x.rstrip('\n'))

    userr.close()
    return useragentss


def main():
    agents = useragent()
    proxies = proxy('proxy.txt')

    testing = False

    if testing!= True:

        thread1 = threading.Thread(target=newMonitors.journeys,
                                   args=([['214674', '649902', '665248', '649121', '369573', '731140', '34487', '526643'], agents, proxies]))

        thread2 = threading.Thread(target=newMonitors.sportinglife, args=(['25638008', '25419151', '25553744', '25464157'], agents, proxies))
        thread3 = threading.Thread(target=newMonitors.holtRenfrew, args=([['20308282005', '20283499006', '20269276012', '20269278007', '20269739011'], agents, proxies]))
        thread4 = threading.Thread(target=newMonitors.uggCa, args=(
        ['1135092:CHE', '5955:DRI', '5955:BLK', '5955:CHE', '1135092:BLK', '1135092:DRI', "1134991:CHE", "1134991:BLK",
         '1122553:CHE', '1135092:MSG', '1134991S:FRSN', '1135092S:FRSN'], agents, resi))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
 
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
   

main()
