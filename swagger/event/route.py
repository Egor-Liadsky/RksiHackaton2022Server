import json

import flask
import flask_restplus
from flask import request

import database.handler
import database.processor
import swagger.event.models as models
from swagger.event.namespace import event


@event.route('/')
class Event(flask_restplus.Resource):
    @event.doc(params={'token': "Токен пользователя"},
               body=models.new_event,
               responses={200: "{'id', 'integer'}", 421: "Не найден один из обязательных параметров"})
    def post(self):
        data = json.loads(request.data.decode())
        valid_data = (
        data.get('date_start'), data.get('header'), data.get('text'), data.get('url'))
        if database.processor.DataProcessor().validate(valid_data):
            id = database.handler.Db().insert_event(data.get('date_start'), data.get('header'),
                                                    data.get('text'),
                                                    data.get('url'))
            response = flask.Response(json.dumps({'id': id}, ensure_ascii=True), status=200)

        else:
            response = flask.Response(json.dumps({"id": None}, ensure_ascii=True), status=412)

        return response

    @event.response(200, 'Success', models.event)
    def get(self):
        return database.handler.Db().select_all_event()


@event.route('/<string:id>')
class EventWithId(flask_restplus.Resource):
    @event.response(200, 'Success', models.event)
    @event.response(421, "Не найден один из обязательных параметров")
    def get(self, id):
        if id is not None:
            result = database.handler.Db().select_event(int(id))
            if result is None:
                response = flask.Response(json.dumps({"id": None}, ensure_ascii=True), status=412)
            else:
                response = flask.Response(json.dumps(result, ensure_ascii=True), status=200)
        else:
            response = flask.Response(json.dumps({"id": None}, ensure_ascii=True), status=412)
        return response

    @event.doc(params={'token': "Токен пользователя"})
    @event.response(200, 'Success')
    @event.response(404, "Не найден")
    def delete(self, id):
        if id is not None:
            database.handler.Db().delete_event(int(id))
            response = flask.Response(status=200)
        else:
            response = flask.Response(status=404)
        return response

    @event.doc(params={'token': "Токен пользователя"},
               body=models.new_event)
    @event.response(200, 'Success', models.event_result)
    def put(self, id):
        data = json.loads(request.data.decode())
        valid_data = (
        data.get('date_start'), data.get('header'), data.get('text'), data.get('url'))
        if database.processor.DataProcessor().validate(valid_data):
            database.handler.Db().update_event(id, data.get('date_start'), data.get('header'),
                                               data.get('text'),
                                               data.get('url'))
            response = flask.Response(json.dumps({'id': int(id)}, ensure_ascii=True), status=200)

        else:
            response = flask.Response(json.dumps({"id": None}, ensure_ascii=True), status=412)

        return response
