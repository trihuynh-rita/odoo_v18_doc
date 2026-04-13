# So sánh hai giải pháp phổ biến nhất cho Odoo Community: **Odoo Full Accounting Kit (Cybrosys)** và **Odoo Mates Accounting (`om_account_accountant`)**. 

Việc chọn module nào không chỉ phụ thuộc vào số lượng tính năng, mà còn nằm ở cách chúng can thiệp vào core Odoo và khả năng mở rộng (scalability) khi dự án lớn lên.

### 1. So sánh Tổng quan (Chi phí, Hiệu năng, Kiến trúc)

Cả hai bộ module đều tuân thủ giấy phép **LGPL-3 (Hoàn toàn miễn phí)**, bạn có quyền sử dụng, sửa đổi mã nguồn cho mục đích thương mại mà không phải trả phí bản quyền.

| Tiêu chí | Cybrosys (`base_accounting_kit`) | Odoo Mates (`om_account_accountant` và các module phụ) |
| :--- | :--- | :--- |
| **Chi phí bản quyền** | 0 VNĐ | 0 VNĐ |
| **Triết lý thiết kế code** | **All-in-one (Nguyên khối):** Nhồi nhét mọi thứ (Asset, Budget, Report, Dashboard) vào một gói khổng lồ. | **Modular (Phân rã):** Chia nhỏ thành từng app độc lập (`om_account_asset`, `om_account_budget`, báo cáo riêng). |
| **Hiệu năng & Tốc độ tải** | Chậm hơn một chút. Khởi tạo Dashboard tốn tài nguyên do truy vấn trực tiếp lượng lớn dữ liệu (ORM search) để vẽ biểu đồ bằng JS/Owl. | **Rất nhẹ.** Tối ưu cực tốt vì chỉ gọi dữ liệu khi người dùng chủ động xuất báo cáo. Giao diện native của Odoo. |
| **UI/UX (Giao diện)** | Rất đẹp, hiện đại. Cố gắng sao chép trải nghiệm của Odoo Enterprise. | Tối giản. Khôi phục lại giao diện kế toán của các phiên bản Odoo cũ (v11, v12). |
| **Tính tương thích (Maintainability)**| Khó customize sâu. Do ghi đè (override) nhiều function lõi của `account.move`, dễ xảy ra xung đột với các module bên thứ ba khác. | **Thân thiện với Developer.** Kế thừa (`_inherit`) rất chuẩn mực, ít can thiệp thô bạo vào core. Dễ dàng viết code mở rộng thêm. |

---

### 2. Phân tích Chi tiết Tính năng (Feature-by-Feature)

**A. Báo cáo Tài chính (Financial Reports: PDF/Excel)**
* **Odoo Mates:** Sử dụng engine báo cáo QWeb tiêu chuẩn của Odoo. Các bản in PDF như Bảng cân đối kế toán, Kết quả kinh doanh, Sổ cái rất chuẩn mực, dễ đọc và nhẹ. Tốc độ xuất Excel cực nhanh.
* **Cybrosys:** Cung cấp hệ thống báo cáo "động" trên màn hình (Dynamic Reports) cho phép click vào từng dòng (drill-down) để xem bút toán chi tiết. Tuy nhiên, khi xuất ra PDF tiếng Việt với thư viện `wkhtmltopdf`, module này đôi khi bị vỡ layout do cấu trúc CSS tĩnh phức tạp.

**B. Quản lý Tài sản (Asset Management) & Ngân sách (Budget)**
* **Odoo Mates:** Tách hẳn thành hai module riêng là `om_account_asset` và `om_account_budget`. Nếu dự án công ty bạn chưa cần quản lý tài sản cố định ngay lập tức, bạn không cần cài, giúp database đỡ "rác".
* **Cybrosys:** Tích hợp cứng bên trong. Tính năng khấu hao tài sản (Depreciation) của Cybrosys tự động hóa tốt hơn một chút và giao diện cấu hình trực quan hơn.

**C. Bảng điều khiển (Accounting Dashboard)**
* **Cybrosys:** Đây là điểm ăn tiền nhất của họ. Dashboard cung cấp cái nhìn tổng quan ngay lập tức về Dòng tiền, Hóa đơn quá hạn, Lãi/Lỗ theo thời gian thực. 
* **Odoo Mates:** Không có Dashboard đồ sộ. Màn hình mặc định chỉ là dạng Kanban view hiển thị các Sổ nhật ký (Journals).

**D. Khóa sổ Kế toán (Lock Dates)**
Cả hai đều hỗ trợ tốt tính năng khóa sổ (Lock Date for Non-Advisers / All Users). Code xử lý logic chặn (raise ValidationError) khi sửa bút toán trong kỳ đã khóa của cả hai bên đều dựa trên core standard của Odoo, không có sự chênh lệch.

---

### 3. Khuyến nghị từ góc độ Odoo Framework

