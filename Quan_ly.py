
from datetime import datetime

from Cay_trong import CayTrong
from cay_an_qua import CayAnQua
from cay_lay_go import CayLayGo
from Cham_soc import ChamSoc

class QuanLy:

    def __init__(self):
        self.ds_cay_trong = []
        self.ds_cham_soc = []

    def them_cay(self, cay):
        if not isinstance(cay, (CayAnQua, CayLayGo)):
            print("Chi chap nhan CayAnQua hoac CayLayGo!")
            return False

        if self.tim_cay(cay.ma_cay) is not None:
            print("Ma cay da ton tai!")
            return False

        if cay.ma_cay.strip() == "" or cay.ten_cay.strip() == "":
            print("Ma cay va ten cay khong duoc rong!")
            return False

        if cay.so_luong < 0 or cay.dien_tich <= 0:
            print("So luong hoac dien tich khong hop le!")
            return False

        try:
            datetime.strptime(cay.ngay_trong, "%d/%m/%Y")
        except ValueError:
            print("Ngay trong khong hop le!")
            return False

        self.ds_cay_trong.append(cay)
        print("Them cay trong thanh cong!")
        return True

    def tim_cay(self, ma_cay):
        for cay in self.ds_cay_trong:
            if cay.ma_cay == ma_cay:
                return cay

        return None

    def tim_cay_theo_ten(self, ten_cay):
        ket_qua = []

        for cay in self.ds_cay_trong:
            if ten_cay.lower() in cay.ten_cay.lower():
                ket_qua.append(cay)

        return ket_qua

    def sua_cay(self, ma_cay, ten_moi,so_luong_moi, dien_tich_moi):

        cay = self.tim_cay(ma_cay)

        if cay is None:
            print("Khong tim thay cay!")
            return False

        if ten_moi.strip() == "":
            print("Ten cay khong duoc rong!")
            return False

        return cay.cap_nhat(ten_moi, so_luong_moi, dien_tich_moi)

    def xoa_cay(self, ma_cay):
        cay = self.tim_cay(ma_cay)

        if cay is None:
            print("Khong tim thay cay can xoa!")
            return False

        for cs in self.ds_cham_soc:
            if cs.ma_cay == ma_cay:
                print("Cay dang co du lieu cham soc!")
                print("Hay xu ly du lieu cham soc truoc.")
                return False

        self.ds_cay_trong.remove(cay)
        print("Xoa cay thanh cong!")
        return True

    def hien_thi_ds_cay(self):
        if len(self.ds_cay_trong) == 0:
            print("Danh sach cay trong dang rong!")
            return

        print("\n===== DANH SACH CAY TRONG =====")

        for cay in self.ds_cay_trong:
            cay.hien_thi()
            print("-" * 40)

    def sap_xep_theo_ten(self):
        self.ds_cay_trong.sort(key=lambda cay: cay.ten_cay.lower())

        print("Da sap xep cay theo ten A-Z!")

    def sap_xep_theo_so_luong(self):
        self.ds_cay_trong.sort(
            key=lambda cay: cay.so_luong,
            reverse=True
            )

        print("Da sap xep so luong giam dan!")

    def them_cham_soc(self, cs):

        if not isinstance(cs, ChamSoc):
            print("Doi tuong cham soc khong hop le!")
            return False

        if self.tim_cham_soc(cs.ma_cham_soc) is not None:
            print("Ma cham soc da ton tai!")
            return False

        if self.tim_cay(cs.ma_cay) is None:
            print("Khong tim thay ma cay can cham soc!")
            return False

        self.ds_cham_soc.append(cs)
        print("Them cong viec cham soc thanh cong!")
        return True

    def tim_cham_soc(self, ma_cham_soc):
        for cs in self.ds_cham_soc:
            if cs.ma_cham_soc == ma_cham_soc:
                return cs
            
        return None

    def sua_cham_soc(self, ma_cham_soc,ngay_moi, cong_viec_moi, chi_phi_moi):

        cs = self.tim_cham_soc(ma_cham_soc)

        if cs is None:
            print("Khong tim thay cong viec!")
            return False

        return cs.cap_nhat(ngay_moi, cong_viec_moi, chi_phi_moi)

    # Xoa cong viec cham soc
    def xoa_cham_soc(self, ma_cham_soc):
        cs = self.tim_cham_soc(ma_cham_soc)

        if cs is None:
            print("Khong tim thay cong viec can xoa!")
            return False

        self.ds_cham_soc.remove(cs)
        print("Xoa cong viec cham soc thanh cong!")
        return True

    def hoan_thanh_cham_soc(self, ma_cham_soc):
        cs = self.tim_cham_soc(ma_cham_soc)

        if cs is None:
            print("Khong tim thay cong viec!")
            return False

        return cs.hoan_thanh()

    def hien_thi_ds_cham_soc(self):
        if len(self.ds_cham_soc) == 0:
            print("Chua co cong viec cham soc!")
            return

        print("\n===== DANH SACH CHAM SOC =====")

        for cs in self.ds_cham_soc:
            cs.hien_thi()
            print("Tinh trang lich:", cs.kiem_tra_lich())
            print("-" * 40)

    def xem_cham_soc_theo_cay(self, ma_cay):
        cay = self.tim_cay(ma_cay)

        if cay is None:
            print("Khong tim thay cay!")
            return

        print("\nLich cham soc cua:", cay.ten_cay)
        dem = 0

        for cs in self.ds_cham_soc:
            if cs.ma_cay == ma_cay:
                cs.hien_thi()
                print("Lich:", cs.kiem_tra_lich())
                dem += 1

        if dem == 0:
            print("Cay nay chua co lich cham soc!")

    def thong_ke_so_luong(self):
        so_lo_an_qua = 0
        so_lo_lay_go = 0
        so_cay_an_qua = 0
        so_cay_lay_go = 0

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
        print("Tong so cay:",
              so_cay_an_qua + so_cay_lay_go)

    def thong_ke_thu_hoach(self):
        tong_san_luong = 0

        for cay in self.ds_cay_trong:
            if isinstance(cay, CayAnQua):
                tong_san_luong += cay.san_luong

        print("\nTong san luong qua:",
              tong_san_luong, "kg")

        return tong_san_luong

    def thong_ke_go(self):
        tong_the_tich = 0

        for cay in self.ds_cay_trong:
            if isinstance(cay, CayLayGo):
                tong_the_tich += cay.tinh_the_tich_go()

        print("\nTong the tich hinh tru uoc tinh:",
              round(tong_the_tich, 2), "m3")

        return tong_the_tich

    def thong_ke_chi_phi(self):
        tong_du_kien = 0
        tong_da_thuc_hien = 0
        so_hoan_thanh = 0

        for cs in self.ds_cham_soc:
            tong_du_kien += cs.chi_phi
            tong_da_thuc_hien += cs.tinh_chi_phi()

            if cs.trang_thai == "Da hoan thanh":
                so_hoan_thanh += 1

        print("\n===== THONG KE CHAM SOC =====")
        print("Tong cong viec:", len(self.ds_cham_soc))
        print("Da hoan thanh:", so_hoan_thanh)
        print("Chua thuc hien:",
              len(self.ds_cham_soc) - so_hoan_thanh)
        print("Tong chi phi du kien:",
              tong_du_kien, "VND")
        print("Chi phi da thuc hien:",
              tong_da_thuc_hien, "VND")

        return tong_da_thuc_hien

    def bao_cao_tong_hop(self):
        print("\n========== BAO CAO TONG HOP ==========")

        self.thong_ke_so_luong()
        self.thong_ke_thu_hoach()
        self.thong_ke_go()
        self.thong_ke_chi_phi()

        print("\n======================================")

