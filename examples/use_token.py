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
    token="mytoken"
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