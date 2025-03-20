"""
@Filename:pytest-result-sender
@Author:  Freya
@Time:    2025/3/10 15:14
@Describe:...
"""

from datetime import datetime

# 导入pytest，收集用例
import pytest
import requests

data = {"passed": 0, "failed": 0}


def pytest_addoption(parser):
    parser.addini(
        "send_when",
        help="When do you like to send your content?\n every or on_fail.",
    )
    parser.addini(
        "send_api",
        help="Where will you send your content?\n Please input your link.",
    )


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含了全部用例
    data["total"] = len(session.items)
    print("==================:", data["total"])


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


# 到这里，配置已经加载完成，包括pytest.ini
def pytest_configure(config: pytest.Config):
    """
    配置加载完毕之后
    测试用例执行之前
    """
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")


def pytest_unconfigure():
    """
    测试用例执行之后
    """
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} pytest结束执行")
    data["duration"] = data["end_time"] - data["start_time"]
    data["passed_ratio"] = f"{data['passed'] / data['total'] * 100:.2f}%"

    """assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    assert data["total"] == 3
    assert data['passed']==2
    assert data['failed']==1
    assert data['passed_ratio']==f"{2/3*100:.2f}%"""

    send_result()


def send_result():
    if not data["send_when"]:
        return
    if data["send_when"] == "on_fail" and data["failed"] == 0:
        return
    if not data["send_api"]:
        return

    url = data["send_api"]
    content = f"""
        python自动化测试结果


        测试时间：{data['start_time']}
        用例数量：{data['total']}
        执行时长：{data['duration']}
        测试通过：<font color="green">{data['passed']}</font>
        测试失败：<font color="red">{data['failed']}</font>
        测试通过率：{data['passed_ratio']}


        测试报告地址：http://baidu.com
        """

    try:
        requests.post(
            url,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": content,
                },
            },
        )
    except Exception:
        pass

    data["send_done"] = 1  # 发送成功
