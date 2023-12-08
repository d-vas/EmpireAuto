def location_parse(loc_line):
    state_zipcode = loc_line.split(', ')[-1]
    street_city = loc_line.rsplit(', ', 1)[0]
    state, zipcode = state_zipcode.split()
    city = street_city.split(', ')[-1]
    street = street_city.replace(city, '')
    print(street, city, state, zipcode, sep='\n')
    return street, city, state, zipcode

