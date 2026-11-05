from datetime import date, datetime


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
