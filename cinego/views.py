from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import models
from .models import NguoiDung, Phim, Ve, DanhGia, QuanTriVien, RapChieu, LichChieu
from .serializers import (
    NguoiDungSerializer,
    PhimSerializer,
    VeSerializer,
    DanhGiaSerializer,
    QuanTriVienSerializer,
    RapChieuSerializer,
    LichChieuSerializer,
    DangKySerializer,
)

# 🌟 Trang chủ
def homepage(request):
    now_showing = Phim.objects.filter(is_now_showing=True)
    coming_soon = Phim.objects.filter(coming_soon=True)

    return render(
        request,
        "homepage.html",
        {
            "now_showing": now_showing,
            "coming_soon": coming_soon,
        },
    )

# 🧑‍💻 API CRUD - Người dùng
class NguoiDungListCreate(generics.ListCreateAPIView):
    queryset = NguoiDung.objects.all()
    serializer_class = NguoiDungSerializer

# 🎬 API CRUD - Phim
class PhimListCreate(generics.ListCreateAPIView):
    queryset = Phim.objects.all()
    serializer_class = PhimSerializer

class PhimDetailView(RetrieveAPIView):
    queryset = Phim.objects.all()
    serializer_class = PhimSerializer

# 🎟️ API CRUD - Vé
class VeListCreate(generics.ListCreateAPIView):
    queryset = Ve.objects.all()
    serializer_class = VeSerializer

# ⭐ API CRUD - Đánh giá
class DanhGiaListCreate(generics.ListCreateAPIView):
    queryset = DanhGia.objects.all()
    serializer_class = DanhGiaSerializer

# 🔧 API CRUD - Quản trị viên
class QuanTriVienListCreate(generics.ListCreateAPIView):
    queryset = QuanTriVien.objects.all()
    serializer_class = QuanTriVienSerializer

# 🏢 API CRUD - Chi nhánh
class RapChieuListCreate(generics.ListCreateAPIView):
    queryset = RapChieu.objects.all()
    serializer_class = RapChieuSerializer

# 🕒 API CRUD - Lịch Chiếu
class LichChieuListCreate(generics.ListCreateAPIView):
    queryset = LichChieu.objects.all()
    serializer_class = LichChieuSerializer

# 🎬 API đặc biệt: Lấy danh sách phim
@api_view(["GET", "POST"])
def phim_list(request):
    if request.method == "GET":
        phim = Phim.objects.all()
        serializer = PhimSerializer(phim, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PhimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔥 API Đăng nhập trả về JSON
@api_view(["POST"])
def dang_nhap_api(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)

    if user:
        login(request, user)
        return Response({"message": "Đăng nhập thành công!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Email hoặc mật khẩu không đúng!"}, status=status.HTTP_401_UNAUTHORIZED)

# 🌟 Đăng nhập giao diện HTML
def dang_nhap(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return redirect("home")  
        else:
            return render(request, "login.html", {"error": "Sai email hoặc mật khẩu!"})

    return render(request, "login.html")

# 🔐 API Đăng ký
class DangKyView(APIView):
    def post(self, request):
        serializer = DangKySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def so_ghe_con_trong(request, lich_chieu_id):
    try:
        lich_chieu = LichChieu.objects.get(id=lich_chieu_id)
        tong_ghe = 100  # Giả sử mỗi lịch chiếu có 100 ghế
        ghe_da_dat = Ve.objects.filter(lich_chieu=lich_chieu).aggregate(models.Sum("so_ghe"))["so_ghe__sum"] or 0
        ghe_con_trong = tong_ghe - ghe_da_dat
        return JsonResponse({"ghe_con_trong": ghe_con_trong})
    except LichChieu.DoesNotExist:
        return JsonResponse({"error": "Lịch chiếu không tồn tại"}, status=404)

def danh_sach_ghe(request, lichchieu_id):
    # Lấy danh sách số ghế đã đặt từ bảng Ve
    ghe_da_dat = list(Ve.objects.filter(lich_chieu_id=lichchieu_id).values_list('so_ghe', flat=True))

    # Giả sử mỗi rạp có 50 ghế (1 - 50)
    tat_ca_ghe = [
        {"id": i, "so_ghe": i, "da_dat": i in ghe_da_dat}
        for i in range(1, 51)
    ]

    return JsonResponse(tat_ca_ghe, safe=False)