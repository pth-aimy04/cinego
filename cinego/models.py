from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class NguoiDungManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Người dùng phải có email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser phải có is_staff=True.")
        return self.create_user(email, password, **extra_fields)


class NguoiDung(AbstractBaseUser):
    email = models.EmailField(unique=True)
    ho_ten = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = NguoiDungManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ho_ten']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff  

    def has_module_perms(self, app_label):
        return self.is_staff


class Phim(models.Model):
    id = models.BigAutoField(primary_key=True)  # Đảm bảo id là BIGINT
    tieu_de = models.CharField(max_length=100)
    the_loai = models.CharField(max_length=50)
    thoi_luong = models.IntegerField()
    ngay_phat_hanh = models.DateField()
    anh_phim = models.ImageField(upload_to='phim/') 
    dao_dien = models.CharField(max_length=100)

    is_now_showing = models.BooleanField(default=False)
    coming_soon = models.BooleanField(default=False)
    tomtatphim = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tieu_de


class RapChieu(models.Model):
    id = models.AutoField(primary_key=True)  # INT tự động tăng
    ten_rap = models.CharField(max_length=100)
    dia_chi = models.TextField()

    def __str__(self):
        return self.ten_rap


class LichChieu(models.Model):
    id = models.BigAutoField(primary_key=True)  # Đồng bộ kiểu với `Phim`
    phim = models.ForeignKey(Phim, on_delete=models.CASCADE)
    rap = models.ForeignKey(RapChieu, on_delete=models.CASCADE)
    ngay_chieu = models.DateField()
    gio_chieu = models.TimeField()

    def __str__(self):
        return f"{self.phim.tieu_de} - {self.rap.ten_rap} ({self.ngay_chieu} {self.gio_chieu})"


class Ve(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    lich_chieu = models.ForeignKey(LichChieu, on_delete=models.CASCADE)
    so_ghe = models.IntegerField()
    gia_ve = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vé {self.nguoi_dung.email} - {self.lich_chieu.phim.tieu_de} ({self.so_ghe} ghế)"


class DanhGia(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    phim = models.ForeignKey(Phim, on_delete=models.CASCADE)
    diem_danh_gia = models.PositiveSmallIntegerField()
    binh_luan = models.TextField()
    ngay_danh_gia = models.DateTimeField(auto_now_add=True)


class QuanTriVien(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)


class ChiNhanh(models.Model):
    ten_chi_nhanh = models.CharField(max_length=100)
    dia_chi = models.TextField()

    def __str__(self):
        return self.ten_chi_nhanh
