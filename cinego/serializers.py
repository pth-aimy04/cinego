from rest_framework import serializers
from .models import NguoiDung, Phim, Ve, DanhGia, QuanTriVien, RapChieu, LichChieu
from django.contrib.auth import get_user_model

User = get_user_model()

class DangKySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "ho_ten", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            ho_ten=validated_data["ho_ten"]
        )
        return user

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = '__all__'

class PhimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phim
        fields = '__all__'

class VeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ve
        fields = '__all__'

class DanhGiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGia
        fields = '__all__'

class QuanTriVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuanTriVien
        fields = '__all__'

class RapChieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapChieu
        fields = '__all__'

class LichChieuSerializer(serializers.ModelSerializer):  # Thêm lịch chiếu
    class Meta:
        model = LichChieu
        fields = '__all__'
