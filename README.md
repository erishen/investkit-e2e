# InvestKit E2E Tests

End-to-end testing for InvestKit projects using Playwright (Python).

## Project Structure

```
investkit-e2e/
├── tests/
│   ├── conftest.py                      # Test configuration & fixtures
│   ├── test_asset_lens.py               # Asset Lens core tests
│   ├── test_asset_lens_extended.py      # Asset Lens extended tests
│   ├── test_ts_demo.py                  # TS-Demo tests
│   ├── test_stock_analyzer.py           # Stock Analyzer tests
│   ├── test_stock_analyzer_extended.py  # Stock Analyzer extended tests
│   ├── test_lobster.py                  # Lobster tests
│   ├── test_solo_chat.py                # Solo Chat tests
│   └── test_investkit_utils.py          # InvestKit Utils tests
├── .env.example                         # Environment config example
├── pyproject.toml                       # Project configuration
├── Makefile                             # Build scripts
└── README.md
```

## Installation

```bash
# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install
```

## Configuration

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `ASSET_LENS_URL` | Asset Lens service URL | http://localhost:8000 |
| `TS_DEMO_URL` | TS-Demo service URL | http://localhost:3000 |
| `SOLO_CHAT_URL` | Solo Chat service URL | http://localhost:5173 |
| `STOCK_ANALYZER_URL` | Stock Analyzer URL | http://localhost:8001 |
| `LOBSTER_URL` | Lobster service URL | http://localhost:8002 |
| `HEADLESS` | Headless mode | true |

## Running Tests

```bash
# All tests
make test

# Or using pytest directly
pytest -v
```

### By Project

```bash
make test-asset-lens
make test-ts-demo
make test-solo-chat
make test-stock-analyzer
```

### By Marker

```bash
# UI tests
pytest -v -m ui

# API tests
pytest -v -m api

# Performance tests
pytest -v -m slow
```

### Debug Mode

```bash
# Show browser window
pytest -v --headed

# Slow motion (500ms step delay)
make test-debug

# Parallel execution
make test-parallel
```

### Reports

```bash
make report
# or
pytest --html=report.html --self-contained-html
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `asset_lens` | Asset Lens project |
| `ts_demo` | TS-Demo project |
| `solo_chat` | Solo Chat project |
| `stock_analyzer` | Stock Analyzer project |
| `lobster` | Lobster project |
| `investkit_utils` | InvestKit Utils tests |
| `ui` | UI tests |
| `api` | API tests |
| `slow` | Performance tests |

## Helper Utilities

### PageHelper

```python
def test_example(page: Page, page_helper: PageHelper):
    page_helper.goto_fast("http://localhost:8000")
    page_helper.goto_and_wait("http://localhost:8000")
    page_helper.wait_for_text("Welcome")
    page_helper.wait_for_selector(".dashboard")
    page_helper.click_and_wait("button")
    page_helper.fill_and_submit("#input", "value", "#submit")
    page_helper.take_screenshot("test")
    if page_helper.is_visible(".modal"):
        page_helper.click_and_wait(".close")
    text = page_helper.get_text(".title")
    value = page_helper.get_value("#input")
```

### APITester

```python
def test_api(page: Page, api_tester: APITester):
    result = api_tester.get("/api/health", expected_status=[200])
    assert result["status"] == 200
    result = api_tester.post("/api/chat", data={"message": "hello"}, expected_status=[200, 201])
    result = api_tester.delete("/api/item/1")
```

## CI/CD

GitHub Actions workflow:

- **Trigger**: push to main, PR, daily schedule
- **Environment**: Ubuntu Latest + Python 3.11
- **Steps**: lint → format check → E2E tests
- **Artifacts**: screenshots and logs on failure

## Test Results

Results are saved in `test-results/`:

```
test-results/
├── screenshots/     # Failure screenshots
├── videos/          # Recordings (if enabled)
├── traces/          # Traces (if enabled)
└── har/             # HAR files (if enabled)
```

## Best Practices

1. **Use markers** — tag tests for selective running
2. **Independent tests** — each test should not depend on others
3. **Wait strategies** — use `wait_for_*` methods instead of fixed sleeps
4. **Screenshot debugging** — auto-capture on failure
5. **Environment variables** — sensitive config via env vars

## FAQ

### Q: Tests timeout?

Increase timeout in `.env`:

```env
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=60000
```

### Q: How to skip a service test?

```python
def test_example(asset_lens_url: str):
    if not check_server_health(asset_lens_url):
        pytest.skip("Service unavailable")
```

### Q: How to debug a failing test?

```bash
pytest -v --headed --slowmo=500 -k "test_name"
```

## License

MIT
