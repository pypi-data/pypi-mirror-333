import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch import nn


class EnsembleModel(nn.Module):
    """
    A class for handling ensemble models.
    """
    def __init__(self, models):
        super(EnsembleModel, self).__init__()
        self.models = nn.ModuleList(models)

    def forward(self, x):
        outputs = [model(x) for model in self.models]
        return sum(outputs) / len(outputs)


def wrap_model(model):
    """
    Wrap the model to be compatible with adversarial attacks.
    Args:
        model (torch.nn.Module): The model to wrap.
    Returns:
        torch.nn.Module: The wrapped model.
    """
    model.eval()
    return model


def clamp(tensor, min_value, max_value):
    """
    Clamp the tensor values between the specified min and max values.

    Args:
        tensor (torch.Tensor): The tensor to clamp.
        min_value (torch.Tensor): Minimum value.
        max_value (torch.Tensor): Maximum value.

    Returns:
        torch.Tensor: The clamped tensor.
    """
    return torch.max(torch.min(tensor, max_value), min_value)


# Example min/max values for images (can be changed as per dataset)
img_min = 0.0
img_max = 1.0


def loss_function(model, data, target, loss_type='crossentropy'):
    """
    Get the loss function.
    Args:
        model (torch.nn.Module): The model for prediction.
        data (torch.Tensor): The input data.
        target (torch.Tensor): The target labels.
        loss_type (str): Type of loss function ('crossentropy', etc.)
    Returns:
        torch.Tensor: The computed loss value.
    """
    output = model(data)
    if loss_type == 'crossentropy':
        return F.cross_entropy(output, target)
    else:
        raise ValueError("Unsupported loss function")
