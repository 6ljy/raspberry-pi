# 直接使用对应的库进行读取
from sensor import MCP3004
import time
mcp = MCP3004(bus=0, addr=0, vref=5.5)
mcp._spi.max_speed_hz = 2106000
while True:
    print(mcp.read(0))
    time.sleep(4)
