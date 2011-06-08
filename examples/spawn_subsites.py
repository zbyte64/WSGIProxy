from wsgiproxy.proxy import ProxyApp

application = ProxyApp('mysite')

application.create_subapp('/site1/', 'settings.site1_settings')
application.create_subapp('/site2/', 'settings.site2_settings')
application.create_subapp('/', 'settings.base_settings')

