from datetime import date
from math import isfinite
from copy import deepcopy


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


