from bilibili_api import login, user, sync
from bilibili_api.session import Session, Event,Picture
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
model_co = YOLO('yolov8n-seg.pt')
model = YOLO('best.pt')  #这里放权重路径
print("请登录：")
credential = login.login_with_qrcode_term()
try:
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_sessdata()
except:
    print("登陆失败。。。")
    exit()
print("欢迎，", sync(user.get_self_info(credential))['name'], "!")

session = Session(credential)
name_dict = {0: '九条裟罗', 1: '优菈', 2: '八重神子', 3: '刻晴', 4: '可莉', 5: '夜兰', 6: '妮露', 7: '宵宮', 8: '温迪', 9: '珊瑚宫心海', 10: '甘雨', 11: '神里绫华', 12: '纳西妲', 13: '胡桃', 14: '芙宁娜', 15: '钟离', 16: '雷电将军', 17: '枫原万叶'}
@session.on(Event.PICTURE)
async def pic(event: Event):
    img: Picture = event.content
    if not img.url.endswith(('.jpg','.jpeg','.png')):
        await session.reply(event, '图片格式不支持')
        return
    img=Picture.from_url(img.url)
    await img.download("./")
    image = Image.open("img.jpg")
    results = model_co.predict(source=image)[0]
    indexes=np.where(results.boxes.cls.numpy()==0)[0]
    if len(indexes)==0:
        img = cv2.imread('img.jpg')
        pred = model.predict(source=img)[0]
        r=[f'{name_dict[i]}:{format(pred.probs.data[i]*100,".2f")}%' for i in pred.probs.top5[:3]]
        await session.reply(event, '以下是我的猜测结果：\n'+'\n'.join(r))
        return
    pixel_xy = results.masks.xy[indexes[0]]
    points = np.array(pixel_xy, np.int32)
    input_image = cv2.imread('img.jpg')
    black_background = np.zeros_like(input_image)
    cv2.fillPoly(black_background, [points], (255, 255, 255))
    masked_image = cv2.bitwise_and(input_image, black_background)
    cv2.imwrite('img_cold.jpg', masked_image)
    img = cv2.imread('img_cold.jpg')
    pred = model.predict(source=img)[0]
    if pred.probs.data.max()<0.65:
        img = cv2.imread('img.jpg')
        pred = model.predict(source=img)[0]
        r=[f'{name_dict[i]}:{format(pred.probs.data[i]*100,".2f")}%' for i in pred.probs.top5[:3]]
        await session.reply(event, '以下是我的猜测结果：\n'+'\n'.join(r))
        return
    r=[f'{name_dict[i]}:{format(pred.probs.data[i]*100,".2f")}%' for i in pred.probs.top5[:3]]
    await session.reply(event, '以下是我的猜测结果：\n'+'\n'.join(r))

say_hi='''欢迎使用 测测你是原神里的谁
目前由于数据集限制，仅可预测出以下角色：
九条裟罗, 优菈, 八重神子, 刻晴, 可莉, 夜兰, 
妮露, 宵宮, 温迪, 珊瑚宫心海, 甘雨, 神里绫华, 
纳西妲, 胡桃, 芙宁娜, 钟离, 雷电将军, 枫原万叶

本模型基于yolov8制作
上传图片即视为您接受并认可如下内容：
1.您上传的图片将被我们用于且仅用于预测使用。
2.我们不会存储或分享用您上传的个人图片。
2.本模型仅用于娱乐目的。我们无法保证预测的准确性。
3.对于因使用本模型而导致的任何风险，我们概不负责。
4.最终解释权归B站UP主：ych233 所有'''

@session.on(Event.TEXT)
async def reply(event: Event):
    if event.content == "/close":
        session.close()
    else:
        await session.reply(event, say_hi)

sync(session.start())
