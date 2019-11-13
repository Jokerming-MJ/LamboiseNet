from torch import *
import torch.nn as nn
from torch.nn import *
"""Mini- Unet of 2 downscaling layers and 2 upscaling ones, 
    """


class BasicUnet(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(BasicUnet, self).__init__()

        self.name = "UNet"
        self.n_classes = n_classes
        self.n_channels = n_channels

        self.input_layer = DoubleConvolutionLayer(n_channels, 64)
        self.downscaling_layer1 = nn.Sequential(nn.MaxPool2d(2),
                                                DoubleConvolutionLayer(64, 128))
        self.downscaling_layer2 = nn.Sequential(nn.MaxPool2d(2),
                                                DoubleConvolutionLayer(128, 256))
        # TODO add padding ?
        self.up1 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.upscaling_layer1 = DoubleConvolutionLayer(256, 128)
        self.up2 =nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.upscaling_layer = DoubleConvolutionLayer(128, 64)
        self.output_layer = DoubleConvolutionLayer(64, n_classes)

    def forward(self, x):
        out0 = self.input_layer(x)
        out1 = self.downscaling_layer1(out0)
        out = self.downscaling_layer2(out1)
        out = self.up1(out)
        out = cat([out, out1], dim=1)
        out = self.upscaling_layer1(out)
        out = self.up2(out)
        out = cat([out, x], dim=1)
        out = self.upscaling_layer2(out)
        output = self.output_layer(out)
        return output


class DoubleConvolutionLayer(nn.Module):
    def __init__(self, n_channels_input, n_channels_output):
        super(DoubleConvolutionLayer, self).__init__()
        self.double_layer = nn.Sequential(nn.Conv2d(n_channels_input, n_channels_output, kernel_size=3, padding=1),
                                          nn.BatchNorm2d(n_channels_output),
                                          nn.ReLU(inplace=True),
                                          nn.Conv2d(n_channels_output, n_channels_output, kernel_size=3, padding=1),
                                          nn.BatchNorm2d(n_channels_output),
                                          nn.ReLU(inplace=True))

    def forward(self, x):
        x = self.double_layer(x)
        return x
