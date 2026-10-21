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
