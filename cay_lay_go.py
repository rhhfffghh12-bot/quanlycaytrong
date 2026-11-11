
from datetime import datetime
from math import pi
from Cay_trong import CayTrong

class CayLayGo(CayTrong):

    def __init__(self, ma_cay, ten_cay, ngay_trong,
                 so_luong, dien_tich, loai_go,
                 chieu_cao, duong_kinh_than,
                 chu_ky_khai_thac):

        super().__init__(ma_cay, ten_cay, ngay_trong,
            so_luong, dien_tich)

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
        print("Chu ky khai thac:",
              self.chu_ky_khai_thac, "nam")

    def cap_nhat_sinh_truong(self, chieu_cao_moi,
                            duong_kinh_moi):

        if chieu_cao_moi <= 0 or duong_kinh_moi <= 0:
            print("Chieu cao hoac duong kinh khong hop le!")
            return False

        self.chieu_cao = chieu_cao_moi
        self.duong_kinh_than = duong_kinh_moi

        print("Cap nhat sinh truong thanh cong!")
        return True

    def kiem_tra_khai_thac(self):

        so_ngay = self.tinh_tuoi_cay()

        so_ngay_can = self.chu_ky_khai_thac * 365

        if so_ngay >= so_ngay_can:
            return True

        return False

    def tinh_the_tich_go(self):

        duong_kinh_m = self.duong_kinh_than / 100

        ban_kinh = duong_kinh_m / 2

        the_tich_mot_cay = (pi * ban_kinh ** 2 * self.chieu_cao)

        tong_the_tich = the_tich_mot_cay * self.so_luong

        return tong_the_tich

    def du_kien_khai_thac(self):

        ngay_bat_dau = datetime.strptime(self.ngay_trong, "%d/%m/%Y")

        nam_khai_thac = (ngay_bat_dau.year + self.chu_ky_khai_thac)

        try:
            ngay_du_kien = ngay_bat_dau.replace(year=nam_khai_thac)
        except ValueError:
            ngay_du_kien = ngay_bat_dau.replace(
                year=nam_khai_thac,
                day=28
            )

        return ngay_du_kien.strftime("%d/%m/%Y")
