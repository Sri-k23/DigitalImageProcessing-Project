from django.db import models
import cv2
import numpy as np
from skimage.util import random_noise


class Sampleapp(models.Model):
    name = models.CharField(max_length=50)
    emp_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.name} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = cv2.imread(self.emp_image.path)
        if self.name == "GrayScale":
            new_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif self.name == "Color":
            new_image = img
        elif self.name == "Blur":
            new_image = cv2.GaussianBlur(img, (9, 9), cv2.BORDER_DEFAULT)
        elif self.name == "Noise ( Gaussian )":
            noise = np.random.randn(*img.shape) * 50 + 20
            new_image = img + noise
        elif self.name == "Noise ( Salt and Pepper )":
            # Generate salt and pepper noise
            noise = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.randu(noise, 0, 255)
            salt = noise > 250
            pepper = noise < 5
            noise[salt] = 255
            noise[pepper] = 0
            # Add the noise to the image
            new_image = cv2.add(img, cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR))
        elif self.name == "Resizing ( 512 x 512 )":
            new_image = cv2.resize(img, (512, 512))
        elif self.name == "Resizing ( 16 x 16 )":
            new_image = cv2.resize(img, (16, 16))
        elif self.name == "Contrast ( 0-255 )":
            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Determine the maximum and minimum pixel values in the grayscale image
            max_value = np.max(gray_img)
            min_value = np.min(gray_img)

            # Compute the dynamic range of the grayscale image
            dynamic_range = max_value - min_value

            # Compute the scaling factor based on the desired number of levels
            desired_levels = 256
            scaling_factor = (desired_levels - 1) / dynamic_range

            # Apply contrast stretching to the grayscale image
            new_gray_img = ((gray_img - min_value) * scaling_factor).astype(np.uint8)

            # Convert the grayscale image back to BGR
            new_image = cv2.cvtColor(new_gray_img, cv2.COLOR_GRAY2BGR)
        elif self.name == "Contrast ( 0-15 )":
            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Determine the maximum and minimum pixel values in the grayscale image
            max_value = np.max(gray_img)
            min_value = np.min(gray_img)

            # Compute the dynamic range of the grayscale image
            dynamic_range = max_value - min_value

            # Compute the scaling factor based on the desired number of levels
            desired_levels = 16
            scaling_factor = (desired_levels - 1) / dynamic_range

            # Apply contrast stretching to the grayscale image
            new_gray_img = ((gray_img - min_value) * scaling_factor).astype(np.uint8) + min_value

            # Convert the grayscale image back to BGR
            new_image = cv2.cvtColor(new_gray_img, cv2.COLOR_GRAY2BGR)
        elif self.name == "Contrast ( 0-1 )":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply binary thresholding to the grayscale image
            threshold, binary_image = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
            # Convert the binary image back to BGR
            new_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
        elif self.name == "Rotation ( 15 degrees )":
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1)
            new_image = cv2.warpAffine(img, M, (cols, rows))
        elif self.name == "Rotation ( 45 degrees )":
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
            new_image = cv2.warpAffine(img, M, (cols, rows))
        elif self.name == "Rotation ( 90 degrees )":
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
            new_image = cv2.warpAffine(img, M, (cols, rows))
        elif self.name == "Rotation ( 180 degrees )":
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 180, 1)
            new_image = cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        elif self.name == "Histogram Equalization":
            # Convert the color image to the LAB color space
            lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

            # Split the LAB image into L, A, and B channels
            l_channel, a_channel, b_channel = cv2.split(lab_img)

            # Apply histogram equalization to the L channel
            l_channel_eq = cv2.equalizeHist(l_channel)

            # Merge the equalized L channel with the original A and B channels
            lab_img_eq = cv2.merge((l_channel_eq, a_channel, b_channel))

            # Convert the LAB image back to the original color space
            new_image = cv2.cvtColor(lab_img_eq, cv2.COLOR_LAB2BGR)
        else:
            # if the name does not match any of the above conditions,
            # simply save the original image and return
            return

        cv2.imwrite(self.emp_image.path, new_image)

