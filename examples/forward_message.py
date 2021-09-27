from nakuru import (
    CQHTTP,
    GroupMessage
)
from nakuru.entities.components import Plain, Node, Image

app = CQHTTP(
    host="127.0.0.1",
    port=6700,
    http_port=5700
)


@app.receiver("GroupMessage")
async def _(app: CQHTTP, source: GroupMessage):
    # 方法 1
    await app.sendGroupForwardMessage(source.group_id, [
        Node(name="落雪ちゃん", uin=2941383730, content=[
            Plain(text="nc什么时候cos小老师")
        ]),
        Node(name="盐焗雾喵", uin=2190945952, content=[
            Plain(text="今晚就cos小老师")
        ]),
        Node(name="Rosemoe♪ ~ requiem ~", uin=2073412493, content=[
            Plain(text="好耶"),
            Image.fromFileSystem("./src/1.jpg")
        ])
    ])
    # 方法 2
    await app.sendGroupForwardMessage(source.group_id, [
        {
            "type": "node",
            "data": {
                "name": "落雪ちゃん",
                "uin": 2941383730,
                "content": "nc什么时候cos小老师"
            }
        },
        {
            "type": "node",
            "data": {
                "name": "盐焗雾喵",
                "uin": 2190945952,
                "content": "今晚就cos小老师"
            }
        },
        {
            "type": "node",
            "data": {
                "name": "Rosemoe♪ ~ requiem ~",
                "uin": 2073412493,
                "content": [
                    {
                        "type": "text",
                        "data": {"text": "好耶"}
                    },
                    {
                        "type": "image",
                        "data": {"file": "file:///./src/1.jpg"}
                    }
                ]
            }
        }
    ])


app.run()
