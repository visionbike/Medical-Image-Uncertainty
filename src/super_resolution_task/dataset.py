from pathlib import Path
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.transforms import functional as vfn
from .utils import image2tensor

__all__ = ["SRDataset"]


class SRDataset(Dataset):
    """
    Customize the dataset loading function and prepare low/high resolution image data in advanced
    """

    def __init__(self, data_root: str, image_size: int | tuple[int, int], upscale_factor: int) -> None:
        """

        :param data_root: training data set address.
        :param image_size: high resolution image size.
        :param upscale_factor: image magnification.
        """
        super().__init__()
        self.image_paths = [path for path in Path(data_root).iterdir() if path.is_file()]
        #
        self.hr_transforms = transforms.Resize(image_size)
        self.lr_transforms = transforms.Resize(
            size=(image_size[0] // upscale_factor, image_size[1] // upscale_factor),
            interpolation=vfn.InterpolationMode.BICUBIC,
            antialias=True
        )

    def __getitem__(self, batch_index: int) -> tuple[torch.Tensor, ...]:
        # read a batch of image data
        image = Image.open(str(self.image_paths[batch_index]))
        # transform image
        hr_image = self.hr_transforms(image)
        lr_image = self.lr_transforms(hr_image)
        # convert image data into Tensor stream format (PyTorch).
        # note: the range of input and output is between [0, 1]
        lr_tensor = image2tensor(lr_image, range_norm=False, half=False)
        hr_tensor = image2tensor(hr_image, range_norm=False, half=False)
        #
        return lr_tensor, hr_tensor

    def __len__(self) -> int:
        return len(self.image_paths)
