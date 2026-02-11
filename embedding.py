import torch
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import torchvision.transforms as transforms
from PIL import Image

model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def get_image_embedding(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image)
        image = image.unsqueeze(0)

        with torch.no_grad():
            embedding = model(image)

        return embedding.flatten().numpy()
    except:
        return None
