from flask import jsonify, make_response

from ast import literal_eval

from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from parse_request import get_request_data, verify_input_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    is_valid = verify_input_data(data, MOVIE_FIELDS)

    if is_valid:
        new_record = Movie.create(**data)
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(new_movie), 200)
    else:
        return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        if not verify_input_data(data, MOVIE_FIELDS):
            return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        data.pop('id')
        upd_record = Movie.update(row_id, **data)
        try:
            upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(upd_movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if verify_input_data(data, MOVIE_FIELDS):
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        Movie.delete(row_id)
        # use this for 200 response code
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys() and 'relation_id' in data.keys():
        # use this for 200 response code
        try:
            row_id = int(data['id'])
            relation_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        movie = Movie.add_relation(row_id, rel_obj=relation_id)  # add relation here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(movie), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    if 'id' in data.keys():
        # use this for 200 response code
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        # use this for 200 response code
        movie = Movie.clear_relations(row_id)  # clear relations here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['filmography'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###