import torch
from torch.serialization import add_safe_globals
from torch.nn.modules.container import Sequential
import ultralytics.nn.modules as modules
from ultralytics.nn.tasks import SegmentationModel
from ultralytics import YOLO

# ✅ Whitelist di tutti i moduli usati nel modello
add_safe_globals([
    SegmentationModel,
    Sequential,
    modules.Conv,
    modules.C2f,
    modules.SPPF,
    modules.Segment,
    modules.Concat
])

# ✅ Allenamento
model = YOLO('yolov8n-seg.pt')
model.train(data='config.yaml', epochs=1, imgsz=640)
