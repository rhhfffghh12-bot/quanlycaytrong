from datetime import datetime, date

class CayTrong:
    Trang_Thai = (
        "Dang trong",
        "Dang thu hoach",
        "Ket thuc",
    )

    def __init__(self, ma, ten, giong, khu_vuc, ma_vu, dien_tich, so_cay_ban_dau, ngay_trong, trang_thai = "Dang trong"):
        self.ma = self._kiem_tra_chuoi(ma, "Mã cây")
        self.ten = self._kiem_tra_chuoi(ten, "Tên cây")
        self.giong = self._kiem_tra_chuoi(giong, "Giống cây")
        self.khu_vuc = self._kiem_tra_chuoi(giong, "Khu vực")
        self.ma_vu = self._kiem_tra_chuoi(ma_vu, "Mã vụ")
        
        self.dien_tich = self._kiem_tra_so(dien_tich, "Diện tích")

        self.so_cay_ban_dau = self._kiem_tra_so_nguyen(so_cay_ban_dau, "Số cây ban đầu")

        if self.so_cay_ban_dau == 0:
            raise ValueError("Số cây ban đầu phải lớn hơn 0")
        
        self.so_cay_hien_tai = self.so_cay_ban_dau

        self.ngay_trong = self._kiem_tra_ngay(ngay_trong, "Ngày trồng")

        if trang_thai not in self.Trang_Thai:
            raise ValueError("Trạng thái không hợp lệ")
        
        self.trang_thai = trang_thai

        self.lich_su_trong_cay = []
        self.nhat_ky_sinh_truong = []

        def hien_thi(self):
            return (
        f"Ma: {self.ma} | "
        f"Ten: {self.ten} | "
        f"Giong: {self.giong} | "
        f"Khu: {self.khu_vuc} | "
        f"So cay: {self.so_cay_hien_tai}"
        )

    def cap_nhat(self, ten=None, giong=None, khu_vuc=None, dien_tich=None):

        if ten is not None:
            self.ten = ten

        if giong is not None:
            self.giong = giong

        if khu_vuc is not None:
            self.khu_vuc = khu_vuc

        if dien_tich is not None:
            self.dien_tich = dien_tich

    def ghi_nhan_so_cay(self, ngay,
                    so_cay_chet=0,
                    so_cay_bo_sung=0,
                    ghi_chu=""):

        if so_cay_chet < 0 or so_cay_bo_sung < 0:
            print("So cay khong duoc am")
            return

        if so_cay_chet > self.so_cay_hien_tai:
            print("So cay chet vuot so cay hien co")
            return

        self.so_cay_hien_tai = (self.so_cay_hien_tai - so_cay_chet + so_cay_bo_sung)

        self.lich_su_so_cay.append({
        "ngay": ngay,
        "so_cay_chet": so_cay_chet,
        "so_cay_bo_sung": so_cay_bo_sung,
        "ghi_chu": ghi_chu
    })

    def ghi_nhan_sinh_truong(self, ngay, giai_doan, tinh_trang, ghi_chu=""):
        ban_ghi = {
        "ngay": ngay,
        "giai_doan": giai_doan,
        "tinh_trang": tinh_trang,
        "ghi_chu": ghi_chu
    }
        self.nhat_ky_sinh_truong.append(ban_ghi)

    def tinh_ty_le_so_cay(self):
        return round(self.so_cay_hien_tai / self.so_cay_ban_dau * 100, 2)

    def tinh_mat_do(self):
        dien_tich_ha = self.dien_tich / 10000
        return round(self.so_cay_hien_tai / dien_tich_ha, 2)

    def tinh_tuoi_cay(self, ngay_tinh=None):
        ngay_trong = datetime.strptime(self.ngay_trong, "&d-%m-%y").date()

        if ngay_tinh is None:
            ngay_hien_tai = date.today()
        else:
            ngay_hien_tai = datetime.strptime(ngay_tinh, "&d-%m-%y").date()

        return (ngay_hien_tai - ngay_trong).days

    
    # 1. Kiểm tra mã cây, giống cây, tên cây và khu vực
    @staticmethod
    def _kiem_tra_chuoi(gia_tri, ten_truong):
        if not isinstance(gia_tri, str):
            raise ValueError(f"{ten_truong} phải là chuỗi")

        gia_tri = gia_tri.strip()

        if gia_tri == "":
            raise ValueError(f"{ten_truong} không được để trống")

        return gia_tri

    # 2. Kiểm tra diện tích cây trồng
    @staticmethod
    def _kiem_tra_so(gia_tri, ten_truong):
        if isinstance(gia_tri, bool) or not isinstance(
            gia_tri, (int, float)
        ):
            raise ValueError(f"{ten_truong} phải là số")

        if not (0 < gia_tri < float("inf")):
            raise ValueError(f"{ten_truong} phải là số dương hữu hạn")

        return gia_tri

    # 3. Kiểm tra số lượng cây
    @staticmethod
    def _kiem_tra_so_nguyen(gia_tri, ten_truong):
        if isinstance(gia_tri, bool) or not isinstance(gia_tri, int):
            raise ValueError(f"{ten_truong} phải là số nguyên")

        if gia_tri < 0:
            raise ValueError(f"{ten_truong} không được âm")

        return gia_tri

    # 4. Kiểm tra ngày trồng
    @staticmethod
    def _kiem_tra_ngay(gia_tri, ten_truong):
        from datetime import datetime

        if not isinstance(gia_tri, str):
            raise ValueError(f"{ten_truong} phải là chuỗi ngày")

        try:
            ngay = datetime.strptime(gia_tri, "%d-%m-%y")
        except ValueError:
            raise ValueError(f"{ten_truong} phải có dạng DD-MM-YYYY")

        return ngay.strftime("%d-%m-%y")

    
    def to_dict(self):
        return {
            "ma": self.ma,
            "ten": self.ten,
            "giong": self.giong,
            "khu_vuc": self.khu_vuc,
            "ma_vu": self.ma_vu,
            "dien_tich": self.dien_tich,
            "so_cay_ban_dau": self.so_cay_ban_dau,
            "so_cay_hien_tai": self.so_cay_hien_tai,
            "ngay_trong": self.ngay_trong,
            "trang_thai": self.trang_thai,
            "lich_su_so_cay": self.lich_su_so_cay,
            "nhat_ky_sinh_truong": self.nhat_ky_sinh_truong
        }






