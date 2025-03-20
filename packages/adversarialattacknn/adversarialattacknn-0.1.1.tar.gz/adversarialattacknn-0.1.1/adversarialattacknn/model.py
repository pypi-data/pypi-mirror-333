# adversarialattacknn/model.py

import torch
import torchvision.models as models

def load_single_model(model_name: str, pretrained: bool = True):
    """
    Load a single model by name, either pretrained or custom-trained.

    Args:
        model_name (str): The name of the model (e.g., 'resnet18', 'alexnet', etc.).
        pretrained (bool): Whether to load the pretrained weights.

    Returns:
        torch.nn.Module: The loaded model.
    """
    if model_name == 'resnet18':
        model = models.resnet18(pretrained=pretrained)
    elif model_name == 'alexnet':
        model = models.alexnet(pretrained=pretrained)
    else:
        raise ValueError(f"Model {model_name} is not supported.")
    
    return model
