from pathlib import Path

import pytest

from pytest_result_sender import plugin

pytest_plugins = "pytester"  # 我是测试开发


# 创建一个干净的测试环境——即只需要测试需要测试的，其他不要
@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {"passed": 0, "failed": 0}
    yield  # 去测试，结束后再改回来
    plugin.data = bak_data


# 证明配置文件没问题
@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when= {send_when}
send_api=https://baidu.com
"""
    )

    # 断言：配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when

    # 构造一个场景，用例全部测试通过
    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )
    # 使用当前测试项测试以上用例
    pytester.runpytest("-c", str(config_path))

    print(plugin.data)
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert (
            plugin.data.get("send_done") is None
        )  # 如果是on_fail，此测试为通过，无需发送,则data['send_done']就不存在为None


@pytest.mark.parametrize("send_api", ["https://baidu.com", ""])
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when= every
send_api={send_api}
"""
    )

    # 断言：配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_api") == send_api

    # 构造一个场景，用例全部测试通过
    pytester.makepyfile(
        """
    def test_pass():
        ...
    """
    )
    # 使用当前测试项测试以上用例
    pytester.runpytest("-c", str(config_path))

    print(plugin.data)
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert (
            plugin.data.get("send_done") is None
        )  # 如果是on_fail，此测试为通过，无需发送,则data['send_done']就不存在为None
