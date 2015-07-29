import sys
import os
import numpy as np

caffe_root = '/opt/caffe/'
print caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe


def binary_prob_to_npy(path, W, H, C):
    a = caffe.io.caffe_pb2.BlobProto()
    in_file = open(path, 'rb')
    data = in_file.read()
    a.ParseFromString(data)
    means = a.data
    means = np.asarray(means)
    means = means.reshape(C, W, H)
    return means


def load_model():
    caffe.set_mode_cpu()

    mean = binary_prob_to_npy(caffe_root + 'models/web/food101_mean.binaryproto', 256, 256, 3)
    net = caffe.Classifier(caffe_root + 'models/web/g101.prototxt',
                           caffe_root + 'models/web/g101_ft.caffemodel',
                           mean=mean.mean(1).mean(1),
                           channel_swap=(2, 1, 0),
                           raw_scale=255,
                           image_dims=(256, 256))

    return net


def get_labels():
    labels = []
    f = open(caffe_root + 'models/web/labels.txt')
    for line in f:
        label = line
        labels.append(label)

    return labels


def get_predict_labels(img_url, classifier, labels_all):
    labels = []
    scores = classifier.predict([caffe.io.load_image(img_url)], oversample=False)
    label_index = scores.argsort()[:, ::-1][:, :10]
    label_index = label_index.reshape(-1)
    scores = scores.reshape(-1)
    for index in label_index:
        labels.append((labels_all[index][:-1], round(100*scores[index], 2)))
    return labels


if __name__ == "__main__":
    la = get_labels()
    classifier = load_model()
    l = get_predict_labels('../apple_pie.jpg', classifier, la)
    print l
    for k in l:
        print k[0], k[1]
