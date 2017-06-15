from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views, views_user, views_post, views_upload, views_detail, views_search, views_option

app_name = 'webapps'
urlpatterns = [
    url(r'^$', views.index),

    #search
                  url(r'search/usedcar', views_search.usedcarPage, name='searchUsedcar'),

    #User
    url(r'user/loginpage',views_user.loginPage, name='loginPage'),
    url(r'user/getuserinfo',views_user.getUserInfo, name='getuserinfo'),
    url(r'user/signup', views_user.signup),
    url(r'user/register', views_user.register),
    url(r'user/denglu', views_user.userlogin),
    url(r'user/logout', views_user.userlogout),
    url(r'user/changeuser', views_user.changeUser),
    url(r'user/checkemail', views_user.checkEmail),

    #Post
    #url(r'post/(?P<type>[a-z]+)', views.getPostPage),
    url(r'post/carpool/page',views_post.carpoolPage),
    url(r'post/carpool/submit', views_post.carpoolPost),
    url(r'post/usedcar/page', views_post.usercarPage),
    url(r'post/usedcar/submit', views_post.usedcarPost),
    url(r'postresult',views.getPostResult,name='postresult'),

    #Ajax Request
                  url(r'ajax/upload/usedcar', views_upload.usedcar, name='uploadUsedcar'),
                  url(r'ajax/deal/save', views_detail.saveDeal, name='saveDeal'),
                  url(r'ajax/deal/unsave', views_detail.unsaveDeal, name='unsaveDeal'),
                  url(r'ajax/deal/loadmore', views_detail.loadMoreDeal, name='loadMoreDeal'),
                  url(r'ajax/s/usedcar', views_search.ajaxSearchUsedcar, name="ajaxSearchUsedcar"),
                  url(r'ajax/options/carbrand', views_option.getCarBrand, name='getCarBrand'),
                  url(r'ajax/options/carmodel', views_option.getCarModel, name='getCarModel'),

    #Item Detail
    url(r'^deal/(?P<deal_id>[0-9]+)/detail$', views_detail.getDealDetail, name='getDealDetail'),

    #Redirect
    url(r'redirect', views.redirect),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)