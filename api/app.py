from flask import Flask, jsonify, request

from .object_manager import Conflict, ObjectManager3

app = Flask(__name__)

mgr = ObjectManager3()
for i in range(1, 6):
    mgr.put_object(i)


@app.route('/objects', methods=['GET'])
def list_objects():
    """Get all object from the pool.

    POST /objects/get
    In:  N/A
    Out: {"object": 42, "acquired": true}
    Not idempotent
    """
    available, acquired = mgr.list_objects()
    return (
        jsonify(
            [{'object': obj, 'acquired': False} for obj in available] +
            [{'object': obj, 'acquired': True} for obj in acquired],
        ),
        200
    )


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
