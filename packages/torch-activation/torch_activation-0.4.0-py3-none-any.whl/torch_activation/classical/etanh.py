import torch
import torch.nn as nn
from torch import Tensor

from torch_activation import register_activation
from torch_activation.base import BaseActivation


@register_activation
class ETanh(BaseActivation):
    r"""
    Applies the E-Tanh activation function:

    :math:`\text{E-Tanh}(z) = a \cdot \exp(z) \cdot \tanh(z)`

    An activation function combining the exponential and tanh functions.

    Args:
        a (float, optional): Scaling parameter. Default: ``1.0``
        inplace (bool, optional): parameter kept for API consistency, but E-Tanh operation 
                                 cannot be done in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
    """

    def __init__(self, a: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.a = a
          # Unused

    def _forward(self, z) -> Tensor:
        return self.a * torch.exp(z) * torch.tanh(z)


@register_activation
class EvolvedTanhReLU(BaseActivation):
    r"""
    Applies the evolved combination of tanh and ReLU activation function:

    :math:`\text{EvolvedTanhReLU}(z) = a \cdot \tanh(z^2) + \text{ReLU}(z)`

    This activation function was found using neuroevolution and showed the best performance
    on the HAR dataset using LSTM units.

    Args:
        a (float, optional): Scaling parameter. Default: ``1.0``
        inplace (bool, optional): parameter kept for API consistency, but this operation 
                                 cannot be done in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
    """

    def __init__(self, a: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.a = a
          # Unused

    def _forward(self, z) -> Tensor:
        return self.a * torch.tanh(z**2) + torch.relu(z)


@register_activation
class EvolvedTanhLogReLU(BaseActivation):
    r"""
    Applies the evolved regular activation function combining tanh and ReLU:

    :math:`\text{EvolvedTanhLogReLU}(z) = \max(\tanh(\log(z)), \text{ReLU}(z))`

    This activation function was found using neuroevolution.

    Args:
        inplace (bool, optional): parameter kept for API consistency, but this operation 
                                 cannot be done in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
          # Unused

    def _forward(self, z) -> Tensor:
        # Handle potential negative values for log
        safe_log = torch.log(torch.clamp(z, min=1e-10))
        return torch.maximum(torch.tanh(safe_log), torch.relu(z))
