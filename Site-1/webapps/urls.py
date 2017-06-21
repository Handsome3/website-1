from django.conf import settings
from django.conf.urls import url
from . import views, views_user, views_post, views_upload, views_detail, views_search,views_option
from django.conf.urls.static import static

from . import views, views_user, views_post, views_upload, views_detail, views_search, views_option, views_edit

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
                  url(r'user/editProfile', views_user.editProfile, name='editProfile'),

    #Post
    #url(r'post/(?P<type>[a-z]+)', views.getPostPage),
    url(r'post/houserent/page',views_post.getHouseRentPage),
    url(r'post/houserent/submit',views_post.houseRentPost),
    url(r'post/sublease/page',views_post.getSubleasePage),
    url(r'post/sublease/submit',views_post.subleasePost),
    url(r'post/useditem/page',views_post.getUsedItemPage),
    url(r'post/useditem/submit',views_post.usedItemPost),
    url(r'post/mergeorder/page',views_post.getMergeOrderPage),
    url(r'post/mergeorder/submit',views_post.mergeOrderPost),
    url(r'post/carpool/page',views_post.getCarpoolPage),
    url(r'post/carpool/submit', views_post.carpoolPost),
    url(r'post/usedcar/page', views_post.getUsercarPage),
    url(r'post/usedcar/submit', views_post.usedcarPost),
    url(r'postresult',views.getPostResult,name='postresult'),

                  # Edit
                  url(r'deal/edit/(?P<deal_id>[0-9]+)$', views_edit.editDeal, name='editDeal'),
                  url(r'deal/repost/(?P<deal_id>[0-9]+)$', views_edit.repostDeal, name='repostDeal'),

                  # Delete
                  url(r'deal/stop/(?P<deal_id>[0-9]+)$', views_edit.stopDeal, name='stopDeal'),
                  url(r'deal/delete/(?P<deal_id>[0-9]+)$', views_edit.deleteDeal, name='deleteDeal'),

    #Ajax Request
    url(r'upload/images', views_upload.uploadImg),
    url(r'deal/save', views_detail.saveDeal, name='saveDeal'),
    url(r'deal/unsave', views_detail.unsaveDeal, name='unsaveDeal'),
    url(r'deal/loadmore', views_detail.loadMoreDeal, name='loadMoreDeal'),
    url(r'option/carbrand',views_option.getCarBrand,name='getCarBrand'),
    url(r'option/carmodel',views_option.getCarModel,name='getCarModel'),
                  url(r'ajax/deleteimage', views_edit.deleteImage, name='deleteImage'),
                  url(r'ajax/deal/edit', views_edit.ajaxEditDeal, name='ajaxEditDeal'),

                  url(r'ajax/options/carbrand', views_option.getCarBrand, name='getCarBrand'),
                  url(r'ajax/options/carmodel', views_option.getCarModel, name='getCarModel'),

                  url(r'ajax/user/changepw', views_user.changePw, name='changePw'),
                  url(r'ajax/user/changeProfile', views_user.changeProfile, name='changeProfile'),

                  url(r'ajax/s/usedcar', views_search.ajaxSearchUsedcar, name="ajaxSearchUsedcar"),

    #Item Detail
    url(r'^deal/(?P<deal_id>[0-9]+)/detail$', views_detail.getDealDetail, name='getDealDetail'),

    #Redirect
    url(r'redirect', views.redirect),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)