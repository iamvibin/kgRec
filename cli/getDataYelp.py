# This is used to map the auxiliary information (genre, and city) into mapping ID for Yelp

import argparse


def mapping(fr_auxiliary, fw_genre, fw_city):
    '''
    mapping the auxiliary info (e.g., genre, city) into ID

    Inputs:
        @fr_auxiliary: the auxiliary infomation
        @fw_mapping: the auxiliary mapping information
    '''
    genre_map = {}
    city_map = {}

    city_count = genre_count = 0

    for line in fr_auxiliary:

        lines = line.replace('\n', '').split('|')
        if len(lines) != 3:
            continue

        location_id = lines[0].split(':')[1]
        genre_list = []
        city_list = []

        for genre in lines[1].split(":")[1].split(','):
            if genre not in genre_map:
                genre_map.update({genre: genre_count})
                #genre_list.append(genre_count)
                genre_id = genre_map[genre]
                genre_line = str(location_id) + ' ' + str(genre_id) + '\n'
                fw_genre.write(genre_line)
                genre_count = genre_count + 1
            else:
                genre_id = genre_map[genre]
                genre_line = str(location_id) + ' ' + str(genre_id) + '\n'
                fw_genre.write(genre_line)
                #genre_list.append(genre_id)

        for city in lines[2].split(":")[1].split(','):
            if city not in city_map:
                city_map.update({city: city_count})
                #city_list.append(city_count)
                city_id = city_map[city]
                city_line = str(location_id) + ' ' + str(city_id) + '\n'
                fw_genre.write(city_line)
                city_count = city_count + 1
            else:
                city_id = city_map[city]
                #city_list.append(city_id)
                city_line = str(location_id) + ' ' + str(city_id) + '\n'
                fw_city.write(city_line)

    return genre_count, city_count


def print_statistic_info(genre_count, city_count):
    '''
    print the number of genre and city
    '''

    print('The number of genre is: ' + str(genre_count))
    print('The number of city is: ' + str(city_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Map Auxiliary Information into ID''')

    parser.add_argument('--auxiliary', type=str, dest='auxiliary_file', default='data/yelp/auxiliary.txt')
    parser.add_argument('--genre', type=str, dest='genre_file', default='data/yelp/genre_obs.txt')
    parser.add_argument('--city', type=str, dest='city_file', default='data/yelp/city_obs.txt')

    parsed_args = parser.parse_args()

    auxiliary_file = parsed_args.auxiliary_file
    genre_file = parsed_args.genre_file
    city_file = parsed_args.city_file

    fr_auxiliary = open(auxiliary_file, 'r')
    fw_city = open(city_file, 'w')
    fw_genre = open(genre_file, 'w')

    genre_count, city_count = mapping(fr_auxiliary, fw_genre, fw_city)
    print_statistic_info(genre_count, city_count)

    fr_auxiliary.close()
    fw_genre.close()
    fw_city.close()