from datetime import datetime, timedelta
from math import pi


class CayTrong:
    def __init__(self, ma_cay, ten_cay, ngay_trong,
                 so_luong, dien_tich, trang_thai="Dang phat trien"):

        if not ma_cay.strip() or not ten_cay.strip():
            raise ValueError("Ma cay va ten cay khong duoc rong!")

        if so_luong <= 0:
            raise ValueError("So luong cay phai lon hon 0!")

        if dien_tich <= 0:
            raise ValueError("Dien tich phai lon hon 0!")

        ngay = datetime.strptime(ngay_trong, "%d/%m/%Y")

        if ngay.date() > datetime.now().date():
            raise ValueError("Ngay trong khong duoc lon hon ngay hien tai!")

        self.ma_cay = ma_cay.strip()
        self.ten_cay = ten_cay.strip()
        self.ngay_trong = ngay_trong
        self.so_luong = so_luong
        self.dien_tich = dien_tich
        self.trang_thai = trang_thai

    def hien_thi(self):
        print("Ma cay:", self.ma_cay)
        print("Ten cay:", self.ten_cay)
        print("Ngay trong:", self.ngay_trong)
        print("So luong:", self.so_luong)
        print("Dien tich:", self.dien_tich, "m2")
        print("Trang thai:", self.trang_thai)

    def cap_nhat(self, ten_cay, so_luong, dien_tich):
        if not ten_cay.strip():
            print("Ten cay khong duoc de trong!")
            return False

        if so_luong <= 0 or dien_tich <= 0:
            print("So luong va dien tich phai lon hon 0!")
            return False

        self.ten_cay = ten_cay.strip()
        self.so_luong = so_luong
        self.dien_tich = dien_tich

        print("Cap nhat thanh cong!")
        return True

    def tinh_tuoi_cay(self):
        ngay_bat_dau = datetime.strptime(self.ngay_trong, "%d/%m/%Y").date()
        ngay_hien_tai = datetime.now().date()
        so_ngay = (ngay_hien_tai - ngay_bat_dau).days
        return max(0, so_ngay)

    def cap_nhat_trang_thai(self, trang_thai_moi):
        self.trang_thai = trang_thai_moi
        print("Da cap nhat trang thai!")


class CayAnQua(CayTrong):
    def __init__(self, ma_cay, ten_cay, ngay_trong,
                 so_luong, dien_tich, loai_qua,
                 mua_thu_hoach, thoi_gian_cho_qua,
                 san_luong=0):
        super().__init__(ma_cay, ten_cay, ngay_trong, so_luong, dien_tich)

        if thoi_gian_cho_qua < 0 or san_luong < 0:
            raise ValueError("Thoi gian hoac san luong khong hop le!")

        self.loai_qua = loai_qua
        self.mua_thu_hoach = mua_thu_hoach
        self.thoi_gian_cho_qua = thoi_gian_cho_qua
        self.san_luong = san_luong

    def hien_thi(self):
        print("\n===== THONG TIN CAY AN QUA =====")
        super().hien_thi()
        print("Loai qua:", self.loai_qua)
        print("Mua thu hoach:", self.mua_thu_hoach)
        print("Thoi gian cho qua:", self.thoi_gian_cho_qua, "ngay")
        print("San luong:", self.san_luong, "kg")

    def ghi_nhan_thu_hoach(self, so_kg):
        if so_kg <= 0:
            print("San luong thu hoach phai lon hon 0!")
            return False
        self.san_luong += so_kg
        print("Ghi nhan thu hoach thanh cong! Tong san luong:", self.san_luong, "kg")
        return True

    def tinh_nang_suat(self):
        if self.so_luong <= 0:
            return 0
        return self.san_luong / self.so_luong

    def du_kien_thu_hoach(self):
        ngay_bat_dau = datetime.strptime(self.ngay_trong, "%d/%m/%Y")
        ngay_du_kien = ngay_bat_dau + timedelta(days=self.thoi_gian_cho_qua)
        return ngay_du_kien.strftime("%d/%m/%Y")

    def cap_nhat_mua_thu_hoach(self, mua_moi):
        self.mua_thu_hoach = mua_moi
        print("Cap nhat mua thu hoach thanh cong!")


