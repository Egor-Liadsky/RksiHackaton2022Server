
import flask
import flask_restplus

import database.handler
from swagger.auth.namespace import auth
import swagger.auth.models as models
from flask import request
import json
import hashlib

@auth.route('/')
class Auth(flask_restplus.Resource):
    @auth.doc(body=models.registration, responses={200: "{\"token\": string}"})
    def post(self):
        data = json.loads(request.data.decode())

        hash_id = database.handler.Db().insert_user(data.get("fio"), data.get("post"), data.get("organization"),
                                          data.get("status"), data.get("email"), data.get("password"))

        return flask.Response(json.dumps({"token": hash_id}, ensure_ascii=True), status=200)

    @auth.doc(params={"email": "Почта пользователя", "password": "Пароль пользователя"}, responses={200: "{\"token\": string}"})
    def get(self):
        data = request.args
        hash_id = None
        if len(data) > 0:
            user_id = database.handler.Db().select_user(data.get("email"), data.get("password"))
            if user_id is not None:
                hash_id = hashlib.sha256(str(user_id).encode()).hexdigest()
        return flask.Response(json.dumps({"token": hash_id}, ensure_ascii=True), status=200)


    @auth.doc(params={"email": "Почта пользователя", "password": "Пароль пользователя"},
              responses={200: "{\"token\": string}"})
    def get(self):
        data = request.args
        hash_id = None
        if len(data) > 0:
            user_id = database.handler.Db().select_user(data.get("email"), data.get("password"))
            if user_id is not None:
                hash_id = hashlib.sha256(str(user_id).encode()).hexdigest()
        return flask.Response(json.dumps({"token": hash_id}, ensure_ascii=True), status=200)

@auth.route('/<string:token>')
class AuthToken(flask_restplus.Resource):
    @auth.response(200, 'Success', models.registration)
    def get(self, token):
        data = token
        user_data = {'token': None}
        if len(data) > 0:
            user_data = database.handler.Db().select_user_info(data)

        return flask.Response(json.dumps(user_data, ensure_ascii=False), status=200)