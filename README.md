<div align="center">
  <img width="256" src="./logo.png" alt="logo">

# Nakuru Project
一款为 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的正向 WebSocket 设计的 Python SDK，支持纯 CQ 码与消息链的转换处理

在 [kuriyama](https://github.com/Lxns-Network/mirai-python-sdk) 的基础上改动

项目名来源于藍月なくる，图标由[せら](https://www.pixiv.net/users/577968)绘制
</div>

## 食用方法
使用 `pip install nakuru-project` 安装。

需要将 go-cqhttp 的正向 WebSocket 与 HTTP 配置项开启。

## 示例
没有文档，源码就是文档。

```python
from nakuru import (
    CQHTTP,
    GroupMessage,
    Notify,
    GroupMessageRecall,
    FriendRequest
)
from nakuru.entities.components import Plain, Image

app = CQHTTP(
    host="127.0.0.1",
    port=6700,
    http_port=5700,
    token="TOKEN" # 可选，如果配置了 Access-Token
)

@app.receiver("GroupMessage")
async def _(app: CQHTTP, source: GroupMessage):
    # 通过纯 CQ 码处理
    if source.raw_message == "戳我":
        await app.sendGroupMessage(source.group_id, f"[CQ:poke,qq={source.user_id}]")
    # 通过消息链处理
    chain = source.message
    if isinstance(chain[0], Plain):
        if chain[0].text == "看":
            await app.sendGroupMessage(source.group_id, [
                Plain(text="给你看"),
                Image.fromFileSystem("D:/好康的.jpg")
            ])

@app.receiver("GroupMessageRecall")
async def _(app: CQHTTP, source: GroupMessageRecall):
    await app.sendGroupMessage(source.group_id, "你撤回了一条消息")

@app.receiver("Notify")
async def _(app: CQHTTP, source: Notify):
    if source.sub_type == "poke" and source.target_id == 114514:
        await app.sendGroupMessage(source.group_id, "不许戳我")

@app.receiver("FriendRequest")
async def _(app: CQHTTP, source: FriendRequest):
    await app.setFriendRequest(source.flag, True)

app.run()
```

## 贡献
欢迎 PR 代码或提交 Issue，项目现在还存在着许多问题。
