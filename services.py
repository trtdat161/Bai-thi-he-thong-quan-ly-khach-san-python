from models import PhongThuong, PhongVIP, KhachHang, PhieuThue
from file_handler import load_data, save_data
GIA_TOI_THIEU = 1000  # VNĐ/ngày


class QuanLyKhachSan:
    def __init__(self):
        self.danh_sach_phong = []
        self.danh_sach_phieu = []
        self.lich_su = []
        
    def tai_du_lieu(self):
       (self.danh_sach_phong, self.danh_sach_phieu, self.lich_su) = load_data()
       
    def luu_du_lieu(self):
        save_data(self.danh_sach_phong, self.danh_sach_phieu, self.lich_su)
        
    def tim_phong(self, ma_phong):
        for item in self.danh_sach_phong:
            if item.ma_phong == ma_phong:
                return item
        return None
    
    def tinh_tien(self, phong, so_ngay):
    # đa hình phong có thể là PhongThuong hoặc PhongVIP, mỗi lớp tự tính tiền theo cách riêng
        return phong.tinh_tien(so_ngay)
    
    def hien_thi_phong(self):
        if not self.danh_sach_phong:
            print("Danh sách phòng trống.")
            return
        
        print(" ======== Danh sách phòng ======== ")
        
        for phong in self.danh_sach_phong:
            loai = (
                "VIP" if isinstance(phong, PhongVIP) 
                      else "Thường"
            )
            
            print(
                f"Mã phòng: {phong.ma_phong}, Tên phòng: {phong.ten_phong}, "
                f"Loại: {loai}, Giá cơ bản: {phong.gia_co_ban}, "
                f"Trạng thái: {phong.trang_thai}"
            )
            
            if isinstance(phong, PhongVIP):
                print(
                    f"Phí dọn dẹp: {phong.phi_don_dep:,.0f} VNĐ, Phí minibar: {phong.phi_minibar:,.0f} VNĐ"
                )
                
    def them_phong(self, ma_phong, ten_phong, gia_co_ban, loai, phi_don_dep=None, phi_minibar=None):
        if not ma_phong.strip():
            raise ValueError("Mã phòng không được để trống")
        if not ten_phong.strip():
            raise ValueError("Tên phòng không được để trống")
        if any(phong.ma_phong == ma_phong for phong in self.danh_sach_phong):
            raise ValueError(f"Phòng với mã {ma_phong} đã tồn tại")
        if gia_co_ban < GIA_TOI_THIEU:
            raise ValueError(f"Giá cơ bản phải từ {GIA_TOI_THIEU:,.0f} VNĐ trở lên")
        
        # loại phòng: 1 là thường, 2 là VIP
        if loai == "1":
            phong = PhongThuong(ma_phong, ten_phong, gia_co_ban)
            
        elif loai == "2":
            if phi_don_dep is None or phi_minibar is None:
                raise ValueError("Phí dọn dẹp và phí minibar phải được cung cấp cho phòng VIP")
            for ten, phi in (("dọn dẹp", phi_don_dep), ("minibar", phi_minibar)):
                if phi < GIA_TOI_THIEU:
                    raise ValueError(f"Phí {ten} phải từ {GIA_TOI_THIEU:,.0f} VNĐ trở lên")
                    
            phong = PhongVIP(ma_phong, ten_phong, gia_co_ban, phi_don_dep, phi_minibar)
        else:
            raise ValueError("Loại phòng không hợp lệ")
        
        self.danh_sach_phong.append(phong)
        return phong
    
    def dat_phong(
        self,
        ma_phong,
        ma_khach,
        ten_khach,
        cccd,
        so_ngay
    ):
        phong = self.tim_phong(ma_phong)

        if phong is None:
            raise ValueError("Phòng không tồn tại")

        if phong.trang_thai != "Trống":
            raise ValueError("Phòng này đã được thuê")

        if not ma_khach.strip():
            raise ValueError("Mã khách không được để trống bro !")

        if not ten_khach.strip():
            raise ValueError("Tên khách không được để trống bro !")
        
        if not all(ch.isalpha() or ch.isspace() for ch in ten_khach):
            raise ValueError("Tên khách chỉ được chứa chữ cái và khoảng trắng")

        if not cccd.strip():
            raise ValueError("cccd/cmnd không được để trống bro !")
        
        if not (cccd.isascii() and cccd.isdigit() and len(cccd) in (9, 12)):
            raise ValueError("CCCD/CMND phải gồm 9 hoặc 12 chữ số")

        if so_ngay <= 0:
            raise ValueError("Số ngày thuê phải lớn hơn 0")

        # Chỉ đổi trạng thái sau khi đã kiểm tra dữ liệu.
        khach = KhachHang(ma_khach, ten_khach, cccd)
        phieu = PhieuThue(khach, phong, so_ngay)

        phong.dat_phong()
        self.danh_sach_phieu.append(phieu)

        return phieu
    
    # bổ sung câu 4 thêm func trả phòng
    def tra_phong(self, ma_phong):
        phong = self.tim_phong(ma_phong)
        if phong is None:
            raise ValueError("Phòng không tồn tại")

        if phong.trang_thai != "Đã thuê":
            raise ValueError("Phòng này hiện không được thuê bro ơiii!")
        
        phieu = next((p for p in self.danh_sach_phieu if p.phong.ma_phong == ma_phong), None)
        
        if phieu is None:
            raise ValueError("Không tìm thấy phiếu thuê cho phòng này")
        
        tong_tien = self.tinh_tien(phieu.phong, phieu.so_ngay)
        
        # ghi nhận doanh thu trước khi đưa vào lịch sử
        phieu.doanh_thu = tong_tien
        
        self.lich_su.append({
            "ma_phong": phieu.phong.ma_phong,
            "ten_phong": phieu.phong.ten_phong,
            "ma_khach": phieu.khach_hang.ma_khach,
            "ten_khach": phieu.khach_hang.ten,
            "so_ngay": phieu.so_ngay,
            "tong_tien": tong_tien
        })

        phong.tra_phong()
        self.danh_sach_phieu.remove(phieu)

        return phieu, tong_tien
    
    def bao_cao_doanh_thu(self):
        tong_doanh_thu = sum(item["tong_tien"] for item in self.lich_su)
        
        so_phong_trong = sum(1 for phong in self.danh_sach_phong if phong.trang_thai == "Trống")
        print("----- tỔng số phòng -------")
        print(f"Tổng số phòng: {len(self.danh_sach_phong)}")
        print(f"Số phòng trống: {so_phong_trong}")
        print(f"số phòng đang thuê: {len(self.danh_sach_phong) - so_phong_trong}")
        
        print(f"Số phiếu đã thanh toán: {len(self.lich_su)}")
        print(f"Tổng doanh thu: {tong_doanh_thu:,.0f} VNĐ")

        if self.lich_su:
            print("\n--- Lịch sử thanh toán ---")

            for item in self.lich_su:
                print(
                    f"Phòng {item['ma_phong']} | "
                    f"Khách: {item['ten_khach']} | "
                    f"{item['so_ngay']} ngày | "
                    f"{item['tong_tien']:,.0f} VNĐ"
                )

        return tong_doanh_thu