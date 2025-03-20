# Xiaozhi Client

这是一个用于连接小智AI助手的Python客户端库。它提供了简单的接口来进行语音对话和文本交互。

[小智前端-硬件版](https://github.com/78/xiaozhi-esp32)
[小智后端-本地部署版](https://github.com/xinnan-tech/xiaozhi-esp32-server)

## 源码安装

```bash
git clone https://github.com/Eric0308/xiaozhi-client.git
cd xiaozhi-client
conda create -n xiaozhi-client python=3.10 -y
conda activate xiaozhi-client 
pip install -e .
python examples/simple_client.py
```

## pip 安装

```bash
conda create -n xiaozhi-client python=3.10 -y
conda activate xiaozhi-client 
pip install xiaozhi-client
python examples/simple_client.py
```

## 快速开始

这是一个基础的文本对话示例:

```python
import asyncio
import sys
from xiaozhi_client import XiaozhiClient, ClientConfig
from concurrent.futures import ThreadPoolExecutor

async def main():
    client = XiaozhiClient(ClientConfig(ws_url="ws://localhost:8000",))
    
    client.on_tts_end = lambda msg: print("\n请输入消息(输入q退出)：")
    
    # 创建输入循环
    executor = ThreadPoolExecutor(max_workers=1)
    loop = asyncio.get_event_loop()
    
    print("\n请输入消息(输入q退出)：")
    
    try:
        await client.connect()
        while True:
            message = await loop.run_in_executor(executor, sys.stdin.readline)
            message = message.strip()
            
            if message.lower() == 'q':
                break
                
            if message:
                await client.send_txt_message(message)
                # 等待音频播放完成
                while client.is_playing.is_set():
                    await asyncio.sleep(0.1)
    finally:
        await client.close()

asyncio.run(main())
```

完整示例代码请参考 [simple_client.py](examples/simple_client.py)

## 语音对话示例

这是一个基础的语音对话示例:

```python
import asyncio
from xiaozhi_client import XiaozhiClient, ClientConfig, AudioConfig

async def start_voice_chat(
    ws_url: str = "ws://localhost:8000",
    sample_rate: int = 16000,
    channels: int = 1
):
    """启动语音对话"""
    config = ClientConfig(ws_url=ws_url)
    audio_config = AudioConfig(sample_rate=sample_rate, channels=channels)
    client = XiaozhiClient(config, audio_config)
    
    async def on_tts_end(msg):
        print("\n[系统] 继续聆听中... (q:退出)")
        client.resume_voice_input()
        
    client.on_tts_end = on_tts_end
    
    try:
        await client.connect()
        # 启动语音输入
        await client.start_voice_input()
        print("[系统] 开始对话... (q:退出)\n")
        
        # 命令处理循环
        while True:
            cmd = await asyncio.get_event_loop().run_in_executor(None, input, "")
            cmd = cmd.strip().lower()
            
            if cmd == 'q': break

    finally:
        await client.close()
        print("\n[系统] 程序已退出")

asyncio.run(start_voice_chat())
```

完整示例代码请参考 [audio_chat.py](examples/audio_chat.py)

## 特性

- WebSocket连接管理
- 音频编解码（Opus格式）
- 支持实时语音对话
- 支持文本消息交互
- 内置设备标识和认证
- 支持不同的语音识别模式

## 配置项

### ClientConfig
- ws_url: WebSocket服务器地址
- device_token: 设备认证token
- enable_token: 是否启用token认证
- protocol_version: 协议版本（默认1）

### AudioConfig
- sample_rate: 采样率（默认16000）
- channels: 声道数（默认1）
- frame_size: 帧大小（默认960）
- frame_duration: 帧时长（默认20ms）
- format: 音频格式（默认"opus"）

## 支持的消息类型

### 语音识别
```python
# 开始监听
{
    "type": "listen",
    "state": "start",
    "mode": "auto"  # auto/manual/realtime
}

# 停止监听
{
    "type": "listen",
    "state": "stop"
}
```

### TTS状态回调
```python
{
    "type": "tts",
    "state": "start|stop|sentence_start",
    "text": "要说的文本"  # 仅在 sentence_start 时存在
}
```

## 示例

1. 基础文本对话 - `examples/simple_client.py`
2. 实时语音对话 - `examples/audio_chat.py`

## 开发说明

### 音频处理

客户端发送和接收的音频数据都使用Opus编码：
- 采样率：16000Hz
- 声道数：1（单声道）
- 帧大小：960样本/帧
- 帧时长：20ms

### 错误处理

客户端会自动处理连接断开等错误：
- WebSocket连接断开时会触发重连
- 音频解码错误会被捕获并记录
- 网络错误会抛出相应异常

## 依赖

- websockets==10.4
- opuslib==3.0.1
- numpy==2.2.3
- sounddevice==0.5.1
- loguru==0.7.3
- pyaudio==0.2.14

## 协议文档

完整的协议文档请参考API文档。主要包括：
- 设备认证
- 音频流协议
- 消息类型定义
- 错误处理机制

## 致谢
本项目参考和借鉴了以下优秀的开源项目:

[xiaozhi-py](https://github.com/honestQiao/xiaozhi-py) - Python版本的小智客户端实现

[xiaozhi-web-client](https://github.com/TOM88812/xiaozhi-web-client.git) - Web版本的小智客户端实现

感谢所有为此项目做出贡献的开发者和社区成员。
