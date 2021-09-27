from setuptools import setup, find_packages

setup(
    name="nakuru-project",
    version="1.0.0",
    author="Lxns-Network",
    author_email="joinchang1206@gmail.com",
    description="一款为 go-cqhttp 的正向 WebSocket 设计的 Python SDK，支持纯 CQ 码与消息链的转换处理",
    url="https://github.com/Lxns-Network/nakuru-project",
    packages=find_packages(include=("nakuru", "nakuru.*")),
    install_requires=[
        "aiohttp",
        "pydantic",
        "Logbook",
        "async_lru"
    ]
)
