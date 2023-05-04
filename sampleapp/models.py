from django.db import models
import cv2

ACTION_CHOICES= (
    ('RGB to BGR', 'Blue green'),
    ('RGB to GRAY', 'GrayScale'),
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

        else:
            new_image = img
        cv2.imwrite(self.emp_image.path, new_image)