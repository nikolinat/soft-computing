import argparse
import os
import sys
from timeit import default_timer as timer

import numpy as np
import pandas as pd

from Utils.Get_File_Paths import GetFileList
from Utils.Train_Utils import get_anchors
from Utils.utils import detect_object
from yolo import YOLO, detect_video, detect_webcam

data = {}
test_results = {}


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


def read_data():
    with open("data/yolo.csv", 'r') as input_file_stream:
        lines = input_file_stream.readlines()

        for line in lines:
            image_name, boxes = read_line(line)
            data[image_name] = boxes
        return data


def read_line(line):
    values = line.replace('\n', '').split(' ')
    image_name = values[0].split('/')[-1]
    boxes = []
    for i in range(1, len(values)):
        all_boxes = values[i].split(',')
        box = [int(all_boxes[0]), int(all_boxes[1]), int(all_boxes[2]), int(all_boxes[3]), int(all_boxes[4])]
        boxes.append(box)

    return image_name, boxes


def find():
    read_data()

    true_positive = 0
    false_negative = 0
    false_positive = 0

    actual_counter = 0
    for actual_image, actual_boxes in data.items():
        for predicted_image, predicted_boxes in test_results.items():
            if actual_image == predicted_image:
                actual_counter += len(actual_boxes)
                already_added = []
                for predicted_box in predicted_boxes:
                    for actual_box in actual_boxes:
                        if actual_box not in already_added:
                            iou = calculate_iou(actual_box, predicted_box)
                            if iou > 0.5:
                                if predicted_box[4] == actual_box[4]:
                                    true_positive += 1
                                    already_added.append(actual_box)
                                else:
                                    false_positive += 1
                        else:
                            continue
    false_negative = actual_counter - true_positive
    return true_positive, false_positive, false_negative


def calculate_accuracy():

    true_positive, false_positive, false_negative = find()

    accuracy = true_positive / (true_positive + false_positive + false_negative)
    print("Accuracy: ", accuracy * 100)


def calculate_iou(actual_box, predicted_box):
    y_a = max(actual_box[0], predicted_box[0])
    x_a = max(actual_box[1], predicted_box[1])
    y_b = min(actual_box[2], predicted_box[2])
    x_b = min(actual_box[3], predicted_box[3])

    inter_area = max(0, x_b - x_a + 1) * max(0, y_b - y_a + 1)

    true_area = (actual_box[3] - actual_box[1] + 1) * (actual_box[2] - actual_box[0] + 1)

    pred_area = (predicted_box[3] - predicted_box[1] + 1) * (predicted_box[2] - predicted_box[0] + 1)

    iou = inter_area / float(true_area + pred_area - inter_area)

    return max(iou, 0)


src_path = os.path.join(get_parent_dir(1), "yolo")
utils_path = os.path.join(get_parent_dir(1), "Utils")

sys.path.append(src_path)
sys.path.append(utils_path)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Set up folder names for default values
data_folder = os.path.join(get_parent_dir(n=1), "yolo")

image_folder = os.path.join(data_folder, "data")

image_test_folder = os.path.join(image_folder, "test")

detection_results_folder = os.path.join(image_folder, "test_results")
detection_results_file = os.path.join(detection_results_folder, "results.csv")

model_folder = os.path.join(data_folder, "model_data")

model_weights = os.path.join(model_folder, "trained_weights_final.h5")
model_classes = os.path.join(model_folder, "data_classes.txt")

anchors_path = os.path.join(src_path, "model_data", "yolo_anchors.txt")

FLAGS = None

