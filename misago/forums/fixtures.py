from django.utils import timezone
from misago.monitor.fixtures import load_monitor_fixture
from misago.forums.models import Forum
from misago.markdown import post_markdown
from misago.threads.models import Thread, Post
from misago.utils import slugify

def load_fixtures():
    Forum(token='annoucements', name='annoucements', slug='annoucements', type='forum').insert_at(target=None,save=True)
    Forum(token='private', name='private', slug='private', type='forum').insert_at(target=None,save=True)
    Forum(token='reports', name='reports', slug='reports', type='forum').insert_at(target=None,save=True)
    
    root = Forum(token='root', name='root', slug='root').insert_at(target=None,save=True)
    cat = Forum(type='category', name='First Category', slug='first-category').insert_at(target=root,save=True)
    forum = Forum(type='forum', name='First Forum', slug='first-forum', threads=1, posts=1).insert_at(target=cat,save=True)
    Forum(type='redirect', name='Project Homepage', slug='project-homepage', redirect='http://misago-project.org').insert_at(target=cat,save=True)
    Forum.objects.populate_tree(True)
       
    now = timezone.now()
    thread = Thread.create(
                           forum=forum,
                           name='Welcome to Misago!',
                           slug=slugify('Welcome to Misago!'),
                           start=now,
                           last=now,
                           )
    post = Post.create(
                       forum=forum,
                       thread=thread,
                       user_name='Misago Project',
                       ip='127.0.0.1',
                       agent='',
                       post='Welcome to Misago!',
                       post_preparsed='Welcome to Misago!',
                       date=now,
                       )
    thread.start_post = post
    thread.start_poster_name = 'Misago Project'
    thread.start_poster_slug = 'misago-project'
    thread.last_post = post
    thread.last_poster_name = 'Misago Project'
    thread.last_poster_slug = 'misago-project'
    thread.save(force_update=True)
    forum.last_thread = thread
    forum.last_thread_name = thread.name
    forum.last_thread_slug = thread.slug
    forum.last_thread_date = thread.last
    forum.last_poster = thread.last_poster
    forum.last_poster_name = thread.last_poster_name
    forum.last_poster_slug = thread.last_poster_slug
    forum.save(force_update=True)    
    
    load_monitor_fixture({
                          'threads': 1,
                          'posts': 1,
                          })