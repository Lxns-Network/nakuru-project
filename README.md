<div align="center">
  <img width="256" src="./logo.png" alt="logo">

# Nakuru Project
一款为 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的正向 WebSocket 设计的 Python SDK

在 [kuriyama](https://github.com/Lxns-Network/mirai-python-sdk) 的基础上改动

项目名来源于藍月なくる，图标由[せら](https://www.pixiv.net/users/577968)绘制
</div>

## 食用方法
将 `nakuru` 文件夹移至 Python 的 `Lib/site-packages` 目录下。

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

app = CQHTTP(
    host="127.0.0.1",
    port=6700,
    http_port=5700
)

@app.receiver("GroupMessage")
async def _(app: CQHTTP, source: GroupMessage):
    if source.message == "戳我":
        await app.sendGroupMessage(source.group_id, f"[CQ:poke,qq={source.user_id}]")
    elif source.message == "test":
        await app.sendGroupMessage(source.group_id, "test")

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