from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor

from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data, verify_input_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
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
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    is_valid = verify_input_data(data, ACTOR_FIELDS)

    if is_valid:
        if 'date_of_birth' in data.keys():
            try:
                date_of_birth = dt.strptime(data['date_of_birth'], '%d.%m.%Y')
            except:
                return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(new_actor), 200)
    else:
        return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        if not verify_input_data(data, ACTOR_FIELDS):
            return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        if 'date_of_birth' in data.keys():
            try:
                date_of_birth = dt.strptime(data['date_of_birth'], '%d.%m.%y')
            except:
                return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
        # data.pop('id')
        # data = dict([(k, v) for k, v in data.items() if k != 'id'])
        upd_record = Actor.update(row_id, **data)
        try:
            upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        print(upd_record)
        return make_response(jsonify(upd_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if verify_input_data(data, ACTOR_FIELDS):
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        Actor.delete(row_id)
        # use this for 200 response code
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
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
        actor = Actor.add_relation(row_id, rel_obj=relation_id) # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###


def actor_clear_relations():
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
        actor = Actor.clear_relations(row_id) # clear relations here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    return make_response(jsonify(error='Input data is not correct so process could not be ended'), 400)
    ### END CODE HERE ###