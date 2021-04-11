from flask import request


def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """
    data = request.form.to_dict()
    print(data)
    return data


def verify_input_data(data, existing_fields):
    for i in data.keys():
        if i not in existing_fields:
            return False
    return True
