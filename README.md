# InvestKit E2E Tests

使用 Playwright Python 进行端到端测试。

## 安装

```bash
# 安装依赖
pip install -e .

# 安装 Playwright 浏览器
playwright install
```

## 配置

创建 `.env` 文件：

```env
# 服务 URL
ASSET_LENS_URL=http://localhost:8000
SOLO_CHAT_URL=http://localhost:5173
STOCK_ANALYZER_URL=http://localhost:8001

# 浏览器配置
HEADLESS=true
RECORD_VIDEO=false
RECORD_HAR=false
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定项目测试
pytest -m asset_lens
pytest -m solo_chat
pytest -m stock_analyzer

# 运行 UI 测试
pytest -m ui

# 运行 API 测试
pytest -m api

# 运行性能测试
pytest -m slow

# 显示浏览器窗口
pytest --headed

# 并行运行
pytest -n auto

# 生成 HTML 报告
pytest --html=report.html
```

## 测试结构

```
e2e-tests/
├── pyproject.toml          # 项目配置
├── tests/
│   ├── conftest.py         # 测试配置和 fixtures
│   ├── test_asset_lens.py  # Asset Lens 测试
│   ├── test_solo_chat.py   # Solo Chat 测试
│   └── test_stock_analyzer.py # Stock Analyzer 测试
└── test-results/           # 测试结果
    ├── screenshots/        # 失败截图
    ├── videos/             # 录像
    └── traces/             # 追踪
```

## 测试标记

| 标记 | 说明 |
|------|------|
| `asset_lens` | Asset Lens 项目测试 |
| `solo_chat` | Solo Chat 项目测试 |
| `stock_analyzer` | Stock Analyzer 项目测试 |
| `ui` | UI 测试 |
| `api` | API 测试 |
| `slow` | 性能测试 |

## 辅助工具

### PageHelper

```python
def test_example(page: Page, page_helper: PageHelper):
    page_helper.goto_and_wait("http://localhost:8000")
    page_helper.wait_for_text("欢迎")
    page_helper.click_and_wait("button")
    page_helper.take_screenshot("test")
```

### APITester

```python
def test_api(page: Page, api_tester: APITester):
    result = api_tester.get("/api/health", expected_status=[200])
    assert result["status"] == 200
```

## CI/CD

```yaml
# GitHub Actions 示例
- name: Run E2E Tests
  run: |
    pip install -e .
    playwright install
    pytest --headed=false
```
