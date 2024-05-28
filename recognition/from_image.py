from os import path
from argparse import ArgumentParser

from recognition.yolo.yolo_utils import draw_scaled_boxes
from recognition.yolo.yolo_enhancements import interpret_net_predictions, get_boxes
from recognition.yolo.constants import input_img_dims, cls_prob_thresh

import cv2
import numpy as np

from keras.models import load_model
from keras.preprocessing.image import img_to_array

arg_parser = ArgumentParser(description='ral-time test of yolo-v3 network')
arg_parser.add_argument('-i', '--input', help='path to input image')
arg_parser.add_argument('-o', '--output', help='path to resulting image')

# Load YOLO pre-trained model and MS-COCO cls labels
yolo_model = load_model(path.join('model', 'yolo-standard', 'yolo_weights.h5'))


def process_frame(frame: np.ndarray, to_path: str) -> None:
    # Preprocess the frame
    loaded_frame = img_to_array(frame).astype('float32')
    normalized_frame = np.expand_dims(loaded_frame / 255.0, axis=0)

    net_predictions = yolo_model.predict(normalized_frame)
    bounding_boxes = interpret_net_predictions(net_predictions)

    v_boxes, v_labels, v_scores = get_boxes(bounding_boxes, cls_prob_thresh)

    # draw_boxes(frame, v_boxes, v_labels, 0.6)
    draw_scaled_boxes(frame, input_img_dims, v_boxes, v_labels, v_scores)
    cv2.imwrite(to_path, frame)


def read_frames(from_path: str, to_path: str) -> None:
    initial_frame = cv2.imread(from_path)
    resized_image = cv2.resize(initial_frame, dsize=input_img_dims)

    process_frame(resized_image, to_path)


# python ./from_image.py -i="assets/wine.jpg" -o="result_prediction.jpg"
def main():
    args = arg_parser.parse_args()
    read_frames(args.input, args.output)


if __name__ == '__main__':
    main()
