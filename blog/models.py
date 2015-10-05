from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
# Create your models here.

class BlogManager(models.Manager):
    def get_blog(self):
        blogs = self.all()
        if blogs:
            return blogs[0]
        return None

class Blog(models.Model):
    title = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=100)
    entries_per_page = models.IntegerField(default=10)
    recents = models.IntegerField(default=5)
    recent_comments = models.IntegerField(default=5)
    
    objects = BlogManager()
    
    def __str__(self):
         return self.title
         
    def save(self, *args, **kwargs):
        """There should not be more than one Blog object"""
        if Blog.objects.count() == 1 and not self.id:
            raise Exception("Only one blog object allowed.")
        # Call the "real" save() method.
        super(Blog, self).save(*args, **kwargs)

    
class BlogEntry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    text = models.TextField()
    summary = models.TextField()
    created_on = models.DateTimeField(default=datetime.max, editable=False)
    created_by = models.ForeignKey(User, unique=False)
    is_page = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    publish_date = models.DateTimeField(null=True)
    comments_allowed = models.BooleanField(default=True)
    is_rte = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Blog entries'


    def save(self, *args, **kwargs):
        if self.title is None or self.title == '':
            self.title = _infer_title_or_slug(self.text.raw)

        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)

        i = 1
        while True:
            created_slug = self.create_slug(self.slug, i)
            slug_count = BlogEntry.objects.filter(slug__exact=created_slug).exclude(pk=self.pk)
            if not slug_count:
                break
            i += 1
        self.slug = created_slug

        if not self.summary:
            self.summary = _generate_summary(self.text.raw)
        #if not self.meta_keywords:
        #    self.meta_keywords = self.summary
        #if not self.meta_description:
        #    self.meta_description = self.summary

        if self.is_published:
            #default value for created_on is datetime.max whose year is 9999
            if self.created_on.year == 9999:
                self.created_on = self.publish_date
        # Call the "real" save() method.
        super(BlogEntry, self).save(*args, **kwargs)

    def create_slug(self, initial_slug, i=1):
        if not i == 1:
            initial_slug += "-%s" % (i,)
        return initial_slug

    def get_absolute_url(self):
        return reverse('blogentry-detail',
                       kwargs={'year': self.created_on.strftime('%Y'),
                               'month': self.created_on.strftime('%m'),
                               'slug': self.slug})

    def get_edit_url(self):
        return reverse('blog_admin_entry_edit', args=[self.id])