import json

import flask
import flask_restplus
from flask import request

import database.handler
import database.processor
import swagger.step.models as models
from swagger.step.namespace import event_step


@event_step.route('/<string:id>/steps')
class StepsEvent(flask_restplus.Resource):
    @event_step.doc(params={'token': "Токен пользователя"}, body=models.step_event)
    @event_step.response(200, 'Success')
    def post(self, id):
        data = json.loads(request.data.decode())
        parm = request.args
        valid_data = (data.get('date_start'), data.get('date_end'), data.get('header'), data.get('text'), data.get('url'), parm.get('token'))
        response = flask.Response(status=412)
        if database.processor.DataProcessor().validate(valid_data):
            result = database.handler.Db().insert_steps_event(id, data.get('date_start'), data.get('date_end'), data.get('header'),
                                                              data.get('text'), data.get('url'))
            response = flask.Response(json.dumps(result, ensure_ascii=True), status=200)
        return response

    @event_step.doc(params={'token': "Токен пользователя"})
    @event_step.response(200, 'Success')
    def get(self, id):
        parm = request.args
        valid_data = [parm.get('token')]
        response = flask.Response(status=412)
        if database.processor.DataProcessor().validate(valid_data):
            result = database.handler.Db().select_steps_event(id, parm.get('token'))
            response = flask.Response(json.dumps(result, ensure_ascii=True), status=200)
        return response


@event_step.route('/<string:id>/steps/<string:step_id>')
class StepsEventChange(flask_restplus.Resource):
    @event_step.doc(params={'token': "Токен пользователя"}, body=models.step_event)
    @event_step.response(200, 'Success')
    def put(self, id, step_id):
        data = json.loads(request.data.decode())
        parm = request.args
        valid_data = (data.get('date_start'), data.get('date_end'), data.get('header'), data.get('text'), data.get('url'), parm.get('token'))
        response = flask.Response(status=412)
        if database.processor.DataProcessor().validate(valid_data):
            database.handler.Db().update_step_event(id, step_id, data.get('date_start'), data.get('date_end'), data.get('header'),
                                                              data.get('text'), data.get('url'))
            response = flask.Response(status=200)
        return response

    @event_step.doc(params={'token': "Токен пользователя"})
    @event_step.response(200, 'Success')
    def delete(self, id, step_id):
        parm = request.args
        valid_data = [parm.get('token')]
        response = flask.Response(status=412)
        if database.processor.DataProcessor().validate(valid_data):
            database.handler.Db().delete_step_event(id, step_id)
            response = flask.Response(status=200)
        return response