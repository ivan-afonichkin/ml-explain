import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch


def plot_img(image, normalize=True, ax=None, **kwargs):
    if isinstance(image, torch.Tensor):
        image = np.float32(image)

    if len(image.shape) == 4:
        # We can reduce first dimension if there is only 1 sample
        if image.shape[0] == 1:
            image = image[0]
        else:
            raise RuntimeError(f"Plotting image of shape {image.shape} is not supported.")

    # If image consists of only 1 channel, simply reduce it
    if image.shape[0] == 1:
        image = image[0]

    # If there are 3 channels, then transpose image properly
    if image.shape[0] == 3:
        image = image.transpose((1, 2, 0))

    # Convert to 0-1 range
    if normalize:
        image = (image - image.min()) / (image.max() - image.min())

    if ax:
        ax.imshow(image, **kwargs)
    else:
        plt.imshow(image, **kwargs)
        plt.show()


def plot_img_heatmap(image, heatmap, alpha=0.5):
    def _reduce_channels(img):
        if img.shape[0] == 3:
            img = img.mean((0,), keepdim=True)

        if img.shape[1] == 3:
            img = img.mean((1,), keepdim=True)

        return img

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plot_img(image, ax=ax)

    # In order to plot heatmap we reduce it to have only 1 channel
    heatmap = _reduce_channels(heatmap)

    plot_img(heatmap, normalize=False, ax=ax, cmap='hot', interpolation='nearest', alpha=alpha)

    plt.show()


def load_img(img_path, imagenet=False, resize=None, normalize=False):
    pil_img = Image.open(img_path).convert('RGB')

    if imagenet:
        resize, normalize = (224, 224), True

    if resize:
        pil_img = pil_img.resize(resize)

    np_img = np.float32(pil_img)

    if normalize:
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        np_img /= 255
        np_img = (np_img - mean) / std

    torch_img = torch.tensor(np_img, dtype=torch.float32).permute((2, 0, 1))

    return torch_img.unsqueeze(0)