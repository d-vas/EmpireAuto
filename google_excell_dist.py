from geopy.distance import geodesic

print('hi')


work = (43.10781979121913, -76.26552866640294)
home = (43.07713715872313, -76.11094023335463)

dist = geodesic(work, home).miles

print(dist)


