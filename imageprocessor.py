import csv, cv2, datetime
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

class ImageProcessor:
    """
    Performs image dataset pre-processing such as resizing, augmenting the dataset, etc.

    :param target_dimensions: final dimensions of training images
    :param rgb: true if images are in rgb
    :param channels: number of desired channels. if raw images are grayscale, may still want 3 channels for desired neural net input
    """
    def __init__(self, images, target_dimensions=None, augment_data=False, rgb=False, channels=3, time_series=False):
        self.images = images
        self.target_dimensions = target_dimensions
        self.augment_data = augment_data
        self.rgb = rgb
        self.channels = channels
        self.time_series = time_series

    def process_training_data(self):
        """
        :return:  list of processed image data
        """
        print('Extracting training data from csv...')
        start = datetime.datetime.now()

        images = list()
        for raw_image in self.images:
            image = raw_image
            if not self.time_series:
                image = cv2.resize(raw_image, self.target_dimensions, interpolation=cv2.INTER_LINEAR)
            if self.time_series:
                image = list()
                for slice in raw_image:
                    image.append(cv2.resize(slice, self.target_dimensions, interpolation=cv2.INTER_LINEAR))
            elif not self.rgb and self.channels==3:
                image = np.array([image, image, image]).reshape((self.target_dimensions[0], self.target_dimensions[1], 3))

            images.append(image)

        if self.augment_data:
            data_gen = ImageDataGenerator(rotation_range=180)
            data_gen.fit(images)   # TODO: functionality: send data_gen new image set to feature extractor
                                # TODO: functionality: ImDataGen input will be dependent on experimentation results for emotion subsets

        end = datetime.datetime.now()
        print('Training data extraction runtime - ' + str(end-start))

        return np.array(images)