import argparse
import requests
import sys
import xml.etree.ElementTree as ET
import time


#
#Takes route input and check if route is a valid route
#
def validRoute(route):
    try:
        response = requests.get('https://svc.metrotransit.org/NexTrip/Routes?format=json')
        if response.status_code == 200:
            possible_routes = response.json()
            for pos in possible_routes:
                if route.upper() in pos['Description'].upper():
                    #print(pos)
                    return pos
        return None
    except Exception as ex:
        print("Error occurred while verifying route name.")
        print(ex, ex.with_traceback)

def validDirection(routeInfo, direction):
    try:
        key = {
            "south": 1,
            "east": 2,
            "west": 3,
            "north": 4
        }
        routeNum = routeInfo['Route']
        response = requests.get('https://svc.metrotransit.org/NexTrip/Directions/{0}?format=json'.format(routeNum))
        #response consists of key-value pairs
        #print(response.content)
        if response.status_code == 200:
            for pair in response.json():
                if int(key[direction]) == int(pair['Value']):
                    return pair
        return None
    except Exception as ex:
        print("Error occurred while verifying direction")
        print(ex, ex.with_traceback)

def validStop(routeInfo, directionInfo, stopName):
    try:
        routeNum = routeInfo['Route']
        directionNum = directionInfo['Value']
        response = requests.get('https://svc.metrotransit.org/NexTrip/Stops/{0}/{1}?format=json'.format(routeNum, directionNum))
        #print(response.content)
        if response.status_code == 200:
            for pair in response.json():
                if stopName.upper() in pair['Text'].upper():
                    return pair
        return None
    except Exception as ex:
        print("Error occurred while verifying stop")
        print(ex, ex.with_traceback)

def findTimeRemaining(routeInfo, directionInfo, stopInfo):
    try:
        routeNum = routeInfo['Route']
        directionNum = directionInfo['Value']
        stopNum = stopInfo['Value']
        #print(routeNum, directionNum, stopNum)
        response = requests.get('https://svc.metrotransit.org/NexTrip/{0}/{1}/{2}?format=json'.format(routeNum, directionNum, stopNum))
        #print(response.content)
        if (response.status_code == 200) and (response.content is not None):
            busTime = response.json()[1]['DepartureTime']
            busTime = busTime.replace("/Date(", "")
            busTime = busTime.replace("-0600)/", "")
            busTime = time.gmtime(float(str(busTime)[:-3]+'.'+str(busTime)[-3:]))
            #print(busTime)
            currTime = time.gmtime()
            #print(currTime)

            waitTime = {
                "Hour": busTime.tm_hour - currTime.tm_hour,
                "Minute": busTime.tm_min - currTime.tm_min
            }
            #print(waitTime)
            return waitTime
    except Exception as ex:
        print("Error occurred while verifying time remaining")
        print(ex, ex.with_traceback)


if __name__ == '__main__':
    #expecting 3 args
    #Bus Route, Bus Stop Name, Direction
    # “METRO Blue Line” “Target Field Station Platform 1” “south”
    parser = argparse.ArgumentParser()
    parser.add_argument("route", help="string of route name")
    parser.add_argument("stopName", help="string of stop name")
    parser.add_argument("direction", help="string of bus direction")
    args = parser.parse_args()

    #check if route entered is a valid option
    routeInfo = validRoute(args.route)
    if routeInfo is None:
        print("{0} is not a valid route".format(args.route))
        sys.exit()

    #check if direction is valid for this route
    directionInfo = validDirection(routeInfo, args.direction)
    if directionInfo is None:
        print("{0} is not a valid direction for {1}".format(args.direction, args.route))
        sys.exit()

    #check if stopName entered is a valid option
    stopInfo = validStop(routeInfo, directionInfo, args.stopName)
    if stopInfo is None:
        print("{0} is not a valid stop for {1} {2}".format(args.stopName, args.route, args.direction))
        sys.exit()

    

    #print(args.route + " " + args.stopName + " " + args.direction)
    timeInfo = findTimeRemaining(routeInfo, directionInfo, stopInfo)
    #print(timeInfo)
    #TODO return time in minutes
    if(timeInfo['Hour'] > 0):
        print("{0} Hour(s) {1} Minute(s)").format(timeInfo['Hour'], timeInfo['Minute'])
    else:
        print("{0} Minute(s)".format(timeInfo['Minute']))