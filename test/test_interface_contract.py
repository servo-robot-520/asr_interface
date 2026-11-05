"""验证 asr_interface 的接口字段与端点命名契约。"""

import importlib.util
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def lines(relative: str) -> list[str]:
    """返回接口文件中去掉空行、注释与分隔符后的内容行。"""
    return [
        line.strip()
        for line in (PACKAGE_ROOT / relative).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#") and line.strip() != "---"
    ]


def fields(relative: str) -> list[str]:
    """返回接口文件中的字段行，排除常量定义。"""
    return [line for line in lines(relative) if "=" not in line]


def load_ros_msg():
    """直接加载 Python 辅助模块，避免依赖安装后的生成包。"""
    module_path = PACKAGE_ROOT / "python/asr_interface_msg/ros_msg.py"
    spec = importlib.util.spec_from_file_location("asr_interface_ros_msg", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_asr_event_contract() -> None:
    """AsrEvent 必须覆盖唤醒、会话、转写、失败与取消。"""
    assert fields("msg/AsrEvent.msg") == [
        "std_msgs/Header header",
        "string session_id",
        "uint8 event",
        "string text",
        "float32 confidence",
        "string language",
        "string backend",
        "string error",
    ]
    content = "\n".join(lines("msg/AsrEvent.msg"))
    assert "uint8 EVENT_WAKE=0" in content
    assert "uint8 EVENT_FINAL=4" in content
    assert "uint8 EVENT_CANCELED=6" in content


def test_asr_state_contract() -> None:
    """AsrState 必须暴露后端、门控与采集缺口。"""
    assert fields("msg/AsrState.msg") == [
        "std_msgs/Header header",
        "string backend",
        "bool model_loaded",
        "string mode",
        "bool enabled",
        "bool gated",
        "bool session_active",
        "uint64 audio_gap_count",
        "string last_error",
    ]


def test_python_endpoint_helpers() -> None:
    """Python helper 必须区分私有名称与目标节点 FQN。"""
    ros_msg = load_ros_msg()

    assert ros_msg.DEFAULT_NODE_FQN == "/asr"
    assert ros_msg.PRIVATE_TOPIC_EVENT == "~/event"
    assert ros_msg.PRIVATE_TOPIC_STATE == "~/state"

    assert ros_msg.topic_event() == "/asr/event"
    assert ros_msg.topic_state() == "/asr/state"
    assert ros_msg.topic_event("/robot_a/asr") == "/robot_a/asr/event"
    assert ros_msg.topic_event("/robot_a/asr///") == "/robot_a/asr/event"


def test_python_endpoint_helpers_reject_invalid_node_fqn() -> None:
    """Python helper 必须拒绝空、相对、根路径与含空白的节点名。"""
    ros_msg = load_ros_msg()
    for invalid in ("", "asr", "/", "/asr//node", "/asr\t"):
        with pytest.raises(ValueError, match="node_fqn"):
            ros_msg.topic_event(invalid)


def test_helper_files_expose_consistent_private_names() -> None:
    """C++ 与 Python helper 必须使用同一套私有 endpoint 名称。"""
    helper_files = (
        "include/asr_interface/ros_msg.hpp",
        "python/asr_interface_msg/ros_msg.py",
    )
    required = (
        "~/event",
        "~/state",
        "topic_event",
        "topic_state",
    )
    for relative in helper_files:
        content = (PACKAGE_ROOT / relative).read_text(encoding="utf-8")
        assert all(item in content for item in required), relative
