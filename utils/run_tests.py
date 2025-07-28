import os
import time
import pytest

# 生成当前时间戳目录
timestamp = time.strftime("%Y%m%d_%H%M%S")
result_dir = os.path.join("allure-results", timestamp)

# 创建目录
os.makedirs(result_dir, exist_ok=True)

# 运行 pytest，并指定输出目录
pytest.main([f'TestCase/BossTestCase.py', f'--alluredir={result_dir}'])
