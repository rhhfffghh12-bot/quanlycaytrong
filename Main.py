from Quan_ly import QuanLy
from Cham_soc import ChamSoc
from cay_an_qua import CayAnQua
from cay_lay_go import CayLayGo


def nhap_lua_chon(nho_nhat, lon_nhat):
    while True:
        try:
            chon = int(input("Nhap lua chon: "))
            if nho_nhat <= chon <= lon_nhat:
                return chon
        except ValueError:
            pass
        print(f"Vui long nhap so tu {nho_nhat} den {lon_nhat}.")


def nhap_so(nhan, kieu=float):
    while True:
        try:
            return kieu(input(f"{nhan}: "))
        except ValueError:
            print("Vui long nhap so hop le.")


def menu_cay(ql):
    while True:
        print("\n1. Them cay an qua\n2. Them cay lay go\n3. Danh sach cay")
        print("4. Tim cay\n5. Sua cay\n6. Xoa cay\n0. Quay lai")
        chon = nhap_lua_chon(0, 6)
        if chon == 0:
            return
        try:
            if chon in (1, 2):
                chung = (input("Ma cay: ").strip(), input("Ten cay: ").strip(),
                         input("Ngay trong (dd/mm/yyyy): ").strip(),
                         nhap_so("So luong", int), nhap_so("Dien tich (m2)"))
                if chon == 1:
                    cay = CayAnQua(*chung, input("Loai qua: "), input("Mua thu hoach: "),
                                   nhap_so("Thoi gian cho qua (ngay)", int),
                                   nhap_so("San luong (kg)"))
                else:
                    cay = CayLayGo(*chung, input("Loai go: "), nhap_so("Chieu cao (m)"),
                                   nhap_so("Duong kinh than (cm)"),
                                   nhap_so("Chu ky khai thac (nam)", int))
                ql.them_cay(cay)
            elif chon == 3:
                ql.hien_thi_ds_cay()
            elif chon == 4:
                cay = ql.tim_cay(input("Ma cay: ").strip())
                if cay is None:
                    print("Khong tim thay cay!")
                else:
                    cay.hien_thi()
            elif chon == 5:
                ql.sua_cay(input("Ma cay: ").strip(), input("Ten moi: ").strip(),
                           nhap_so("So luong moi", int), nhap_so("Dien tich moi"))
            elif chon == 6:
                ql.xoa_cay(input("Ma cay: ").strip())
        except ValueError as loi:
            print("LOI:", loi)


def menu_cham_soc(ql):
    while True:
        print("\n1. Them cham soc\n2. Danh sach\n3. Sua cham soc")
        print("4. Xoa cham soc\n5. Hoan thanh\n6. Xem theo cay\n0. Quay lai")
        chon = nhap_lua_chon(0, 6)
        if chon == 0:
            return
        try:
            if chon == 1:
                ql.them_cham_soc(ChamSoc(
                    input("Ma cham soc: ").strip(), input("Ma cay: ").strip(),
                    input("Ngay cham soc (dd/mm/yyyy): ").strip(),
                    input("Cong viec: ").strip(), nhap_so("Chi phi")))
            elif chon == 2:
                ql.hien_thi_ds_cham_soc()
            elif chon == 3:
                ql.sua_cham_soc(input("Ma cham soc: ").strip(),
                                input("Ngay moi (dd/mm/yyyy): ").strip(),
                                input("Cong viec moi: ").strip(), nhap_so("Chi phi moi"))
            elif chon == 4:
                ql.xoa_cham_soc(input("Ma cham soc: ").strip())
            elif chon == 5:
                ql.hoan_thanh_cham_soc(input("Ma cham soc: ").strip())
            elif chon == 6:
                ql.xem_cham_soc_theo_cay(input("Ma cay: ").strip())
        except ValueError as loi:
            print("LOI:", loi)


def menu_thong_ke(ql):
    while True:
        print("\n1. So luong cay\n2. San luong qua\n3. The tich go")
        print("4. Chi phi cham soc\n5. Bao cao tong hop\n0. Quay lai")
        chon = nhap_lua_chon(0, 5)
        if chon == 0:
            return
        bao_cao = {
            1: ql.thong_ke_so_luong, 2: ql.thong_ke_thu_hoach,
            3: ql.thong_ke_go, 4: ql.thong_ke_chi_phi,
            5: ql.bao_cao_tong_hop,
        }
        bao_cao[chon]()


def main():
    ql = QuanLy()

    while True:
        print("\n========== QUAN LY CAY TRONG ==========")
        print("1. Quan ly cay trong")
        print("2. Quan ly cham soc")
        print("3. Bao cao va thong ke")
        print("0. Thoat chuong trinh")

        chon = nhap_lua_chon(0, 3)

        if chon == 0:
            print("Cam on ban da su dung chuong trinh!")
            break

        elif chon == 1:
            menu_cay(ql)

        elif chon == 2:
            menu_cham_soc(ql)

        elif chon == 3:
            menu_thong_ke(ql)


if __name__ == "__main__":
    main()
