from flask import Flask, request

from .object_manager import Conflict, ObjectManager3

app = Flask(__name__)

mgr = ObjectManager3()
for i in range(1, 8):
    mgr.put_object(i)


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
