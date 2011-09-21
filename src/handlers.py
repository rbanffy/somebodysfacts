from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        """
        The home
        """
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'hello': 'Hello webapp world'}))

    def post(self):
        raise NotImplementedError


class FactFightHandler(webapp.RequestHandler):
    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class SubmitAFactHandler(webapp.RequestHandler):
    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError
