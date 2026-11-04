from Cay_trong import CayTrong
from Cham_soc import ChamSoc
from nhan_vien import NhanVien
from Kinh_doanh import KinhDoanh

import json
import os
from pathlib import Path

class QuanLyTrangTrai:
    def __init__(self):
        self.cay_trong = {}
        self.cham_soc = {}
        self.nhan_vien = {}
        self.kinh_doanh = KinhDoanh()


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


    # THEM NHAN VIEN
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

    def sua_nhan_vien(self, ma_nv, **thay_doi):
        nv = self.lay_nv(ma_nv)
        nv.cap_nhat(**thay_doi)


    def _kiem_tra_nv(self, ds_ma):

        # Kiem tra ma nhan vien trung nhau
        if len(ds_ma) != len(set(ds_ma)):
            raise ValueError("Trung ma nhan vien trong phan cong")

        # Kiem tra tung nhan vien
        for ma in ds_ma:
            nv = self.lay_nv(ma)

            if nv.trang_thai != "Dang lam viec":
                raise ValueError(f"Nhan vien {ma} da nghi viec")


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

        # Kiem tra nhan vien
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
            self.kinh_doanh.ghi_chi_phi(
                f"CS:{ma_cv}",
                cv.ma_cay,
                ngay,
                "Cham soc",
                tong,
                f"{cv.loai} - {cv.noi_dung}",
                ma_cv
            )


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




