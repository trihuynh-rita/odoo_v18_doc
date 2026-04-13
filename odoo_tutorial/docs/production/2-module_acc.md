# MODULE ACC

## Các module cho hệ thống ACC

### 1. Nhóm Nền tảng Kế toán (Bắt buộc)

Để hệ thống đáp ứng chuẩn mực tài chính cơ bản và có thể xuất báo cáo, dự án cần cài đặt chuỗi module sau:

  * **`account` (Invoicing):** Module lõi quản lý hóa đơn khách hàng, hóa đơn nhà cung cấp và công nợ (phải thu/phải trả).
  * **`l10n_vn` (Vietnam - Accounting):** Cung cấp cấu trúc dữ liệu chuẩn theo Thông tư của Bộ Tài chính Việt Nam (Hệ thống tài khoản, các loại thuế GTGT đầu ra/đầu vào).
  * **`base_accounting_kit` (từ Cybrosys) hoặc `account_financial_report` (từ OCA):** Mở khóa tính năng sổ cái (General Ledger), bút toán thủ công (Journal Entries) và các báo cáo tài chính (Bảng cân đối kế toán, Báo cáo kết quả hoạt động kinh doanh) vốn bị ẩn ở bản Community.

### 2. Nhóm Kế toán Quản trị & Dự án (Analytic Accounting)

Đối với các dự án công ty có cấu trúc đa chi nhánh hoặc mô hình tập đoàn, việc hạch toán chung vào một sổ cái là không đủ. Bạn cần cài đặt:

  * **`analytic` (Analytic Accounting):** Cho phép tạo các "Tài khoản phân tích" (Analytic Accounts) độc lập. Module này dùng để bóc tách, theo dõi chi phí và doanh thu chi tiết cho từng dự án, phòng ban, hoặc từng mảng kinh doanh cụ thể mà không làm rối Hệ thống tài khoản chính (Chart of Accounts).

### 3. Nhóm Tích hợp Luồng dữ liệu

Kế toán cần nhận dữ liệu tự động từ các nghiệp vụ vận hành khác trong doanh nghiệp:

  * **`pos_accounting` (Tích hợp Kế toán POS):** Cần thiết nếu công ty có vận hành mảng nhà hàng (F&B) hoặc chuỗi cửa hàng bán lẻ. Module này đảm bảo việc tự động hạch toán doanh thu, thuế và tiền mặt ngay khi nhân viên thu ngân đóng ca (Close Session) trên hệ thống Point of Sale.
  * **`stock_account` (Tích hợp Kế toán Kho):** Cho phép kích hoạt tính năng định giá hàng tồn kho tự động (Automated Inventory Valuation). Khi có phiếu xuất hoặc nhập kho vật tư, hệ thống tự động sinh bút toán thay đổi giá trị tài sản.
  * **`hr_expense` (Chi phí nhân sự):** Cho phép nhân viên trực tiếp tạo yêu cầu hoàn ứng, thanh toán chi phí công tác để bộ phận kế toán duyệt và ghi sổ.

-----

