from models.error import Error

def check_error_name_exists(name, exclude_id=None):
    query = Error.query.filter(Error.name == name)
    if exclude_id:
        query = query.filter(Error.id != exclude_id)
    return query.first() is not None
