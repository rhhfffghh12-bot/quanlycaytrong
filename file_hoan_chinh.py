from datetime import date, datetime
from math import isfinite
from copy import deepcopy
import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'data' / 'trang_trai.json'

# ========================================================================
# NGUOI 1 - CLASS CAY TRONG + CHAM SOC + TOAN BO MENU CUA NGUOI 1
# ========================================================================

class CayTrong:
    TRANG_THAI = ("Dang trong", "Dang thu hoach", "Ket thuc")
    Trang_Thai = TRANG_THAI

    def __init__(self, ma, ten, giong, khu_vuc, ma_vu, dien_tich, so_cay_ban_dau, ngay_trong, trang_thai="Dang trong"):
        self.ma = self._kiem_tra_chuoi(ma, "Ma cay")
        self.ten = self._kiem_tra_chuoi(ten, "Ten cay")
        self.giong = self._kiem_tra_chuoi(giong, "Giong")
        self.khu_vuc = self._kiem_tra_chuoi(khu_vuc, "Khu vuc")
        self.ma_vu = self._kiem_tra_chuoi(ma_vu, "Ma vu")
        self.dien_tich = self._kiem_tra_so(dien_tich, "Dien tich")
        self.so_cay_ban_dau = self._kiem_tra_so_nguyen(so_cay_ban_dau, "So cay ban dau")
        if self.so_cay_ban_dau == 0:
            raise ValueError("So cay ban dau phai lon hon 0")
        self.so_cay_hien_tai = self.so_cay_ban_dau
        self.ngay_trong = self._kiem_tra_ngay(ngay_trong, "Ngay trong")
        self.doi_trang_thai(trang_thai)
        self.lich_su_so_cay = []
        self.nhat_ky_sinh_truong = []

    @staticmethod
    def _kiem_tra_chuoi(gia_tri, ten_truong):
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} khong duoc de trong")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_so(gia_tri, ten_truong):
        if isinstance(gia_tri, bool) or not isinstance(gia_tri, (int, float)) or not isfinite(gia_tri) or gia_tri <= 0:
            raise ValueError(f"{ten_truong} phai la so duong")
        return gia_tri

    @staticmethod
    def _kiem_tra_so_nguyen(gia_tri, ten_truong):
        if isinstance(gia_tri, bool) or not isinstance(gia_tri, int) or gia_tri < 0:
            raise ValueError(f"{ten_truong} phai la so nguyen khong am")
        return gia_tri

    @staticmethod
    def _kiem_tra_ngay(gia_tri, ten_truong):
        try:
            return date.fromisoformat(gia_tri).isoformat()
        except (TypeError, ValueError):
            raise ValueError(f"{ten_truong} phai theo dang YYYY-MM-DD")

    def hien_thi(self):
        return (f"Ma: {self.ma} | Ten: {self.ten} | Giong: {self.giong} | "
                f"Khu: {self.khu_vuc} | Vu: {self.ma_vu} | "
                f"So cay: {self.so_cay_hien_tai} | Trang thai: {self.trang_thai}")

    def cap_nhat(self, ten=None, giong=None, khu_vuc=None, dien_tich=None):
        thay_doi = {}
        for ten_truong, gia_tri in (("ten",ten),("giong",giong),("khu_vuc",khu_vuc)):
            if gia_tri is not None:
                thay_doi[ten_truong] = self._kiem_tra_chuoi(gia_tri,ten_truong)
        if dien_tich is not None:
            thay_doi["dien_tich"] = self._kiem_tra_so(dien_tich,"Dien tich")
        for ten_truong, gia_tri in thay_doi.items():
            setattr(self,ten_truong,gia_tri)

    def doi_trang_thai(self, trang_thai):
        if trang_thai not in self.TRANG_THAI:
            raise ValueError("Trang thai cay khong hop le")
        self.trang_thai = trang_thai

    def ghi_nhan_so_cay(self, ngay, so_cay_chet=0, so_cay_bo_sung=0, ghi_chu=""):
        ngay = self._kiem_tra_ngay(ngay,"Ngay ghi nhan")
        if ngay < self.ngay_trong:
            raise ValueError("Ngay ghi nhan truoc ngay trong")
        chet = self._kiem_tra_so_nguyen(so_cay_chet,"So cay chet")
        them = self._kiem_tra_so_nguyen(so_cay_bo_sung,"So cay bo sung")
        if chet > self.so_cay_hien_tai:
            raise ValueError("So cay chet vuot so cay hien tai")
        self.so_cay_hien_tai += them - chet
        self.lich_su_so_cay.append({"ngay":ngay,"so_cay_chet":chet,
                                   "so_cay_bo_sung":them,"ghi_chu":ghi_chu})

    def ghi_nhan_sinh_truong(self, ngay, giai_doan, tinh_trang, ghi_chu=""):
        ngay = self._kiem_tra_ngay(ngay,"Ngay ghi nhan")
        if ngay < self.ngay_trong:
            raise ValueError("Ngay ghi nhan truoc ngay trong")
        self.nhat_ky_sinh_truong.append({"ngay":ngay,
            "giai_doan":self._kiem_tra_chuoi(giai_doan,"Giai doan"),
            "tinh_trang":self._kiem_tra_chuoi(tinh_trang,"Tinh trang"),
            "ghi_chu":ghi_chu})

    def tinh_ty_le_so_cay(self):
        return round(self.so_cay_hien_tai / self.so_cay_ban_dau * 100,2)

    def tinh_mat_do(self):
        return round(self.so_cay_hien_tai / (self.dien_tich / 10000),2)

    def tinh_tuoi_ngay(self, ngay_tinh=None):
        ngay = date.today() if ngay_tinh is None else date.fromisoformat(ngay_tinh)
        so_ngay = (ngay - date.fromisoformat(self.ngay_trong)).days
        if so_ngay < 0:
            raise ValueError("Chua den ngay trong")
        return so_ngay

    def tinh_tuoi_cay(self, ngay_tinh=None):
        return self.tinh_tuoi_ngay(ngay_tinh)

    def to_dict(self):
        return deepcopy(vars(self))

    @classmethod
    def from_dict(cls, du_lieu):
        cay = cls(*(du_lieu[x] for x in ("ma","ten","giong","khu_vuc","ma_vu",
                     "dien_tich","so_cay_ban_dau","ngay_trong")),
                  du_lieu.get("trang_thai","Dang trong"))
        cay.so_cay_hien_tai = cls._kiem_tra_so_nguyen(du_lieu.get("so_cay_hien_tai",cay.so_cay_ban_dau),"So cay hien tai")
        cay.lich_su_so_cay = deepcopy(du_lieu.get("lich_su_so_cay",[]))
        cay.nhat_ky_sinh_truong = deepcopy(du_lieu.get("nhat_ky_sinh_truong",[]))
        return cay