**Tài liệu tham khảo:**

  * *Odoo Official Documentation*: Đặc tả kỹ thuật và luồng hoạt động của hệ thống tài khoản phân tích (Analytic Accounting) để quản lý chi phí dự án trực tiếp trên framework ([https://www.odoo.com/documentation/17.0/applications/finance/accounting/others/analytic_accounting.html](https://www.google.com/search?q=https://www.odoo.com/documentation/17.0/applications/finance/accounting/others/analytic_accounting.html)).
  * *Odoo Community Association (OCA) GitHub*: Kho lưu trữ các tiêu chuẩn module báo cáo tài chính mã nguồn mở ([https://github.com/OCA/account-financial-reporting](https://github.com/OCA/account-financial-reporting)).

## Nền tảng kế toán

### 1. Danh sách các Module cần thiết

**Nhóm Module Lõi (Có sẵn trong hệ thống Odoo Community):**
* **Invoicing (`account`):** Module cốt lõi để quản lý hóa đơn khách hàng và hóa đơn nhà cung cấp. 

**Nhóm Module Kế toán Mã nguồn mở (Bên thứ ba):**
* **Odoo Full Accounting Kit (bởi Cybrosys Techno Solutions)** hoặc **Odoo Accounting (bởi Odoo Mates):** Đây là các module miễn phí tốt nhất hiện nay trên hệ thống Odoo Apps Store. Chúng cung cấp đầy đủ các tính năng bị thiếu trong bản Community như: Sổ cái (General Ledger), Quản lý tài sản (Asset Management), Ngân sách (Budget), Báo cáo tài chính (PDF/Excel), và Khóa sổ kỳ kế toán.

**Nhóm Module Kế toán Việt Nam (Localization):**
* **Vietnam - Accounting (`l10n_vn`):** Thường do cộng đồng OCA (Odoo Community Association) hoặc đối tác Viindoo phát triển. Module này cung cấp Hệ thống tài khoản chuẩn theo Thông tư 200/2014/TT-BTC hoặc 133/2016/TT-BTC, cấu hình sẵn các loại thuế GTGT (VAT) và định dạng tiền tệ mặc định là Việt Nam Đồng (VND).

---

### 2. Cách khắc phục lỗi Font Unicode Tiếng Việt khi xuất PDF

Lỗi hiển thị tiếng Việt (ô vuông, mất chữ, tràn khung) khi in hóa đơn hoặc báo cáo trong Odoo xuất phát từ thư viện ngoại vi tên là `wkhtmltopdf`. Odoo sử dụng công cụ này để chuyển đổi dữ liệu HTML sang PDF. Nếu máy chủ thiếu font chữ hoặc sử dụng sai phiên bản `wkhtmltopdf`, quá trình render Unicode sẽ thất bại.



**Cách xử lý triệt để trên máy chủ (thường là Ubuntu/Linux):**
1.  **Cài đặt đúng phiên bản có vá lỗi Qt (Qt-patched):** Tuyệt đối không cài `wkhtmltopdf` bằng lệnh `apt-get install` mặc định của Ubuntu vì bản phân phối này thiếu bản vá giao diện Qt. Bạn phải tải trực tiếp gói `.deb` bản 0.12.5-1 hoặc 0.12.6 từ kho lưu trữ chính thức của `wkhtmltopdf` trên GitHub và cài đặt bằng lệnh `dpkg`.
2.  **Cài đặt bộ Font chữ MS Core hỗ trợ Tiếng Việt:** Chạy lệnh sau trên máy chủ để nạp các font tiêu chuẩn (như Times New Roman, Arial):
    `sudo apt-get install ttf-mscorefonts-installer`
3.  **Xóa bộ nhớ đệm (cache) của font:**
    `sudo fc-cache -f -v`
4.  **Khởi động lại dịch vụ Odoo:** Để hệ thống cập nhật và nhận diện thư viện đồ họa mới.

---

### 3. Thứ tự cài đặt chuẩn xác

Để tránh lỗi xung đột cơ sở dữ liệu (Database constraint violations), bạn **bắt buộc** phải thao tác theo đúng trình tự sau:

1.  **Cài đặt `wkhtmltopdf` và Font chữ (Trên Server):** Hoàn tất toàn bộ thiết lập ở mục 2 trước khi thao tác trên giao diện web của Odoo.
2.  **Cài đặt Module Lõi:** Truy cập menu *Apps (Ứng dụng)* -> Tìm và cài đặt module **Invoicing** đầu tiên để tạo nền tảng cơ sở dữ liệu.
3.  **Cài đặt Gói Kế toán Việt Nam:** Cài đặt module **Vietnam - Accounting (`l10n_vn`)**. Ngay sau khi cài xong, hệ thống sẽ yêu cầu bạn chọn Công ty (Company) và tự động áp đặt Hệ thống tài khoản theo Thông tư kế toán bạn chọn.
4.  **Cài đặt Accounting Kit (Bên thứ 3):** Đưa thư mục code giải nén của Cybrosys hoặc Odoo Mates vào thư mục `addons_path` trên máy chủ. Kích hoạt Developer Mode (Chế độ nhà phát triển) trên web, chọn *Update Apps List (Cập nhật danh sách ứng dụng)* và bấm cài đặt module **Full Accounting Kit**.

---

### 4. Tổng hợp Chi phí

* **Chi phí bản quyền mã nguồn (License):** 0 VNĐ. Toàn bộ Odoo Community, PostgreSQL, Cybrosys Kit và gói `l10n_vn` đều miễn phí.
* **Chi phí hạ tầng máy chủ (Cloud Server / VPS):** Phụ thuộc vào nhà cung cấp hạ tầng (như AWS, Google Cloud, DigitalOcean hoặc các đơn vị trong nước). Một cấu hình trung bình để chạy mượt mà tốn khoảng 250.000đ - 1.000.000đ/tháng (tùy thuộc vào thông số RAM và CPU được cấp phát).

*Tài liệu tham khảo:*
* *GitHub (odoo/odoo)*: Các bản ghi chú phát hành (RFC) liên quan đến phát triển hệ thống tài khoản Việt Nam (`l10n_vn`).
* *Odoo Apps Store*: Đặc tả kỹ thuật và yêu cầu môi trường của các gói mở rộng từ Cybrosys và Odoo Mates.

Bạn có muốn tôi cung cấp đoạn script lệnh (Bash shell) để dọn dẹp các phiên bản `wkhtmltopdf` bị lỗi cũ và tự động hóa quá trình cài đặt bộ vá lỗi Qt kèm font Tiếng Việt trên máy chủ Ubuntu của bạn không?

[Hướng dẫn sửa lỗi xuất PDF bằng wkhtmltopdf cho Odoo trên Ubuntu](https://www.youtube.com/watch?v=CEZy4BBvRxs)
Video này hướng dẫn trực quan các bước gỡ lỗi và cấu hình wkhtmltopdf trên môi trường Ubuntu để đảm bảo báo cáo PDF không bị mất chữ hoặc thiếu định dạng.


http://googleusercontent.com/youtube_content/8