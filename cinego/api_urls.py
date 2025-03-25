from django.urls import path
from .views import (
    NguoiDungListCreate,
    PhimListCreate,
    VeListCreate,
    DanhGiaListCreate,
    QuanTriVienListCreate,
    RapChieuListCreate,
    LichChieuListCreate,  # Thêm API lịch chiếu
    PhimDetailView,
    DangKyView,
    phim_list,
    dang_nhap_api,
    so_ghe_con_trong,
    danh_sach_ghe,
)

urlpatterns = [
    path('nguoidung/', NguoiDungListCreate.as_view(), name='nguoidung-api'),
    path('phim/', PhimListCreate.as_view(), name='phim-api'),
    path('ve/', VeListCreate.as_view(), name='ve-api'),
    path('danhgia/', DanhGiaListCreate.as_view(), name='danhgia-api'),
    path('quantrivien/', QuanTriVienListCreate.as_view(), name='quantrivien-api'),
    path('rapchieu/', RapChieuListCreate.as_view(), name='rapchieu-api'),
    path('lichchieu/', LichChieuListCreate.as_view(), name='lichchieu-api'),  # API lịch chiếu
    path("phim/<int:pk>/", PhimDetailView.as_view(), name="phim-detail"),
    path("phim-list/", phim_list, name="phim-list-api"),
    path("dang-nhap/", dang_nhap_api, name="dang_nhap_api"),
    path("dang-ky/", DangKyView.as_view(), name="dang-ky"),
    path('so-ghe-con-trong/<int:lich_chieu_id>/', so_ghe_con_trong, name='so_ghe_con_trong'),
    path("ghe/<int:lichchieu_id>/", danh_sach_ghe, name="danh_sach_ghe"),
]
