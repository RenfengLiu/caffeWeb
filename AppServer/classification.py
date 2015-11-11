import sys
import numpy as np

CAFFE_ROOT = '/opt/caffe/'
MEAN_FILE = 'models/FoodNov9/food_mean.binaryproto'
DEPLOY_FILE = 'models/FoodNov9/deploy.prototxt'
MODEL_FILE = 'models/FoodNov9/googlenet_quick_iter_40000.caffemodel'
LABEL_FILE = 'models/FoodNov9/label.txt'
RETURN_TOP_N = 10
sys.path.insert(0, CAFFE_ROOT + 'python')
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

    mean = binary_prob_to_npy(CAFFE_ROOT + MEAN_FILE, 256, 256, 3)
    net = caffe.Classifier(CAFFE_ROOT + DEPLOY_FILE,
                           CAFFE_ROOT + MODEL_FILE,
                           mean=mean.mean(1).mean(1),
                           channel_swap=(2, 1, 0),
                           raw_scale=255,
                           image_dims=(256, 256))

    return net


def get_labels():
    labels = []
    f = open(CAFFE_ROOT + LABEL_FILE)
    for line in f:
        label = line
        labels.append(label)

    return labels


def get_predict_labels(img_url, trained_classifier, labels_all):
    labels = []
    scores = trained_classifier.predict([caffe.io.load_image(img_url)], oversample=False)
    label_index = scores.argsort()[:, ::-1][:, :RETURN_TOP_N]
    label_index = label_index.reshape(-1)
    scores = scores.reshape(-1)
    for index in label_index:
        labels.append((labels_all[index][:-1], round(scores[index], 4)))
    return labels


if __name__ == "__main__":
    la = get_labels()
    classifier = load_model()
    l = get_predict_labels('../apple_pie.jpg', classifier, la)
    print l
    for k in l:
        print k[0], k[1]
