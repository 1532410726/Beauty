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


class TestContentActivity:

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
        current_date = date.today()
        strtime = current_date + timedelta(days=3)
        endtime = current_date + timedelta(days=1)
        nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        body = {
            "activityPublishTimeStr": f"{strtime}",
            "activityRegisterEndTimeStr": f"{endtime}",
            "hotActivityName": f"测试，{nowtime}",
            "incentiveScheme": "1756"
        }
        r = requests.post(url, headers=headers, json=body)
        account_data = r.json()
        assert r.status_code == 200
        assert account_data["message"] == "OK!"
        logger.info("添加活动成功1")

    @pytest.mark.skip(reason="暂不执行")
    def test_activity_update(self, token):
        # 查询url
        search_url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/list"
        # 更新url
        update_url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/update"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        body = {
            "pageNo": "1",
            "pageSize": "50"
        }
        r = requests.post(search_url, headers=headers, json=body)
        account_data = r.json()

        activity_id = account_data["data"]["content"][0]["activityId"]
        nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_body = {
            "createBy": "1747799318597311243",
            "updateBy": "1747799318597311243",
            "createByName": "王斌斌",
            "updateByName": "王斌斌",
            "createTime": f"{nowtime}",
            "updateTime": f"{nowtime}",
            "deleted": 0,
            "activityId": f"{activity_id}",
            "hotActivityName": "活动测试",
            "activityRegisterEndTime": "2025-06-20 00:00:00",
            "activityPublishTime": "2025-06-21 00:00:00",
            "activityRegisterEndTimeStr": "2025-06-21 00:00",
            "activityPublishTimeStr": "2025-06-22 00:00",
            "activityDesc": "",
            "remark": "",
            "flyGroupId": "",
            "incentiveScheme": "11"
        }
        update_r = requests.post(update_url, headers=headers, json=update_body)
        update_data = update_r.json()
        logger.info(update_data)
        assert update_r.status_code == 200
        assert update_data["message"] == "OK!"

    pass

    @pytest.mark.skip(reason="不执行删除")
    def test_activity_del(self, token):
        """
        删除列表第一条数据
        :param token:
        :return:
        """
        # 查询url
        search_url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/list"
        # 删除url
        delete_url = "https://apitest.dingdingclub.com/makeup-film/contentActivity/delete"
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
        body = {
            "pageNo": "1",
            "pageSize": "50"
        }
        # 调用查询接口
        r = requests.post(search_url, headers=headers, json=body)
        account_data = r.json()
        # 获取列表第二条数据的活动ID，用于后面调用删除接口时传入的ID
        activity_id = account_data["data"]["content"][0]["activityId"]
        logger.info(account_data["data"]["content"][0]["activityId"])

        delete_body = [activity_id]
        # 调用删除接口
        delete_r = requests.post(delete_url, headers=headers, json=delete_body)
        delete_data = delete_r.json()
        logger.info(delete_data)
        # 断言，状态码判断200，message判断OK！
        assert delete_r.status_code == 200
        assert delete_data["message"] == "OK!"
        logger.info(f"删除成功，ID：{activity_id}")

