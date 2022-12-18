import datetime

from flask_restplus import fields
from swagger.member import namespace

member_event = namespace.member.model('member_event', {
    'event_id': fields.Integer,
    'user_id': fields.Integer,
})
