from django.conf.urls import url
from . import views
from . import views_user
from . import views_post
from . import views_upload
from . import views_detail
from django.conf.urls.static import static
from django.conf import settings

app_name = 'webapps'
urlpatterns = [
    url(r'^$', views.index),

    #search
    url(r'searchcarpool',views.searchCarpool),
    url(r'searchuseditem',views.searchUsedItem),
    url(r'searchhouse',views.searchHouse),
    url(r'searchusedCar',views.searchUsedCar),
    url(r'searchmergeorder',views.searchMergeOrder),

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
    url(r'upload/usedcar', views_upload.usedcar),
    url(r'deal/save', views_detail.saveDeal, name='saveDeal'),
    url(r'deal/unsave', views_detail.unsaveDeal, name='unsaveDeal'),
    url(r'deal/loadmore', views_detail.loadMoreDeal, name='loadMoreDeal'),

    #Item Detail
    url(r'^deal/(?P<deal_id>[0-9]+)/detail$', views_detail.getDealDetail, name='getDealDetail'),

    #Redirect
    url(r'redirect', views.redirect),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)