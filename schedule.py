#-*- coding: utf-8 -*-

import ast
import urllib2
import json
import inspect

BLOCK_SIZE = 20

def  time_to_int(time):
    (hour, minute) = time.split(":")

    ihour = int(hour)
    iminute = int(minute)

    assert ihour >= 0 and ihour <= 24
    assert iminute >= 0 and iminute <= 59

    return ihour * 60 + iminute

def is_overlap(interval, time):
    return interval.start <= time and time <= interval.finish

def interval_length(interval):
    return interval.finish - interval.start

class Interval:
    def  __int_to_time(self, i):
        hour = i / 60
        minute = i - 60 * hour
        return str(hour).rjust(2,"0") + ":" + str(minute).rjust(2,"0")
    def __init__(self, start, finish):
        self.start =time_to_int(start)
        self.finish = time_to_int(finish)
    def __eq__(self, other):
        return self.start == other.start and self.finish == other.finish
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return '{0} -- {1}'.format(self.__int_to_time(self.start), self.__int_to_time(self.finish))
    def __hash__(self):
        return hash(self.start) ^ hash(self.finish)
    def __repr__(self):
        return 'Interval: ' + str(self)
    def __lt__(self, other):
         return self.start < other.start



def find_times_interval(intervals, room_name):
    start = time_to_int("08:00")
    finish = time_to_int("18:00")

    min_length = interval_length(Interval("00:00", "01:30"))

    current_time = start
    current_interval = 0

    printed_room = False

    while current_time < finish:


        # reached end of intervals:
        if len(intervals) == current_interval:
            free_interval = Interval("00:00", "00:00")
            free_interval.start = current_time
            free_interval.finish = finish
            if interval_length(free_interval) > min_length:

                if printed_room == False:
                    print room_name.encode("utf-8")
                    printed_room = True

                print "Free interval: ", free_interval
            current_time = finish
            break

        i = intervals[current_interval]

        if is_overlap(i, current_time):
            current_time = i.finish
        else:
            free_interval = Interval("00:00", "00:00")
            free_interval.start = current_time
            free_interval.finish = i.start

            if interval_length(free_interval) > min_length:

                if printed_room == False:
                    print room_name.encode("utf-8")
                    printed_room = True

                print "Free interval: ", free_interval
            current_time = i.finish
        current_interval = current_interval + 1

def find_times(dic):

    for key, value in dic.iteritems():
        find_times_interval(value, key)

def get_page(url):
    response = urllib2.urlopen(url)

    return response.read()




def sort_room_times(dic):
    result = dict()

    for key, value in dic.iteritems():
        li = list(value)
        li.sort()
        result[key] = li

    return result

def parse_times(year, month, day, start_room, size, rooms, room_times):

    date = str(year).rjust(2,"0") + str(month).rjust(2,"0") + str(day).rjust(2,"0")

    url = "https://se.timeedit.net/web/chalmers/db1/public/ri.json?p={0}-{0}&objects=".format(date)


    for i in range(start_room,start_room+size):

        url += rooms[i][0]

        if i is not (start_room+size-1):
            url += "%2C"

    print url

    raw_json = get_page(url)
    decoded_json = json.loads(raw_json)

    valid_rooms = set([y for (x,y) in rooms   ])

    for reservation in decoded_json["reservations"]:
        i = Interval(reservation["starttime"], reservation["endtime"])

        rs = reservation["columns"][0].split()

        for room in rs:
            room = room.strip(",")

            if room in valid_rooms:

                if room not in room_times:
                    room_times[room] = set()

                room_times[room].add(i)

def process():

    with open ("rooms.txt", "r") as file:
        s=file.read().replace('\n', '')

    rooms = x = ast.literal_eval(s)
    room_times = dict()


    start_room = 0

    while start_room < len(rooms):
        parse_times(15,10,2, start_room, min(len(rooms) - start_room, BLOCK_SIZE), rooms, room_times )
        start_room = start_room + BLOCK_SIZE

    return sort_room_times(room_times)



#rs = process()



find_times(rs)
