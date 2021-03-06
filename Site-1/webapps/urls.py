from django.conf import settings
from django.conf.urls import url
from . import views, views_user, views_post, views_upload, views_detail, views_search, views_option, views_edit
from django.conf.urls.static import static

app_name = 'webapps'
urlpatterns = [
    url(r'^$', views.index),
    #search
    url(r'search/(?P<type>[a-z]+)$', views_search.searchPage, name="searchPage"),
    url(r'sitesearch', views_search.siteSearch, name='siteSearch'),

    #User
    url(r'user/loginpage',views_user.loginPage, name='loginPage'),
    url(r'user/getuserinfo',views_user.getUserInfo, name='getuserinfo'),
    url(r'user/signup', views_user.signup, name='signupPage'),
    url(r'user/register', views_user.register),
    url(r'user/denglu', views_user.userlogin),
    url(r'user/logout', views_user.userlogout),
    url(r'user/changeuser', views_user.changeUser),
    url(r'user/checkemail', views_user.checkEmail),
    url(r'user/editProfile', views_user.editProfile, name='editProfile'),

    #Post
    url(r'post/(?P<type>[a-z]+)/page', views_post.postPage, name="postPage"),
    url(r'post/(?P<type>[a-z]+)/submit', views_post.submitPost, name='submitPost'),

    # Edit
    url(r'deal/edit/(?P<deal_id>[0-9]+)$', views_edit.editDeal, name='editDeal'),
    url(r'deal/repost/(?P<deal_id>[0-9]+)$', views_edit.repostDeal, name='repostDeal'),
    url(r'deal/stop/(?P<deal_id>[0-9]+)$', views_edit.stopDeal, name='stopDeal'),
    url(r'deal/delete/(?P<deal_id>[0-9]+)$', views_edit.deleteDeal, name='deleteDeal'),
    url(r'deal/edit/editcarpool', views_edit.editCarpool, name='editCarpool'),
    url(r'deal/edit/editmergeorder', views_edit.editMergeorder, name='editMergeorder'),
    url(r'deal/edit/editusedcar', views_edit.editUsedcar, name='editUsedcar'),
    url(r'deal/edit/edituseditem', views_edit.editUseditem, name='editUsedItem'),
    url(r'deal/edit/editsublease', views_edit.editSublease, name='editSublease'),
    url(r'deal/edit/edithouserent', views_edit.editHouserent, name='editHouserent'),

    #Ajax Request
    url(r'upload/images', views_upload.uploadImg, name='uploadImg'),
    url(r'deal/save', views_detail.saveDeal, name='saveDeal'),
    url(r'deal/unsave', views_detail.unsaveDeal, name='unsaveDeal'),
    url(r'deal/loadmore', views_user.loadMoreDeal, name='loadMoreDeal'),
    url(r'option/carbrand',views_option.getCarBrand,name='getCarBrand'),
    url(r'option/carmodel',views_option.getCarModel,name='getCarModel'),
    url(r'ajax/deleteimage', views_edit.deleteImage, name='deleteImage'),
    url(r'ajax/deal/edit/carpool', views_edit.editCarpool, name='editCarpool'),

    url(r'ajax/options/carbrand', views_option.getCarBrand, name='getCarBrand'),
    url(r'ajax/options/carmodel', views_option.getCarModel, name='getCarModel'),
    url(r'ajax/options/state', views_option.getState, name='getState'),
    url(r'ajax/options/city', views_option.getCity, name='getCity'),
    url(r'ajax/options/location', views_option.getLocation, name='getLocation'),

    url(r'ajax/options/itemtype', views_option.getItemtype, name='getItemtype'),


    url(r'ajax/user/changepw', views_user.changePw, name='changePw'),
    url(r'ajax/user/changeProfile', views_user.changeProfile, name='changeProfile'),

    url(r'ajax/s/(?P<type>[a-z]+)$', views_search.ajaxSearch, name='ajaxSearch'),

    #Item Detail
    url(r'^deal/(?P<deal_id>[0-9]+)/detail$', views_detail.getDealDetail, name='getDealDetail'),

    #Redirect
    url(r'redirect', views.redirect),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)