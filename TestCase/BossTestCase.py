from datetime import date, datetime, timedelta
import json
import pytest
import requests
from utils.log_utils import logger


@pytest.fixture(scope="module")
def token():
    """获取token的fixture，整个模块只执行一次"""
    proxies = {
        'http': 'http://127.0.0.1:8888',  # 抓包工具的HTTP代理地址
        'https': 'http://127.0.0.1:8888',  # 抓包工具的HTTPS代理地址（通常与HTTP相同）
    }
    sms_url = "https://apitest.dingdingclub.com/auth/auth/send-sms-login-code?phone=15367494408"
    requests.get(sms_url)
    url = "https://apitest.dingdingclub.com/auth/auth/sms-login?phone=15367494408&code=123456"
    r = requests.get(url)
    response_data = r.json()
    token = response_data["data"]["token"]
    # print(token)
    return token


class TestBoss:
    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_zonglan(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getHrJobHenEfficiencySummary"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}招聘总览查询成功")

    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_renxiao(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getHrJobHenEfficiencyHrUser"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}招聘人效查询成功")

    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_bumen(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getDeptRecruitmentProgress"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}部门招聘进度查询成功")

    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_qudao(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getChannelAnalysis"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}渠道分析查询成功")

    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_mianshiguan(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getInterviewerAnalysis"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}面试官分析查询成功")

    @pytest.mark.parametrize("month", ["2025-05", "2025-06", "2025-07"])
    def test_search_renyuanbianhua(self, token, month):
        url = "https://apitest.dingdingclub.com/boss/boss/empEfficiency/hr/getUserChange"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        params = {
            'month': month
        }
        r = requests.get(url, headers=headers, params=params)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info(f"{month}人员变化查询成功")
