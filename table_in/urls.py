from django.urls import path, re_path
from . import views
from .views import StatusChange, CreateFields, UsersUpdate, UsersDelete, GeneratePdf, pdf_generate
#
from django.conf import settings
from django.conf.urls.static import static

# PDF
# from .views import MyPDF
# from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path(r'pdf/', pdf_generate, name='pdf_url'),
#     path(r'test_pdf/', views.test_pdf_render, name='test_pdf'),
    path(r'generate_pdf/', GeneratePdf.as_view(), name='generate_pdf'),
    path(r'create_fields/', CreateFields.as_view(), name='create_fields'),
    path(r'list_users/', views.list_users, name='list_users_url'),
    path(r'list_users/<int:pk>/edit/',
         UsersUpdate.as_view(), name='list_users_edit_url'),
    path(r'list_users/<int:pk>/delete/',
         UsersDelete.as_view(), name='users_delete_url'),
    path(r'status_change/', StatusChange.as_view(), name='status_change'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)