from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('user_info/', views.user_info, name='user_info'),
	path('change_nickname/', views.change_nickname, name='change_nickname'),
	path('change_pwd/', views.change_pwd, name='change_pwd'),
	path('bind_email/', views.bind_email, name='bind_email'),
	path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
	path('forgot_pwd/', views.forgot_pwd, name='forgot_pwd'),

]

urlpatterns += staticfiles_urlpatterns()