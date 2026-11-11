from datetime import datetime

class ChamSoc:

    def __init__(self, ma_cham_soc, ma_cay,
                 ngay_cham_soc, cong_viec, chi_phi,
                 trang_thai="Chua thuc hien"):

        if ma_cham_soc.strip() == "":
            raise ValueError("Ma cham soc khong duoc rong!")

        if ma_cay.strip() == "":
            raise ValueError("Ma cay khong duoc rong!")

        if cong_viec.strip() == "":
            raise ValueError("Cong viec khong duoc rong!")

        if chi_phi < 0:
            raise ValueError("Chi phi khong duoc am!")

        datetime.strptime(ngay_cham_soc, "%d/%m/%Y")

        if trang_thai not in ("Chua thuc hien", "Da hoan thanh"):
            raise ValueError("Trang thai khong hop le!")

        self.ma_cham_soc = ma_cham_soc
        self.ma_cay = ma_cay
        self.ngay_cham_soc = ngay_cham_soc
        self.cong_viec = cong_viec
        self.chi_phi = chi_phi
        self.trang_thai = trang_thai

    def hien_thi(self):
        print("\n===== THONG TIN CHAM SOC =====")
        print("Ma cham soc:", self.ma_cham_soc)
        print("Ma cay:", self.ma_cay)
        print("Ngay cham soc:", self.ngay_cham_soc)
        print("Cong viec:", self.cong_viec)
        print("Chi phi:", self.chi_phi, "VND")
        print("Trang thai:", self.trang_thai)

    def cap_nhat(self, ngay_moi, cong_viec_moi,
                 chi_phi_moi):

        if self.trang_thai == "Da hoan thanh":
            print("Khong the sua cong viec da hoan thanh!")
            return False

        if cong_viec_moi.strip() == "":
            print("Ten cong viec khong duoc rong!")
            return False

        if chi_phi_moi < 0:
            print("Chi phi khong duoc am!")
            return False

        try:
            datetime.strptime(ngay_moi, "%d/%m/%Y")
        except ValueError:
            print("Ngay khong hop le! Dung dd/mm/yyyy.")
            return False

        self.ngay_cham_soc = ngay_moi
        self.cong_viec = cong_viec_moi
        self.chi_phi = chi_phi_moi

        print("Cap nhat cong viec thanh cong!")
        return True

    def hoan_thanh(self):

        if self.trang_thai == "Da hoan thanh":
            print("Cong viec nay da hoan thanh truoc do!")
            return False

        self.trang_thai = "Da hoan thanh"

        print("Da danh dau hoan thanh cong viec!")
        return True

    def kiem_tra_lich(self):

        if self.trang_thai == "Da hoan thanh":
            return "Da hoan thanh"

        ngay_cong_viec = datetime.strptime(self.ngay_cham_soc, "%d/%m/%Y").date()

        hom_nay = datetime.now().date()

        so_ngay = (ngay_cong_viec - hom_nay).days

        if so_ngay < 0:
            return "Qua han " + str(abs(so_ngay)) + " ngay"

        elif so_ngay == 0:
            return "Can thuc hien hom nay"

        else:
            return "Con " + str(so_ngay) + " ngay"

    def tinh_chi_phi(self):

        if self.trang_thai == "Da hoan thanh":
            return self.chi_phi

        return 0


