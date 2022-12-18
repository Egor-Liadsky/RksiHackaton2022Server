import json

import flask
import flask_restplus
from flask import request

import database.handler
import database.processor
import swagger.event.models as models
from swagger.member.namespace import member


@member.route('/event/<string:event_id>')
class MemberEvent(flask_restplus.Resource):
    @member.response(200, 'Success')
    @member.response(404, "Мероприятия не существует/токен не валидный.")
    @member.doc(params={'token': "Токен пользователя"})
    def post(self, event_id):
        parm = request.args
        valid_data = (event_id, parm.get('token'))
        response = flask.Response(status=404)
        if database.processor.DataProcessor().validate(valid_data):
            is_event = database.handler.Db().insert_member_event(event_id, parm.get('token'))
            response = flask.Response(status=404) if is_event is None else flask.Response(status=200)
        return response

    @member.doc(params={'token': "Токен пользователя"})
    @member.response(404, "Мероприятия не существует/токен не валидный.")
    def get(self, event_id):
        result = database.handler.Db().select_event_members(event_id)
        response = flask.Response(json.dumps(result), status=200)
        return response

    @member.doc(params={'token': "Токен пользователя"})
    @member.response(404, "Мероприятия не существует/токен не валидный.")
    def delete(self, event_id):
        parm = request.args
        valid_data = (event_id, parm.get('token'))
        response = flask.Response(status=404)
        if database.processor.DataProcessor().validate(valid_data):
            database.handler.Db().delete_member_self_remove(event_id, parm.get('token'))
            response = flask.Response(status=200)
        return response


@member.route('/event/<string:event_id>/truncate')
class MemberTruncate(flask_restplus.Resource):
    @member.doc(params={'token': "Токен пользователя"})
    @member.response(404, "Мероприятия не существует/токен не валидный.")
    def delete(self, event_id):
        database.handler.Db().delete_truncate_member_event(event_id)
        return flask.Response(status=200)


@member.route('/event/me')
class MemberTruncate(flask_restplus.Resource):
    @member.doc(params={'token': "Токен пользователя"})
    @member.response(404, "Мероприятия не существует/токен не валидный.")
    def get(self):
        parm = request.args
        valid_data = [parm.get('token')]
        response = flask.Response(status=404)
        if database.processor.DataProcessor().validate(valid_data):
            result = database.handler.Db().select_user_event(parm.get('token'))
            response = flask.Response(json.dumps(result),status=200)
        return response