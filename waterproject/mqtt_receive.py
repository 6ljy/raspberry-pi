# subscriber.py
import paho.mqtt.client as mqtt

# 当服务器响应的时候，会回调这个函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅 raspberry/topic 主题
    client.subscribe("wateringljy/windows")
    
# 回调函数，当收到消息时，触发该函数
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 设置遗嘱消息（立遗嘱），当树莓派断电，或者网络出现异常中断时，发送遗嘱消息往这个 topic
client.will_set('watering_ljy/raspberry', b'{"status": "Off"}')

# 创建连接，三个参数分别为 broker 地址，broker 端口号，保活时间 broker.emqx.io 是免费的mqtt服务器，如果是自己搭建的服务器需要填上自己的ip地址
#当服务器响应的时候 会回调 on_connect 方法
client.connect("broker.emqx.io", 1883, 60)

# 设置网络循环堵塞，在调用 disconnect() 或程序崩溃前，不会主动结束程序
client.loop_forever()
