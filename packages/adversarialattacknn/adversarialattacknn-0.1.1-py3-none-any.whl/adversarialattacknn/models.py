import os
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import timm
import numpy as np
import pandas as pd
from PIL import Image

# Constants
IMG_HEIGHT, IMG_WIDTH = 224, 224
IMG_MAX, IMG_MIN = 1.0, 0.0

# Model lists
CNN_MODELS = ['resnet50', 'vgg16', 'mobilenet_v2', 'inception_v3']
VIT_MODELS = ['vit_base_patch16_224', 'pit_b_224', 'visformer_small', 'swin_tiny_patch4_window7_224']
ALL_MODELS = CNN_MODELS + VIT_MODELS


def load_pretrained_model(cnn_models=None, vit_models=None):
    cnn_models = cnn_models or []
    vit_models = vit_models or []
    
    for model_name in cnn_models:
        if model_name in models.__dict__:
            yield model_name, models.__dict__[model_name](weights="DEFAULT")
        else:
            raise ValueError(f"Model {model_name} not found in torchvision")
    
    for model_name in vit_models:
        yield model_name, timm.create_model(model_name, pretrained=True)

vit_model_pkg = ['vit_base_patch16_224', 'pit_b_224', 'cait_s24_224', 
                 'visformer_small', 'tnt_s_patch16_224', 'levit_256', 
                 'convit_base', 'swin_tiny_patch4_window7_224']

def load_single_model(model_name):
    if model_name in models.__dict__:
        model = models.__dict__[model_name](weights="DEFAULT")
    elif model_name in vit_model_pkg:
        model = timm.create_model(model_name, pretrained=True)
    else:
        raise ValueError(f"Unknown model: {model_name}")

    device = torch.device("cpu")  # Ensure CPU execution
    return wrap_model(model.eval().to(device))  # Move to CPU only

def wrap_model(model):
    """
    Wraps a model with preprocessing steps (resizing and normalization).
    """
    model_name = model.__class__.__name__
    resize_dim = 224
    
    if hasattr(model, 'default_cfg'):
        mean, std = model.default_cfg['mean'], model.default_cfg['std']
    else:
        mean, std = ([0.5] * 3, [0.5] * 3) if 'Inc' in model_name else ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        resize_dim = 299 if 'Inc' in model_name else 224
    
    return nn.Sequential(PreprocessingModel(resize_dim, mean, std), model)


def save_images(output_dir, adversaries, filenames):
    """
    Save adversarial images to the specified directory.
    """
    adversaries = (adversaries.detach().permute(0, 2, 3, 1).cpu().numpy() * 255).astype(np.uint8)
    os.makedirs(output_dir, exist_ok=True)
    for i, filename in enumerate(filenames):
        Image.fromarray(adversaries[i]).save(os.path.join(output_dir, filename))


def clamp(x, x_min, x_max):
    """Clamp tensor values within a specified range."""
    return torch.min(torch.max(x, x_min), x_max)


class PreprocessingModel(nn.Module):
    def __init__(self, resize, mean, std):
        super().__init__()
        self.resize = transforms.Resize(resize)
        self.normalize = transforms.Normalize(mean, std)
    
    def forward(self, x):
        return self.normalize(self.resize(x))


class EnsembleModel(nn.Module):
    def __init__(self, models, mode='mean'):
        super().__init__()
        self.device = next(models[0].parameters()).device
        self.models = nn.ModuleList([model.to(self.device) for model in models])
        self.mode = mode
    
    def forward(self, x):
        outputs = torch.stack([model(x) for model in self.models], dim=0)
        return torch.mean(outputs, dim=0) if self.mode == 'mean' else outputs


class AdvDataset(torch.utils.data.Dataset):
    def __init__(self, input_dir, output_dir=None, targeted=False, target_class=None, eval_mode=False):
        self.targeted = targeted
        self.target_class = target_class
        self.data_dir = output_dir if eval_mode else os.path.join(input_dir, 'images')
        self.f2l = self.load_labels(os.path.join(input_dir, 'labels.csv'))
        
        mode = 'Eval' if eval_mode else 'Train'
        print(f"=> {mode} mode: using data from {self.data_dir}")
        if not eval_mode:
            print(f"Saving images to {output_dir}")

    def __len__(self):
        return len(self.f2l)

    def __getitem__(self, idx):
        filename = list(self.f2l.keys())[idx]
        filepath = os.path.join(self.data_dir, filename)
        image = Image.open(filepath).resize((IMG_HEIGHT, IMG_WIDTH)).convert('RGB')
        image_tensor = torch.tensor(np.array(image).astype(np.float32) / 255).permute(2, 0, 1)
        label = self.f2l[filename]
        return image_tensor, label, filename

    def load_labels(self, file_path):
        df = pd.read_csv(file_path)
        if self.targeted:
            return {row['filename']: ([row['label'], self.target_class] if self.target_class else [row['label'], row['targeted_label']]) for _, row in df.iterrows()}
        return {row['filename']: row['label'] for _, row in df.iterrows()}


if __name__ == '__main__':
    dataset = AdvDataset(input_dir='./data_targeted', targeted=True, eval_mode=False)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=False)
    for images, labels, filenames in dataloader:
        print(images.shape, labels, filenames)
        break