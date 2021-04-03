from flask import Flask, request

from .object_manager import Conflict, ObjectManager3

app = Flask(__name__)
mgr = ObjectManager3()


@app.route('/objects', methods=['POST'])
def put_object():
    """Add the object to the pool.

    POST /objects
    In:  {"object": 42, "acquired": false}
    Out: {"object": 42, "acquired": false}
    Idempotent
    """
    obj_json = request.json
    try:
        obj = obj_json['object']
        acquired = obj_json.get('acquired', False)
    except KeyError:
        return {'error': 'missing key "object"'}, 400

    try:
        created = mgr.put_object(obj, acquire=acquired)
    except (TypeError, ValueError) as err:
        return {'error': str(err)}, 400
    if created:
        return {'object': obj, 'acquired': acquired}, 201
    return {'object': obj, 'acquired': acquired}, 200


@app.route('/objects/get', methods=['POST'])
def get_object():
    """Get object from the pool.

    POST /objects/get
    In:  N/A
    Out: {"object": 42, "acquired": true}
    Not idempotent
    """
    try:
        obj = mgr.get_object()
    except Conflict as err:
        return {'error': str(err)}, 409
    return {'object': obj, 'acquired': True}, 200


@app.route('/objects/<int:obj>', methods=['POST'])
def free_object(obj):
    """Return the object into the pool.

    POST /objects/42
    In:  {"acquired": false}
    Out: {"object": 42, "acquired": false}
    Idempotent
    """
    obj_json = request.json
    try:
        acquired = obj_json['acquired']
    except KeyError:
        return {'error': 'missing key "acquired"'}, 400

    if acquired:
        return {'error': 'cannot acquire a particular object'}, 400

    try:
        mgr.free_object(obj)
    except (TypeError, ValueError) as err:
        return {'error': str(err)}, 400
    except Conflict as err:
        return {'error': str(err)}, 404
    return {'object': obj, 'acquired': acquired}, 200


@app.route('/objects/<int:obj>', methods=['DELETE'])
def drop_object(obj):
    """Drop the object from the pool.

    DELETE /objects/42
    In:  N/A
    Out: {'object': obj, 'acquired': false, 'deleted': true}
    Idempotent
    """
    try:
        dropped = mgr.drop_object(obj)
    except Conflict as err:
        return {'error': str(err)}, 409
    status = 200 if dropped else 404
    return {'object': obj, 'acquired': False, 'deleted': True}, status
