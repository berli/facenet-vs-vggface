"""Performs face alignment and calculates L2 distance between the embeddings of images."""

# MIT License
# 
# Copyright (c) 2016 David Sandberg
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import copy
import argparse
import facenet
import align.detect_face
import shutil

no_face = ''

def main(args):

    with tf.Graph().as_default():

        with tf.Session() as sess:
      
            # Load the model
            facenet.load_model(args.model)

            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            threshold = 1.0
            path = args.image_files_path[:args.image_files_path.rfind('/')]
            global no_face 
            no_face = path+'/not_face/'
            print('no_face path:', no_face)
            if( not os.path.exists(no_face)):
                os.mkdir(no_face)
            flog = open('compare.log', 'a+')
            for image_file in os.listdir(args.image_files_path):
                image = args.image_files_path + '/'+image_file
                if os.path.isdir(image):
                    continue;
                images = load_and_align_data(args.target_files, image, args.image_size, args.margin, args.gpu_memory_fraction)
                # Run forward pass to calculate embeddings
                feed_dict = { images_placeholder: images, phase_train_placeholder:False }
                emb = sess.run(embeddings, feed_dict=feed_dict)
                
                nrof_images = len(images)

                # Print distance matrix
                print('Distance matrix')
                if( len(images) < 2):
                    continue
                
                min_dist = 2.001
                for i in range(1, nrof_images):
                    dist = np.sqrt(np.sum(np.square(np.subtract(emb[0,:], emb[1,:]))))
                    print('dist:', dist)
                    if( dist < min_dist):
                        min_dist = dist
                if(min_dist > threshold and args.is_move ):
                    shutil.move(image, no_face+'/'+image_file)
                    flog.write(image_file + ' dist: ' + str(dist) +'\n')
                    flog.flush()
            
def load_and_align_data(image_paths, image_file, image_size, margin, gpu_memory_fraction):

    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor
    
    print('Creating networks and loading parameters')
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
  
    tmp_image_paths=copy.copy(image_paths)
    tmp_image_paths.append(image_file)
    print('image_file:',image_file)
    print('tmp_image_paths:',tmp_image_paths)
    img_list = []
    for image in tmp_image_paths:
        img = misc.imread(os.path.expanduser(image), mode='RGB')
        img_size = np.asarray(img.shape)[0:2]
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        if len(bounding_boxes) < 1:
          print("can't detect face, move ", image)
          shutil.move(image, no_face + image_file[image_file.rfind('/'):])
          continue
        det = np.squeeze(bounding_boxes[0,0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        img_list.append(prewhitened)
    images = np.stack(img_list)
    return images

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('model', type=str, 
        help='Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('target_files', type=str, nargs='+', help='target to compare')
    #parser.add_argument('image_files', type=str,  nargs='+', help='target to compare')
    parser.add_argument('image_files_path', type=str, help='search path to compare')
    parser.add_argument('--is_move', type=int,
        help='move the image to no_face', default=1)
    parser.add_argument('--image_size', type=int,
        help='Image size (height, width) in pixels.', default=160)
    parser.add_argument('--margin', type=int,
        help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    parser.add_argument('--gpu_memory_fraction', type=float,
        help='Upper bound on the amount of GPU memory that will be used by the process.', default=1.0)
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