Là một kỹ sư phần mềm phát triển hệ thống ERP cho doanh nghiệp, quyết định chọn module sẽ định hình khả năng bảo trì code của bạn trong tương lai:

1.  **Nên chọn Odoo Mates khi:** Bạn ưu tiên sự ổn định, hệ thống chạy nhanh, và bạn tự tin vào khả năng lập trình của mình để viết thêm các tính năng (Custom modules) mở rộng sau này. Kiến trúc Modular của Odoo Mates là chuẩn mực hoàn hảo cho các dự án ERP tùy chỉnh sâu, đảm bảo khi nâng cấp version (ví dụ từ Odoo 17 lên 18) sẽ ít vỡ code nhất.
2.  **Nên chọn Cybrosys khi:** Bạn cần triển khai hệ thống cực nhanh (như một MVP cho startup), không muốn code thêm nhiều, và người dùng cuối (bộ phận Kế toán) thích một giao diện hào nhoáng, có sẵn Dashboard phân tích dòng tiền đẹp mắt để báo cáo trực tiếp cho Giám đốc mà không cần xuất Excel.

---

**Tài liệu tham khảo:**
* *Kho lưu trữ mã nguồn mở (GitHub)*: Mã nguồn kiến trúc phân rã của Odoo Mates ([https://github.com/odoomates](https://github.com/odoomates)).
* *Odoo Apps Store (Cybrosys)*: Thông số kỹ thuật và luồng xử lý báo cáo động của Odoo Full Accounting Kit ([https://apps.odoo.com/apps/modules/17.0/base_accounting_kit/](https://apps.odoo.com/apps/modules/17.0/base_accounting_kit/)).

Có khá nhiều lựa chọn khác ngoài hai cái đã đề cập. Dưới đây là bảng tổng hợp đầy đủ, phân theo nguồn gốc:

---

## Các module thay thế / bổ sung cho kế toán Odoo Community

### 🔵 Từ OCA (Odoo Community Association — mã nguồn mở, miễn phí)

| Module | Chức năng chính |
|---|---|
| **`mis_builder`** | Hệ thống báo cáo động, tạo báo cáo với các hàng KPI và cột theo kỳ kế toán, lý tưởng để so sánh theo tháng/quý/năm. Kết nối được với cả dữ liệu kế toán, bán hàng, mua hàng, nhân sự, kho… Đây là lựa chọn **mạnh nhất và linh hoạt nhất** trong hệ sinh thái Community. |
| **`account_financial_report`** | Sổ cái (General Ledger), Cân đối thử (Trial Balance), Open Items — đã đề cập trong yêu cầu. |
| **`account_reconcile_oca`** | Đối chiếu ngân hàng (bank reconciliation), được refactor hoàn toàn từ v16 trở đi. |
| **`account_banking_sepa_direct_debit` / `account_payment_order`** | Quản lý file thanh toán theo chuẩn SEPA và các định dạng ngân hàng phổ biến, đã hoạt động hơn 10 năm trong cộng đồng OCA. |
| **`account_bank_statement_import_*`** | Nhập tự động các file sao kê ngân hàng (OFX, CSV, CAMT…), giảm thiểu nhập liệu thủ công. |

### 🟡 Từ Odoo Mates (miễn phí trên GitHub)

| Module | Chức năng chính |
|---|---|
| **`om_account_accountant`** | Bổ sung các tính năng: báo cáo tài chính, quản lý tài sản cố định (Asset Management), quản lý ngân sách (Budget Management), nhập sao kê ngân hàng, báo cáo theo ngày. Là đối thủ trực tiếp của `base_accounting_kit`. |

### 🟠 Từ nhà phát triển thứ ba (trả phí trên Odoo App Store)

| Module | Nhà cung cấp | Ghi chú |
|---|---|---|
| **`accounting_pdf_reports`** | Odoo Mates | Báo cáo PDF: Sổ cái, Balance Sheet, P&L, Partner Ledger |
| **`dynamic_financial_reports`** | Nhiều vendor | Xem báo cáo trực tiếp trên web (không cần xuất PDF) |
| **`account_accountant` (bản port)** | Các vendor khác nhau | Port lại module Enterprise |

---

## Gợi ý cho dự án Việt Nam

Nếu kết hợp với `l10n_vn`, stack được khuyến nghị là:

```
account + l10n_vn + mis_builder + account_financial_report (OCA)
```

Hoặc nếu muốn đơn giản hơn (1 module duy nhất):

```
account + l10n_vn + base_accounting_kit (Cybrosys)
```

**Điểm khác biệt quan trọng giữa `base_accounting_kit` và `om_account_accountant`:** Cả hai đều làm việc tương tự nhau, nhưng `base_accounting_kit` của Cybrosys được cập nhật thường xuyên hơn và có hỗ trợ kỹ thuật trả phí, trong khi `om_account_accountant` hoàn toàn miễn phí và mã nguồn mở trên GitHub.