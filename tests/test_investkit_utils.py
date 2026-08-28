"""
InvestKit Utils E2E Tests.
InvestKit 共享模块测试
"""

import importlib
from pathlib import Path

import pytest


@pytest.mark.investkit_utils
class TestInvestkitUtilsImports:
    """测试模块导入"""

    def test_import_main_module(self):
        """测试主模块导入 - 验证版本号和核心导出"""
        import investkit_utils

        assert hasattr(investkit_utils, "__version__"), "investkit_utils 缺少 __version__ 属性"
        assert isinstance(investkit_utils.__version__, str), "__version__ 应为字符串"
        assert investkit_utils.__version__ != "", "__version__ 不应为空字符串"
        assert hasattr(investkit_utils, "__all__"), "investkit_utils 缺少 __all__ 属性"
        expected_exports = {"Config", "get_logger", "get_config"}
        actual_exports = set(investkit_utils.__all__)
        missing = expected_exports - actual_exports
        assert not missing, f"investkit_utils 缺少核心导出: {missing}"

    def test_import_config(self):
        """测试配置模块导入 - 验证核心配置类存在"""
        from investkit_utils import config

        assert hasattr(config, "__all__"), "config 模块缺少 __all__ 属性"
        expected = {"Config", "get_config", "ConfigLoader"}
        actual = set(config.__all__)
        missing = expected - actual
        assert not missing, f"config 模块缺少核心导出: {missing}"

    def test_import_log_utils(self):
        """测试日志模块导入 - 验证核心日志函数存在"""
        from investkit_utils import log_utils

        assert hasattr(log_utils, "__all__"), "log_utils 模块缺少 __all__ 属性"
        expected = {"get_logger", "setup_logging", "LoggerManager"}
        actual = set(log_utils.__all__)
        missing = expected - actual
        assert not missing, f"log_utils 模块缺少核心导出: {missing}"

    def test_import_api_docs(self):
        """测试 API 文档模块导入 - 验证核心聚合函数存在"""
        from investkit_utils import api_docs

        assert hasattr(api_docs, "__all__"), "api_docs 模块缺少 __all__ 属性"
        expected = {"aggregate_openapi_docs", "ServiceRegistry", "APIService"}
        actual = set(api_docs.__all__)
        missing = expected - actual
        assert not missing, f"api_docs 模块缺少核心导出: {missing}"


@pytest.mark.investkit_utils
class TestInvestkitUtilsConfig:
    """测试配置功能"""

    def test_config_template_exists(self):
        """测试配置模板存在 - 验证文件内容和结构"""
        import investkit_utils

        package_path = Path(investkit_utils.__file__).parent
        config_template = package_path / "config" / "config.template.yaml"

        assert config_template.exists(), f"配置模板文件不存在: {config_template}"
        content = config_template.read_text(encoding="utf-8")
        assert len(content) > 0, "配置模板文件为空"
        assert "app:" in content or "database:" in content, "配置模板应包含 app 或 database 配置节"


@pytest.mark.investkit_utils
class TestInvestkitUtilsLogger:
    """测试日志功能"""

    def test_logger_creation(self):
        """测试日志器创建 - 验证返回对象类型和方法"""
        from investkit_utils.log_utils import get_logger

        logger = get_logger("test")
        assert isinstance(logger.__class__.__name__, str), "get_logger 应返回 logger 对象"
        assert hasattr(logger, "info"), "logger 缺少 info 方法"
        assert hasattr(logger, "error"), "logger 缺少 error 方法"
        assert callable(logger.info), "logger.info 应为可调用方法"
        assert callable(logger.error), "logger.error 应为可调用方法"

    def test_logger_levels(self):
        """测试日志级别 - 验证所有标准日志方法可用"""
        from investkit_utils.log_utils import get_logger

        logger = get_logger("test_levels")
        required_methods = {"info", "error", "warning", "debug"}
        for method_name in required_methods:
            assert hasattr(logger, method_name), f"logger 缺少 {method_name} 方法"
            assert callable(getattr(logger, method_name)), f"logger.{method_name} 应为可调用方法"
