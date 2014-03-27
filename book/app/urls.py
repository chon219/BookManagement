from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'book.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),
    url(r'^add/$', views.add),
    url(r'^log/$', views.log),
    url(r'^borrow/$', views.book_borrow),
    url(r'^return/$', views.book_return),
)
