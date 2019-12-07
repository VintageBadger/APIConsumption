import argparse
import requests

def lookup(route, stopName, direction):
    try:
        r = requests.get('http://svc-api:47101/api/Routes')
        if r.status_code == 200:
            print(r.json())
    except Exception as ex:
        print(ex)






if __name__ == '__main__':
    #expecting 3 args
    #Bus Route, Bus Stop Name, Direction
    parser = argparse.ArgumentParser()
    parser.add_argument("route", help="string of route name")
    parser.add_argument("stopName", help="string of stop name")
    parser.add_argument("direction", help="string of bus direction")
    args = parser.parse_args()

    print(args.route + " " + args.stopName + " " + args.direction)
    lookup(args.route, args.stopName, args.direction)
    #return time in minutes
    print("return not functional yet")