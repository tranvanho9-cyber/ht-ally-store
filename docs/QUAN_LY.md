# Hướng dẫn quản lý kho (nội bộ)

## Cập nhật plugin (mỗi lần chỉ 1 thao tác)
1. Vào repo trên github.com -> thư mục `rbz` -> **Add file > Upload files**.
2. Kéo file `.rbz` mới vào (tên dạng `dc_explode_v5_3_2.rbz`, số phiên bản ở cuối) -> **Commit changes**.
3. Xong. GitHub tự tạo lại `catalog.json` sau ~30 giây. HT Ally ở máy người dùng tự hiện nút **Cập nhật**.

Không cần sửa `catalog.json`, không cần đóng lại HT Ally.

## Thêm plugin mới
Sửa `plugins.json` (thêm 1 khối giống `dc_explode`), rồi đưa file `.rbz` của nó vào `rbz/`.
`loader` và `folder` phải đúng tên bên trong file .rbz (vd `dc_explode.rb` và `dc_explode`).

## Cập nhật chính HT Ally
Đưa `HT_Ally_v1_x_y.rbz` vào `rbz/` cùng cách trên; Ally tự báo có bản mới.

## Kho này
Tài khoản: tranvanho9-cyber · Kho: ht-ally-store · catalog: https://raw.githubusercontent.com/tranvanho9-cyber/ht-ally-store/main/catalog.json

## Các trường tùy chọn trong plugins.json (HT Ally 1.8 trở lên)
- `"category": "Dựng hình"`: nhóm của plugin, Ally tự tạo nút lọc theo chữ này (viết giống nhau cho cùng nhóm).
- `"video": "https://..."`: link video hướng dẫn, nút "?" trên thẻ sẽ mở link này.
- `"min_su": 2022` và `"max_su": 2026`: năm SketchUp thấp nhất và cao nhất mà plugin chạy được. Ngoài khoảng này Ally báo "Không tương thích" và không cho cài.
- `"changelog"`: ghi chú phiên bản, hiện ở nút "Có gì mới" khi có bản cập nhật:
```json
"changelog": [
  { "version": "5.4.2", "date": "22/10/2026", "items": ["Thêm hộp thoại mua", "Sửa lỗi xoay vân"] }
]
```
- `"price"`, `"version"`, `"rbz_prefix"`, `"loader"`, `"folder"`: như hướng dẫn ở trên.

Trong `meta` có thể thêm `"news"` (thông báo tính năng mới), `"support_zalo"`, `"support_email"`, `"website"`.
