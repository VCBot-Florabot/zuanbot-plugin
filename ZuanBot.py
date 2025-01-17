import random
import json

flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    #print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("ZuanBot 加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    print(flora_api)
    pass


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    try:
        global ws_client
        global ws_server
        send_address = data.get("SendAddress")
        
        ws_client = send_address.get("WebSocketClient")
        ws_server = send_address.get("WebSocketServer")
    except:
        ws_client=None
        ws_server=None
        pass
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        print(uid, gid, mid, msg)
        if gid is not None and msg in ["#祖安lite","#祖安full"]:
            send_compatible(msg="请在私聊环境中使用",gid=gid,uid=uid,data=data)
            return
        if msg == "#祖安lite":
            send_compatible(msg=zuan_lite(), gid=gid,uid=uid,data=data)
        if msg == "#祖安full":
            send_compatible(msg=zuan_full(), gid=gid,uid=uid,data=data)

def zuan_lite():
    #load zuan_lite.json
    zuan_lite_list=json.load(open(f"./{flora_api.get('ThePluginPath')}/res/zuan-lite.json",mode="r",errors='ignore'))
    num = make_random(len(zuan_lite_list))
    print(zuan_lite_list[num]['index'])
    return zuan_lite_list[num]['text']

def zuan_full():
    #load zuan_full.json
    zuan_full_list=json.load(open(f"./{flora_api.get('ThePluginPath')}/res/zuan-full.json",mode="r",errors='ignore'))
    num = make_random(len(zuan_full_list))
    print(zuan_full_list[num]['index'])
    return zuan_full_list[num]['text']


def make_random(max:int):
    print(max)
    return random.randint(0,max)

def send_compatible(msg:str,gid:str|int,uid: str|int,data: dict=None):  #兼容性函数,用于兼容旧版本API
    if flora_api.get("FloraVersion") == 'v1.01':
        send_msg(msg=msg,gid=gid,uid=uid)
    else:
        send_type=flora_api.get("ConnectionType")
        send_address=flora_api.get("FrameworkAddress")
        send_msg(msg=msg,gid=gid,uid=uid,send_type=send_type,ws_client=ws_client,ws_server=ws_server)
        