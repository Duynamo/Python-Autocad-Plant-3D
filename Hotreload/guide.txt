# Tổng quan hệ thống Hot-Reload cho Custom Script trong AutoCAD Plant 3D

Hệ thống này được thiết kế để giải quyết hai vấn đề lớn nhất khi phát triển Custom Script: tốc độ phát triển và chất lượng mã nguồn. Nó bao gồm 4 tệp chính phối hợp với nhau một cách thông minh.

---
### 1. `hotreload_impl.py`: Trái tim của Logic

- **Vai trò:** Đây là tệp mà **bạn, với tư cách là lập trình viên, sẽ làm việc nhiều nhất**. Nó chứa logic dựng hình cốt lõi của bạn trong hàm `run()`.
- **Cách hoạt động:** Tệp này được thiết kế để chỉ chứa mã Python thuần túy cho việc tạo hình. Nó không cần các câu lệnh `import` hay các decorator `@activate`, `@param` vì nó không bao giờ được Plant 3D gọi trực tiếp. Nó giống như một bản thiết kế chi tiết.
- **Tóm lại:** Đây là nơi bạn viết mã để vẽ cái van, cái co, hay bất kỳ chi tiết nào bạn muốn.

---
### 2. `primitives.py`: Thư viện Trợ giúp & Nâng cao Chất lượng

- **Vai trò:** Đây là một thư viện trợ giúp (helper library) được viết tùy chỉnh để làm cho việc viết mã trong `hotreload_impl.py` trở nên **dễ dàng, dễ đọc và an toàn hơn**.
- **Cách hoạt động:** Nó cung cấp các "lớp bao bọc" (wrapper classes) như `primitives.Box` hay `primitives.Cylinder`. Các lớp này thông minh hơn các hàm gốc, ví dụ như tự động đặt đáy của khối hộp lên mặt phẳng Z=0.
- **Tóm lại:** Đây là bộ công cụ "xịn" giúp bạn xây dựng mô hình nhanh hơn và ít lỗi hơn.

---
### 3. `hotreload.py`: Người Quản lý & Cầu nối

- **Vai trò:** Đây là tệp "cửa ngõ" được **đăng ký chính thức với Plant 3D** (`PLANTREGISTERCUSTOMSCRIPTS`). Nó đóng vai trò là cầu nối giữa Plant 3D và mã nguồn mới nhất của bạn.
- **Cách hoạt động:** Khi được gọi, nó sẽ đọc nội dung của `hotreload_impl.py`, chuẩn bị một môi trường thực thi (có sẵn thư viện `primitives.py`), và chạy mã nguồn đó.
- **Tóm lại:** Tệp này là người quản lý, đảm bảo rằng mã nguồn mới nhất của bạn luôn được sử dụng và được cung cấp đầy đủ công cụ.

---
### 4. `hotreload.lsp`: Người Tự động hóa Công việc

- **Vai trò:** Đây là một script AutoLISP giúp **tự động hóa các thao tác nhàm chán trong AutoCAD**.
- **Cách hoạt động:** Nó tạo ra một lệnh tùy chỉnh tên là `SYNCWRAPPER`. Khi bạn gõ lệnh này, nó sẽ tự động: xóa đối tượng cũ, dọn dẹp bộ nhớ cache của block, và tái tạo đối tượng mới.
- **Tóm lại:** Tệp này giúp bạn cập nhật mô hình chỉ bằng một lệnh duy nhất.

---
### Tổng kết quy trình làm việc (Workflow)

#### Thiết lập (Làm 1 lần):
1.  Đăng ký `hotreload.py` bằng lệnh `PLANTREGISTERCUSTOMSCRIPTS`.
2.  Tải `hotreload.lsp` vào AutoCAD bằng lệnh `APPLOAD`.

#### Chu trình phát triển (Lặp đi lặp lại):
1.  **Chỉnh sửa:** Mở và thay đổi logic dựng hình trong `hotreload_impl.py`. Lưu lại.
2.  **Đồng bộ:** Chuyển sang AutoCAD và gõ lệnh `SYNCWRAPPER`.
3.  **Xem kết quả:** Đối tượng mới với những thay đổi của bạn ngay lập tức xuất hiện.

##### Lưu ý quan trọng nhất:
Các tham số được truyền vào hàm run cần được đồng bộ trong cả 
hotreload và hotreload_impl .
→ Cần hình dung được các tham số nào sẽ tùy biến trước khi thực hiện viết code
　nếu không code sẽ không chạy

