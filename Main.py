from pathlib import Path

from Quan_ly_trang_trai import QuanLyTrangTrai
from Cay_trong import CayTrong
from Cham_soc import ChamSoc
from nhan_vien import NhanVien

DATA_FILE = (Path(__file__).resolve().parent / "data" / "trang_trai.json")


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

def ma_nv_list():
    du_lieu = nhap("Nhap ma nhan vien, cach nhau dau phay")

    return [
        ma.strip()
        for ma in du_lieu.split(",")
        if ma.strip()
    ]

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
                print("Luong:", q.tinh_luong_nhan_vien(
                    ma, thang, nam, so("Phu cap"), so("Thuong"), so("Khau tru")
                ))
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
                q.thu_hoach(nhap("Ma thu hoach"), nhap("Ma lo cay"),
                           nhap("Ngay YYYY-MM-DD"), so("So luong kg"),
                           nhap("Pham chat (Enter = Dat)") or "Dat")
                print("Da ghi thu hoach.")
            elif chon == "4":
                hien_ban_ghi(kd.thu_hoach)
            elif chon == "5":
                q.tao_don(nhap("Ma don hang"), nhap("Ma lo cay"),
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
                q.ghi_chi_phi(nhap("Ma chi phi"), nhap("Ma lo cay"),
                              nhap("Ngay YYYY-MM-DD"), nhap("Loai chi phi"),
                              so("So tien"), nhap("Ghi chu"))
                print("Da ghi chi phi.")
            elif chon == "11":
                hien_ban_ghi(kd.chi_phi)
            elif chon == "12":
                ma = nhap("Ma lo cay")
                q.lay_cay(ma)
                print("Ton kho kha dung (kg):", kd.ton_kho(ma))
            elif chon == "13":
                ma = nhap("Ma lo cay (Enter = tat ca)") or None
                hien_ban_ghi([q.bao_cao(ma)])
            else:
                print("Lua chon khong hop le.")
        except (ValueError, KeyError, TypeError) as loi:
            print("LOI:", loi)


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
                ds = sorted(
                    q.cay_trong.values(),
                    key=lambda c: c.ma
                )

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
                chi_tiet_cay(
                    q.lay_cay(nhap("Ma lo can xem"))
                )

            # SUA THONG TIN
            elif chon == "5":
                ma = nhap("Ma lo can sua")
                cay = q.lay_cay(ma)

                print("De trong va Enter neu muon giu gia tri cu.")

                ten = nhap_tuy_chon("Ten cay", cay.ten)
                giong = nhap_tuy_chon("Giong", cay.giong)
                khu = nhap_tuy_chon("Khu vuc", cay.khu_vuc)
                dt = nhap_tuy_chon(
                    "Dien tich m2",
                    cay.dien_tich
                )

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
                    "Da ghi nhan. So cay hien tai:",
                    cay.so_cay_hien_tai
                )

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


def hien_bao_cao(ql):
    print("\n========== BAO CAO TRANG TRAI ==========")

    # Chon bao cao toan trang trai hoac tung lo
    ma_cay = input(
        "Nhap ma lo cay (Enter = toan trang trai): "
    ).strip()

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

    print("=" * 50)
    print("HE THONG QUAN LY TRANG TRAI")
    print("=" * 50)

    # ====================================
    # BUOC 1: KHOI TAO VA DOC DU LIEU
    # ====================================

    if DATA_FILE.exists():

        try:
            ql = QuanLyTrangTrai.doc(DATA_FILE)

            print("\nDa doc du lieu trang trai thanh cong!")

        except (ValueError, KeyError, TypeError, OSError, AttributeError) as loi:

            print("\nLOI DOC DU LIEU:", loi)

            print(
                "Khong the khoi dong vi du lieu cu "
                "khong hop le."
            )

            print(
                "Hay kiem tra file JSON truoc khi "
                "chay lai chuong trinh."
            )

            return

    else:
        ql = QuanLyTrangTrai()

        print("\nChua co du lieu duoc luu.")
        print("Da khoi tao trang trai moi!")

    # ====================================
    # BUOC 2: HIEN THI MENU CHINH
    # ====================================

    while True:

        print("\n" + "=" * 50)
        print("             MENU CHINH")
        print("=" * 50)

        print("1. Quan ly cay trong")
        print("2. Quan ly nhan vien")
        print("3. Quan ly cham soc cay trong")
        print("4. Quan ly kinh doanh")
        print("5. Bao cao tong hop trang trai")
        print("6. Luu du lieu")
        print("7. Tai lai du lieu da luu")
        print("0. Thoat chuong trinh")

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

            # QUAN LY NHAN VIEN
            elif chon == "2":

                print("\nDang mo quan ly nhan vien...")

                menu_nv(ql)

            # QUAN LY CHAM SOC
            elif chon == "3":

                print("\nDang mo quan ly cham soc...")

                menu_cham_soc(ql)

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

                        print(
                            "\nThoat chuong trinh khong luu."
                        )

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


# CHAY CHUONG TRINH
if __name__ == "__main__":
    main()

