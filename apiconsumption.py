import argparse
import requests
import sys
import xml.etree.ElementTree as ET

def findTimeRemaining(route, stopName, direction):
    pass

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
                    print(pos)
                    return pos

        print(response.status_code)
        return None
    except Exception as ex:
        print("Error occurred while verifying route name.")
        print(ex, ex.with_traceback)



if __name__ == '__main__':
    #expecting 3 args
    #Bus Route, Bus Stop Name, Direction
    parser = argparse.ArgumentParser()
    parser.add_argument("route", help="string of route name")
    parser.add_argument("stopName", help="string of stop name")
    parser.add_argument("direction", help="string of bus direction")
    args = parser.parse_args()

    #TODO check if route entered is a valid option
    routeInfo = validRoute(args.route)
    if routeInfo is None:
        print("{0} is not a valid route".format(args.route))
        sys.exit()

    #TODO need to check if direction is valid for this route
    

    #TODO need to check if stopName entered is a valid option


    print(args.route + " " + args.stopName + " " + args.direction)
    findTimeRemaining(args.route, args.stopName, args.direction)
    #TODO return time in minutes
    print("return not functional yet")