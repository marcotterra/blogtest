from datetime import datetime
from django.conf.urls import url
from blog.models import BlogEntry, Blog

from blog.views import BlogEntryList, BlogEntryDetail, AuthorView, BlogMonthArchive, BlogYearArchive

urlpatterns = [
    url(r'^$', BlogEntryList.as_view(), name='blogentry-list'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<slug>[-\w]+)/$',
        BlogEntryDetail.as_view(),
        name='blogentry-detail'),

    url(r'^author/(?P<username>[\w.@+-]+)/$',
        AuthorView.as_view(),
        name='author-detail'),
    
    url(r'^(?P<year>[0-9]{4})/$',
        BlogYearArchive.as_view(),
        name="article_year_archive"),    

    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        BlogMonthArchive.as_view(month_format='%m'),
        name="archive_month_numeric"),
]