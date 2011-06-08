from wsgiproxy.spawn import SpawningApplication
import os

USE_GEVENT = False

class ProxyApp(object):
    def __init__(self, appname):
        self.subapps = list()
        self.appname = appname
        self.spawn_cmd = ['bin/python', '%s/manage.py' % self.appname, 'run_gunicorn', '-b', '127.0.0.1:__PORT__']
    
    def create_subapp(self, suburl, settings):
        spawn_cmd = list(self.spawn_cmd)
        if USE_GEVENT:
            spawn_cmd.extend(('-k', 'gevent'))
        spawn_cmd.append('--settings=%s' % settings)
        application = SpawningApplication(spawn_cmd, cwd=os.getcwd())
        self.subapps.append((suburl, application))

    def __call__(self, environ, start_response):
        # Note that usually you wouldn't be writing a pure WSGI
        # application, you might be using some framework or
        # environment.  But as an example...
        url = environ['PATH_INFO']
        for suburl, application in self.subapps:
            if url.startswith(suburl):
                environ['SCRIPT_URL'] = suburl
                if suburl:
                    environ['PATH_INFO'] = environ['PATH_INFO'][len(suburl)-1:]
                return application(environ, start_response)
        print 'no match', str(dict(environ))
