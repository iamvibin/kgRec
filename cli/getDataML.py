# This is used to map the auxiliary information (genre, director and actor) into mapping ID for MovieLens
import argparse

def mapping(fr_auxiliary, fw_actor, fw_genre, fw_director):
    '''
    mapping the auxiliary info (e.g., genre, director, actor) into ID

    Inputs:
        @fr_auxiliary: the auxiliary infomation
        @fw_mapping: the auxiliary mapping information
    '''
    actor_map = {}
    director_map = {}
    genre_map = {}

    actor_count = director_count = genre_count = 0

    for line in fr_auxiliary:

        lines = line.replace('\n', '').split('|')
        if len(lines) != 4:
            continue

        movie_id = lines[0].split(':')[1]
        genre_list = []
        director_list = []
        actor_list = []

        for genre in lines[1].split(":")[1].split(','):
            if genre not in genre_map:
                genre_map.update({genre: genre_count})
                genre_id = genre_map[genre]
                genre_line = str(movie_id) + ' ' + str(genre_id) + '\n'
                fw_genre.write(genre_line)
                genre_count = genre_count + 1
            else:
                genre_id = genre_map[genre]
                genre_line = str(movie_id) + ' ' + str(genre_id) + '\n'
                fw_genre.write(genre_line)


        for director in lines[2].split(":")[1].split(','):
            if director not in director_map:
                director_map.update({director: director_count})
                director_id = director_map[director]
                director_line = str(movie_id) + ' ' + str(director_id) + '\n'
                fw_director.write(director_line)
                director_count = director_count + 1
            else:
                director_id = director_map[director]
                director_line = str(movie_id) + ' ' + str(director_id) + '\n'
                fw_director.write(director_line)

        for actor in lines[3].split(':')[1].split(','):
            if actor not in actor_map:
                actor_map.update({actor: actor_count})
                actor_id = actor_map[actor]
                actor_line = str(movie_id) + ' ' + str(actor_id) + '\n'
                fw_actor.write(actor_line)
                actor_count = actor_count + 1
            else:
                actor_id = actor_map[actor]
                actor_line = str(movie_id) + ' ' + str(actor_id) + '\n'
                fw_actor.write(actor_line)


    return genre_count, director_count, actor_count


def print_statistic_info(genre_count, director_count, actor_count):
    '''
    print the number of genre, director and actor
    '''

    print('The number of genre is: ' + str(genre_count))
    print('The number of director is: ' + str(director_count))
    print('The number of actor is: ' + str(actor_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=''' Map Auxiliary Information into ID''')

    parser.add_argument('--auxiliary', type=str, dest='auxiliary_file', default='data/ml/auxiliary.txt')
    parser.add_argument('--actor', type=str, dest='actor_file', default='data/ml/actor_obs.txt')
    parser.add_argument('--director', type=str, dest='genre_file', default='data/ml/genre_obs.txt')
    parser.add_argument('--genre', type=str, dest='director_file', default='data/ml/director_obs.txt')

    parsed_args = parser.parse_args()

    auxiliary_file = parsed_args.auxiliary_file
    actor_file = parsed_args.actor_file
    genre_file = parsed_args.genre_file
    director_file = parsed_args.director_file

    fr_auxiliary = open(auxiliary_file, 'r')
    fw_actor = open(actor_file, 'w')
    fw_genre = open(genre_file, 'w')
    fw_director = open(director_file, 'w')


    genre_count, director_count, actor_count = mapping(fr_auxiliary, fw_actor, fw_genre, fw_director)
    print_statistic_info(genre_count, director_count, actor_count)

    fr_auxiliary.close()
    fw_actor.close()
    fw_director.close()
    fw_genre.close()