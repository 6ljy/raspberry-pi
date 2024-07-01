import paho.mqtt.client as mqtt
import time
#rc 值 连接情况
#0 连接成功
#1 协议版本错误
#2 无效的客户端标识
#3 服务器无法使用
#4 错误的用户名或密码
#5 未经授权
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
client = mqtt.Client()
client.on_connect = on_connect
# 连接到服务器 会调用 on_connect 方法
client.connect("broker.emqx.io", 1883, 60)

# 每间隔 1 秒钟向 raspberry/windows 发送一个消息，连续发送 5 次
for i in range(5):
    # 四个参数分别为：主题，发送内容，QoS, 是否保留消息
    # QOS的值含义： 0最多一次 1至少一次 2仅此一次
    client.publish('watering_ljy/raspberry', payload=i, qos=0, retain=False)
    print(f"send {i} to watering_ljy/raspberry")
    time.sleep(1)
    
client.loop_forever()
