from django.conf.urls.static import static
from django.urls import path, include

from HW_28_1 import settings
from ads.views.service import index
from ads.views.ad import AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView, AdImageView
from ads.views.category import CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView, \
    CategoryDeleteView
from ads.views.user import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', index, name="index"),
    path("cat/", CategoryListView.as_view(), name="categories"),
    path("cat/create/", CategoryCreateView.as_view(), name="categories_create"),
    path("cat/<int:pk>/", CategoryDetailView.as_view(), name="category"),
    path("cat/<int:pk>/update/", CategoryUpdateView.as_view(), name="delete_category"),
    path("cat/<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete_category"),
    path("ad/", AdListView.as_view(), name="ads"),
    path("ad/create/", AdCreateView.as_view(), name="ads_create"),
    path("ad/<int:pk>/", AdDetailView.as_view(), name="ad"),
    path("ad/<int:pk>/update/", AdUpdateView.as_view(), name="update_ad"),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name="delete_ad"),
    path("ad/<int:pk>/upload_image/", AdImageView.as_view(), name="upload_image"),
    path("user/", UserListView.as_view(), name="users"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user"),
    path("user/create/", UserCreateView.as_view(), name="create_user"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="update_user"),
    path("user/<int:pk>/delete/", UserDeleteView.as_view(), name="delete_user")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