class CayLayGo(CayTrong):
    def __init__(self, ma_cay, ten_cay, ngay_trong,
                 so_luong, dien_tich, loai_go,
                 chieu_cao, duong_kinh_than,
                 chu_ky_khai_thac):
        super().__init__(ma_cay, ten_cay, ngay_trong, so_luong, dien_tich)

        if chieu_cao <= 0 or duong_kinh_than <= 0:
            raise ValueError("Chieu cao va duong kinh phai lon hon 0!")
        if chu_ky_khai_thac <= 0:
            raise ValueError("Chu ky khai thac phai lon hon 0!")

        self.loai_go = loai_go
        self.chieu_cao = chieu_cao
        self.duong_kinh_than = duong_kinh_than
        self.chu_ky_khai_thac = chu_ky_khai_thac

    def hien_thi(self):
        print("\n===== THONG TIN CAY LAY GO =====")
        super().hien_thi()
        print("Loai go:", self.loai_go)
        print("Chieu cao trung binh:", self.chieu_cao, "m")
        print("Duong kinh than:", self.duong_kinh_than, "cm")
        print("Chu ky khai thac:", self.chu_ky_khai_thac, "nam")

    def cap_nhat_sinh_truong(self, chieu_cao_moi, duong_kinh_moi):
        if chieu_cao_moi <= 0 or duong_kinh_moi <= 0:
            print("Chieu cao hoac duong kinh khong hop le!")
            return False
        self.chieu_cao = chieu_cao_moi
        self.duong_kinh_than = duong_kinh_moi
        print("Cap nhat sinh truong thanh cong!")
        return True

    def kiem_tra_khai_thac(self):
        ngay_khai_thac = datetime.strptime(self.du_kien_khai_thac(), "%d/%m/%Y").date()
        ngay_hien_tai = datetime.now().date()
        return ngay_hien_tai >= ngay_khai_thac

    def tinh_the_tich_go(self):
        duong_kinh_m = self.duong_kinh_than / 100
        ban_kinh = duong_kinh_m / 2
        the_tich_mot_cay = pi * (ban_kinh ** 2) * self.chieu_cao
        return the_tich_mot_cay * self.so_luong

    def du_kien_khai_thac(self):
        ngay_bat_dau = datetime.strptime(self.ngay_trong, "%d/%m/%Y")
        nam_khai_thac = ngay_bat_dau.year + self.chu_ky_khai_thac
        try:
            ngay_du_kien = ngay_bat_dau.replace(year=nam_khai_thac)
        except ValueError:
            ngay_du_kien = ngay_bat_dau.replace(year=nam_khai_thac, day=28)
        return ngay_du_kien.strftime("%d/%m/%Y")


