import torch
import torch.nn as nn
import torch.nn.functional as F

class EnsembleModel(nn.Module):
    """
    A class for handling ensemble models by averaging predictions from multiple models.
    """
    def __init__(self, models):
        super().__init__()
        self.models = nn.ModuleList(models)

    def forward(self, x):
        return torch.mean(torch.stack([model(x) for model in self.models]), dim=0)


def wrap_model(model):
    """
    Ensures the model is in evaluation mode for consistent adversarial attack behavior.
    
    Args:
        model (torch.nn.Module): The model to wrap.
    
    Returns:
        torch.nn.Module: The wrapped model in eval mode.
    """
    return model.eval()


def clamp(tensor, min_value, max_value):
    """
    Clamps tensor values between specified min and max values.
    
    Args:
        tensor (torch.Tensor): The tensor to clamp.
        min_value (float): Minimum allowed value.
        max_value (float): Maximum allowed value.
    
    Returns:
        torch.Tensor: The clamped tensor.
    """
    return torch.clamp(tensor, min_value, max_value)

# Image normalization limits (Modify as per dataset requirements)
IMG_MIN = 0.0  # Example: 0 for unnormalized images, -1 for normalized ImageNet
IMG_MAX = 1.0  # Example: 1 for unnormalized images, 1 for normalized ImageNet


def loss_function(model, data, target, loss_type='crossentropy'):
    """
    Computes loss for a given model and data.
    
    Args:
        model (torch.nn.Module): The model for prediction.
        data (torch.Tensor): Input data.
        target (torch.Tensor): Target labels.
        loss_type (str): Type of loss function. Options: ['crossentropy', 'mse', 'kl_div']
    
    Returns:
        torch.Tensor: The computed loss value.
    """
    output = model(data)
    
    if loss_type == 'crossentropy':
        return F.cross_entropy(output, target)
    elif loss_type == 'mse':
        return F.mse_loss(output, target)
    elif loss_type == 'kl_div':
        return F.kl_div(F.log_softmax(output, dim=1), F.softmax(target, dim=1), reduction='batchmean')
    else:
        raise ValueError(f"Unsupported loss function: {loss_type}")
