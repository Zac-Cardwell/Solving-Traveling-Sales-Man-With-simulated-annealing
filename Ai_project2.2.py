# CS 3642-W01:  ARTIFICIAL INTELLIGENCE
# Zac Cardwell
# 000935263
# Assignment 2
# 2-28
# Zac Cardwell

import random
import math
import datetime

cities = ["New York", "Los Angeles", "Chicago", "Minneapolis", "Denver", "Dallas", "Seattle", "Boston", "San Francisco", "St. Louis", "Houston", "Phoenix","Salt Lake City"]
distance_matrix = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]
hq = 0
vehicle_num = 1

class vehicle_driver:
    def  __init__(self):
        self.total_distance = 0
        self.cities = []
        self.travels = []

    def add_city(self, city, distancez):
        self.cities.append(city)
        self.total_distance += distancez
        self.travels.append(distancez)

    def get_info(self):
        return self.cities, self.travels

    def clear(self):
        self.cities.clear()
        self.travels.clear()
        self.total_distance = 0

    def final(self, cit, trav, tot):
        self.cities = list(cit)
        self.travels = list(trav)
        self.total_distance = tot


def find_distance(froms, to):
    a = cities.index(froms)
    b = cities.index(to)
    return distance_matrix[a][b]


def fill_random(best):
    best.clear()
    cities_left = list(cities)
    best.add_city('New York', 0)
    cities_left.remove("New York")
    froms = 'New York'
    for i in range(len(cities)-1):
        if len(cities_left) > 0:
            x = random.randrange(0,len(cities_left))
        else:
            x = 0
        to = cities_left[x]
        numb = find_distance(froms, to)
        best.add_city(to, numb)
        froms = to
        cities_left.remove(to)


def simulated_annealing():
    initial_temp = 90
    alpha = 0.01
    final_temp = .1
    current_temp = initial_temp
    best, current, next = vehicle_driver(), vehicle_driver(), vehicle_driver()
    fill_random(best)

    while current_temp > final_temp:
        fill_random(next)
        current.clear()
        current.add_city('New York', 0)
        best_cities, best_distance = best.get_info()
        next_cities, next_distance = next.get_info()
        fromz = 'New York'

        for i in range(len(cities)):
            best_numb = best_cities.index(fromz)
            next_numb = next_cities.index(fromz)
            x, y = current.get_info()

            if next_numb +1 < len(next_cities) and best_numb+1 < len(best_cities):

                if next_distance[next_numb +1] <= best_distance[best_numb +1] and (next_cities[next_numb +1] in x) is False:
                    current.add_city(next_cities[next_numb +1], next_distance[next_numb +1])
                    fromz = next_cities[next_numb + 1]

                elif  random.uniform(0, 1) < math.exp(((best_distance[best_numb+1] - next_distance[next_numb+1])/100) / current_temp) and (next_cities[next_numb +1] in x) is False:
                    current.add_city(next_cities[next_numb + 1], next_distance[next_numb + 1])
                    fromz = next_cities[next_numb + 1]

                elif (best_cities[best_numb +1] in x) is False:
                    current.add_city(best_cities[best_numb +1], best_distance[best_numb+1])
                    fromz = best_cities[best_numb +1]

                else:
                    x, y = current.get_info()
                    for i in best_cities:
                        if (i in x) is False:
                            tepz = find_distance(current.cities[len(current.cities)-1], i)
                            current.add_city(i, tepz)
                            fromz = i

            else:
                x, y = current.get_info()
                for i in best_cities:
                    if (i in x) is False:
                        tepz = find_distance(current.cities[len(current.cities)-1], i)
                        current.add_city(i, tepz)

        x, y = current.get_info()
        if current.total_distance < best.total_distance and len(y) == 13:
            best.final(x, y, current.total_distance)
        current_temp -= alpha
    return best


test = simulated_annealing()
High_Score_bot = open("TSM_High_Scores.txt", 'r+')
ptr = High_Score_bot.readlines()
best = 10000000
for i in ptr:
    if i.find("Simulated Annealing") != -1:
        ex =  [int(s) for s in i.split() if s.isdigit()]
        date = datetime.datetime.now()
        temp = ex[0]
        if ex[0] < best:
            best = ex[0]

if test.total_distance < best:
    strz = ""
    for i in cities:
        strz += i + " - "
    strz1 = "Simulated Annealing solved a New High Score: " + str(test.total_distance)
    strz2 = strz + '\nat ' + str(date)
    High_Score_bot.write('\r\n' + strz1 + "\n" + strz2)

print(test.cities)
print(test.total_distance)