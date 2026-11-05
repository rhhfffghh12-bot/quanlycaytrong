from datetime import date
from math import isfinite
from copy import deepcopy


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
