from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user_info import views as user_info_views


urlpatterns = [

    path('search', views.search),
    path('id=<int:ids>', views.index, name='property'),
    path('id=<int:ids>/book_form', views.book_form, name='book_form'),
    path('id=<int:ids>/<int:uid>-book', views.book, name='book'),

    path('comment/<int:id>',views.comment,name='comment'),
    path('update_comment/',views.update_comment,name='update_comment'),

    path('post/uid=<int:ids>', views.post, name='post'),
    path('my-property/uid=<int:ids>', views.user_posted, name='myproperty'),
    path('my-property/pid=<int:ids>-review', views.review, name='review'),
    path('my-property/pid=<int:ids>-edit-form', views.edit_form, name='edit_form'),
    path('my-property/pid=<int:ids>-edit', views.edit, name='edit'),
    path('my-property/pid=<int:ids>-add-img', views.add_img, name='add-img'),
    path('my-property/pid=<int:ids>-del-img', views.del_img, name='del-img'),
    path('my-property/pid=<int:ids>-del-pic', views.del_pic, name='del-pic'),
    path('my-property/pid=<int:ids>-delete', views.delete, name='delete'),
    path('my-booking/uid=<int:ids>', views.user_booked, name='mybooking'),
    path('my-booking/pid=<int:ids>-review', views.book_review, name='book_review'),
    path('my-booking/rid=<int:ids>-edit-form', views.book_edit_form, name='book_edit_form'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('my-booking/rid=<int:ids>-edit', views.book_edit_process, name='book_edit'),
    path('my-booking/rid=<int:ids>-delete-form', views.book_delete, name='book_delete'),
    path('my-booking/rid=<int:ids>-delete', views.book_delete_process, name='book_delete_process'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()