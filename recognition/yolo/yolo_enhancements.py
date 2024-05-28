from os import path
from .yolo_utils import BoundBox, decode_netout, correct_yolo_boxes
from recognition.model.read_parameters import read_classes, read_anchors
from .constants import *

import tensorflow as tf
from numpy import array

class_labels = read_classes(path.join('./model', 'yolo-standard', 'classes.txt'))
anchors = read_anchors(path.join('./model', 'yolo-standard', 'anchors.txt'))

# get all the results above a threshold
def get_boxes(boxes, thresh: float) -> tuple[list[BoundBox], list[str], list[float]]:
    v_boxes, v_labels, v_scores = [], [], []

    # enumerate all boxes
    for box in boxes:
        # enumerate all possible labels
        for i in range(len(class_labels)):
            # check if the threshold for this label is high enough
            if box.classes[i] <=thresh:
                continue

            v_boxes.append(box)
            v_labels.append(class_labels[i])
            v_scores.append(box.classes[i] * 100)

    # don't break, many labels may trigger for one box
    return v_boxes, v_labels, v_scores


def perform_nms(b_boxes: list[BoundBox]) -> list[BoundBox]:
    # Suppress non-maximal boxes
    b_boxes_np = array([[bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax, bbox.get_score()] for bbox in b_boxes])

    # Perform non-max suppression using tf.image.non_max_suppression
    selected_indices = tf.image.non_max_suppression(b_boxes_np[:, :4], b_boxes_np[:, 4], max_output_size=50,
                                                    iou_threshold=nms_threshold)

    # Filter out boxes using selected indices
    selected_boxes = [b_boxes[i] for i in selected_indices.numpy()]
    return selected_boxes

def interpret_net_predictions(pred_boxes: list[BoundBox]):
    b_boxes: list[BoundBox] = []
    for i, encoded_pred in enumerate(pred_boxes):
        # decode the output of the CNN
        b_boxes += decode_netout(encoded_pred[0], anchors[i], cls_prob_thresh, *input_img_dims)

    # correct the sizes of the bounding boxes for the shape of the image
    correct_yolo_boxes(b_boxes, *input_img_dims, *input_img_dims)

    # return do_nms(b_boxes, nms_threshold)
    return b_boxes if len(b_boxes) == 0 else perform_nms(b_boxes)