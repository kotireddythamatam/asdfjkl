from django.urls import path
from home.views import *
urlpatterns = [
    path('signup/',user_registration_view),
    path('login',login),
    path('to_mail',to_mail),
    path('otp_to_mail',otp_to_mail),
    path('change_password',change_password),
    path('link_to_mail',link_to_mail),
    path('home',home),
    path('python',python),
    path('django',django),
    path('restapi',restapi),
    path('html',html),
    path('css',css),
    path('js',js),
    path('bootstrap',bootstrap),
    path('mysql',mysql),
    path('mongodb',mongodb),
    # path('profile',profile),
    path('logout',logout),
    path('like',comment_like),
    path('dislike',comment_dislike),
    path('replycomment/<int:id>',reply_comment),
    path('comment',create_comment),
    path('chatting',chatting),
    path('image',image_upload),


]
