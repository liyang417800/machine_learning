# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
import flask_restful


app = Flask(__name__)
api = flask_restful.Api(app)

class HelloWorld(flask_restful.Resource):
    def get(self):
        a = {"detail": "", "syscode": 200, "sumdrp": "0.0", "types": "rain", "results": [{"tm": "2019-09-10T09:00:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:05:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:10:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:15:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:20:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:25:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:30:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:35:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:40:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:45:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:50:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T09:55:00", "drp": "0.0", "stcd": "1956    "}, {"tm": "2019-09-10T10:00:00", "drp": "0.0", "stcd": "1956    "}]}
        return a

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