class QuanLy:
    def __init__(self):
        self.ds_cay_trong = []

        self.tai_khoan_admin = "HuyDuyDat"
        self.mat_khau_admin = "BaConHeo"

    def them_cay(self, cay):
        if not isinstance(cay, (CayAnQua, CayLayGo)):
            print("Chi chap nhan CayAnQua hoac CayLayGo!")
            return False
        if self.tim_cay(cay.ma_cay) is not None:
            print("Ma cay da ton tai!")
            return False
        if not cay.ma_cay.strip() or not cay.ten_cay.strip():
            print("Ma cay va ten cay khong duoc rong!")
            return False

        self.ds_cay_trong.append(cay)
        return True

    def tim_cay(self, ma_cay):
        for cay in self.ds_cay_trong:
            if cay.ma_cay == ma_cay:
                return cay
        return None

    def sua_cay(self, ma_cay, ten_moi, so_luong_moi, dien_tich_moi):
        cay = self.tim_cay(ma_cay)
        if cay is None:
            print("Khong tim thay cay!")
            return False
        return cay.cap_nhat(ten_moi, so_luong_moi, dien_tich_moi)

    def xoa_cay(self, ma_cay):
        cay = self.tim_cay(ma_cay)
        if cay is None:
            print("Khong tim thay cay can xoa!")
            return False

        self.ds_cay_trong.remove(cay)
        print("Xoa cay thanh cong!")
        return True

    def hien_thi_ds_cay(self):
        if not self.ds_cay_trong:
            print("Danh sach cay trong dang rong!")
            return

        print("\n===============================================================================================")
        print(f"{'DANH SACH CAY TRONG':^90}")
        print("===============================================================================================")
        print(
            f"{'Ma Cay':<8} | {'Ten Cay':<22} | {'Loai':<12} | {'Ngay Trong':<12} | {'So Luong':<10} | {'Dien Tich (m2)':<15}")
        print("-" * 95)

        for cay in self.ds_cay_trong:
            loai = "Cay An Qua" if isinstance(cay, CayAnQua) else "Cay Lay Go"
            print(
                f"{cay.ma_cay:<8} | {cay.ten_cay:<22} | {loai:<12} | {cay.ngay_trong:<12} | {cay.so_luong:<10} | {cay.dien_tich:<15}")

        print("===============================================================================================")

    def thong_ke_so_luong(self):
        so_lo_an_qua = so_lo_lay_go = so_cay_an_qua = so_cay_lay_go = 0
        for cay in self.ds_cay_trong:
            if isinstance(cay, CayAnQua):
                so_lo_an_qua += 1
                so_cay_an_qua += cay.so_luong
            elif isinstance(cay, CayLayGo):
                so_lo_lay_go += 1
                so_cay_lay_go += cay.so_luong

        print("\n===== THONG KE CAY TRONG =====")
        print("So nhom cay an qua:", so_lo_an_qua)
        print("So nhom cay lay go:", so_lo_lay_go)
        print("Tong cay an qua:", so_cay_an_qua)
        print("Tong cay lay go:", so_cay_lay_go)
        print("Tong so cay:", so_cay_an_qua + so_cay_lay_go)

    def thong_ke_thu_hoach(self):
        tong_san_luong = sum(cay.san_luong for cay in self.ds_cay_trong if isinstance(cay, CayAnQua))
        print("\nTong san luong qua:", tong_san_luong, "kg")
        return tong_san_luong

    def thong_ke_go(self):
        tong_the_tich = sum(cay.tinh_the_tich_go() for cay in self.ds_cay_trong if isinstance(cay, CayLayGo))
        print("\nTong the tich hinh tru uoc tinh:", round(tong_the_tich, 2), "m3")
        return tong_the_tich

    def bao_cao_tong_hop(self):
        print("\n========== BAO CAO TONG HOP ==========")
        self.thong_ke_so_luong()
        self.thong_ke_thu_hoach()
        self.thong_ke_go()
        print("\n======================================")


    def khoi_tao_du_lieu_mau(ql):
    # 3 Cây ăn quả mẫu
        cay1 = CayAnQua("AQ01", "Xoai Cat Hoa Loc", "15/03/2022", 50, 250.0, "Xoai", "Mua He", 730, 1200.0)
        cay2 = CayAnQua("AQ02", "Sau Rieng Monthong", "10/05/2021", 30, 300.0, "Sau Rieng", "Mua Mua", 1460, 850.0)
        cay3 = CayAnQua("AQ03", "Cam Sanh", "20/08/2023", 100, 200.0, "Cam", "Mua Thu", 365, 1500.0)
        ql.them_cay(cay1)
        ql.them_cay(cay2)
        ql.them_cay(cay3)

    # 3 Cây lấy gỗ mẫu
        cay4 = CayLayGo("LG01", "Cay Keo La Tram", "12/01/2018", 200, 1000.0, "Go Keo", 12.5, 25.0, 7)
        cay5 = CayLayGo("LG02", "Cay Bach Dan", "05/06/2019", 150, 800.0, "Go Bach Dan", 15.0, 22.0, 8)
        cay6 = CayLayGo("LG03", "Cay Go Te", "18/10/2015", 50, 500.0, "Go Quy", 18.0, 35.0, 15)
        ql.them_cay(cay4)
        ql.them_cay(cay5)
        ql.them_cay(cay6)


def nhap_lua_chon(nho_nhat, lon_nhat):
    while True:
        try:
            chon = int(input("Nhap lua chon: "))
            if nho_nhat <= chon <= lon_nhat:
                return chon
        except ValueError:
            pass
        print(f"Vui long nhap so tu {nho_nhat} den {lon_nhat}.")


def nhap_so(nhan, kieu=float):
    while True:
        try:
            return kieu(input(f"{nhan}: "))
        except ValueError:
            print("Vui long nhap so hop le.")


