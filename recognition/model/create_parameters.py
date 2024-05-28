from argparse import ArgumentParser
from os import path

arg_parser = ArgumentParser()
arg_parser.add_argument('-cf', '--class-file', help='relative path to a created classes file')
arg_parser.add_argument('-af', '--anchor-file', help='relative path to a created anchors file')

class_labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
                "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
                "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
                "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
                "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
                "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                "scissors", "teddy bear", "hair drier", "toothbrush"]

default_anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]

def write_class_labels(to_file: str) -> None:
    with open(to_file, 'w+') as desc:
        for label in class_labels:
            desc.write(f'{label}\n')

def write_anchors(to_file: str) -> None:
    with open(to_file, 'w+') as desc:
        for anchor in default_anchors:
            for item in anchor:
                desc.write(f'{item} ')
            desc.write('\n')


def does_dir_exist(file_path: str) -> bool:
    return path.exists(file_path) and path.isfile(file_path)


def main():
    args = arg_parser.parse_args()
    class_file, anchor_file = args.class_file, args.anchor_file

    if not class_file:
        class_file = 'classes.txt'
    if not anchor_file:
        anchor_file = 'anchors.txt'

    if does_dir_exist(class_file) or does_dir_exist(anchor_file):
        return

    write_class_labels(class_file)
    write_anchors(anchor_file)

if __name__ == '__main__':
    main()
