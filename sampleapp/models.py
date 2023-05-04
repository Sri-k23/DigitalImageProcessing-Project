from django.db import models
import cv2
import numpy as np


ACTION_CHOICES = (
    ('RGB to BGR', 'BGR'),
    ('RGB to GRAY', 'GrayScale'),
    ('Color', 'Color'),
    ('Blur', 'Blur'),
    ('Noise ( Gaussian )', 'Noise ( Gaussian )'),
    ('Noise ( Salt and Pepper )', 'Noise ( Salt and Pepper )'),
    ('Resizing ( 512 x 512 )', 'Resizing ( 512 x 512 )'),
    ('Resizing ( 16 x 16 )', 'Resizing ( 16 x 16 )'),
    ('Contrast ( 0-255 )', 'Contrast ( 0-255 )'),
    ('Contrast ( 0-15 )', 'Contrast ( 0-15 )'),
    ('Contrast ( 0-1 )', 'Contrast ( 0-1 )'),
    ('Rotation ( 15 degrees )', 'Rotation ( 15 degrees )'),
    ('Rotation ( 45 degrees )', 'Rotation ( 45 degrees )'),
    ('Rotation ( 90 degrees )', 'Rotation ( 90 degrees )'),
    ('Rotation ( 180 degrees )', 'Rotation ( 180 degrees )'),
    ('Histogram Equalization', 'Histogram Equalization'),
)


class Sampleapp(models.Model):
    name = models.CharField(max_length=50, choices=ACTION_CHOICES)
    emp_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.name} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = cv2.imread(self.emp_image.path)
        if self.name == "RGB to BGR":
            new_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif self.name == "RGB to GRAY":
            new_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        elif self.name == "Color":
            if img.shape[-1] == 1:
                new_image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            else:
                # Image is already in RGB format
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
            pepper = noise < 3
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
            lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab_img)
            l_channel_eq = cv2.equalizeHist(l_channel)
            lab_img_eq = cv2.merge((l_channel_eq, a_channel, b_channel))
            new_image = lab_img_eq
        else:
            new_image = img
        cv2.imwrite(self.emp_image.path, new_image)