class ChamSoc:
    LOAI_CONG_VIEC = ("Tuoi nuoc", "Bon phan", "Phun thuoc", "Cat tia", "Kiem tra sau benh", "Khac")

    TRANG_THAI = ("Chua thuc hien", "Dang thuc hien", "Hoan thanh", "Da huy")


    def __init__(self, ma_cv, ma_cay, loai, ngay_du_kien, ma_nhan_vien, noi_dung, so_luong_du_kien=0, don_vi="", ten_vat_tu=""):
        # Kiểm tra thông tin công việc
        self.ma_cv = self._kiem_tra_chuoi(ma_cv, "Mã công việc")
        self.ma_cay = self._kiem_tra_chuoi(ma_cay, "Mã cây")
        self.loai = self._kiem_tra_chuoi(loai, "Loại công việc")

        # Kiểm tra loại công việc có hợp lệ không
        if self.loai not in self.LOAI_CONG_VIEC:
            raise ValueError("Loại công việc không hợp lệ")

        # Kiểm tra ngày dự kiến
        self.ngay_du_kien = self._kiem_tra_ngay(ngay_du_kien, "Ngày dự kiến")

        # Kiểm tra danh sách nhân viên
        self.ma_nhan_vien = self._kiem_tra_ds_nv(ma_nhan_vien)

        # Kiểm tra nội dung chăm sóc
        self.noi_dung = self._kiem_tra_chuoi(noi_dung, "Nội dung")

        # Kiểm tra số lượng dự kiến
        self.so_luong_du_kien = self._kiem_tra_so(so_luong_du_kien, "Số lượng dự kiến")

        # Thông tin vật tư
        self.don_vi = self._kiem_tra_chuoi(don_vi, "Đơn vị") if self.so_luong_du_kien > 0 else don_vi

        self.ten_vat_tu = ten_vat_tu

        # Trạng thái ban đầu 
        self.trang_thai = "Chua thuc hien"

        # Thông tin thuc te
        self.ngay_thuc_hien = None
        self.so_luong_thuc_te = None

        # Chi phí
        self.chi_phi_vat_tu = 0
        self.chi_phi_nhan_cong = 0
        self.chi_phi_khac = 0

        # Kết quả và lý do hủy
        self.ghi_chu_ket_qua = ""
        self.ly_do_huy = ""

        # Lịch sử công việc
        self.nhat_ky = []

    @staticmethod
    def _kiem_tra_chuoi(gia_tri, ten_truong):
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} khong duoc de trong")
        return gia_tri.strip()

    #Kiểm tra số lượng và chi phí
    @staticmethod
    def _kiem_tra_so(gia_tri, ten_truong):
        import math

        if isinstance(gia_tri, bool) or not isinstance(gia_tri, (int, float)):
            raise ValueError(f"{ten_truong} phai la so")

        if not math.isfinite(gia_tri) or gia_tri < 0:
            raise ValueError(f"{ten_truong} phai la so khong am")

        return gia_tri

    # Kiểm tra ngày tháng
    @staticmethod
    def _kiem_tra_ngay(gia_tri, ten_truong):
        from datetime import date

        if not isinstance(gia_tri, str):
            raise ValueError("Ngay phai la chuoi")

        try:
            return date.fromisoformat(gia_tri).isoformat()
        except ValueError:
            raise ValueError(f"{ten_truong} phai co dang YYYY-MM-DD")

    # Kiểm tra danh sách nhân viên
    @classmethod
    def _kiem_tra_ds_nv(cls, danh_sach):
        if not isinstance(danh_sach, list):
            raise ValueError("Phai nhap danh sach nhan vien")

        ket_qua = []

        for ma in danh_sach:
            ma = cls._kiem_tra_chuoi(ma, "Ma nhan vien")

            if ma in ket_qua:
                raise ValueError("Ma nhan vien bi trung")

            ket_qua.append(ma)

        return ket_qua

    def hien_thi(self):
        return (
            f"Ma cong viec: {self.ma_cv}\n"
            f"Ma cay: {self.ma_cay}\n"
            f"Loai: {self.loai}\n"
            f"Ngay du kien: {self.ngay_du_kien}\n"
            f"Nhan vien: {', '.join(self.ma_nhan_vien)}\n"
            f"Trang thai: {self.trang_thai}"
        )

    def cap_nhat_ke_hoach(self, ngay_du_kien=None, noi_dung=None, so_luong_du_kien=None):

        if self.trang_thai != "Chua thuc hien":
           raise ValueError("Khong the sua ke hoach")

        if ngay_du_kien is not None:
           self.ngay_du_kien = self._kiem_tra_ngay(ngay_du_kien, "Ngay du kien")

        if noi_dung is not None:
           self.noi_dung = self._kiem_tra_chuoi(noi_dung, "Noi dung")

        if so_luong_du_kien is not None:
            self.so_luong_du_kien = self._kiem_tra_so(so_luong_du_kien, "So luong du kien")


    def phan_cong(self, ma_nhan_vien):
        if self.trang_thai != "Chua thuc hien":
            raise ValueError("Khong the phan cong")

        self.ma_nhan_vien = self._kiem_tra_ds_nv(ma_nhan_vien)

        self._ghi_nhat_ky("Phan cong", ", ".join(self.ma_nhan_vien))

    def bat_dau(self):
        if self.trang_thai != "Chua thuc hien":
            raise ValueError("Trang thai khong hop le")

        # Cho phep bat dau khi chua phan cong nhan vien.
        # Phan cong la tuy chon; khong phai rang buoc de chay rieng module.
        self.trang_thai = "Dang thuc hien"

        self._ghi_nhat_ky("Bat dau", "Bat dau cham soc")


    def hoan_thanh(self, ngay_thuc_hien, so_luong_thuc_te=0, chi_phi_vat_tu=0, chi_phi_nhan_cong=0, chi_phi_khac=0, ghi_chu=""):

        if self.trang_thai != "Dang thuc hien":
            raise ValueError("Cong viec chua duoc bat dau")

        ngay = self._kiem_tra_ngay(ngay_thuc_hien, "Ngay thuc hien")

        sl = self._kiem_tra_so(so_luong_thuc_te, "So luong thuc te")
        vt = self._kiem_tra_so(chi_phi_vat_tu, "Chi phi vat tu")
        nc = self._kiem_tra_so(chi_phi_nhan_cong, "Chi phi nhan cong")
        khac = self._kiem_tra_so(chi_phi_khac, "Chi phi khac")

        self.ngay_thuc_hien = ngay
        self.so_luong_thuc_te = sl
        self.chi_phi_vat_tu = vt
        self.chi_phi_nhan_cong = nc
        self.chi_phi_khac = khac
        self.ghi_chu_ket_qua = ghi_chu

        self.trang_thai = "Hoan thanh"

        self._ghi_nhat_ky("Hoan thanh", f"Chi phi: {self.tinh_chi_phi()}")


    # Tính tổng chi phí
    def tinh_chi_phi(self):
        return (self.chi_phi_vat_tu + self.chi_phi_nhan_cong + self.chi_phi_khac)


    # Hủy và kiểm tra công việc quá hạn
    def huy(self, ly_do):
        if self.trang_thai in ("Hoan thanh", "Da huy"):
            raise ValueError("Khong the huy cong viec nay")

        self.ly_do_huy = self._kiem_tra_chuoi(ly_do, "Ly do huy")

        self.trang_thai = "Da huy"

        self._ghi_nhat_ky("Huy", self.ly_do_huy)

    def kiem_tra_qua_han(self, ngay_kiem_tra=None):
        if self.trang_thai in ("Hoan thanh", "Da huy"):
            return False

        if ngay_kiem_tra is None:
            ngay = date.today().isoformat()
        else:
            ngay = self._kiem_tra_ngay(ngay_kiem_tra, "Ngay kiem tra")
        return ngay > self.ngay_du_kien


    # Nhật ký chăm sóc
    def _ghi_nhat_ky(self, hanh_dong, noi_dung):
        self.nhat_ky.append({
            "thoi_diem": datetime.now().isoformat(timespec="seconds"),
            "hanh_dong": hanh_dong,
            "noi_dung": noi_dung
        })
    def xem_nhat_ky(self):
        return [x.copy() for x in self.nhat_ky]


    def to_dict(self):
        return {
            "ma_cv": self.ma_cv,
            "ma_cay": self.ma_cay,
            "loai": self.loai,
            "ngay_du_kien": self.ngay_du_kien,
            "ma_nhan_vien": self.ma_nhan_vien.copy(),
            "noi_dung": self.noi_dung,
            "so_luong_du_kien": self.so_luong_du_kien,
            "don_vi": self.don_vi,
            "ten_vat_tu": self.ten_vat_tu,
            "trang_thai": self.trang_thai,
            "ngay_thuc_hien": self.ngay_thuc_hien,
            "so_luong_thuc_te": self.so_luong_thuc_te,
            "chi_phi_vat_tu": self.chi_phi_vat_tu,
            "chi_phi_nhan_cong": self.chi_phi_nhan_cong,
            "chi_phi_khac": self.chi_phi_khac,
            "ghi_chu_ket_qua": self.ghi_chu_ket_qua,
            "ly_do_huy": self.ly_do_huy,
            "nhat_ky": self.xem_nhat_ky()
        }


    @classmethod
    def from_dict(cls, du_lieu):
        cv = cls(
            du_lieu["ma_cv"],
            du_lieu["ma_cay"],
            du_lieu["loai"],
            du_lieu["ngay_du_kien"],
            du_lieu["ma_nhan_vien"],
            du_lieu["noi_dung"],
            du_lieu["so_luong_du_kien"],
            du_lieu["don_vi"],
            du_lieu["ten_vat_tu"]
        )

        cv.trang_thai = du_lieu["trang_thai"]
        cv.ngay_thuc_hien = du_lieu["ngay_thuc_hien"]
        cv.so_luong_thuc_te = du_lieu["so_luong_thuc_te"]

        cv.chi_phi_vat_tu = du_lieu["chi_phi_vat_tu"]
        cv.chi_phi_nhan_cong = du_lieu["chi_phi_nhan_cong"]
        cv.chi_phi_khac = du_lieu["chi_phi_khac"]

        cv.ghi_chu_ket_qua = du_lieu["ghi_chu_ket_qua"]
        cv.ly_do_huy = du_lieu["ly_do_huy"]
        cv.nhat_ky = du_lieu["nhat_ky"]

        return cv

def chi_tiet_cay(cay):
    print("\n========== THONG TIN LO CAY ==========")
    for nhan, gia_tri in (
        ("Ma lo", cay.ma), ("Ten cay", cay.ten),
        ("Giong", cay.giong), ("Khu vuc", cay.khu_vuc),
        ("Ma vu", cay.ma_vu), ("Ngay trong", cay.ngay_trong),
        ("Dien tich (m2)", cay.dien_tich),
        ("So cay ban dau", cay.so_cay_ban_dau),
        ("So cay hien tai", cay.so_cay_hien_tai),
        ("Trang thai", cay.trang_thai),
        ("Ty le so cay hien tai (%)", cay.tinh_ty_le_so_cay()),
        ("Mat do (cay/ha)", cay.tinh_mat_do()),
    ):
        print(f"{nhan}: {gia_tri}")

    try:
        print("So ngay tu khi trong:", cay.tinh_tuoi_ngay())
    except ValueError:
        print("So ngay tu khi trong: Chua den ngay trong")

def thong_ke_cay(q):
    ds = list(q.cay_trong.values())

    if not ds:
        print("Chua co du lieu cay trong.")
        return

    print("\n========== THONG KE CAY TRONG ==========")
    print("So lo cay:", len(ds))
    print("Tong dien tich (m2):", round(sum(c.dien_tich for c in ds), 2))
    print("Tong so cay ban dau:", sum(c.so_cay_ban_dau for c in ds))
    print("Tong so cay hien tai:", sum(c.so_cay_hien_tai for c in ds))

    print("So cay theo trang thai:")
    for tt in CayTrong.TRANG_THAI:
        print(f"  {tt}: {sum(c.trang_thai == tt for c in ds)} lo")

    theo_khu = {}

    for cay in ds:
        if cay.khu_vuc not in theo_khu:
            theo_khu[cay.khu_vuc] = {
                "so_lo": 0,
                "dien_tich": 0,
                "so_cay": 0
            }

        thong_ke = theo_khu[cay.khu_vuc]
        thong_ke["so_lo"] += 1
        thong_ke["dien_tich"] += cay.dien_tich
        thong_ke["so_cay"] += cay.so_cay_hien_tai

    print("Thong ke theo khu vuc:")

    for khu, thong_ke in sorted(theo_khu.items()):
        print(
            f"  {khu}: {thong_ke['so_lo']} lo | "
            f"{thong_ke['dien_tich']:g} m2 | "
            f"{thong_ke['so_cay']} cay"
        )

