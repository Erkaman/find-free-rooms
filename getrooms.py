import urllib2
import json
from pprint import pprint

def get_page(url):
    response = urllib2.urlopen(url)
    return response.read()

def format_url(start,max):
    return "https://se.timeedit.net/web/chalmers/db1/public/objects?max={1}&fr=t&partajax=t&im=f&sid=3&l=sv_SE&types=186&start={0}&part=t&media=txt".format(str(start),str(max))

def print_rooms(rooms):
    for pair in rooms:
        print pair

def bad_room(s):
    s = s.lower()
    return s.find("eklanda") != -1 or s.find("lindholmen") != -1 or s.find("vasa") != -1

def get_rooms(start, max):
    url = format_url(start,max)
    print url
    raw_json = get_page(url)
    decoded_json = json.loads(raw_json)

    result = []
    start = start
    end = start + len(decoded_json["records"])

    for i in range(start,end):
        record = decoded_json["records"][i-start]

        room_info_url = "https://se.timeedit.net/web/chalmers/db1/public/objects/{0}.json".format(record["textId"])

        room_info = json.loads(get_page(room_info_url))

        values = room_info["records"][0]["fields"][2]["values"]
        if len(values) > 0:
            building = values[0]
            if not bad_room(building):
                result.append((record["ident"], record["values"]))


    return (end-start, result)

app = []
block_size = 50
start = 0
while True:

    (c, li) = get_rooms(start,block_size)
    app.extend(li)
    start = start + block_size

    if c is not block_size:
        break


print str(app)

with open("rooms.txt", "w") as file:
    file.write(str(app))
