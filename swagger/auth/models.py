from flask_restplus import  fields
from swagger.auth.namespace import auth

registration = auth.model('registration', {
    'fio': fields.String,
    'post': fields.String,
    'organization': fields.String,
    'status': fields.String,
    'email': fields.String,
    'password': fields.String,
})

authorization = auth.model('authorization', {
    'email': fields.String,
    'password': fields.String,
})

