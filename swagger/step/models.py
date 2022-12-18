import datetime

from flask_restplus import fields
from swagger.event import namespace

step_event = namespace.event.model('step_event', {
    'event_id': fields.Integer,
    'date_start': fields.DateTime,
    'date_end': fields.DateTime,
    'header': fields.String,
    'text': fields.String,
    'url': fields.String,
})
