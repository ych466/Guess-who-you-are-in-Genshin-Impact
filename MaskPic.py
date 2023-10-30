from torchvision.models.detection import maskrcnn_resnet50_fpn_v2,MaskRCNN_ResNet50_FPN_V2_Weights
import torch
from torchvision.io import read_image,write_jpeg
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
model = maskrcnn_resnet50_fpn_v2(weights=weights).to(device)
model.eval()
import os
from alive_progress import alive_bar
root = "dataset"
data_x=[]
data_y=[]
classes=os.listdir(root)
if not os.path.exists(f'{root}_cold'):os.makedirs(f'{root}_cold')
with alive_bar(25000) as bar:
    for i,dir in enumerate(os.listdir(root)):
        if not os.path.exists(f'{root}_cold\{dir}'):os.makedirs(f'{root}_cold\{dir}')
        for name in os.listdir(f"{root}\{dir}"):
            img=read_image(f"{root}\{dir}\{name}").to(device).unsqueeze(0)/255
            with torch.no_grad():
                r=model(img)[0]
            bar()
            if len(r['labels'])==0 or r['labels'][0]!=1:continue
            img=(r['masks'][0]*img*255).to(torch.uint8).squeeze(0).to('cpu')
            write_jpeg(img,f'{root}_cold\{dir}\{name}')
           