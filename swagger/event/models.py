import datetime

from flask_restplus import fields
from swagger.event import namespace

event = namespace.event.model('event', {
    'id': fields.Integer,
    'date_start': fields.DateTime,
    'header': fields.String,
    'text': fields.String,
    'url': fields.String,
})

step_event = namespace.event.model('step_event', {
    'event_id': fields.Integer,
    'date_start': fields.DateTime,
    'date_end': fields.DateTime,
    'header': fields.String,
    'text': fields.String,
    'url': fields.String,
})

array_event = namespace.event.model('array_event', {
    'events': fields.List(fields.Nested(event)),
})

new_event = namespace.event.model('new_event', {
    'date_start': fields.DateTime,
    'header': fields.String,
    'text': fields.String,
    'url': fields.String,
})

event_result = namespace.event.model('event_result', {
    'id': fields.Integer,
})
