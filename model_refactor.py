import numpy as np
import torch
from torch import nn
from constants import IMG_SIZE, NUM_CHANNELS
from torch.autograd import Variable


# def get_convnet_output_size(network, input_size=IMG_SIZE):
#     input_size = input_size or IMG_SIZE

#     if type(network) != list:
#         network = [network]

#     in_channels = network[0].conv1.in_channels

#     output = Variable(torch.ones(1, in_channels, input_size, input_size))
#     output.require_grad = False
#     for conv in network:
#         output = conv.forward(output)

#     return np.asscalar(np.prod(output.data.shape)), output.data.size()[2]


class ConvLayer(nn.Module):
    def __init__(self, in_c, out_c, kernel_size, max_pool_stride=2,
                 dropout_ratio=0.5):
        super(ConvLayer, self).__init__()
        self.conv1 = nn.Conv2d(in_c, out_c, kernel_size=kernel_size)
        self.conv2 = nn.Conv2d(out_c, out_c, kernel_size=kernel_size)
        self.max_pool2d = nn.MaxPool2d(max_pool_stride)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout2d(p=dropout_ratio)

    def forward(self, x):
        x = self.relu(self.conv2(self.relu(self.conv1(x))))
        return self.dropout(self.max_pool2d(x))


class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.num_classes = 15
#         self.convs = []
#         self.convs.append(ConvLayer(NUM_CHANNELS, 32, kernel_size=5))
#         self.convs.append(ConvLayer(32, 64, kernel_size=5))
#         conv_output_size, _ = get_convnet_output_size(self.convs)
#         self.fully_connected1 = nn.Linear(conv_output_size, 1024)
#         self.fully_connected2 = nn.Linear(1024, self.num_classes)
          #
          # Determine conv_output_size first
        self.convo_stack = nn.Sequential(
            ConvLayer(NUM_CHANNELS, 32, kernel_size=5),
            ConvLayer(32, 64, kernel_size=5),
            
            # reshape x?
            # x = x.view(x.size(0), -1)
            nn.Linear(215296, 1024),
            nn.ReLU(),
            nn.Linear(1024, self.num_classes)
        )

    def forward(self, x):
        for conv in self.convs:
            x = conv(x)
        x = x.view(x.size(0), -1)
#         x = nn.function.relu(self.fully_connected1(x))
#         x = nn.ReLU(self.fully_connected1(x))
        x = nn.functional.relu(self.fully_connected1(x))
        return nn.functional.log_softmax(self.fully_connected2(x))
