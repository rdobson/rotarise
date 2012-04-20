from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rotarise.views.home', name='home'),
    # url(r'^rotarise/', include('rotarise.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       
                       
    # Authentication/login related re-directs.                   
    (r'^register/','rotarise.auth.views.register'), 
                       
    (r'^login/(?P<code>\d{1})/$', 'rotarise.auth.views.login'),
    (r'^login/','rotarise.auth.views.login'),
                       
    (r'^logout/', 'rotarise.auth.views.logout'),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done$', 'django.contrib.auth.views.password_change_done'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
                       
                       
)
