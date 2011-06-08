from wsgiproxy.proxy import ProxyApp

application = ProxyApp('mysite')

application.create_subapp('/site1/', 'settings.site1_settings')
application.create_subapp('/site2/', 'settings.site2_settings')
application.create_subapp('/', 'settings.base_settings')

#Note: this assumes gunicorn and django, make sure gunicorn is in your installed apps
#Example usage: bin/gunicorn spawn_subsites:application

