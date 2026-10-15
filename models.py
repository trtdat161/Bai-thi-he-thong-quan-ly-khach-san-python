
class Phong:
    def __init__(self, ma_phong, ten_phong, gia_co_ban, trang_thai="Trống"):
        self.ma_phong = ma_phong
        self.ten_phong = ten_phong
        self.gia_co_ban = float(gia_co_ban)
        
        # protected
        self._trang_thai = trang_thai
        
    @property
    def trang_thai(self):
        return self._trang_thai
    
    def dat_phong(self):
        if self._trang_thai != "Trống":
            raise ValueError("Phòng đã được thuê")
        
        self._trang_thai = "Đã thuê"
        
    def tra_phong(self):
        if self._trang_thai != "Đã thuê":
            raise ValueError("Phòng chưa được thuê")
        
        self._trang_thai = "Trống"
        
    def tinh_tien(self, so_ngay):
        raise NotImplementedError("Phương thức này lớp con sẽ thực hiện cụ thể")
    
    # to_dict là để chuyển đổi object thành dict để dễ lưu file json
    def to_dict(self):
        return {
            "loai": self.__class__.__name__,
            "ma_phong": self.ma_phong,
            "ten_phong": self.ten_phong,
            "gia_co_ban": self.gia_co_ban,
            "trang_thai": self._trang_thai
        }
        
# lớp con là PhongThuong
class PhongThuong(Phong):
    def tinh_tien(self, so_ngay):
        if so_ngay <= 0:
            raise ValueError("Số ngày phải lớn hơn 0")
        return self.gia_co_ban * so_ngay

class PhongVIP(Phong):
    def __init__(self, ma_phong, ten_phong, gia_co_ban, phi_don_dep, phi_minibar, trang_thai="Trống"):
        super().__init__(ma_phong, ten_phong, gia_co_ban, trang_thai)
        # 
        self.phi_don_dep = float(phi_don_dep)
        self.phi_minibar = float(phi_minibar)

    def tinh_tien(self, so_ngay):
        if so_ngay <= 0:
            raise ValueError("Số ngày phải lớn hơn 0")
        return (
            self.gia_co_ban * so_ngay + self.phi_don_dep + self.phi_minibar # phòng víp thì + thêm phí dọn dẹp và minibar
        )
        
    def to_dict(self):
        data = super().to_dict() # to_dict của thằng cha
        data["phi_don_dep"] = self.phi_don_dep
        data["phi_minibar"] = self.phi_minibar
        return data
    
class KhachHang:
    def __init__(self, ma_khach, ten, cccd):
        self.ma_khach = ma_khach
        self.ten = ten
        self.cccd = cccd
    
    def to_dict(self):
        return {
            "ma_khach": self.ma_khach,
            "ten": self.ten,
            "cccd": self.cccd
        }
        
class PhieuThue:
    def __init__(self, khach_hang, phong, so_ngay):
        self.khach_hang = khach_hang
        self.phong = phong
        self.so_ngay = so_ngay
        
    def tinh_tong_tien(self, so_ngay=None):
        # Giữ tương thích với services.py đang gọi phieu.tinh_tong_tien(phieu.so_ngay)
        if so_ngay is None:
            so_ngay = self.so_ngay
        return self.phong.tinh_tien(so_ngay)
    
    def to_dict(self):
        return {
            "khach_hang": self.khach_hang.to_dict(),
            "ma_phong": self.phong.ma_phong,
            "so_ngay": self.so_ngay
        }