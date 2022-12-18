from flask import Flask


app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False

import swagger.route