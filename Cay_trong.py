from datetime import date
from math import isfinite
from copy import deepcopy


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