if __name__ == "__main__":
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """

    parser.add_argument(
        "--input_path",
        type=str,
        default=image_test_folder,
        help="Path to image/video directory. All subdirectories will be included. Default is "
             + image_test_folder,
    )

    parser.add_argument(
        "--output",
        type=str,
        default=detection_results_folder,
        help="Output path for detection results. Default is "
             + detection_results_folder,
    )

    parser.add_argument(
        "--no_save_img",
        default=False,
        action="store_true",
        help="Only save bounding box coordinates but do not save output images with annotated boxes. Default is False.",
    )

    parser.add_argument(
        "--file_types",
        "--names-list",
        nargs="*",
        default=[],
        help="Specify list of file types to include. Default is --file_types .jpg .jpeg .png .mp4",
    )

    parser.add_argument(
        "--yolo_model",
        type=str,
        dest="model_path",
        default=model_weights,
        help="Path to pre-trained weight files. Default is " + model_weights,
    )

    parser.add_argument(
        "--anchors",
        type=str,
        dest="anchors_path",
        default=anchors_path,
        help="Path to YOLO anchors. Default is " + anchors_path,
    )

    parser.add_argument(
        "--classes",
        type=str,
        dest="classes_path",
        default=model_classes,
        help="Path to YOLO class specifications. Default is " + model_classes,
    )

    parser.add_argument(
        "--gpu_num", type=int, default=1, help="Number of GPU to use. Default is 1"
    )

    parser.add_argument(
        "--confidence",
        type=float,
        dest="score",
        default=0.25,
        help="Threshold for YOLO object confidence score to show predictions. Default is 0.25.",
    )

    parser.add_argument(
        "--box_file",
        type=str,
        dest="box",
        default=detection_results_file,
        help="File to save bounding box results to. Default is "
             + detection_results_file,
    )

    parser.add_argument(
        "--postfix",
        type=str,
        dest="postfix",
        default="_bb",
        help='Specify the postfix for images with bounding boxes. Default is "_bb"',
    )

    parser.add_argument(
        "--is_tiny",
        default=False,
        action="store_true",
        help="Use the tiny Yolo version for better performance and less accuracy. Default is False.",
    )

    parser.add_argument(
        "--webcam",
        default=False,
        action="store_true",
        help="Use webcam for real-time detection. Default is False.",
    )

    FLAGS = parser.parse_args()

    save_img = not FLAGS.no_save_img

    file_types = FLAGS.file_types

    webcam_active = FLAGS.webcam

    if file_types:
        input_paths = GetFileList(FLAGS.input_path, endings=file_types)
    else:
        input_paths = GetFileList(FLAGS.input_path)

    # Split images and videos
    img_endings = (".jpg", ".jpeg", ".png")
    vid_endings = (".mp4", ".mpeg", ".mpg", ".avi")

    input_image_paths = []
    input_video_paths = []
    for item in input_paths:
        if item.endswith(img_endings):
            input_image_paths.append(item)
        elif item.endswith(vid_endings):
            input_video_paths.append(item)

    output_path = FLAGS.output
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if FLAGS.is_tiny and FLAGS.anchors_path == anchors_path:
        anchors_path = os.path.join(
            os.path.dirname(FLAGS.anchors_path), "yolo-tiny_anchors.txt"
        )

    anchors = get_anchors(anchors_path)
    # define YOLO detector
    yolo = YOLO(
        **{
            "model_path": FLAGS.model_path,
            "anchors_path": anchors_path,
            "classes_path": FLAGS.classes_path,
            "score": FLAGS.score,
            "gpu_num": FLAGS.gpu_num,
            "model_image_size": (416, 416),
        }
    )

    # Make a dataframe for the prediction outputs
    out_df = pd.DataFrame(
        columns=[
            "image",
            "image_path",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "label",
            "confidence",
            "x_size",
            "y_size",
        ]
    )

    # labels to draw on images
    class_file = open(FLAGS.classes_path, "r")
    input_labels = [line.rstrip("\n") for line in class_file.readlines()]
    print("Found {} input labels: {} ...".format(len(input_labels), input_labels))

    if input_image_paths and not webcam_active:
        print(
            "Found {} input images: {} ...".format(
                len(input_image_paths),
                [os.path.basename(f) for f in input_image_paths[:5]],
            )
        )
        start = timer()

        # This is for images
        for i, img_path in enumerate(input_image_paths):
            head, tail = os.path.split(img_path)
            print(tail)
            print("-------------------------------------------------")
            prediction, image = detect_object(
                yolo,
                img_path,
                save_img=save_img,
                save_img_path=FLAGS.output,
                postfix=FLAGS.postfix,
            )
            y_size, x_size, _ = np.array(image).shape
            for single_prediction in prediction:
                out_df = out_df.append(
                    pd.DataFrame(
                        [
                            [
                                os.path.basename(img_path.rstrip("\n")),
                                img_path.rstrip("\n"),
                            ]
                            + single_prediction
                            + [x_size, y_size]
                        ],
                        columns=[
                            "image",
                            "image_path",
                            "xmin",
                            "ymin",
                            "xmax",
                            "ymax",
                            "label",
                            "confidence",
                            "x_size",
                            "y_size",
                        ],
                    )
                )

            if tail in test_results.keys():
                test_results[tail].append(prediction)
            else:
                test_results[tail] = prediction
        calculate_accuracy()
        end = timer()
        print(
            "Processed {} images in {:.1f}sec - {:.1f}FPS".format(
                len(input_image_paths),
                end - start,
                len(input_image_paths) / (end - start),
            )
        )
        out_df.to_csv(FLAGS.box, index=False)

    # This is for videos
    # for pre-recorded videos present in the Test_Images folder
    if input_video_paths and not webcam_active:
        print(
            "Found {} input videos: {} ...".format(
                len(input_video_paths),
                [os.path.basename(f) for f in input_video_paths[:5]],
            )
        )
        start = timer()
        for i, vid_path in enumerate(input_video_paths):
            output_path = os.path.join(
                FLAGS.output,
                os.path.basename(vid_path).replace(".", FLAGS.postfix + "."),
            )
            detect_video(yolo, vid_path, output_path=output_path)

        end = timer()
        print(
            "Processed {} videos in {:.1f}sec".format(
                len(input_video_paths), end - start
            )
        )
    # for Webcam
    if webcam_active:
        start = timer()
        detect_webcam(yolo)
        end = timer()
        print("Processed from webcam for {:.1f}sec".format(end - start))

    # Close the current yolo session
    yolo.close_session()
