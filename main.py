# Copyright (C) 2018  Artsiom Sanakoyeu and Dmytro Kotovenko
#
# This file is part of Adaptive Style Transfer
#
# Adaptive Style Transfer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Adaptive Style Transfer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import fire
import tensorflow as tf

tf.set_random_seed(228)
from model import Artgan


def main(model_name, phase='train', image_size=256 * 3, ptad='./data/vincent-van-gogh_road-with-cypresses-1890', ptcd=None, total_steps=300000,
         batch_size=1, lr=0.0002, save_freq=1000, ngf=32, ndf=64, dlw=1., tlw=100., flw=100., dsr=0.8, ii_dir=None, save_dir=None, ckpt_nmbr=None):
    """

    Args:
        model_name: ('model1') Name of the model
        phase: ('train') Specify current phase: train or inference.
        image_size (int): (256 * 3) For training phase: will crop out images of this particular size.
                                    For inference phase: each input image will have the smallest side of this size.
                                    For inference recommended size is 1280.
        ptad (str): path_to_art_dataset : Directory with paintings representing style we want to learn.
        ptcd (str): path_to_content_dataset: Path to Places365 training dataset.
        total_steps (int): (3e5) Total number of steps
        batch_size (int): (1) # images in batch
        lr (float): (0.0002) initial learning rate for adam
        save_freq (int): (1000) Save model every save_freq steps
        ngf (int): (32) Number of filters in first conv layer of generator(encoder-decoder).
        ndf (int): (64) Number of filters in first conv layer of discriminator.
        dlw (float): (1.) discr_loss_weight: Weight of discriminator loss.
        tlw (float): (100.) transformer_loss_weight: Weight of transformer loss.
        flw (float): (100.) feature_loss_weight: Weight of feature loss.
        dsr: (float): (0.8) discr_success_rate: Rate of trials that discriminator will win on average.
        ii_dir: (list): inference_images_dir: Directory with images we want to process.
        save_dir (str): Directory to save inference output images. If not specified will save in the model directory.
        ckpt_nmbr (int): Checkpoint number we want to use for inference. Might be None (unspecified), then the latest available will be used.


    Returns:

    """
    path_to_art_dataset = ptad
    path_to_content_dataset = ptcd
    discr_loss_weight = dlw
    transformer_loss_weight = tlw
    feature_loss_weight = flw
    discr_success_rate = dsr
    inference_images_dir = ii_dir

    tfconfig = tf.ConfigProto(allow_soft_placement=False)
    tfconfig.gpu_options.allow_growth = True
    with tf.Session(config=tfconfig) as sess:
        model = Artgan(sess, model_name, batch_size, image_size, total_steps, save_freq, lr, ngf, ndf, phase, path_to_content_dataset, path_to_art_dataset, discr_loss_weight,
                       transformer_loss_weight, feature_loss_weight)

        if phase == 'train':
            model.train(discr_success_rate, ckpt_nmbr=ckpt_nmbr)
        if phase == 'inference' or phase == 'test':
            print("Inference.")
            model.inference(inference_images_dir, resize_to_original=False,
                            to_save_dir=save_dir,
                            ckpt_nmbr=ckpt_nmbr)

        if phase == 'inference_on_frames' or phase == 'test_on_frames':
            print("Inference on frames sequence.")
            model.inference_video(path_to_folder=inference_images_dir[0],
                                  resize_to_original=False,
                                  to_save_dir=save_dir,
                                  ckpt_nmbr=ckpt_nmbr)
        sess.close()


if __name__ == '__main__':
    fire.Fire(main)