def menu_cay(q):

    while True:
        print("\n========== QUAN LY CAY TRONG ==========")
        print("1. Them lo cay")
        print("2. Xem danh sach lo cay")
        print("3. Tim kiem theo ma, ten, giong, khu, vu")
        print("4. Xem chi tiet mot lo cay")
        print("5. Sua thong tin lo cay")
        print("6. Ghi nhan cay chet / trong bo sung")
        print("7. Ghi nhan sinh truong va tinh trang")
        print("8. Xem lich su thay doi so cay")
        print("9. Xem nhat ky sinh truong")
        print("10. Doi trang thai lo cay")
        print("11. Thong ke cay trong")
        print("12. Xoa lo cay")
        print("13. Luu du lieu")
        print("0. Quay lai menu chinh")

        chon = nhap("Chon")

        if chon == "0":
            return

        try:
            # THEM LO CAY
            if chon == "1":
                cay = CayTrong(
                    nhap("Ma lo cay"),
                    nhap("Ten cay"),
                    nhap("Giong"),
                    nhap("Khu vuc"),
                    nhap("Ma vu"),
                    so("Dien tich m2"),
                    so("So cay ban dau", True),
                    nhap("Ngay trong YYYY-MM-DD")
                )

                q.them_cay(cay)
                print("Da them lo cay:", cay.ma)

            # XEM DANH SACH
            elif chon == "2":
                ds = sorted(q.cay_trong.values(), key=lambda c: c.ma)

                print(f"Danh sach: {len(ds)} lo cay")
                hien(ds)

            # TIM KIEM
            elif chon == "3":
                tu_khoa = nhap("Tu khoa can tim")
                ds = q.tim_cay(tu_khoa)

                print(f"Tim thay {len(ds)} lo")
                hien(ds)

            # XEM CHI TIET
            elif chon == "4":
                chi_tiet_cay(q.lay_cay(nhap("Ma lo can xem")))

            # SUA THONG TIN
            elif chon == "5":
                ma = nhap("Ma lo can sua")
                cay = q.lay_cay(ma)

                print("De trong va Enter neu muon giu gia tri cu.")

                ten = nhap_tuy_chon("Ten cay", cay.ten)
                giong = nhap_tuy_chon("Giong", cay.giong)
                khu = nhap_tuy_chon("Khu vuc", cay.khu_vuc)
                dt = nhap_tuy_chon("Dien tich m2", cay.dien_tich)

                thay_doi = {}

                if ten is not None:
                    thay_doi["ten"] = ten

                if giong is not None:
                    thay_doi["giong"] = giong

                if khu is not None:
                    thay_doi["khu_vuc"] = khu

                if dt is not None:
                    thay_doi["dien_tich"] = float(dt)

                if thay_doi:
                    q.sua_cay(ma, **thay_doi)
                    print("Da cap nhat lo cay.")
                else:
                    print("Khong co thong tin thay doi.")

            # GHI NHAN CAY CHET / TRONG BO SUNG
            elif chon == "6":
                cay = q.lay_cay(nhap("Ma lo"))

                cay.ghi_nhan_so_cay(
                    nhap("Ngay ghi nhan YYYY-MM-DD"),
                    so("So cay chet", True),
                    so("So cay trong bo sung", True),
                    nhap("Ghi chu")
                )

                print(
                    "Da ghi nhan. So cay hien tai:", cay.so_cay_hien_tai)

            # GHI NHAN SINH TRUONG
            elif chon == "7":
                cay = q.lay_cay(nhap("Ma lo"))

                cay.ghi_nhan_sinh_truong(
                    nhap("Ngay ghi nhan YYYY-MM-DD"),
                    nhap("Giai doan sinh truong"),
                    nhap("Tinh trang cay"),
                    nhap("Ghi chu")
                )

                print("Da them nhat ky sinh truong.")

            # XEM LICH SU SO CAY
            elif chon == "8":
                cay = q.lay_cay(nhap("Ma lo"))

                if not cay.lich_su_so_cay:
                    print("Chua co lich su thay doi so cay.")

                for i, x in enumerate(cay.lich_su_so_cay, 1):
                    print(
                        f"{i}. {x['ngay']} | "
                        f"Chet: {x['so_cay_chet']} | "
                        f"Bo sung: {x['so_cay_bo_sung']} | "
                        f"Ghi chu: {x.get('ghi_chu', '')}"
                    )

            # XEM NHAT KY SINH TRUONG
            elif chon == "9":
                cay = q.lay_cay(nhap("Ma lo"))

                if not cay.nhat_ky_sinh_truong:
                    print("Chua co nhat ky sinh truong.")

                for i, x in enumerate(cay.nhat_ky_sinh_truong, 1):
                    print(
                        f"{i}. {x['ngay']} | "
                        f"{x['giai_doan']} | "
                        f"{x['tinh_trang']} | "
                        f"{x.get('ghi_chu', '')}"
                    )

            # DOI TRANG THAI
            elif chon == "10":
                cay = q.lay_cay(nhap("Ma lo"))

                print("1. Dang trong")
                print("2. Dang thu hoach")
                print("3. Ket thuc")

                lua_chon = nhap("Chon trang thai moi")

                mapping = {
                    "1": "Dang trong",
                    "2": "Dang thu hoach",
                    "3": "Ket thuc"
                }

                if lua_chon not in mapping:
                    print("Trang thai khong hop le.")
                    continue

                cay.doi_trang_thai(mapping[lua_chon])

                print("Trang thai moi:", cay.trang_thai)

            # THONG KE CAY TRONG
            elif chon == "11":
                thong_ke_cay(q)

            # XOA LO CAY
            elif chon == "12":
                cay = q.lay_cay(nhap("Ma lo can xoa"))

                print("Sap xoa:", cay.hien_thi())

                if nhap("Xac nhan xoa? (y/n)").lower() == "y":
                    q.xoa_cay(cay.ma)
                    print("Da xoa lo cay.")
                else:
                    print("Da huy thao tac xoa.")

            # LUU DU LIEU
            elif chon == "13":
                q.luu(DATA_FILE)
                print("Da luu du lieu:", DATA_FILE)

            else:
                print("Lua chon khong hop le.")

        except (ValueError, KeyError, TypeError, OSError) as loi:
            print("LOI:", loi)
            print("Hay kiem tra du lieu va thu lai.")

def dam_bao_lo_cay(q, ma_cay):
    """Cho phep bat ky menu nao tu nhap lo cay thieu, khong can vao menu Nguoi 1."""
    if ma_cay in q.cay_trong:
        return ma_cay
    print(f"\nChua co lo cay '{ma_cay}' trong du lieu.")
    if nhap("Tao lo cay nay ngay tai day? (y/n)").lower() != "y":
        raise ValueError("Can lo cay hop le de tiep tuc. Chua thay doi du lieu.")
    # Chi tao tu thong tin nguoi dung nhap; KHONG tu sinh du lieu gia.
    cay = CayTrong(
        ma_cay, nhap("Ten cay"), nhap("Giong"), nhap("Khu vuc"),
        nhap("Ma vu"), so("Dien tich m2"),
        so("So cay ban dau", True), nhap("Ngay trong YYYY-MM-DD")
    )
    q.them_cay(cay)
    print("Da tao lo cay:", ma_cay)
    return ma_cay


def ma_nv_list():
    print("Co the bo trong ma nhan vien de quan ly cham soc doc lap.")
    du_lieu = nhap("Nhap ma nhan vien (Enter = chua phan cong), cach nhau dau phay")

    return [
        ma.strip()
        for ma in du_lieu.split(",")
        if ma.strip()
    ]

def menu_cham_soc(q):
    while True:
        print("\n========== QUAN LY CHAM SOC ==========")
        print("1. Them cong viec\n2. Danh sach cong viec\n3. Doi phan cong")
        print("4. Bat dau\n5. Hoan thanh\n6. Huy cong viec\n7. Xoa cong viec")
        print("8. Xem nhat ky\n9. Xem cong viec qua han\n0. Quay lai")
        chon = nhap("Chon")
        if chon == "0":
            return
        try:
            if chon == "1":
                ma, ma_cay = nhap("Ma cong viec"), nhap("Ma lo cay")
                print("Loai hop le:", ", ".join(ChamSoc.LOAI_CONG_VIEC))
                cv = ChamSoc(
                    ma, ma_cay, nhap("Loai cong viec"),
                    nhap("Ngay du kien YYYY-MM-DD"), ma_nv_list(),
                    nhap("Noi dung"), so("So luong du kien"),
                    nhap("Don vi"), nhap("Ten vat tu")
                )
                dam_bao_lo_cay(q, ma_cay)
                q.them_cham_soc(cv)
                print("Da them cong viec.")
            elif chon == "2":
                hien(list(q.cham_soc.values()))
            elif chon == "3":
                q.sua_phan_cong(nhap("Ma cong viec"), ma_nv_list())
                print("Da doi phan cong.")
            elif chon == "4":
                q.bat_dau_cham_soc(nhap("Ma cong viec"))
                print("Da bat dau.")
            elif chon == "5":
                q.hoan_thanh_cham_soc(
                    nhap("Ma cong viec"), nhap("Ngay thuc hien YYYY-MM-DD"),
                    so("So luong thuc te"), so("Chi phi vat tu"),
                    so("Chi phi nhan cong"), so("Chi phi khac"), nhap("Ghi chu")
                )
                print("Da hoan thanh va ghi nhan chi phi.")
            elif chon == "6":
                q.huy_cham_soc(nhap("Ma cong viec"), nhap("Ly do huy"))
                print("Da huy.")
            elif chon == "7":
                ma = nhap("Ma cong viec")
                if nhap("Xac nhan xoa? (y/n)").lower() == "y":
                    q.xoa_cham_soc(ma)
                    print("Da xoa.")
            elif chon == "8":
                hien_ban_ghi(q.lay_cv(nhap("Ma cong viec")).xem_nhat_ky())
            elif chon == "9":
                hien([cv for cv in q.cham_soc.values() if cv.kiem_tra_qua_han()])
            else:
                print("Lua chon khong hop le.")
        except (ValueError, KeyError, TypeError) as loi:
            print("LOI:", loi)
            print("Goi y: De trong ma nhan vien neu chua co du lieu Nguoi 2.")

