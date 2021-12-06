from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import db

app = Flask(__name__)
api = Api(app)
cors = CORS(app,  resources={r"/*": {"origins": "*"}})



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class PGN(Resource):
    def get(self, name, action):
        if action == "getPlayerGames":
            games = db.getPlayerGames(name)

            return {"games": games}
        else:
            room = db.getRoomInfo(name)
            if action == "save":
                if room == None:
                    db.makeNewRoom(name)
                else:
                    db.updateRoom(name)

            if action == "view":
                game = db.getRoomGame(name)
                return {
                    "game": game
                }


api.add_resource(PGN, '/PGN/<name>/<action>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4500, debug=True)