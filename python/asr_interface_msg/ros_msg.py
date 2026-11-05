"""asr_interface 的 ROS endpoint 名称辅助函数。"""

from __future__ import annotations

DEFAULT_NODE_FQN = "/asr"

# 下列私有名称仅供 endpoint owner（asr 节点自身）创建 endpoint 时使用。
PRIVATE_TOPIC_EVENT = "~/event"
PRIVATE_TOPIC_STATE = "~/state"

_ASCII_WHITESPACE = " \t\n\r\v\f"


def _normalized_node_fqn(node_fqn: str) -> str:
    """校验并返回去掉尾部 '/' 的 asr 节点全名。"""
    trimmed = node_fqn.rstrip("/")
    if (
            not trimmed
            or not trimmed.startswith("/")
            or trimmed == "/"
            or "//" in trimmed
            or any(character in _ASCII_WHITESPACE for character in trimmed)
    ):
        raise ValueError(
            "node_fqn must be an absolute, non-root ROS name without ASCII whitespace"
        )
    return trimmed


def _endpoint_name(node_fqn: str, endpoint_suffix: str) -> str:
    """拼接节点全名与 endpoint 后缀。"""
    return f"{_normalized_node_fqn(node_fqn)}/{endpoint_suffix}"


def topic_event(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回识别事件话题的绝对名称。"""
    return _endpoint_name(node_fqn, "event")


def topic_state(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回识别状态话题的绝对名称。"""
    return _endpoint_name(node_fqn, "state")


__all__ = [
    "DEFAULT_NODE_FQN",
    "PRIVATE_TOPIC_EVENT",
    "PRIVATE_TOPIC_STATE",
    "topic_event",
    "topic_state",
]