# ========================================================================
# NGUOI 2 - CLASS NHAN VIEN + KINH DOANH + TOAN BO MENU CUA NGUOI 2
# ========================================================================

class NhanVien:
    TRANG_THAI = (
        "Dang lam viec", "Nghi viec")

    def __init__(self, ma_nv, ho_ten, chuc_vu, ngay_vao_lam, luong_mot_cong, so_dien_thoai=""):

        self.ma_nv = ma_nv
        self.ho_ten = ho_ten
        self.chuc_vu = chuc_vu
        self.ngay_vao_lam = ngay_vao_lam
        self.luong_mot_cong = luong_mot_cong
        self.so_dien_thoai = so_dien_thoai

        self.trang_thai = "Dang lam viec"

        self.cong_viec = {}
        self.bang_cong = {}
        self.nghi_phep = {}


    def cham_cong(self, ngay, so_cong):
        ngay = date.fromisoformat(ngay).isoformat()
        if not isfinite(so_cong):
            raise ValueError("So cong phai la so huu han")
        if self.trang_thai != "Dang lam viec":
            raise ValueError("Nhan vien da nghi viec")

        if so_cong < 0 or so_cong > 1:
            raise ValueError("So cong phai tu 0 den 1")

        if ngay in self.bang_cong:
            raise ValueError("Ngay nay da cham cong")

        self.bang_cong[ngay] = so_cong

    def tinh_tong_cong(self, thang, nam):
        tong = 0
        for ngay, so_cong in self.bang_cong.items():
            if ngay.startswith(f"{nam:04d}-{thang:02d}-"):
                tong += so_cong
        return tong

    def tinh_luong(self, thang, nam, phu_cap=0, thuong=0, khau_tru=0):
        luong = (self.tinh_tong_cong(thang, nam) * self.luong_mot_cong)
        return max(0, luong + phu_cap + thuong - khau_tru)

    def cap_nhat(self, **thay_doi):
        hop_le = {"ho_ten", "chuc_vu", "ngay_vao_lam", "luong_mot_cong", "so_dien_thoai"}
        for truong, gia_tri in thay_doi.items():
            if truong not in hop_le:
                raise ValueError(f"Khong the sua {truong}")
            if truong == "luong_mot_cong":
                if not isfinite(gia_tri) or gia_tri < 0:
                    raise ValueError("Luong mot cong phai la so khong am")
            elif truong == "ngay_vao_lam":
                date.fromisoformat(gia_tri)
            elif not isinstance(gia_tri, str) or (truong != "so_dien_thoai" and not gia_tri.strip()):
                raise ValueError(f"{truong} khong duoc de trong")
        for truong, gia_tri in thay_doi.items():
            setattr(self, truong, gia_tri)

    def doi_trang_thai(self, trang_thai):
        if trang_thai not in self.TRANG_THAI:
            raise ValueError("Trang thai khong hop le")
        self.trang_thai = trang_thai

    def them_cong_viec(self, ma_cv):
        if self.trang_thai != "Dang lam viec":
            raise ValueError("Nhan vien da nghi viec")
        if ma_cv in self.cong_viec:
            raise ValueError("Cong viec da duoc giao")
        self.cong_viec[ma_cv] = "Duoc giao"

    def hoan_thanh_cong_viec(self, ma_cv):
        if ma_cv not in self.cong_viec:
            raise ValueError("Cong viec chua duoc giao")
        self.cong_viec[ma_cv] = "Hoan thanh"

    def hien_thi(self):
        return (f"{self.ma_nv} | {self.ho_ten} | {self.chuc_vu} | "
                f"{self.so_dien_thoai} | {self.trang_thai} | "
                f"Luong/cong: {self.luong_mot_cong:g}")

    def to_dict(self):
        return deepcopy(vars(self))

    @classmethod
    def from_dict(cls, data):
        nv = cls(data["ma_nv"], data["ho_ten"], data["chuc_vu"],
                 data["ngay_vao_lam"], data["luong_mot_cong"],
                 data.get("so_dien_thoai", ""))
        nv.doi_trang_thai(data["trang_thai"])
        nv.cong_viec = deepcopy(data["cong_viec"])
        nv.bang_cong = deepcopy(data["bang_cong"])
        nv.nghi_phep = deepcopy(data["nghi_phep"])
        return nv

class KinhDoanh:

    def __init__(self):
        self.khach_hang = {}
        self.thu_hoach = []
        self.don_hang = []
        self.chi_phi = []


    @staticmethod
    def _chuoi(gia_tri, ten_truong):
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} khong duoc de trong")
        return gia_tri.strip()

    @staticmethod
    def _ngay(gia_tri):
        if not isinstance(gia_tri, str):
            raise ValueError("Ngay phai la chuoi")
        try:
            ngay = date.fromisoformat(gia_tri)
        except ValueError:
            raise ValueError("Ngay khong hop le")
        if ngay.isoformat() != gia_tri:
            raise ValueError("Can dung YYYY-MM-DD")

        return gia_tri

    @staticmethod
    def _so(gia_tri, ten_truong, lon_hon_0=False):
        if (
            isinstance(gia_tri, bool)
            or not isinstance(gia_tri, (int, float))
            or not isfinite(gia_tri)
        ):
            raise ValueError(f"{ten_truong} phai la so")

        if gia_tri < 0 or (lon_hon_0 and gia_tri == 0):
            raise ValueError(f"{ten_truong} khong hop le")
        return gia_tri


    @staticmethod
    def _tim(danh_sach, truong, ma):
        return next((x for x in danh_sach if x[truong] == ma), None)

    @classmethod
    def _ma_da_co(cls, danh_sach, truong, ma):
        return cls._tim(danh_sach, truong, ma) is not None

    def them_khach_hang(self, ma_kh, ten, so_dien_thoai="", dia_chi=""):

        ma_kh = self._chuoi(ma_kh, "Ma khach hang")
        ten = self._chuoi(ten, "Ten khach hang")

        if ma_kh in self.khach_hang:
            raise ValueError("Ma khach hang da ton tai")

        self.khach_hang[ma_kh] = {
            "ma_kh": ma_kh,
            "ten": ten,
            "so_dien_thoai": so_dien_thoai,
            "dia_chi": dia_chi,
            "trang_thai": "Hoat dong"
        }


    def ghi_thu_hoach(self, ma_th, ma_cay, ngay, so_luong_kg, pham_chat="Dat"):

        ma_th = self._chuoi(ma_th, "Ma thu hoach")
        ma_cay = self._chuoi(ma_cay, "Ma cay")

        ngay = self._ngay(ngay)

        self._so(so_luong_kg, "So luong thu hoach", lon_hon_0=True)

        if self._ma_da_co(self.thu_hoach, "ma_th", ma_th):
            raise ValueError("Ma thu hoach da ton tai")

        self.thu_hoach.append({
            "ma_th": ma_th,
            "ma_cay": ma_cay,
            "ngay": ngay,
            "so_luong_kg": so_luong_kg,
            "pham_chat": pham_chat
        })

# Tính tổng sản lượng
    def tong_thu_hoach(self, ma_cay=None):
        tong = 0
        for th in self.thu_hoach:
            if ma_cay is None or th["ma_cay"] == ma_cay:
                tong += th["so_luong_kg"]

        return tong

# Quản lý tồn kho
    def ton_kho(self, ma_cay):
        da_giao = 0
        dang_giu = 0

        for dh in self.don_hang:
            if dh["ma_cay"] == ma_cay:

                if dh["trang_thai"] == "Da giao":
                    da_giao += dh["so_luong_kg"]

                elif dh["trang_thai"] == "Cho giao":
                    dang_giu += dh["so_luong_kg"]

        return (
            self.tong_thu_hoach(ma_cay)
            - da_giao
            - dang_giu
        )

