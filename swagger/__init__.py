from flask_restplus import Api
import flask_app
import settings

api = Api(flask_app.app, doc=settings.URL_SWAGGER, version=settings.API_VER, path='')
api.description = 'Все методы ВХакатоне'

import swagger.route