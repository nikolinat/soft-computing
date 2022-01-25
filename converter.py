INPUT_FILE_PATH = "data/data.csv"
OUTPUT_FILE_PATH = "data/yolo.csv"
IMAGE_ROOT_DIR = "/content/TrainYourOwnYOLO/Data/Source_Images/images/"

dictionary = {'As': 0, 'Ap': 1, 'At': 2, 'Ak': 3, '2s': 4, '2p': 5, '2t': 6, '2k': 7, '3s': 8, '3p': 9, '3t': 10,
              '3k': 11, '4s': 12, '4p': 13, '4t': 14, '4k': 15, '5s': 16, '5p': 17, '5t': 18, '5k': 19, '6s': 20,
              '6p': 21,
              '6t': 22, '6k': 23, '7s': 24,
              '7p': 25, '7t': 26, '7k': 27, '8s': 28, '8p': 29, '8t': 30, '8k': 31, '9s': 32, '9p': 33,
              '9t': 34, '9k': 35,
              '10s': 36, '10p': 37, '10t': 38, '10k': 39, 'Js': 40, 'Jp': 41, 'Jt': 42, 'Jk': 43, 'Qs': 44, 'Qp': 45,
              'Qt': 46, 'Qk': 47,
              'Ks': 48, 'Kp': 49, 'Kt': 50, 'Kk': 51}

numbers = {}


def google_sheet_csv_to_yolo_csv(input_file_path=INPUT_FILE_PATH, output_file_path=OUTPUT_FILE_PATH,
                                 image_root_dir=IMAGE_ROOT_DIR):
    with open(input_file_path, 'r') as input_file_stream:
        lines = input_file_stream.readlines()

    with open(output_file_path, 'w') as output_file_stream:
        for line in lines:
            values, numbers = google_sheet_csv_line_to_yolo_values(line)
            image, rest = values[0] + '.jpg', values[1:]

            output_file_stream.write(image_root_dir + image + ' ')

            num_of_bounding_boxes = int(len(rest) / 5)
            for i in range(num_of_bounding_boxes):
                output_file_stream.write(','.join(rest[i * 5: i * 5 + 5]))
                if i < num_of_bounding_boxes - 1:
                    output_file_stream.write(" ")

            output_file_stream.write('\n')


def google_sheet_csv_line_to_yolo_values(line):
    values = line.replace(',', ' ').replace('"', '').strip().split(' ')

    if len(values) % 5 != 1:  # one because of image on 0.
        print('Not enough values on line:', line)

    for i in range(1, len(values)):
        if i % 5 in [3, 4]:  # adding top_x + width / top_y + height
            values[i] = str(int(values[i - 2]) + int(values[i]))
        if i % 5 == 0:
            if values[i] in numbers.keys():
                numbers[values[i]] = numbers[values[i]] + 1
            else:
                numbers[values[i]] = 1
            values[i] = str(dictionary.get(values[i]))

    return values, numbers


google_sheet_csv_to_yolo_csv()