def menu_cay(ql):
    while True:
        print("\n--- QUAN LY CAY TRONG ---")
        print("1. Them cay")
        print("2. Hien thi danh sach cay")
        print("3. Tim cay")
        print("4. Sua cay")
        print("5. Xoa cay")
        print("0. Quay lai")
        chon = nhap_lua_chon(0, 5)
        if chon == 0:
            return
        try:
            if chon == 1:
                print("\n--- Chon loai cay ---")
                print("1. Cay an qua.")
                print("2. Cay lay go.")
                chon_cay = str(nhap_lua_chon(1, 2))
                chung = (input("Ma cay: ").strip(), input("Ten cay: ").strip(),
                         input("Ngay trong (dd/mm/yyyy): ").strip(),
                         nhap_so("So luong", int), nhap_so("Dien tich (m2)"))
                if chon_cay == "1":
                    cay = CayAnQua(*chung, input("Loai qua: "), input("Mua thu hoach: "),
                                   nhap_so("Thoi gian cho qua (ngay)", int),
                                   nhap_so("San luong (kg)"))
                elif chon_cay == "2":
                    cay = CayLayGo(*chung, input("Loai go: "), nhap_so("Chieu cao (m)"),
                                   nhap_so("Duong kinh than (cm)"),
                                   nhap_so("Chu ky khai thac (nam)", int))
                else:
                    print("Lua chon khong hop le!")
                    continue
                if ql.them_cay(cay):
                    print("Them cay trong thanh cong!")
            elif chon == 2:
                ql.hien_thi_ds_cay()
            elif chon == 3:
                cay = ql.tim_cay(input("Ma cay: ").strip())
                if cay is None:
                    print("Khong tim thay cay!")
                else:
                    cay.hien_thi()
            elif chon == 4:
                ql.sua_cay(input("Ma cay: ").strip(), input("Ten moi: ").strip(),
                           nhap_so("So luong moi", int), nhap_so("Dien tich moi"))
            elif chon == 5:
                ql.xoa_cay(input("Ma cay: ").strip())
        except ValueError as loi:
            print("LOI:", loi)


def menu_thong_ke(ql):
    while True:
        print("\n--- THONG KE & BAO CAO ---")
        print("1. So luong cay")
        print("2. San luong qua")
        print("3. The tich go")
        print("4. Bao cao tong hop")
        print("0. Quay lai")
        chon = nhap_lua_chon(0, 4)
        if chon == 0:
            return
        bao_cao = {
            1: ql.thong_ke_so_luong,
            2: ql.thong_ke_thu_hoach,
            3: ql.thong_ke_go,
            4: ql.bao_cao_tong_hop,
        }
        bao_cao[chon]()

def dang_nhap(self):
    so_lan_sai = 3
    print("\n================ ĐĂNG NHẬP HỆ THỐNG QUẢN LÝ CÂY TRỒNG ================")
    for i in range(so_lan_sai):
        print(f"Bạn còn {so_lan_sai - i} lần thử.")
        tk = input("Nhập tên tài khoản: ")
        mk = input("Nhập mật khẩu: ")

        if tk == self.tai_khoan_admin and mk == self.mat_khau_admin:
            print("-> Đăng nhập quyền Admin thành công! Chào mừng bạn đến với hệ thống.")
            return True
        else:
            print("-> Tài khoản hoặc mật khẩu không chính xác. Vui lòng thử lại!\n")

    print("-> Bạn đã nhập sai quá 3 lần. Hệ thống tự động thoát bảo mật!")
    return False

def main():
    ql = QuanLy()
    if not dang_nhap(ql):
        return
    ql.khoi_tao_du_lieu_mau()

    while True:
        print("\n========== QUAN LY CAY TRONG ==========")
        print("1. Quan ly cay trong")
        print("2. Bao cao va thong ke")
        print("0. Thoat chuong trinh")

        chon = nhap_lua_chon(0, 2)
        if chon == 0:
            print("Cam on ban da su dung chuong trinh!")
            break
        elif chon == 1:
            menu_cay(ql)
        elif chon == 2:
            menu_thong_ke(ql)


if __name__ == "__main__":
    main()
