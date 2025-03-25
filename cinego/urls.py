from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Trang chính
    path("", views.homepage, name="home"), 

    # Đăng nhập giao diện web
    path("dang-nhap/", views.dang_nhap, name="dang_nhap"),

    # Nhúng toàn bộ API từ file riêng
    path("api/", include("cinego.api_urls")),
]

# Thêm cấu hình upload ảnh trong chế độ DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)