# Tạo đơn hàng
    def tao_don_hang(self, ma_dh, ma_cay, ma_kh, ngay, so_luong_kg, don_gia):

        ma_dh = self._chuoi(ma_dh, "Ma don hang")
        ma_cay = self._chuoi(ma_cay, "Ma cay")
        ma_kh = self._chuoi(ma_kh, "Ma khach hang")
        ngay = self._ngay(ngay)

        self._so(so_luong_kg, "So luong", True)
        self._so(don_gia, "Don gia", True)

        if ma_kh not in self.khach_hang:
            raise ValueError("Khach hang khong ton tai")

        if self._ma_da_co(self.don_hang, "ma_dh", ma_dh):
            raise ValueError("Ma don hang da ton tai")

        if so_luong_kg > self.ton_kho(ma_cay):
            raise ValueError("Khong du hang ton kho")

        self.don_hang.append({
            "ma_dh": ma_dh,
            "ma_cay": ma_cay,
            "ma_kh": ma_kh,
            "ngay": ngay,
            "so_luong_kg": so_luong_kg,
            "don_gia": don_gia,
            "trang_thai": "Cho giao",
            "ngay_giao": None,
            "da_thanh_toan": 0,
            "lich_su_thanh_toan": []
        })


    def giao_hang(self, ma_dh, ngay_giao=None):
        # Tim don hang theo ma
        dh = self._tim(self.don_hang, "ma_dh", ma_dh)

        if dh is None:
            raise ValueError("Don hang khong ton tai")

        # Chi giao don dang cho giao
        if dh["trang_thai"] != "Cho giao":
            raise ValueError("Don hang khong o trang thai cho giao")

        # Neu khong nhap ngay thi lay ngay hien tai
        if ngay_giao is None:
            ngay_giao = date.today().isoformat()
        else:
            ngay_giao = self._ngay(ngay_giao)

        # Ngay giao khong duoc truoc ngay dat
        if ngay_giao < dh["ngay"]:
            raise ValueError("Ngay giao khong duoc truoc ngay dat")

        # Cap nhat trang thai
        dh["trang_thai"] = "Da giao"
        dh["ngay_giao"] = ngay_giao

        return dh


    def thanh_toan(self, ma_dh, so_tien, ngay=None):
        # Tim don hang
        dh = self._tim(self.don_hang, "ma_dh", ma_dh)

        if dh is None:
            raise ValueError("Don hang khong ton tai")

        # Chi thanh toan khi da giao
        if dh["trang_thai"] != "Da giao":
            raise ValueError("Don hang chua duoc giao")

        # Kiem tra so tien phai lon hon 0
        so_tien = self._so(so_tien, "So tien thanh toan", lon_hon_0=True)

        # Kiem tra ngay thanh toan
        if ngay is None:
            ngay = date.today().isoformat()
        else:
            ngay = self._ngay(ngay)

        if ngay < dh["ngay_giao"]:
            raise ValueError("Ngay thanh toan khong duoc truoc ngay giao")

        # Tinh gia tri don hang
        tong_tien = dh["so_luong_kg"] * dh["don_gia"]

        # Tinh so tien con no
        con_no = tong_tien - dh["da_thanh_toan"]

        if so_tien > con_no:
            raise ValueError("So tien thanh toan vuot qua cong no")

        # Cap nhat so tien da thanh toan
        dh["da_thanh_toan"] += so_tien

        # Luu lich su thanh toan
        dh["lich_su_thanh_toan"].append({
            "ngay": ngay,
            "so_tien": so_tien
        })

        return dh["da_thanh_toan"]


    def huy_don(self, ma_dh):
        # Tim don hang
        dh = self._tim(self.don_hang, "ma_dh", ma_dh)

        if dh is None:
            raise ValueError("Don hang khong ton tai")

        # Chi cho huy don dang cho giao
        if dh["trang_thai"] != "Cho giao":
            raise ValueError("Chi duoc huy don dang cho giao")

        if dh["da_thanh_toan"] > 0:
            raise ValueError("Don hang da thanh toan, khong the huy")

        # Cap nhat trang thai
        dh["trang_thai"] = "Da huy"

        return dh


    def ghi_chi_phi(self, ma_cp, ma_cay, ngay, loai, so_tien, ghi_chu="", nguon_tham_chieu=""):

        # Kiem tra ma chi phi
        ma_cp = self._chuoi(ma_cp, "Ma chi phi")

        # Kiem tra ma cay
        ma_cay = self._chuoi(ma_cay, "Ma cay")

        # Kiem tra ngay phat sinh
        ngay = self._ngay(ngay)

        # Kiem tra loai chi phi
        loai = self._chuoi(loai, "Loai chi phi")

        # Kiem tra so tien
        so_tien = self._so(so_tien, "So tien", lon_hon_0=True)

        # Kiem tra ma chi phi trung
        if self._ma_da_co(self.chi_phi, "ma_cp", ma_cp):
            raise ValueError("Ma chi phi da ton tai")

        # Kiem tra nguon tham chieu trung
        if nguon_tham_chieu:
            for cp in self.chi_phi:
                if cp["nguon_tham_chieu"] == nguon_tham_chieu:
                    raise ValueError("Chi phi tu nguon nay da duoc ghi nhan")

        # Tao ban ghi chi phi
        ban_ghi = {
            "ma_cp": ma_cp,
            "ma_cay": ma_cay,
            "ngay": ngay,
            "loai": loai,
            "so_tien": so_tien,
            "ghi_chu": ghi_chu,
            "nguon_tham_chieu": nguon_tham_chieu
        }

        # Them vao danh sach
        self.chi_phi.append(ban_ghi)

        return ban_ghi


    def tong_chi_phi(self, ma_cay=None):
        tong = 0

        for cp in self.chi_phi:
            if ma_cay is None or cp["ma_cay"] == ma_cay:
                tong += cp["so_tien"]

        return tong


    def tinh_doanh_thu(self, ma_cay=None):
        tong_doanh_thu = 0

        for dh in self.don_hang:
            if dh["trang_thai"] == "Da giao":
                if ma_cay is None or dh["ma_cay"] == ma_cay:
                    thanh_tien = (dh["so_luong_kg"] * dh["don_gia"])
                    tong_doanh_thu += thanh_tien

        return tong_doanh_thu

    def tinh_da_thu(self, ma_cay=None):
        tong_da_thu = 0

        for dh in self.don_hang:
            if dh["trang_thai"] == "Da giao":
                if ma_cay is None or dh["ma_cay"] == ma_cay:
                    tong_da_thu += dh["da_thanh_toan"]

        return tong_da_thu

    def tinh_cong_no(self, ma_cay=None):
        doanh_thu = self.tinh_doanh_thu(ma_cay)
        da_thu = self.tinh_da_thu(ma_cay)

        return doanh_thu - da_thu

    def tinh_loi_nhuan_tam_tinh(self, ma_cay=None):
        doanh_thu = self.tinh_doanh_thu(ma_cay)
        chi_phi = self.tong_chi_phi(ma_cay)

        loi_nhuan = doanh_thu - chi_phi

        return loi_nhuan

    def bao_cao(self, ma_cay=None):

        tong_san_luong = self.tong_thu_hoach(ma_cay)

        da_giao = 0
        dang_giu = 0

        for dh in self.don_hang:
            if ma_cay is None or dh["ma_cay"] == ma_cay:

                if dh["trang_thai"] == "Da giao":
                    da_giao += dh["so_luong_kg"]

                elif dh["trang_thai"] == "Cho giao":
                    dang_giu += dh["so_luong_kg"]

        ton_kho_kha_dung = (
            tong_san_luong - da_giao - dang_giu
        )

        return {
            "tong_thu_hoach": tong_san_luong,
            "da_giao": da_giao,
            "dang_giu": dang_giu,
            "ton_kho_kha_dung": ton_kho_kha_dung,
            "doanh_thu": self.tinh_doanh_thu(ma_cay),
            "da_thu": self.tinh_da_thu(ma_cay),
            "cong_no": self.tinh_cong_no(ma_cay),
            "chi_phi": self.tong_chi_phi(ma_cay),
            "loi_nhuan_tam_tinh":
            self.tinh_loi_nhuan_tam_tinh(ma_cay)
        }


    def to_dict(self):
        return {
            "khach_hang": deepcopy(self.khach_hang),
            "thu_hoach": deepcopy(self.thu_hoach),
            "don_hang": deepcopy(self.don_hang),
            "chi_phi": deepcopy(self.chi_phi)
        }


    @classmethod
    def from_dict(cls, du_lieu):
        if not isinstance(du_lieu, dict):
            raise ValueError("Du lieu phai la Dictionary")

        khach_hang = du_lieu["khach_hang"]
        thu_hoach = du_lieu["thu_hoach"]
        don_hang = du_lieu["don_hang"]
        chi_phi = du_lieu["chi_phi"]

        if not isinstance(khach_hang, dict):
            raise ValueError("Khach hang phai la Dictionary")

        for danh_sach in (thu_hoach, don_hang, chi_phi):
            if not isinstance(danh_sach, list):
                raise ValueError("Du lieu danh sach khong hop le")

        kd = cls()

        kd.khach_hang = deepcopy(khach_hang)
        kd.thu_hoach = deepcopy(thu_hoach)
        kd.don_hang = deepcopy(don_hang)
        kd.chi_phi = deepcopy(chi_phi)

        return kd

