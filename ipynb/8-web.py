from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import json


class BaseRequestHandler(RequestHandler):
    def jsonfiy(self, data):
        self.set_header('content-type', 'application/json')
        self.write(json.dumps(data))


class JsonResponseMixIn:
    def jsonfiy(self, **kwargs):
        self.set_header('content-type', 'application/json')
        self.write(json.dumps(kwargs))


class XmlResponseMixIn:
    def xmlfiy(self, **kwargs):
        self.set_header('content-type', 'text/xml')
        es = []
        for k, v in kwargs.items():
            e = '<{k}>{v}</{k}>'.format(k=k, v=str(v))
            es.append(e)
        xml = '<root>\n\r{0}\n</root>'.format('\n\r'.join(es))
        self.write(xml)


class MainHandler(XmlResponseMixIn, RequestHandler):
    def get(self):
        # self.set_header('content-type', 'application/json')
        # self.write(json.dumps({'a': 1}))
        #self.jsonfiy(a=1)
        self.xmlfiy(a=1)
        self.finish()


app = Application([
    ('/', MainHandler)
], debug=True)


app.listen(1024, address='0.0.0.0')
server = HTTPServer(app)

if __name__ == '__main__':
    IOLoop.current().start()
