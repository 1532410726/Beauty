import datetime
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


class TestcontentActivity:

    @pytest.mark.parametrize(
        "body", [
            {
                # 默认查询
                "pageNo": 1,
                "pageSize": 50
            },
            {
                # 查询报名中活动
                "pageNo": 1,
                "pageSize": 10,
                "activityStatus": "1"
            },
            {
                # 查询报名已结束活动
                "pageNo": 1,
                "pageSize": 10,
                "activityStatus": "2"
            },
            {
                # 查询已发布活动
                "pageNo": 1,
                "pageSize": 10,
                "activityStatus": "4"
            }
        ]
    )
    def test_search_list(self, token, body):
        """
        查询活动列表list数据
        :param token:
        :return:
        """
        url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/list"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        r = requests.post(url, headers=headers, json=body)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info("活动报名查询成功")

    def test_activity_add(self, token):
        url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/add"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        current_date = datetime.date.today()
        strtime = current_date + datetime.timedelta(days=3)
        endtime = current_date + datetime.timedelta(days=1)

        body = {
            "activityPublishTimeStr": f"{strtime}",
            "activityRegisterEndTimeStr": f"{endtime}",
            "hotActivityName": "测试",
            "incentiveScheme": "1756"
        }
        r = requests.post(url, headers=headers, json=body)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info("添加活动成功1")