def menu_nv(q):
    while True:
        print("\n========== QUAN LY NHAN VIEN ==========")
        print("1. Them nhan vien\n2. Danh sach nhan vien\n3. Tim nhan vien")
        print("4. Sua thong tin\n5. Cham cong\n6. Tinh luong")
        print("7. Cho nghi viec\n8. Xoa nhan vien\n0. Quay lai")
        chon = nhap("Chon")
        if chon == "0":
            return
        try:
            if chon == "1":
                nv = NhanVien(
                    nhap("Ma nhan vien"), nhap("Ho ten"), nhap("Chuc vu"),
                    nhap("Ngay vao lam YYYY-MM-DD"), so("Luong mot cong"),
                    nhap("So dien thoai")
                )
                q.them_nhan_vien(nv)
                print("Da them nhan vien.")
            elif chon == "2":
                hien(q.danh_sach_nhan_vien())
            elif chon == "3":
                hien(q.tim_nhan_vien(nhap("Tu khoa")))
            elif chon == "4":
                nv = q.lay_nv(nhap("Ma nhan vien"))
                thay_doi = {}
                for truong, nhan in (
                    ("ho_ten", "Ho ten"), ("chuc_vu", "Chuc vu"),
                    ("ngay_vao_lam", "Ngay vao lam YYYY-MM-DD"),
                    ("luong_mot_cong", "Luong mot cong"),
                    ("so_dien_thoai", "So dien thoai")
                ):
                    gia_tri = nhap_tuy_chon(nhan, getattr(nv, truong))
                    if gia_tri is not None:
                        thay_doi[truong] = (float(gia_tri) if truong == "luong_mot_cong" else gia_tri)
                q.sua_nhan_vien(nv.ma_nv, **thay_doi)
                print("Da cap nhat.")
            elif chon == "5":
                q.cham_cong_nhan_vien(
                    nhap("Ma nhan vien"), nhap("Ngay YYYY-MM-DD"),
                    so("So cong (0 den 1)")
                )
                print("Da cham cong.")
            elif chon == "6":
                ma = nhap("Ma nhan vien")
                thang, nam = so("Thang", True), so("Nam", True)
                if not 1 <= thang <= 12 or not 1 <= nam <= 9999:
                    raise ValueError("Thang hoac nam khong hop le")
                print("Luong:", q.tinh_luong_nhan_vien(ma, thang, nam, so("Phu cap"), so("Thuong"), so("Khau tru")))
            elif chon == "7":
                q.nghi_viec(nhap("Ma nhan vien"))
                print("Da ghi nhan nghi viec.")
            elif chon == "8":
                ma = nhap("Ma nhan vien")
                if nhap("Xac nhan xoa? (y/n)").lower() == "y":
                    q.xoa_nhan_vien(ma)
                    print("Da xoa.")
            else:
                print("Lua chon khong hop le.")
        except (ValueError, KeyError, TypeError) as loi:
            print("LOI:", loi)

def hien_ban_ghi(danh_sach):
    if not danh_sach:
        print("Khong co du lieu.")
    for ban_ghi in danh_sach:
        print(" | ".join(f"{ten}: {gia_tri}" for ten, gia_tri in ban_ghi.items()))

def menu_kinh_doanh(q):
    kd = q.kinh_doanh
    while True:
        print("\n========== QUAN LY KINH DOANH ==========")
        print("1. Them khach hang\n2. Danh sach khach hang\n3. Ghi thu hoach")
        print("4. Xem thu hoach\n5. Tao don hang\n6. Xem don hang")
        print("7. Giao hang\n8. Thanh toan\n9. Huy don hang")
        print("10. Ghi chi phi\n11. Xem chi phi\n12. Xem ton kho")
        print("13. Bao cao kinh doanh\n0. Quay lai")
        chon = nhap("Chon")
        if chon == "0":
            return
        try:
            if chon == "1":
                q.them_khach_hang(nhap("Ma khach hang"), nhap("Ten khach hang"),
                                  nhap("So dien thoai"), nhap("Dia chi"))
                print("Da them khach hang.")
            elif chon == "2":
                hien_ban_ghi(kd.khach_hang.values())
            elif chon == "3":
                ma_th, ma_cay = nhap("Ma thu hoach"), nhap("Ma lo cay")
                dam_bao_lo_cay(q, ma_cay)
                q.thu_hoach(ma_th, ma_cay,
                           nhap("Ngay YYYY-MM-DD"), so("So luong kg"),
                           nhap("Pham chat (Enter = Dat)") or "Dat")
                print("Da ghi thu hoach.")
            elif chon == "4":
                hien_ban_ghi(kd.thu_hoach)
            elif chon == "5":
                ma_dh, ma_cay = nhap("Ma don hang"), nhap("Ma lo cay")
                dam_bao_lo_cay(q, ma_cay)
                q.tao_don(ma_dh, ma_cay,
                          nhap("Ma khach hang"), nhap("Ngay YYYY-MM-DD"),
                          so("So luong kg"), so("Don gia moi kg"))
                print("Da tao don hang.")
            elif chon == "6":
                hien_ban_ghi(kd.don_hang)
            elif chon == "7":
                kd.giao_hang(nhap("Ma don hang"), nhap("Ngay giao YYYY-MM-DD"))
                print("Da giao hang.")
            elif chon == "8":
                kd.thanh_toan(nhap("Ma don hang"), so("So tien"),
                             nhap("Ngay thanh toan YYYY-MM-DD"))
                print("Da ghi thanh toan.")
            elif chon == "9":
                ma = nhap("Ma don hang")
                if nhap("Xac nhan huy? (y/n)").lower() == "y":
                    kd.huy_don(ma)
                    print("Da huy don.")
            elif chon == "10":
                ma_cp, ma_cay = nhap("Ma chi phi"), nhap("Ma lo cay")
                dam_bao_lo_cay(q, ma_cay)
                q.ghi_chi_phi(ma_cp, ma_cay,
                              nhap("Ngay YYYY-MM-DD"), nhap("Loai chi phi"),
                              so("So tien"), nhap("Ghi chu"))
                print("Da ghi chi phi.")
            elif chon == "11":
                hien_ban_ghi(kd.chi_phi)
            elif chon == "12":
                ma = nhap("Ma lo cay")
                dam_bao_lo_cay(q, ma)
                print("Ton kho kha dung (kg):", kd.ton_kho(ma))
            elif chon == "13":
                ma = nhap("Ma lo cay (Enter = tat ca)") or None
                hien_ban_ghi([q.bao_cao(ma)])
            else:
                print("Lua chon khong hop le.")
        except (ValueError, KeyError, TypeError) as loi:
            print("LOI:", loi)

# ========================================================================
# NGUOI 3 - LOP TICH HOP, HAM DUNG CHUNG, BAO CAO, MENU CHINH
# ========================================================================
# Trong QuanLyTrangTrai, cac nhom phuong thuc duoc danh dau ro chu so huu.
# 5 CLASS DUOC GIU NGUYEN: khong them class phu, khong gan ham dong.

