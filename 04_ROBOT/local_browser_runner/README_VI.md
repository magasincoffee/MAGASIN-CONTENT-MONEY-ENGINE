# MAGASIN Local Browser Runner V1

Mục tiêu: cho phép GitHub giao **các browser task đã được code và allowlist sẵn** tới máy Windows của Owner thông qua GitHub Actions self-hosted runner.

## Five-Step

1. QUESTION — chỉ tự động hóa những bước đã chứng minh cần thiết.
2. DELETE — không có remote shell tổng quát, không nhận lệnh PowerShell tùy ý.
3. SIMPLIFY — một repo-scoped self-hosted runner + một Chrome profile robot + JSON command nhỏ.
4. ACCELERATE — GitHub push/dispatch giao task trực tiếp xuống máy.
5. AUTOMATE — mở rộng action allowlist chỉ sau khi từng workflow đã được chứng minh an toàn và hữu ích.

## Kiến trúc

```text
GitHub command JSON
       |
       v
GitHub Actions workflow
       |
       v
repo-scoped self-hosted runner on Owner Windows
       |
       v
PowerShell launcher
       |
       v
Playwright attach -> Chrome CDP 127.0.0.1:9222
       |
       v
Shopee Affiliate / other future allowlisted browser flows
       |
       v
sanitized evidence artifact
```

Không có cookie/password/OTP/session-token export.

## Security boundaries

- runner scoped vào repository này;
- custom runner label: `magasin-browser`;
- Chrome remote debugging chỉ bind `127.0.0.1`;
- Chrome dùng profile riêng: `%LOCALAPPDATA%\MAGASIN\ChromeRobot`;
- command JSON không có field arbitrary shell;
- action hiện tại duy nhất:
  - `SHOPEE_AFFILIATE_LINK_SMOKE_TEST`;
- URL sản phẩm phải là HTTPS Shopee Vietnam;
- `shop_id/item_id` trong command phải khớp URL;
- không mua hàng;
- không gửi message;
- không đổi payout/KYC/tax;
- không tự xử lý password/OTP/MFA/CAPTCHA.

## One-time install trên Windows

Sau khi code này có trên main, tải bootstrap từ GitHub và chạy trong PowerShell:

```powershell
$Url = "https://raw.githubusercontent.com/magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE/main/04_ROBOT/local_browser_runner/bootstrap_runner.ps1"
$File = "$env:TEMP\magasin-bootstrap-runner.ps1"
Invoke-WebRequest $Url -OutFile $File
powershell -ExecutionPolicy Bypass -File $File
```

Bootstrap sẽ:

1. kiểm tra/cài GitHub CLI và Python nếu thiếu;
2. yêu cầu Owner login GitHub một lần nếu cần;
3. lấy short-lived runner registration token bằng quyền repo của Owner;
4. tải GitHub Actions runner mới nhất;
5. đăng ký runner repo-scoped với label `magasin-browser`;
6. thêm runner vào Windows Startup để tự chạy khi Owner đăng nhập;
7. mở Chrome profile robot với CDP local-only.

Không gửi GitHub token cho chat.

## One-time Shopee login

Chrome robot sẽ mở:

`https://affiliate.shopee.vn/`

Owner tự đăng nhập một lần trong profile này và tự xử lý OTP/MFA/CAPTCHA.

Sau đó giữ profile `ChromeRobot`; workflow sau tái sử dụng session local.

## Giao việc từ GitHub

Workflow:

`.github/workflows/magasin-local-browser-runner.yml`

Có hai cách:

### A. Manual GitHub Run workflow

Chọn command JSON repo-relative.

### B. Robot-control branch

Workflow tự chạy khi file sau thay đổi trên branch `robot-control`:

`04_ROBOT/local_browser_runner/commands/current.json`

Điều này cho phép Brain/Work cập nhật một command JSON hợp lệ trên GitHub để giao task xuống máy Owner mà không cần remote shell.

## Command schema

Ví dụ:

```json
{
  "schema_version": "magasin.local-browser-command.v1",
  "command_id": "MCME-049-smoke-01",
  "action": "SHOPEE_AFFILIATE_LINK_SMOKE_TEST",
  "product_url": "https://shopee.vn/product/1651109667/27495157821",
  "expected_shop_id": "1651109667",
  "expected_item_id": "27495157821",
  "created_at": "2026-09-23T22:00:00+07:00"
}
```

Mọi field không có trong schema bị fail-closed.

## Evidence

Output local/workflow artifact:

`04_ROBOT/local_browser_runner/evidence/`

Evidence chỉ chứa trạng thái sanitized như:

- command_id;
- generated affiliate URL nếu có;
- redirect status;
- final product match;
- final sanitized URL;
- HTTP status;
- safety assertions.

Không ghi cookie, password, OTP, token.

## Khi login hết hạn

Robot trả:

`WAIT_OWNER_LOGIN_REQUIRED`

Owner chỉ cần mở profile Chrome robot đang chạy và đăng nhập lại. Không tạo account mới và không gửi credential cho Work.

## Không cài runner như Windows Service

Runner được giữ trong logged-in desktop session để Chrome/Playwright có thể thao tác browser UI. Startup shortcut tự khởi động runner sau khi Owner login Windows.
