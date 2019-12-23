import torch
import torch.nn as nn
import torch.nn.functional as F


class Pooling2d(nn.Module):
    def __init__(self, nch=[], pool=2, type='avg'):
        super().__init__()

        if type == 'avg':
            self.pooling = nn.AvgPool2d(pool)
        elif type == 'max':
            self.pooling = nn.MaxPool2d(pool)
        elif type == 'conv':
            self.pooling = nn.Conv2d(nch, nch, kernel_size=pool, stride=pool)

    def forward(self, x):
        return self.pooling(x)


class UnPooling2d(nn.Module):
    def __init__(self, nch=[], pool=2, type='nearest'):
        super().__init__()

        if type == 'nearest':
            self.unpooling = nn.Upsample(scale_factor=pool, mode='nearest', align_corners=True)
        elif type == 'bilinear':
            self.unpooling = nn.Upsample(scale_factor=pool, mode='bilinear', align_corners=True)
        elif type == 'conv':
            self.unpooling = nn.ConvTranspose2d(nch, nch, kernel_size=pool, stride=pool)

    def forward(self, x):
        return self.unpooling(x)


class Concat(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x1, x2):
        diffy = x2.size()[2] - x1.size()[2]
        diffx = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffx // 2, diffx - diffx // 2,
                        diffy // 2, diffy - diffy // 2])

        return torch.cat([x2, x1], dim=1)


class CNR1d(nn.Module):
    def __init__(self, nch_in, nch_out, bnorm=True, brelu=True):
        super().__init__()

        layers = nn.Linear(nch_in, nch_out)
        if bnorm:
            layers.append(nn.InstanceNorm1d(nch_out))
        if brelu:
            layers.append(nn.LeakyReLU(brelu))

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)


class CNR2d(nn.Module):
    def __init__(self, nch_in, nch_out, kerner_size=4, stride=2, padding=1, bnorm=True, brelu=True, bdrop=False):
        super().__init__()
        layers = [nn.Conv2d(nch_in, nch_out, kernel_size=kerner_size, stride=stride, padding=padding)]

        if bnorm:
            layers.append(nn.InstanceNorm2d(nch_out))

        if brelu:
            layers.append(nn.LeakyReLU(brelu))
        else:
            layers.append(nn.ReLU())

        if bdrop:
            layers.append(nn.Dropout2d(bdrop))

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)


class DECNR2d(nn.Module):
    def __init__(self, nch_in, nch_out, kerner_size=4, stride=2, padding=1, bnorm=True, brelu=True, bdrop=False):
        super().__init__()
        layers = [nn.ConvTranspose2d(nch_in, nch_out, kernel_size=kerner_size, stride=stride, padding=padding)]
        if bnorm:
            layers.append(nn.InstanceNorm2d(nch_out))
        if brelu:
            layers.append(nn.LeakyReLU(brelu))
        if bdrop:
            layers.append(nn.Dropout2d(bdrop))

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)



class Conv2d(nn.Module):
    def __init__(self, nch_in, nch_out, kernel_size=3):
        super(Conv2d, self).__init__()
        self.conv = nn.Conv2d(nch_in, nch_out, kernel_size=kernel_size, padding=int((kernel_size - 1) / 2))

    def forward(self, x):
        return self.conv(x)


class Linear(nn.Module):
    def __init__(self, nch_in, nch_out):
        super(Linear, self).__init__()
        self.linear = nn.Linear(nch_in, nch_out)

    def forward(self, x):
        return self.linear(x)


class TV1dLoss(nn.Module):
    def __init__(self):
        super(TV1dLoss, self).__init__()

    def forward(self, input):
        # loss = torch.mean(torch.abs(input[:, :, :, :-1] - input[:, :, :, 1:])) + \
        #        torch.mean(torch.abs(input[:, :, :-1, :] - input[:, :, 1:, :]))
        loss = torch.mean(torch.abs(input[:, :-1] - input[:, 1:]))

        return loss


class TV2dLoss(nn.Module):
    def __init__(self):
        super(TV2dLoss, self).__init__()

    def forward(self, input):
        loss = torch.mean(torch.abs(input[:, :, :, :-1] - input[:, :, :, 1:])) + \
               torch.mean(torch.abs(input[:, :, :-1, :] - input[:, :, 1:, :]))
        return loss


class SSIM2dLoss(nn.Module):
    def __init__(self):
        super(SSIM2dLoss, self).__init__()

    def forward(self, input, targer):
        loss = 0
        return loss