class QuanLyTrangTrai:
    def __init__(self):
        self.cay_trong = {}
        self.cham_soc = {}
        self.nhan_vien = {}
        self.kinh_doanh = KinhDoanh()


    # ===== NGUOI 1: NGHIEP VU CAY TRONG =====
    def them_cay(self, cay):
        if not isinstance(cay, CayTrong):
            raise TypeError("Phai la doi tuong CayTrong")

        if cay.ma in self.cay_trong:
            raise ValueError("Ma cay da ton tai")

        self.cay_trong[cay.ma] = cay

    def lay_cay(self, ma):
        if ma not in self.cay_trong:
            raise ValueError("Khong tim thay cay")

        return self.cay_trong[ma]


    def tim_cay(self, tu_khoa):
        tu_khoa = tu_khoa.casefold().strip()
        return [c for c in self.cay_trong.values()
                if any(tu_khoa in str(getattr(c, truong)).casefold()
                       for truong in ("ma", "ten", "giong", "khu_vuc", "ma_vu"))]

    def sua_cay(self, ma, **thay_doi):
        self.lay_cay(ma).cap_nhat(**thay_doi)

    def xoa_cay(self, ma):
        self.lay_cay(ma)
        if any(cv.ma_cay == ma for cv in self.cham_soc.values()):
            raise ValueError("Lo cay co lich su cham soc, khong the xoa")
        if any(item["ma_cay"] == ma for danh_sach in
               (self.kinh_doanh.thu_hoach, self.kinh_doanh.don_hang, self.kinh_doanh.chi_phi)
               for item in danh_sach):
            raise ValueError("Lo cay co du lieu kinh doanh, khong the xoa")
        del self.cay_trong[ma]

    # ===== NGUOI 1: NGHIEP VU CHAM SOC CAY TRONG =====
    def lay_cv(self, ma_cv):
        if ma_cv not in self.cham_soc:
            raise ValueError("Khong tim thay cong viec")
        return self.cham_soc[ma_cv]

    def them_cham_soc(self, cv):

        # Kiem tra doi tuong
        if not isinstance(cv, ChamSoc):
            raise TypeError("Can doi tuong ChamSoc")

        # Kiem tra ma trung
        if cv.ma_cv in self.cham_soc:
            raise ValueError("Trung ma cong viec")

        # Kiem tra lo cay
        cay = self.lay_cay(cv.ma_cay)

        if cay.trang_thai == "Ket thuc":
            raise ValueError("Lo cay da ket thuc")

        # Kiem tra ngay cham soc
        if cv.ngay_du_kien < cay.ngay_trong:
            raise ValueError("Ngay cham soc truoc ngay trong")

        # Khong phan cong van duoc tao va chay cong viec doc lap.
        # Neu co ma NV, ma do van phai hop le de bao ve tinh nhat quan.
        self._kiem_tra_nv(cv.ma_nhan_vien)

        for ma in cv.ma_nhan_vien:
            nv = self.lay_nv(ma)

            if cv.ma_cv in nv.cong_viec:
                raise ValueError("Cong viec da co trong nhan vien")

        # Luu cong viec
        self.cham_soc[cv.ma_cv] = cv

        # Dong bo sang nhan vien
        for ma in cv.ma_nhan_vien:
            nv = self.lay_nv(ma)
            nv.them_cong_viec(cv.ma_cv)


    def sua_phan_cong(self, ma_cv, ds_ma):

        cv = self.lay_cv(ma_cv)

        if cv.trang_thai != "Chua thuc hien":
            raise ValueError("Chi doi phan cong khi chua bat dau")

        self._kiem_tra_nv(ds_ma)

        ma_cu = set(cv.ma_nhan_vien)
        ma_moi = set(ds_ma)

        for ma in ma_moi - ma_cu:
            if ma_cv in self.lay_nv(ma).cong_viec:
                raise ValueError("Cong viec da co trong nhan vien")

        cv.phan_cong(ds_ma)

        # Xoa phan cong cu
        for ma in ma_cu - ma_moi:
            self.lay_nv(ma).cong_viec.pop(ma_cv, None)

        # Them phan cong moi
        for ma in ma_moi - ma_cu:
            self.lay_nv(ma).them_cong_viec(ma_cv)


    def bat_dau_cham_soc(self, ma_cv):

        cv = self.lay_cv(ma_cv)

        self._kiem_tra_nv(cv.ma_nhan_vien)

        cv.bat_dau()


    def hoan_thanh_cham_soc(self, ma_cv, ngay, so_luong=0, chi_phi_vat_tu=0, chi_phi_nhan_cong=0, chi_phi_khac=0, ghi_chu=""):

        cv = self.lay_cv(ma_cv)
        cay = self.lay_cay(cv.ma_cay)

        if ngay < cay.ngay_trong:
            raise ValueError("Ngay thuc hien truoc ngay trong")

        # Khong ghi trung chi phi
        for cp in self.kinh_doanh.chi_phi:
            if cp.get("nguon_tham_chieu") == ma_cv:
                raise ValueError("Chi phi cong viec da duoc ghi nhan")

        # Hoan thanh cong viec
        cv.hoan_thanh(ngay, so_luong, chi_phi_vat_tu, chi_phi_nhan_cong, chi_phi_khac, ghi_chu)

        # Cap nhat cho nhan vien
        for ma in cv.ma_nhan_vien:
            nv = self.lay_nv(ma)
            nv.hoan_thanh_cong_viec(ma_cv)

        # Tinh tong chi phi
        tong = cv.tinh_chi_phi()

        # Chuyen sang KinhDoanh
        if tong > 0:
            self.kinh_doanh.ghi_chi_phi(f"CS:{ma_cv}", cv.ma_cay, ngay, "Cham soc", tong, f"{cv.loai} - {cv.noi_dung}", ma_cv)


    def huy_cham_soc(self, ma_cv, ly_do):

        cv = self.lay_cv(ma_cv)
        cv.huy(ly_do)

        for ma in cv.ma_nhan_vien:
            nv = self.lay_nv(ma)
            nv.cong_viec.pop(ma_cv, None)


    def xoa_cham_soc(self, ma_cv):

        cv = self.lay_cv(ma_cv)

        if cv.trang_thai != "Chua thuc hien":
            raise ValueError("Chi xoa cong viec chua thuc hien")

        for ma in cv.ma_nhan_vien:
            nv = self.lay_nv(ma)
            nv.cong_viec.pop(ma_cv, None)

        del self.cham_soc[ma_cv]


    # ===== NGUOI 2: QUAN LY NHAN VIEN =====
    def them_nhan_vien(self, nv):
        if not isinstance(nv, NhanVien):
            raise TypeError("Phai la doi tuong NhanVien")

        if nv.ma_nv in self.nhan_vien:
            raise ValueError("Ma nhan vien da ton tai")

        self.nhan_vien[nv.ma_nv] = nv


    # LAY NHAN VIEN THEO MA
    def lay_nv(self, ma_nv):
        if ma_nv not in self.nhan_vien:
            raise ValueError("Khong tim thay nhan vien")

        return self.nhan_vien[ma_nv]


    # CAP NHAT THONG TIN NHAN VIEN
    def sua_nhan_vien(self, ma_nv, **thay_doi):
        nv = self.lay_nv(ma_nv)
        nv.cap_nhat(**thay_doi)


    # TIM KIEM NHAN VIEN
    def tim_nhan_vien(self, tu_khoa):
        tu_khoa = tu_khoa.casefold()
        ket_qua = []

        for nv in self.nhan_vien.values():
            if (
                tu_khoa in nv.ma_nv.casefold()
                or tu_khoa in nv.ho_ten.casefold()
                or tu_khoa in nv.chuc_vu.casefold()
            ):
                ket_qua.append(nv)

        return ket_qua


    # DANH SACH NHAN VIEN
    def danh_sach_nhan_vien(self):
        return list(self.nhan_vien.values())


    # CHO NHAN VIEN NGHI VIEC
    def nghi_viec(self, ma_nv):
        nv = self.lay_nv(ma_nv)

        for cv in self.cham_soc.values():
            if ma_nv in cv.ma_nhan_vien:
                if cv.trang_thai in ("Chua thuc hien", "Dang thuc hien"):
                    raise ValueError("Nhan vien con cong viec chua hoan thanh")

        nv.doi_trang_thai("Nghi viec")

    # XOA NHAN VIEN
    def xoa_nhan_vien(self, ma_nv):
        nv = self.lay_nv(ma_nv)

        if nv.cong_viec or nv.bang_cong or nv.nghi_phep:
            raise ValueError("Nhan vien da co lich su, khong the xoa")

        for cv in self.cham_soc.values():
            if ma_nv in cv.ma_nhan_vien:
                raise ValueError("Nhan vien dang co du lieu phan cong")

        del self.nhan_vien[ma_nv]

    # CHAM CONG NHAN VIEN
    def cham_cong_nhan_vien(self, ma_nv, ngay, so_cong):
        nv = self.lay_nv(ma_nv)

        nv.cham_cong(ngay, so_cong)

    # TINH LUONG NHAN VIEN
    def tinh_luong_nhan_vien(self, ma_nv, thang, nam, phu_cap=0, thuong=0, khau_tru=0):
        nv = self.lay_nv(ma_nv)

        return nv.tinh_luong(thang, nam, phu_cap, thuong, khau_tru) 

    # ===== PHOI HOP NGUOI 1 + 2: KIEM TRA NHAN VIEN DUOC PHAN CONG =====
    def _kiem_tra_nv(self, ds_ma):

        # Kiem tra ma nhan vien trung nhau
        if len(ds_ma) != len(set(ds_ma)):
            raise ValueError("Trung ma nhan vien trong phan cong")

        # Kiem tra tung nhan vien
        for ma in ds_ma:
            nv = self.lay_nv(ma)

            if nv.trang_thai != "Dang lam viec":
                raise ValueError(f"Nhan vien {ma} da nghi viec")



    # ===== NGUOI 2: NGHIEP VU KINH DOANH =====
    def them_khach_hang(self, *args):
        return self.kinh_doanh.them_khach_hang(*args)


    def thu_hoach(self, ma_th, ma_cay, ngay, so_luong, pham_chat="Dat"):

        cay = self.lay_cay(ma_cay)

        if cay.trang_thai == "Ket thuc":
            raise ValueError("Lo cay da ket thuc")

        if ngay < cay.ngay_trong:
            raise ValueError("Ngay thu hoach truoc ngay trong")

        self.kinh_doanh.ghi_thu_hoach(ma_th, ma_cay, ngay, so_luong, pham_chat)


    def tao_don(self, ma_dh, ma_cay, ma_kh, ngay, so_luong, don_gia):

        # Kiem tra lo cay
        self.lay_cay(ma_cay)

        # Chuyen yeu cau sang KinhDoanh
        self.kinh_doanh.tao_don_hang(ma_dh, ma_cay, ma_kh, ngay,so_luong, don_gia)

    def ghi_chi_phi(self, ma_cp, ma_cay, ngay, loai, so_tien, ghi_chu=""):

        self.lay_cay(ma_cay)

        self.kinh_doanh.ghi_chi_phi(ma_cp, ma_cay, ngay, loai, so_tien, ghi_chu)


    # ===== NGUOI 3: BAO CAO, KIEM TRA DU LIEU, LUU VA DOC =====
    def bao_cao(self, ma_cay=None):

        if ma_cay is not None:
            self.lay_cay(ma_cay)

        ket_qua = self.kinh_doanh.bao_cao(ma_cay)

        if ma_cay is None:
            ket_qua["so_lo_cay"] = len(self.cay_trong)
            ket_qua["so_cong_viec"] = len(self.cham_soc)
        else:
            ket_qua["so_lo_cay"] = 1
            ket_qua["so_cong_viec"] = sum(
                cv.ma_cay == ma_cay
                for cv in self.cham_soc.values()
            )

        ket_qua["so_nhan_vien"] = len(self.nhan_vien)

        ket_qua["cong_viec_qua_han"] = sum(
            cv.kiem_tra_qua_han()
            for cv in self.cham_soc.values()
            if ma_cay is None or cv.ma_cay == ma_cay
        )

        if ma_cay is None:
            ket_qua["ton_kho_kha_dung_kg"] = sum(
                self.kinh_doanh.ton_kho(ma)
                for ma in self.cay_trong
            )

        return ket_qua


    def to_dict(self):
        return {
            "version": 1,

            "cay_trong": [
                cay.to_dict()
                for cay in self.cay_trong.values()
            ],

            "nhan_vien": [
                nv.to_dict()
                for nv in self.nhan_vien.values()
            ],

            "cham_soc": [
                cv.to_dict()
                for cv in self.cham_soc.values()
            ],

            "kinh_doanh": self.kinh_doanh.to_dict()
        }


    @classmethod
    def from_dict(cls, data):

        if not isinstance(data, dict):
            raise ValueError("Du lieu khong hop le")

        if data.get("version") != 1:
            raise ValueError("Phien ban du lieu khong hop le")

        ql = cls()

        # Khoi phuc cay trong
        for item in data["cay_trong"]:
            cay = CayTrong.from_dict(item)
            ql.them_cay(cay)

        # Khoi phuc nhan vien
        for item in data["nhan_vien"]:
            nv = NhanVien.from_dict(item)
            ql.them_nhan_vien(nv)

        # Khoi phuc cham soc
        for item in data["cham_soc"]:
            cv = ChamSoc.from_dict(item)

            if cv.ma_cv in ql.cham_soc:
                raise ValueError("Trung ma cong viec")

            ql.lay_cay(cv.ma_cay)

            for ma in cv.ma_nhan_vien:
                ql.lay_nv(ma)

            ql.cham_soc[cv.ma_cv] = cv

        # Khoi phuc kinh doanh
        ql.kinh_doanh = KinhDoanh.from_dict(
            data["kinh_doanh"]
        )

        # Kiem tra lien ket
        ql.kiem_tra_lien_ket()

        return ql


    def kiem_tra_lien_ket(self):

        # Kiem tra cong viec
        for ma_cv, cv in self.cham_soc.items():

            self.lay_cay(cv.ma_cay)

            for ma_nv in cv.ma_nhan_vien:
                nv = self.lay_nv(ma_nv)

                if cv.trang_thai == "Hoan thanh":
                    mong_doi = "Hoan thanh"
                else:
                    mong_doi = "Duoc giao"

                if cv.trang_thai == "Da huy":
                    if ma_cv in nv.cong_viec:
                        raise ValueError("Cong viec da huy van con phan cong")
                elif nv.cong_viec.get(ma_cv) != mong_doi:
                    raise ValueError("Du lieu nhan vien chua dong bo")

        # Kiem tra giao dich
        kd = self.kinh_doanh

        for danh_sach in (kd.thu_hoach, kd.don_hang, kd.chi_phi):
            for ban_ghi in danh_sach:
                self.lay_cay(ban_ghi["ma_cay"])

        for ma in self.cay_trong:
            if kd.ton_kho(ma) < 0:
                raise ValueError("Ton kho bi am")

        return True


    def luu(self, duong_dan="data/trang_trai.json"):

        # Kiem tra du lieu truoc khi luu
        self.kiem_tra_lien_ket()

        path = Path(duong_dan)

        # Tao thu muc neu chua co
        path.parent.mkdir(parents=True,exist_ok=True)

        # Ghi vao file tam
        temp = path.with_name(path.name + ".tmp")

        try:
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

            # Thay file chinh bang file tam
            os.replace(temp, path)

        finally:
            if temp.exists():
                temp.unlink()


    @classmethod
    def doc(cls, duong_dan="data/trang_trai.json"):

        with open(duong_dan, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

def nhap(ten):
    return input(f"{ten}: ").strip()

def so(ten, so_nguyen=False):
    while True:
        try:
            gia_tri = nhap(ten)

            if so_nguyen:
                return int(gia_tri)

            return float(gia_tri)

        except ValueError:
            print("Hay nhap so hop le")

def hien(ds):
    if not ds:
        print("Khong co du lieu")
        return

    for doi_tuong in ds:
        print(doi_tuong.hien_thi())

def nhap_tuy_chon(ten, hien_tai):
    """Nhan Enter de giu gia tri cu, khong ep nhap lai tat ca."""
    gia_tri = nhap(f"{ten} [{hien_tai}] (Enter = giu nguyen)")
    return gia_tri if gia_tri else None

def hien_bao_cao(ql):
    print("\n========== BAO CAO TRANG TRAI ==========")

    # Chon bao cao toan trang trai hoac tung lo
    ma_cay = input("Nhap ma lo cay (Enter = toan trang trai): ").strip()

    if ma_cay == "":
        ket_qua = ql.bao_cao()
        print("\nBAO CAO TOAN TRANG TRAI")
    else:
        ket_qua = ql.bao_cao(ma_cay)
        print(f"\nBAO CAO LO CAY {ma_cay}")

    print("-" * 45)

    for ten, gia_tri in ket_qua.items():
        ten_hien_thi = ten.replace("_", " ").title()

        if isinstance(gia_tri, float):
            print(f"{ten_hien_thi}: {gia_tri:,.2f}")
        elif isinstance(gia_tri, int):
            print(f"{ten_hien_thi}: {gia_tri:,}")
        else:
            print(f"{ten_hien_thi}: {gia_tri}")

    print("-" * 45)

def main():

    print("\n" + "=" * 54)
    print("HE THONG QUAN LY TRANG TRAI".center(54))
    print("=" * 54)

    # ====================================
    # BUOC 1: KHOI TAO VA DOC DU LIEU
    # ====================================

    
    if DATA_FILE.exists():
        try:
            ql = QuanLyTrangTrai.doc(DATA_FILE)

            print("\nTrang thai: Da tai trang trai thanh cong")
            print("Du lieu: Da doc tu file trang_trai.json")

        except (ValueError, KeyError, TypeError, OSError, AttributeError) as loi:
            print("\nLOI DOC DU LIEU:", loi)
            print("Khong the khoi dong vi du lieu cu khong hop le.")
            print("Hay kiem tra file JSON truoc khi chay lai.")
            return

    else:
        ql = QuanLyTrangTrai()

        print("\nChua co du lieu duoc luu.")
        print("Da khoi tao trang trai moi!")

    # ====================================
    # BUOC 2: HIEN THI MENU CHINH
    # ====================================

    while True:

        print("\n" + "=" * 54)
        print("MENU CHINH".center(54))
        print("=" * 54)

        print("\n--- NGUOI 1: CAY TRONG VA CHAM SOC ---")
        print("1. Quan ly cay trong")
        print("2. Quan ly cham soc cay trong")

        print("\n--- NGUOI 2: NHAN VIEN VA KINH DOANH ---")
        print("3. Quan ly nhan vien")
        print("4. Quan ly kinh doanh")

        print("\n--- NGUOI 3: QUAN LY TONG HOP ---")
        print("5. Bao cao tong hop trang trai")
        print("6. Luu du lieu")
        print("7. Tai lai du lieu da luu")

        print("\n0. Thoat chuong trinh")

        print("=" * 50)

        chon = input("Nhap lua chon cua ban: ").strip()

        # ====================================
        # BUOC 3: XU LY CAC LUA CHON
        # ====================================

        try:

            # QUAN LY CAY TRONG
            if chon == "1":

                print("\nDang mo quan ly cay trong...")

                menu_cay(ql)

            # QUAN LY CHAM SOC CAY TRONG (NGUOI 1)
            elif chon == "2":

                print("\nDang mo quan ly cham soc...")

                menu_cham_soc(ql)

            # QUAN LY NHAN VIEN (NGUOI 2)
            elif chon == "3":

                print("\nDang mo quan ly nhan vien...")

                menu_nv(ql)

            # QUAN LY KINH DOANH
            elif chon == "4":

                print("\nDang mo quan ly kinh doanh...")

                menu_kinh_doanh(ql)

            # BAO CAO TONG HOP
            elif chon == "5":

                hien_bao_cao(ql)

            # LUU DU LIEU
            elif chon == "6":

                ql.luu(DATA_FILE)

                print("\nDa luu du lieu thanh cong!")
                print("File:", DATA_FILE)

            # TAI LAI DU LIEU
            elif chon == "7":

                if not DATA_FILE.exists():

                    print("\nChua co file du lieu de tai lai.")

                else:

                    xac_nhan = input(
                        "Tai lai se bo cac thay doi "
                        "chua luu. Tiep tuc? (y/n): "
                    ).strip().lower()

                    if xac_nhan == "y":

                        ql_moi = QuanLyTrangTrai.doc(DATA_FILE)

                        ql = ql_moi

                        print("\nDa tai lai du lieu thanh cong!")

                    else:
                        print("\nDa huy thao tac tai lai.")

            # THOAT CHUONG TRINH
            elif chon == "0":

                print("\nBan co muon thoat chuong trinh?")
                print("1. Luu du lieu va thoat")
                print("2. Thoat khong luu")
                print("3. Quay lai menu")

                lua_chon = input("Nhap lua chon: ").strip()

                if lua_chon == "1":

                    ql.luu(DATA_FILE)

                    print("\nDa luu du lieu thanh cong!")
                    print("Cam on ban da su dung chuong trinh!")

                    break

                elif lua_chon == "2":

                    xac_nhan = input(
                        "Ban chac chan muon thoat "
                        "khong luu? (y/n): "
                    ).strip().lower()

                    if xac_nhan == "y":

                        print("\nThoat chuong trinh khong luu.")

                        break

                    else:

                        print("\nDa huy thao tac thoat.")

                elif lua_chon == "3":

                    print("\nQuay lai menu chinh.")

                else:

                    print("\nLua chon khong hop le!")

            # LUA CHON SAI
            else:

                print("\nLua chon khong hop le!")
                print("Vui long chon tu 0 den 7.")

        # ====================================
        # BUOC 4: XU LY LOI
        # ====================================

        except (ValueError, KeyError, TypeError, OSError, AttributeError) as loi:

            print("\nDA XAY RA LOI:", loi)

            print("Vui long kiem tra du lieu va thu lai.")

    # ====================================
    # BUOC 5: KET THUC
    # ====================================

    print("\nChuong trinh da ket thuc.")

if __name__ == "__main__":
    main()
