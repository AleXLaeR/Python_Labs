from os import path
from argparse import ArgumentParser

# from mss import mss as monitor

from recognition.yolo.yolo_utils import draw_scaled_boxes
from recognition.yolo.yolo_enhancements import interpret_net_predictions, get_boxes
from recognition.yolo.constants import input_img_dims, cls_prob_thresh

import cv2
import numpy as np

from keras.models import load_model
from keras.preprocessing.image import img_to_array


arg_parser = ArgumentParser(description='ral-time test of yolo-v3 network')
arg_parser.add_argument('-f', '--file', help='path to video file')

# Load YOLO pre-trained model and MS-COCO cls labels
yolo_model = load_model(path.join('model', 'yolo-standard', 'yolo_weights.h5'))

# sct = monitor()
# monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

def process_frame(frame: np.ndarray) -> None:
    loaded_frame = img_to_array(frame).astype('float32')
    normalized_frame = np.expand_dims(loaded_frame / 255.0, axis=0)

    net_predictions = yolo_model.predict(normalized_frame)
    bounding_boxes = interpret_net_predictions(net_predictions)

    v_boxes, v_labels, v_scores = get_boxes(bounding_boxes, cls_prob_thresh)

    draw_scaled_boxes(frame, input_img_dims, v_boxes, v_labels, v_scores)
    cv2.imshow('Object Detection', frame)


def read_frames(from_path: str = None) -> None:
    capture_target = 0 if from_path is None else from_path
    video_capture = cv2.VideoCapture(capture_target)

    if not video_capture.isOpened():
        return

    is_processing_active = True
    while is_processing_active:
        is_valid_img, frame = video_capture.read()

        if not is_valid_img:
            is_processing_active = False

        resized_image = cv2.resize(frame, dsize=input_img_dims)
        process_frame(resized_image)

         # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_processing_active = False

    video_capture.release()
    cv2.destroyAllWindows()


# python ./from_image.py --file="assets/wine.mp4"
def main():
    args = arg_parser.parse_args()
    read_frames(args.file)


if __name__ == '__main__':
    main()
