# asr_interface

## 简介

`asr_interface` 定义通用语音识别节点（`/asr`）的 ROS 2 事件、状态与端点名称：

- `AsrEvent`：唤醒、语音起点、中间结果、句尾、最终结果、失败与取消；
- `AsrState`：后端、模型加载、模式、门控、会话与采集缺口状态。

本包只包含 **ASR 的通用识别接口**，不包含鸭子口令、电量查询、TTS 或播放语义；这些属于
`duck_asr_interface` 或其他业务包。

生成命名空间为 `asr_interface`，Python 模块为 `asr_interface_msg`。

## 端点约定

- `~/...` 是 endpoint owner（`asr` 节点自身）使用的私有名称；只能由创建 publisher 的节点使用。
- 外部消费者必须传入目标 `asr` 节点的完整节点名（FQN），由 helper 生成绝对名称。
- 默认节点 FQN 为 `/asr`。

| 类型 | owner 私有名称 | 外部消费者 helper |
| --- | --- | --- |
| 事件话题 | `~/event` | `topic_event(node_fqn)` |
| 状态话题 | `~/state` | `topic_state(node_fqn)` |

`node_fqn` 必须是非根绝对 ROS 名称，不能包含 ASCII 空白或中间的空路径段；尾部多余 `/` 会自动移除。

例如目标节点是 `/robot_a/asr` 时：

```text
/robot_a/asr/event
/robot_a/asr/state
```

## 消息

### `AsrEvent`

```msg
std_msgs/Header header
string session_id
uint8 event
string text
float32 confidence
string language
string backend
string error
```

事件常量的取值和含义以 `msg/AsrEvent.msg` 内的注释为准：

| 常量 | 值 | 语义 |
| --- | --- | --- |
| `EVENT_WAKE` | 0 | 唤醒词命中，`text` 为关键词 |
| `EVENT_SPEECH_START` | 1 | 会话内检测到语音起点 |
| `EVENT_PARTIAL` | 2 | 中间识别结果 |
| `EVENT_ENDPOINT` | 3 | 检测到句尾 |
| `EVENT_FINAL` | 4 | 最终识别结果 |
| `EVENT_FAILED` | 5 | 识别失败，`error` 说明原因 |
| `EVENT_CANCELED` | 6 | 会话被门控或超时取消 |

事件语义是边沿，不是电平：一次唤醒只发一个 `EVENT_WAKE`，一句话只发一个 `EVENT_FINAL`。

### `AsrState`

```msg
std_msgs/Header header
string backend
bool model_loaded
string mode
bool enabled
bool gated
bool session_active
uint64 audio_gap_count
string last_error
```

通过 `transient_local` QoS 发布，新订阅者可以立即拿到最新状态。

## C++ 使用

```cpp
#include "asr_interface/ros_msg.hpp"

// asr 节点自己创建 endpoint 时使用私有名称。
const auto private_event = asr_interface::kPrivateTopicEvent;

// 外部节点必须给出目标 asr 的节点全名。
constexpr std::string_view asr_fqn = "/robot_a/asr";
const auto event_topic = asr_interface::topic_event(asr_fqn);
const auto state_topic = asr_interface::topic_state(asr_fqn);

asr_interface::MsgAsrEvent msg;
```

## Python 使用

```python
from asr_interface_msg.ros_msg import (
    PRIVATE_TOPIC_EVENT,
    topic_event,
    topic_state,
)

asr_fqn = "/robot_a/asr"
print(PRIVATE_TOPIC_EVENT)       # ~/event
print(topic_event(asr_fqn))      # /robot_a/asr/event
print(topic_state(asr_fqn))      # /robot_a/asr/state
```

## 构建与测试

```bash
source /opt/ros/humble/setup.bash

colcon build --base-paths src --packages-select asr_interface
colcon test --base-paths src --packages-select asr_interface
colcon test-result --test-result-base build/asr_interface/test_results --verbose
```

接口依赖：

- `builtin_interfaces`
- `std_msgs`
- `rosidl_default_generators` / `rosidl_default_runtime`

设计文档：[`docs/duck-ros2-asr-architecture.zh-CN.md`](../../docs/duck-ros2-asr-architecture.zh-CN.md)。
