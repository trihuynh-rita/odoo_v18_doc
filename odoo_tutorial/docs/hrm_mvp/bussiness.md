### 1. Quản lý Dữ liệu Nhân sự Cốt lõi (Core HR & Employee Data)
* **Mô tả:** Đây là cơ sở dữ liệu tập trung (Centralized Database) lưu trữ toàn bộ hồ sơ kỹ thuật số của nhân viên, bao gồm thông tin cá nhân, hợp đồng lao động, cấu trúc phòng ban, và lịch sử công tác.
* **Chức năng:** Giúp HR dễ dàng truy xuất thông tin, theo dõi vòng đời nhân viên. Thông thường, tính năng này đi kèm cổng thông tin tự phục vụ (Self-service portal) để nhân viên tự cập nhật thông tin cá nhân hoặc xem sổ tay nhân viên.

### 2. Quản lý Chấm công và Tiền lương (Time, Attendance & Payroll)
* **Mô tả:** Tự động hóa việc ghi nhận thời gian làm việc và tính toán thu nhập hàng tháng.
* **Chức năng:** Hệ thống thu thập dữ liệu từ máy chấm công sinh trắc học hoặc ứng dụng check-in, quản lý lịch duyệt nghỉ phép (Leave Management), và tự động đối chiếu với các chính sách thuế, bảo hiểm xã hội, phụ cấp để xuất ra bảng lương (Payroll) chính xác, giảm thiểu sai sót thủ công.

### 3. Quản lý Tuyển dụng (Applicant Tracking System - ATS)
* **Mô tả:** Quản lý luồng công việc từ khâu thu hút ứng viên cho đến khi nhận việc (Onboarding).
* **Chức năng:** Cho phép tạo yêu cầu tuyển dụng, đăng tin tự động lên các nền tảng việc làm, phân loại CV, lên lịch phỏng vấn, và gửi email phản hồi tự động. Khi một ứng viên trúng tuyển, dữ liệu từ ATS sẽ tự động chuyển sang module Core HR.

---
### Tài liệu tham khảo:
* **Wikipedia:** Các tính năng cốt lõi này được tham chiếu theo tiêu chuẩn cấu trúc hệ thống trong bài viết [Human resource management system (HRMS)](https://en.wikipedia.org/wiki/Human_resource_management_system) (mục *Functions* bao gồm Core HR, Payroll, và Applicant tracking).
* **Hệ thống Thông tin Nhân sự (HRIS):** Theo các tài liệu học thuật về Hệ thống Thông tin Quản lý, đây là 3 module bắt buộc phải có để chuyển đổi số nghiệp vụ nhân sự truyền thống sang tự động hóa.

Bạn có muốn tôi thiết kế một sơ đồ thực thể kết nối (ERD) cơ bản cho một trong ba module này để dễ hình dung cách lưu trữ dưới database không?