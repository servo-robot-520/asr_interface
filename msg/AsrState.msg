# 语音识别状态快照。以 transient_local QoS 发布，新订阅者可立即拿到最新状态。

# 时间戳与 frame_id。
std_msgs/Header header

# 当前识别后端名称，例如 mock、sherpa_onnx、vosk。
string backend

# 模型是否已成功加载。
bool model_loaded

# 识别模式，例如 wake_command、keyword_command、push_to_talk、free_asr、off。
string mode

# 识别是否启用；false 时节点仍运行，但不处理音频。
bool enabled

# 是否因播放而门控静音。
bool gated

# 当前是否有唤醒会话。
bool session_active

# 检测到的 AudioStream 序号缺口次数。
uint64 audio_gap_count

# 最近一次错误；无错误时为空。
string last_error
