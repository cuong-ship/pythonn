import json

# ------------------ Lớp Sinh Viên ------------------
class SinhVien:
    def __init__(self, ma, ten, lop, ngay_sinh):
        self.ma = ma
        self.ten = ten
        self.lop = lop
        self.ngay_sinh = ngay_sinh
        self.diem = {}

    def to_dict(self):
        return {
            "ma": self.ma,
            "ten": self.ten,
            "lop": self.lop,
            "ngay_sinh": self.ngay_sinh,
            "diem": self.diem
        }

    @staticmethod
    def from_dict(data):
        sv = SinhVien(data["ma"], data["ten"], data["lop"], data["ngay_sinh"])
        sv.diem = data.get("diem", {})
        return sv


# ------------------ Lớp Quản Lý ------------------
class QuanLyDiem:
    def __init__(self):
        self.ds = []

    def khoi_tao(self):
        self.ds = []
        print("Danh sách đã được khởi tạo.")

    def danh_sach_rong(self):
        return len(self.ds) == 0

    def them_dau(self, sv):
        self.ds.insert(0, sv)

    def them_cuoi(self, sv):
        self.ds.append(sv)

    def hien_thi(self):
        if not self.ds:
            print(" Danh sách rỗng.")
        else:
            print("\n DANH SÁCH SINH VIÊN:")
            for sv in self.ds:
                print(f"{sv.ma} | {sv.ten} | Lớp: {sv.lop} | Ngày sinh: {sv.ngay_sinh} | Điểm: {sv.diem}")

    def tim_ma(self, ma):
        return next((sv for sv in self.ds if sv.ma == ma), None)

    def xoa_ma(self, ma):
        truoc = len(self.ds)
        self.ds = [sv for sv in self.ds if sv.ma != ma]
        if len(self.ds) < truoc:
            print(" Đã xóa sinh viên.")
        else:
            print(" Không tìm thấy mã.")

    def ghi_file(self, ten_file):
        with open(ten_file, "w", encoding="utf-8") as f:
            json.dump([sv.to_dict() for sv in self.ds], f, ensure_ascii=False, indent=2)
        print(f" Đã ghi vào file {ten_file}")

    def doc_file(self, ten_file):
        try:
            with open(ten_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.ds = [SinhVien.from_dict(sv) for sv in data]
            print(f" Đã đọc danh sách từ file {ten_file}")
        except FileNotFoundError:
            print(" File không tồn tại.")

    def nhap_diem(self, ma_sv, mon, diem):
        sv = self.tim_ma(ma_sv)
        if sv:
            try:
                diem = float(diem)
                sv.diem[mon] = diem
                print(" ✅ Nhập điểm thành công.")
            except ValueError:
                print(" ❌ Điểm không hợp lệ.")
        else:
            print(" ❌ Không tìm thấy sinh viên.")

    def diem_trung_binh(self, sv):
        if not sv.diem:
            return None
        return round(sum(sv.diem.values()) / len(sv.diem), 2)


# ------------------ Nhập từ bàn phím ------------------
def nhap_sinh_vien():
    ma = input(" Nhập mã sinh viên: ")
    ten = input(" Nhập họ tên: ")
    lop = input(" Nhập lớp: ")
    ngay_sinh = input(" Nhập ngày sinh: ")
    return SinhVien(ma, ten, lop, ngay_sinh)


# ------------------ Menu ------------------
def menu():
    ql = QuanLyDiem()
    while True:
        print("\n--------- MENU QUẢN LÝ ĐIỂM THI ---------")
        print("1. Khởi tạo danh sách")
        print("2. Thêm sinh viên vào đầu")
        print("3. Thêm sinh viên vào cuối")
        print("4. Hiển thị danh sách sinh viên")
        print("5. Nhập điểm cho sinh viên")
        print("6. Tính điểm trung bình của sinh viên")
        print("7. Tìm sinh viên theo mã")
        print("8. Xóa sinh viên theo mã")
        print("9. Ghi danh sách ra file")
        print("10. Đọc danh sách từ file")
        print("0. Thoát")
        chon = input("👉 Nhập lựa chọn: ")

        if chon == '1':
            ql.khoi_tao()
        elif chon == '2':
            sv = nhap_sinh_vien()
            ql.them_dau(sv)
        elif chon == '3':
            sv = nhap_sinh_vien()
            ql.them_cuoi(sv)
        elif chon == '4':
            ql.hien_thi()
        elif chon == '5':
            ma = input(" Nhập mã sinh viên: ")
            mon = input(" Nhập tên môn: ")
            diem = input(" Nhập điểm: ")
            ql.nhap_diem(ma, mon, diem)
        elif chon == '6':
            ma = input(" Nhập mã sinh viên: ")
            sv = ql.tim_ma(ma)
            if sv:
                dtb = ql.diem_trung_binh(sv)
                if dtb is not None:
                    print(f" 👉 Điểm trung bình: {dtb}")
                else:
                    print(" Chưa có điểm.")
            else:
                print(" Không tìm thấy sinh viên.")
        elif chon == '7':
            ma = input(" Nhập mã cần tìm: ")
            sv = ql.tim_ma(ma)
            if sv:
                print(f" {sv.ma} | {sv.ten} | Lớp: {sv.lop} | Ngày sinh: {sv.ngay_sinh} | Điểm: {sv.diem}")
            else:
                print(" Không tìm thấy.")
        elif chon == '8':
            ma = input(" Nhập mã cần xóa: ")
            ql.xoa_ma(ma)
        elif chon == '9':
            ql.ghi_file("diemthi.json")
        elif chon == '10':
            ql.doc_file("diemthi.json")
        elif chon == '0':
            print(" Thoát chương trình.")
            break
        else:
            print(" ❗ Lựa chọn không hợp lệ.")


# ------------------ Chạy chương trình ------------------
if __name__ == "__main__":
    menu()
