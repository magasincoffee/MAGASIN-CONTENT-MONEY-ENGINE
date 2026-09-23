# ACCESSTRADE Browser Explorer V1

Mục tiêu: sau khi Owner tự đăng nhập ACCESSTRADE trong trình duyệt, Robot tự đi qua các trang nội bộ có thể truy cập và tạo bản đồ cấu trúc để Brain biết chính xác:

- menu nào tồn tại;
- campaign/tool/report nào có route;
- trang nào chứa form;
- các link nội bộ;
- các API/XHR endpoint cùng host đã được frontend gọi;
- đâu là vùng nhạy cảm cần Owner gate;
- adapter nào đáng viết tiếp để rút ngắn đường tới affiliate click/order/cash.

## Five-Step

QUESTION:
Ta có thực sự cần reverse-engineer toàn bộ hệ thống hay chỉ cần biết route/API đủ để lấy campaign, tạo deeplink và đọc report?

DELETE:
V1 không tự login, không lấy password/OTP/cookie, không submit form, không bấm button, không đăng ký campaign, không tạo affiliate link, không sửa hồ sơ, không rút tiền, không dùng paid traffic, không viết generic browser agent.

SIMPLIFY:
Chỉ làm một read-only site mapper.

ACCELERATE:
Sau khi có site_map.json, chỉ viết adapter cho đường tiền ngắn nhất:

    CAMPAIGN / PRODUCT
    → DEEPLINK
    → CLICK REPORT
    → CONVERSION / COMMISSION

AUTOMATE:
Chỉ sau khi các read adapter và money attribution đã được xác minh.

## Cài đặt

Yêu cầu Python 3.11+.

    cd 04_ROBOT/accesstrade_browser_explorer
    python -m venv .venv

Windows:

    .venv\Scripts\activate

macOS/Linux:

    source .venv/bin/activate

Cài dependency:

    pip install -r requirements.txt
    python -m playwright install chromium

## Chạy V1

### Cách khuyên dùng khi đăng nhập ACCESSTRADE bằng Google

Google có thể từ chối OAuth bên trong Chromium do Playwright tự mở. Không cố bypass cảnh báo đó.

Thay vào đó:

1. Mở **Chrome thật** bằng một profile riêng dành cho Robot, có bật local remote debugging.
2. Owner tự đăng nhập Google/ACCESSTRADE trong Chrome đó.
3. Robot chỉ attach vào phiên Chrome đã đăng nhập.

PowerShell:

    $Chrome = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
    if (-not (Test-Path $Chrome)) {
        $Chrome = "$env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe"
    }

    $RobotChromeProfile = "$HOME\accesstrade-robot-chrome"

    Start-Process $Chrome -ArgumentList @(
        "--remote-debugging-port=9222",
        "--user-data-dir=$RobotChromeProfile",
        "https://pub2.accesstrade.vn/report/overview"
    )

Trong Chrome vừa mở:
- Owner tự đăng nhập;
- tự xử lý Google OAuth/MFA/CAPTCHA;
- vào ACCESSTRADE Publisher Dashboard.

Sau đó chạy Robot:

    $PY = ".\.venv\Scripts\python.exe"
    & $PY explorer.py --cdp-url http://127.0.0.1:9222 --no-login-wait --max-pages 20

Robot không tự đăng nhập Google và không export cookie ra output.

Profile `$HOME\accesstrade-robot-chrome` chỉ nằm trên máy Owner. Không commit/upload/chia sẻ thư mục đó.

### Cách cũ — Playwright tự mở Chromium

Chỉ dùng khi login bình thường không bị provider chặn:

    python explorer.py

Robot sẽ mở Chromium.

1. Owner đăng nhập ACCESSTRADE bình thường.
2. Owner tự xử lý OTP/CAPTCHA nếu có.
3. Vào Publisher dashboard.
4. Quay lại terminal và nhấn ENTER.
5. Robot bắt đầu khám phá các link nội bộ cùng host.

Mặc định tối đa 180 trang:

    python explorer.py --max-pages 180

Muốn test nhanh:

    python explorer.py --max-pages 20

## Giữ login giữa các lần chạy — tùy chọn

Mặc định phiên login không được lưu lại sau khi process kết thúc.

Nếu Owner chủ động muốn dùng persistent profile:

    python explorer.py --profile-dir .browser-profile

Cảnh báo: thư mục .browser-profile có thể chứa cookie phiên đăng nhập. Nó đã được git-ignore và tuyệt đối không được commit/upload/chia sẻ.

## Output

Mỗi lần chạy tạo:

    runtime/accesstrade_scan_YYYYMMDD_HHMMSS/
      pages.jsonl
      site_map.json
      network_endpoints.json
      summary.md

pages.jsonl:
- URL đã sanitize;
- title;
- HTTP status;
- heading;
- menu label;
- button label;
- form schema không có value;
- internal links;
- body text excerpt đã redact;
- sensitive flag.

site_map.json:
Bản đồ trang/link để Brain phân tích cấu trúc website.

network_endpoints.json chỉ lưu:
- HTTP method;
- origin + path;
- status;
- resource type.

Không lưu:
- headers;
- cookies;
- Authorization;
- request body;
- response body;
- query token.

summary.md:
Tóm tắt nhanh scan.

## Safety mặc định

Robot chỉ điều hướng bằng URL được lấy từ anchor href.

Robot không click button vì button có thể gây side effect.

Các URL chứa logout, delete, remove-account, close-account, deactivate bị chặn.

Các khu vực payment/tax/KYC/profile/account được map route nhưng không lưu body text mặc định.

## Test

    python -m unittest test_explorer.py

## Definition of Done V1

PASS khi:

1. Owner có thể login thủ công.
2. Robot map được dashboard và các route nội bộ same-origin.
3. Có site_map.json.
4. Có danh sách network endpoint không chứa token/header/body.
5. Không submit form và không tạo side effect.
6. Không ghi credential/cookie vào output.
7. Brain có đủ evidence để chọn adapter tiếp theo.

## V2 sau khi scan

Không viết V2 trước khi xem output V1.

Ứng viên V2:
1. campaign_reader
2. shopee_smartlink_reader
3. deeplink_builder
4. click_report_reader
5. conversion_commission_reader

Các adapter write/action phải có Owner authorization riêng.
