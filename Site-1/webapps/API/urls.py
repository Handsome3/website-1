from django.conf.urls import url
from . import session

urlpatterns = [
    url(r'sessionDetail/(?P<session_key>.+)/$', session.SessionDetailView.as_view()),
    url(r'newSession', session.SessionView.as_view()),
]