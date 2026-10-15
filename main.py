
# import models
# print("models đang dùng:", models.__file__)
# import inspect
# print(inspect.getsource(models.PhongThuong))


from services import QuanLyKhachSan


def nhap_so(thong_bao, kieu=float):
    while True:
        try:
            giatri = kieu(input(thong_bao).strip())
            return giatri
        except ValueError:
            print(f"Dữ liệu không hợp lệ, xin nhập lại: ")
            
def nhap_chuoi(thong_bao):
    return input(thong_bao).strip()

def them_phong(ql): # ql là quản ký khách sạn viết tắt
    print("----- Thêm phòng mới -----")
    
    ma_phong = nhap_chuoi("Nhập mã phòng: ")
    ten_phong = nhap_chuoi("Nhập tên phòng: ")
    gia_co_ban = nhap_so("Nhập giá cơ bản/ngày: ", float)
    
    print("1. Phòng thường")
    print("2. Phòng VIP")

    loai = nhap_chuoi("Chọn loại phòng: ")
    
    phi_don_dep = 0
    phi_minibar = 0
    
    if loai == "2":
        phi_don_dep = nhap_so("Nhập phí dọn dẹp: ", float)
        phi_minibar = nhap_so("Nhập phí minibar: ", float)
        
    phong = ql.them_phong(
        ma_phong,
        ten_phong,
        gia_co_ban,
        loai,
        phi_don_dep,
        phi_minibar
    )

    print(f"Đã thêm phòng {phong.ma_phong} thành công!")
    
    
def dat_phong(ql):
    print("------ Đặt phòng ------")
    
    ma_phong = nhap_chuoi("nhập mã phòng cần đặt:")
    ma_khach = nhap_chuoi("nhập mã khách: ")
    ten_khach = nhap_chuoi("Nhập tên khách: ")
    cccd = nhap_chuoi("Nhập số CCCD/CMND: ")
    so_ngay = nhap_so("Nhập số ngày thuê: ", int)

    phieu = ql.dat_phong(
        ma_phong,
        ma_khach,
        ten_khach,
        cccd,
        so_ngay
    )
    
    print(
        f"Đặt phòng thành công: {phieu.phong.ma_phong} | "
        f"Khách: {phieu.khach_hang.ten} | "
        f"Số ngày: {phieu.so_ngay}"
    )
    

def tra_phong(ql):
    print(" ------- Trả phòng & Thanh toán ------- ")

    ma_phong = nhap_chuoi("Nhập mã phòng cần trả: ")

    phieu, tong_tien = ql.tra_phong(ma_phong)

    print("\nThanh toán thành công!")
    print(f"Mã phòng: {phieu.phong.ma_phong}")
    print(f"Tên khách: {phieu.khach_hang.ten}")
    print(f"Loại phòng: {phieu.phong.__class__.__name__}")
    print(f"Số ngày thuê: {phieu.so_ngay}")
    print(f"Giá cơ bản/ngày: {phieu.phong.gia_co_ban:,.0f} VNĐ")

    if phieu.phong.__class__.__name__ == "PhongVIP":
        print(
            f"Phí dọn dẹp: "
            f"{phieu.phong.phi_don_dep:,.0f} VNĐ"
        )
        print(
            f"Phí minibar: "
            f"{phieu.phong.phi_minibar:,.0f} VNĐ"
        )

    print(f"TỔNG THANH TOÁN: {tong_tien:,.0f} VNĐ")

def menu():
    print("\n" + "=" * 42)
    print("       HỆ THỐNG QUẢN LÝ KHÁCH SẠN")
    print("=" * 42)
    print("1. Hiển thị danh sách phòng")
    print("2. Thêm phòng mới")
    print("3. Đặt phòng")
    print("4. Trả phòng & Thanh toán")
    print("5. Xem báo cáo doanh thu")
    print("0. Thoát & Lưu dữ liệu")
    print("=" * 42)
    
# hàm chính
def main():
    
    ql = QuanLyKhachSan()
    
    try: 
        ql.tai_du_lieu()
        
    except (OSError, ValueError) as e:
        print(f"Không thể tải dữ liệu: {e}")
        return
    
    print(f"Đã tải dữ liệu khách sạn. Số phòng hiện có: {len(ql.danh_sach_phong)} ")
    while True:
        menu()
        lua_chon = nhap_chuoi("Nhập lựa chọn: ")

        try:
            if lua_chon == "1":
                ql.hien_thi_phong()

            elif lua_chon == "2":
                them_phong(ql)
                ql.luu_du_lieu()

            elif lua_chon == "3":
                dat_phong(ql)
                ql.luu_du_lieu()

            elif lua_chon == "4":
                tra_phong(ql)
                ql.luu_du_lieu()

            elif lua_chon == "5":
                ql.bao_cao_doanh_thu()

            elif lua_chon == "0":
                ql.luu_du_lieu()
                print("Đã lưu dữ liệu. Tạm biệt!")
                break

            else:
                print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")

        except (ValueError, OSError) as e:
            print(f"Không thể thực hiện thao tác: {e}")

        except Exception as e:
            # Bắt lỗi ngoài dự kiến để CLI không thoát đột ngột.
            print(f"Đã xảy ra lỗi ngoài dự kiến: {e}")


if __name__ == "__main__":
    main()
