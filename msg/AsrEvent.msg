# 语音识别事件。由 asr 节点或组合式 AsrNode 发布。
# 同一唤醒会话的所有事件共享 session_id；事件是边沿，不是电平。

# 唤醒词命中，text 为命中的关键词。
uint8 EVENT_WAKE=0
# 会话内检测到语音起点。
uint8 EVENT_SPEECH_START=1
# 会话内的中间识别结果。
uint8 EVENT_PARTIAL=2
# 检测到句尾，后端即将给出最终结果。
uint8 EVENT_ENDPOINT=3
# 最终识别结果；一句话只发一次。
uint8 EVENT_FINAL=4
# 识别失败。
uint8 EVENT_FAILED=5
# 会话被取消，例如播放门控或超时。
uint8 EVENT_CANCELED=6

# 时间戳与 frame_id。
std_msgs/Header header

# 一次唤醒会话的标识；同一会话的 partial/final 共享该值。
string session_id

# 事件类型，取 EVENT_* 常量。
uint8 event

# EVENT_WAKE 为关键词；EVENT_PARTIAL/EVENT_FINAL 为转写文本；其他事件为空。
string text

# 本次结果的置信度；后端不支持时为 0。
float32 confidence

# 识别语言，例如 zh-CN；为空表示后端默认。
string language

# 实际使用的识别后端名称。
string backend

# 失败原因；仅 EVENT_FAILED 时非空。
string error
