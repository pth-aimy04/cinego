from django.contrib import admin
from .models import NguoiDung, Phim, Ve, DanhGia, QuanTriVien,ChiNhanh
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NguoiDung

admin.site.register(NguoiDung)
admin.site.register(Phim)
admin.site.register(Ve)
admin.site.register(DanhGia)
admin.site.register(QuanTriVien)
admin.site.register(ChiNhanh)