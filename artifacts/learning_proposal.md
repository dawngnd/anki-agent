# Learning Proposal: Lưu trữ Artifacts và Thông tin vào thư mục `artifacts/`

## 1. Phân loại (Classification)
- **Loại hình**: **Rule** (Quy tắc workspace cấp thư mục gốc).
- **Phạm vi**: Áp dụng cho toàn bộ workspace [anki-agent](file:///home/dangnd/code/github/anki-agent).
- **Tập tin đích**: [GEMINI.md](file:///home/dangnd/code/github/anki-agent/GEMINI.md).

## 2. Lý do và Mục tiêu (Rationale)
Mặc định, hệ thống AGY lưu trữ các artifacts trong thư mục nội bộ `brain` (`~/.gemini/antigravity-cli/brain/<conversation-id>/`). Người dùng muốn toàn bộ thông tin làm việc, tài liệu tổng kết và artifacts được lưu trực tiếp vào thư mục [artifacts/](file:///home/dangnd/code/github/anki-agent/artifacts) nằm trong thư mục gốc của dự án để thuận tiện xem, quản lý phiên bản và lưu trữ trong repository.

## 3. Nội dung đề xuất thêm vào [GEMINI.md](file:///home/dangnd/code/github/anki-agent/GEMINI.md)

Tập tin [GEMINI.md](file:///home/dangnd/code/github/anki-agent/GEMINI.md) hiện chưa tồn tại. Đề xuất tạo mới tập tin với nội dung sau:

```markdown
# Quy tắc Dự án (Project Rules)

## Lưu trữ Artifacts và Tài liệu Làm việc (Artifact & Work Storage)
- **Vị trí lưu trữ**: Mọi thông tin làm việc, tài liệu tóm tắt/báo cáo, và artifact được tạo ra phải được lưu trực tiếp vào thư mục `artifacts/` của workspace dự án (`artifacts/<tên-file>.md`), thay vì chỉ lưu trong thư mục nội bộ `brain` của AGY.
- **Quy trình thực hiện**: Khi tạo hoặc cập nhật một artifact, luôn đồng thời ghi hoặc sao chép nội dung đó vào thư mục `artifacts/` trong workspace để người dùng có thể truy cập và quản lý trực tiếp trong dự án.
```

## 4. Các bước tiếp theo
Sau khi bạn phê duyệt đề xuất này bằng cách bấm **Proceed** hoặc phản hồi đồng ý, tôi sẽ tiến hành tạo tập tin [GEMINI.md](file:///home/dangnd/code/github/anki-agent/GEMINI.md) với nội dung trên.
