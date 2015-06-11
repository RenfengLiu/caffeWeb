
import sys
import os
import numpy as np
# import matplotlib.pyplot as plt
# import h5py

caffe_root = os.path.join(os.path.dirname(__file__), '../../../caffe/')  
print caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe


def BinaryProbToNPY(path, W, H, C):
    a = caffe.io.caffe_pb2.BlobProto()
    in_file = open(path, 'rb')
    data = in_file.read()
    a.ParseFromString(data)
    means = a.data
    means = np.asarray(means)
    means = means.reshape(C, W, H)
    return means


def load_model():
    global caffe_root

    caffe.set_phase_test()
    caffe.set_mode_cpu()

    # Make sure that caffe is on the python path:
    net = caffe.Classifier(caffe_root + 'models/food101/deploy.prototxt',
                           caffe_root + 'models/food101/bvlc_googlenet_iter_560000.caffemodel')

    mean = BinaryProbToNPY(caffe_root + 'models/food101/food_mean.binaryproto', 256, 256, 3)
    net.set_mean('data', mean)  # ImageNet mean
    net.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    net.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    # net.set_phase_test()
    # net.set_mode_cpu()
    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    '''
    f = h5py.File('image_mean.mat')
    mean = f['image_mean']
    mean = np.asarray(mean)
    print mean.shape[2:]
    net.set_mean('data', mean)  # ImageNet mean
    net.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    net.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    '''

    # net.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'))  # ImageNet mean
    # net.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    # net.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    # print net
    return net


def get_labels():
    labels = []
    f = open(caffe_root + 'models/labels.txt')
    i = 0
    for line in f:
        # print line
        lable = line
        labels.append(lable)

    return labels


def get_predict_labels(img_url, classifier, labels_all):
    labels = []
    scores = classifier.predict([caffe.io.load_image(img_url)],oversample = False)
    label_index = scores.argsort()[:,::-1][:,:5]
    # print label_index
    label_index = label_index.reshape(-1)
    # print scores.shape
    scores = scores.reshape(-1)
    for index in label_index:
        # print index, labels_all[index][:-2], scores[index]
        labels.append((labels_all[index][:-2], round(100*scores[index], 2)))
    return labels


# if __name__=="__main__":
# 	la = get_labels()
# 	classifier = load_model()
# 	l = get_predict_labels('/opt/GlucoGuide/user_photo/1/meal_20141126_042204.jpg', classifier, la)
# 	print l
# 	for k in l:
# 		print k[0], k[1]
# 	# get_labels()

