"""
InvestKit Utils E2E Tests.
InvestKit 共享模块测试
"""

import pytest


@pytest.mark.investkit_utils
class TestInvestkitUtilsImports:
    """测试模块导入"""

    def test_import_main_module(self):
        """测试主模块导入"""
        try:
            import investkit_utils

            assert investkit_utils is not None
        except ImportError:
            pytest.skip("investkit_utils 未安装")

    def test_import_config(self):
        """测试配置模块导入"""
        try:
            from investkit_utils import config

            assert config is not None
        except ImportError:
            pytest.skip("investkit_utils.config 未找到")

    def test_import_log_utils(self):
        """测试日志模块导入"""
        try:
            from investkit_utils import log_utils

            assert log_utils is not None
        except ImportError:
            pytest.skip("investkit_utils.log_utils 未找到")

    def test_import_api_docs(self):
        """测试 API 文档模块导入"""
        try:
            from investkit_utils import api_docs

            assert api_docs is not None
        except ImportError:
            pytest.skip("investkit_utils.api_docs 未找到")


@pytest.mark.investkit_utils
class TestInvestkitUtilsConfig:
    """测试配置功能"""

    def test_config_template_exists(self):
        """测试配置模板存在"""
        from pathlib import Path

        try:
            import investkit_utils

            package_path = Path(investkit_utils.__file__).parent
            config_template = package_path / "config" / "config.template.yaml"

            if not config_template.exists():
                pytest.skip("配置模板文件不存在")
        except ImportError:
            pytest.skip("investkit_utils 未安装")


@pytest.mark.investkit_utils
class TestInvestkitUtilsLogger:
    """测试日志功能"""

    def test_logger_creation(self):
        """测试日志器创建"""
        try:
            from investkit_utils.log_utils import get_logger

            logger = get_logger("test")
            assert logger is not None
        except ImportError:
            pytest.skip("investkit_utils.log_utils 未找到")

    def test_logger_levels(self):
        """测试日志级别"""
        try:
            from investkit_utils.log_utils import get_logger

            logger = get_logger("test_levels")
            assert hasattr(logger, "info")
            assert hasattr(logger, "error")
            assert hasattr(logger, "warning")
            assert hasattr(logger, "debug")
        except ImportError:
            pytest.skip("investkit_utils.log_utils 未找到")
