import json
import os

from models import Phong, PhongThuong, PhongVIP, KhachHang, PhieuThue





TEN_FILE = os.path.join(os.path.dirname(__file__), "khachsan_data.json")

def save_data(danh_sach_phong, danh_sach_phieu, lich_su):
    """Lưu dữ liệu khách sạn vào json file"""
    
    data = {
        "danh_sach_phong": [
            item.to_dict() for item in danh_sach_phong
        ],
        "danh_sach_phieu": [
            item.to_dict() for item in danh_sach_phieu
        ],
        "lich_su": lich_su or []
    }
    try:
        with open(TEN_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("Dữ liệu lưu thành công")
                
    except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
            raise 
        
def _tao_phong(item):
    loai = item.get("loai")
    if loai == "PhongThuong":
        return PhongThuong(item["ma_phong"], item["ten_phong"],
                           item["gia_co_ban"], item["trang_thai"])
    if loai == "PhongVIP":
        return PhongVIP(item["ma_phong"], item["ten_phong"], item["gia_co_ban"],
                        item["phi_don_dep"], item["phi_minibar"], item["trang_thai"])
    raise ValueError(f"Loại phòng không hợp lệ: {loai}")


def load_data():
    """Load dữ liệu khách sạn từ json file"""
    if not os.path.exists(TEN_FILE):
        return [], [], []

    try:
        with open(TEN_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"file json ko hợp lệ: {e}") from e
    except OSError as e:
        raise ValueError(f"Lỗi khi đọc file: {e}") from e

    try:
        danh_sach_phong = [_tao_phong(i) for i in data.get("danh_sach_phong", [])]
        phong_theo_ma = {p.ma_phong: p for p in danh_sach_phong}

        danh_sach_phieu = []
        for item in data.get("danh_sach_phieu", []):
            kh = item["khach_hang"]
            khach_hang = KhachHang(kh["ma_khach"], kh["ten"], kh["cccd"])

            ma_phong = item["ma_phong"]
            if ma_phong not in phong_theo_ma:
                raise ValueError(f"Phòng với mã {ma_phong} không tồn tại trong danh sách phòng")

            danh_sach_phieu.append(
                PhieuThue(khach_hang, phong_theo_ma[ma_phong], item["so_ngay"])
            )

        lich_su = data.get("lich_su", [])
        if not isinstance(lich_su, list):
            raise ValueError("Dữ liệu lịch sử không hợp lệ")

        return danh_sach_phong, danh_sach_phieu, lich_su

    except KeyError as e:
        raise ValueError(f"Dữ liệu trong json không hợp lệ: {e}") from e