from datetime import datetime


class CayTrong:
    def __init__(self, ma_cay, ten_cay, ngay_trong,
                 so_luong, dien_tich, trang_thai="Dang phat trien"):

        self.ma_cay = ma_cay
        self.ten_cay = ten_cay
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
        if so_luong < 0 or dien_tich <= 0:
            print("So luong hoac dien tich khong hop le!")
            return False

        self.ten_cay = ten_cay
        self.so_luong = so_luong
        self.dien_tich = dien_tich

        print("Cap nhat thanh cong!")
        return True

    def tinh_tuoi_cay(self):
        ngay_bat_dau = datetime.strptime(self.ngay_trong, "%d/%m/%Y")
        ngay_hien_tai = datetime.now()

        so_ngay = (ngay_hien_tai - ngay_bat_dau).days
        return max(0, so_ngay)

    def cap_nhat_trang_thai(self, trang_thai_moi):
        self.trang_thai = trang_thai_moi
        print("Da cap nhat trang thai!")


