
from datetime import datetime, timedelta
from Cay_trong import CayTrong

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
        print("Thoi gian cho qua:",self.thoi_gian_cho_qua, "ngay")
        print("San luong:", self.san_luong, "kg")

    def ghi_nhan_thu_hoach(self, so_kg):
        if so_kg <= 0:
            print("San luong thu hoach phai lon hon 0!")
            return False

        self.san_luong += so_kg

        print("Ghi nhan thu hoach thanh cong!")
        print("Tong san luong:", self.san_luong, "kg")
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


