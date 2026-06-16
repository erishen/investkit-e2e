# InvestKit E2E Tests

使用 Playwright Python 进行端到端测试。

## 项目结构

```
investkit-e2e/
├── tests/
│   ├── conftest.py              # 测试配置和 fixtures
│   ├── test_asset_lens.py       # Asset Lens 核心测试
│   ├── test_asset_lens_extended.py  # Asset Lens 扩展测试
│   ├── test_ts_demo.py          # TS-Demo 测试
│   ├── test_stock_analyzer.py   # Stock Analyzer 测试
│   ├── test_stock_analyzer_extended.py  # Stock Analyzer 扩展测试
│   ├── test_lobster.py          # Lobster 测试
│   ├── test_solo_chat.py        # Solo Chat 测试
│   └── test_investkit_utils.py  # InvestKit Utils 测试
├── .env.example                 # 环境配置示例
├── pyproject.toml               # 项目配置
├── Makefile                     # 构建脚本
└── README.md                    # 本文件
```

## 安装

```bash
# 安装依赖
pip install -e .

# 安装 Playwright 浏览器
playwright install
```

## 配置

复制 `.env.example` 为 `.env` 并根据实际情况修改：

```bash
cp .env.example .env
```

主要配置项：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ASSET_LENS_URL` | Asset Lens 服务地址 | http://localhost:8000 |
| `TS_DEMO_URL` | TS-Demo 服务地址 | http://localhost:3000 |
| `SOLO_CHAT_URL` | Solo Chat 服务地址 | http://localhost:5173 |
| `STOCK_ANALYZER_URL` | Stock Analyzer 服务地址 | http://localhost:8001 |
| `LOBSTER_URL` | Lobster 服务地址 | http://localhost:8002 |
| `HEADLESS` | 无头模式 | true |

## 运行测试

### 基本命令

```bash
# 运行所有测试
make test

# 或使用 pytest
pytest -v
```

### 按项目运行

```bash
# Asset Lens 测试
make test-asset-lens

# TS-Demo 测试
make test-ts-demo

# Solo Chat 测试
make test-solo-chat

# Stock Analyzer 测试
make test-stock-analyzer
```

### 按类型运行

```bash
# UI 测试
pytest -v -m ui

# API 测试
pytest -v -m api

# 性能测试
pytest -v -m slow
```

### 调试模式

```bash
# 显示浏览器窗口
pytest -v --headed

# 慢速模式（每步延迟 500ms）
make test-debug

# 并行运行
make test-parallel
```

### 生成报告

```bash
# HTML 报告
make report

# 或
pytest --html=report.html --self-contained-html
```

## 测试标记

| 标记 | 说明 |
|------|------|
| `asset_lens` | Asset Lens 项目测试 |
| `ts_demo` | TS-Demo 项目测试 |
| `solo_chat` | Solo Chat 项目测试 |
| `stock_analyzer` | Stock Analyzer 项目测试 |
| `lobster` | Lobster 项目测试 |
| `investkit_utils` | InvestKit Utils 测试 |
| `ui` | UI 测试 |
| `api` | API 测试 |
| `slow` | 性能测试 |

## 辅助工具

### PageHelper

页面操作辅助类：

```python
def test_example(page: Page, page_helper: PageHelper):
    # 快速导航
    page_helper.goto_fast("http://localhost:8000")
    
    # 导航并等待
    page_helper.goto_and_wait("http://localhost:8000")
    
    # 等待文本
    page_helper.wait_for_text("欢迎")
    
    # 等待选择器
    page_helper.wait_for_selector(".dashboard")
    
    # 点击并等待
    page_helper.click_and_wait("button")
    
    # 填充表单
    page_helper.fill_and_submit("#input", "value", "#submit")
    
    # 截图
    page_helper.take_screenshot("test")
    
    # 检查可见性
    if page_helper.is_visible(".modal"):
        page_helper.click_and_wait(".close")
    
    # 获取文本
    text = page_helper.get_text(".title")
    
    # 获取输入值
    value = page_helper.get_value("#input")
```

### APITester

API 测试辅助类：

```python
def test_api(page: Page, api_tester: APITester):
    # GET 请求
    result = api_tester.get("/api/health", expected_status=[200])
    assert result["status"] == 200
    
    # POST 请求
    result = api_tester.post(
        "/api/chat",
        data={"message": "hello"},
        expected_status=[200, 201]
    )
    
    # DELETE 请求
    result = api_tester.delete("/api/item/1")
```

## CI/CD

项目使用 GitHub Actions 进行持续集成：

- **触发条件**：push 到 main 分支、PR、每日定时
- **运行环境**：Ubuntu Latest + Python 3.11
- **测试步骤**：lint → format check → E2E tests
- **结果上传**：测试失败时上传截图和日志

## 测试结果

测试结果保存在 `test-results/` 目录：

```
test-results/
├── screenshots/     # 失败截图
├── videos/          # 录像（启用时）
├── traces/          # 追踪（启用时）
└── har/             # HAR 文件（启用时）
```

## 最佳实践

1. **使用标记**：为测试添加适当的标记，便于筛选运行
2. **独立测试**：每个测试应该独立，不依赖其他测试的状态
3. **等待策略**：使用 `wait_for_*` 方法而非固定等待
4. **截图调试**：失败时自动截图，便于调试
5. **环境变量**：敏感配置使用环境变量

## 常见问题

### Q: 测试超时怎么办？

A: 增加超时时间或在 `.env` 中设置：

```env
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=60000
```

### Q: 如何跳过某个服务测试？

A: 使用 `pytest.skip()` 或在测试中检查服务可用性：

```python
def test_example(asset_lens_url: str):
    if not check_server_health(asset_lens_url):
        pytest.skip("服务不可用")
```

### Q: 如何调试失败的测试？

A: 使用调试模式：

```bash
pytest -v --headed --slowmo=500 -k "test_name"
```
