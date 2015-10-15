from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView
from datetime import datetime

from blog.models import Blog, BlogEntry, BlogManager


class BlogEntryList(ListView):
    template_name = "blog/blog_entry_list.html"
    model = BlogEntry

    def get_context_data(self, **kwargs):
        return super(BlogEntryList, self).get_context_data(**kwargs)
    
    def get_object(self, queryset=None):
        if 'year' in self.kwargs:
            entry = BlogEntry.objects.get(created_on__year=self.kwargs['year'],
                                          created_on__month=self.kwargs['month'],
                                          slug=self.kwargs['slug'])
        else:
            entry = BlogEntry.objects.get(is_page=True, slug=self.kwargs['slug'])
        return entry


class BlogEntryDetail(DetailView):
    template_name = "blog/blog_entry_detail.html"
    model = BlogEntry

    def get_context_data(self, **kwargs):
        context = super(BlogEntryDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

'''
class AuthorView(ListView):
    template_name = "blog/teste.html"
    #model = BlogEntry

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        self.kwargs['author'] = author
        author_posts = author.blogentry_set.filter(is_published=True)
        return author_posts

    def get_paginate_by(self, queryset):
        paginate_by = Blog.objects.get_blog().entries_per_page
        return paginate_by

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['author'] = self.kwargs['author']
        return context
'''

class AuthorView(ListView):
	template_name = "blog/blog_entry_author_list.html"
	model = BlogEntry
	
	def get_queryset(self):
		self.username = get_object_or_404(User, username=self.kwargs['username'])
		return BlogEntry.objects.filter(created_by=self.username)


class BlogYearArchive(YearArchiveView):
    template_name = "blog/blog_archive_year.html"

    queryset = BlogEntry.objects.all()
    date_field = "created_on"
    make_object_list = True
    allow_future = True

class BlogMonthArchive(MonthArchiveView):
    template_name = "blog/blog_archive_month.html"

    queryset = BlogEntry.objects.all()
    date_field = "created_on"
    allow_future = True
