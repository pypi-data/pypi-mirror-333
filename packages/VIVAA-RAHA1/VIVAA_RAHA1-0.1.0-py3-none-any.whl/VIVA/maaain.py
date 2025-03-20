import FreeSimpleGUI as sg
import cv2
import os
from datetime import datetime
import random
import shutil


# Function to resize the image maintaining aspect ratio
def resize_image(image_path, target_width, target_height):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    aspect_ratio = w / h
    if w > h:
        new_w = target_width
        new_h = int(target_width / aspect_ratio)
    else:
        new_h = target_height
        new_w = int(target_height * aspect_ratio)
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized_img

resized_image = resize_image("V:/DATASTRUCT/VIVA/assets/annotated_bgi.png", 1100, 700)
cv2.imwrite("V:/DATASTRUCT/VIVA/assets/resized_bgi.png", resized_image)

# Parent Window
background_img = "V:/DATASTRUCT/VIVA/assets/resized_bgi.png"
layout = [
    [
        sg.Column([
            [sg.Image(background_img, pad=(0, 0))],
            [sg.Text("VIVA", font=("Times New Roman", 24, "bold"), text_color='black')],
            [sg.Button("Hit to Start :)", size=(20, 1))],
            [sg.Button("Help"), sg.Button("About"), sg.Button("Exit")]
        ], element_justification='c', pad=(0, 0))
    ]
]


def create_main_window():
    return sg.Window("VIVA", layout, finalize=True)


def hit_start():
    video_image_icon = "V:/DATASTRUCT/VIVA/assets/VIDEO_PICTURE_ICON.png"
    image_transformation_icon = "V:/DATASTRUCT/VIVA/assets/IMAGE_TRANSFORMATION_ICON.png"
    annotate_icon = "V:/DATASTRUCT/VIVA/assets/ANNOTATE_ICON.png"

    layout = [
        [sg.Text("Choose an option: ", font=("Times New Roman", 20, "bold"))],
        [
            sg.Column([
                [sg.Image(video_image_icon, pad=(0, 0), size=(250, 250))],
                [sg.Button("Video to Image Converter")]
            ], element_justification='c', pad=(0, 0)),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Image(image_transformation_icon, pad=(0, 0), size=(250, 250))],
                [sg.Button("Image Transformer")]
            ], element_justification='c', pad=(0, 0)),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Image(annotate_icon, pad=(0, 0), size=(250, 250))],
                [sg.Button("Annotate Images")]
            ], element_justification='c', pad=(0, 0))
        ],
        [sg.Push(), sg.Button("Back"), sg.Push()]
    ]

    return sg.Window("Options: ", layout, finalize=True)


def Video_Image_Converter():
    layout = [
        [sg.Text("Select a video file:")],
        [sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("MP4 Files", "*.mp4"),))],
        [sg.Button("Convert"), sg.Button("Back")]
    ]
    return sg.Window("Video Image Converter", layout, finalize=True)


def Image_transformer():
    layout = [
        [sg.Text("Select a folder having Images:")],
        [sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Button("Convert"), sg.Button("Back")]
    ]
    return sg.Window("Image Transformer", layout, finalize=True)


def convert_video_to_images(video_path, output_base_dir):
    # Create a directory to save the images
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(output_base_dir, video_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Frames will be saved in: {output_dir}")  # Print the output directory path

    # Load the video
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    layout = [[sg.Text('Converting...')],
              [sg.ProgressBar(frame_count, orientation='h', size=(20, 20), key='-PROGRESS-')],
              [sg.Cancel()]]

    window = sg.Window('Progress', layout)
    progress_bar = window['-PROGRESS-']

    frame_number = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_name = os.path.join(output_dir, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_name, frame)
        frame_number += 1

        event, values = window.read(timeout=10)
        if event == 'Cancel' or event == sg.WINDOW_CLOSED:
            break
        progress_bar.update(current_count=frame_number)

    video.release()
    window.close()


def convert_images_to_grayscale(folder_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(folder_path, "grayscale", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    image_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

    layout = [[sg.Text('Converting...')],
              [sg.ProgressBar(len(image_files), orientation='h', size=(20, 20), key='-PROGRESS-')],
              [sg.Cancel()]]

    window = sg.Window('Progress', layout)
    progress_bar = window['-PROGRESS-']

    for i, image_file in enumerate(image_files):
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event == sg.WINDOW_CLOSED:
            break

        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_image_path = os.path.join(output_dir, image_file)
        cv2.imwrite(gray_image_path, gray_img)

        progress_bar.update(current_count=i + 1)

    window.close()


def annotate_images():
    layout = [
        [sg.Text("Select a folder having Images for Annotation:")],
        [sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Button("Next"), sg.Button("Back")]
    ]
    return sg.Window("Annotate Images", layout, finalize=True)


def annotation_tool(image_paths):
    image_index = 0
    annotations = []
    class_labels = []

    def redraw_box(img, ix, iy, ex, ey):
        img_copy = img.copy()
        cv2.rectangle(img_copy, (ix, iy), (ex, ey), (0, 255, 0), 2)
        return img_copy

    def load_image(index):
        img = cv2.imread(image_paths[index])
        return img, img.copy()

    ix, iy, ex, ey = -1, -1, -1, -1
    drawing = False
    img, img_copy = load_image(image_index)

    def mouse_callback(event, x, y, flags, param):
        nonlocal ix, iy, ex, ey, drawing, img_copy, img, image_index

        if event == cv2.EVENT_LBUTTONDOWN:
            ix, iy = x, y
            drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_copy = redraw_box(img, ix, iy, x, y)
                cv2.imshow("Annotation", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            ex, ey = x, y
            drawing = False
            img_copy = redraw_box(img, ix, iy, ex, ey)
            cv2.imshow("Annotation", img_copy)
            class_label = sg.popup_get_text('Enter class label:')
            if class_label:
                annotations.append((image_paths[image_index], ix, iy, ex, ey, class_label))
                if image_index < len(image_paths) - 1:
                    image_index += 1
                    img, img_copy = load_image(image_index)
                    cv2.imshow("Annotation", img_copy)
                else:
                    cv2.destroyAllWindows()

    cv2.namedWindow("Annotation")
    cv2.setMouseCallback("Annotation", mouse_callback)

    while True:
        cv2.imshow("Annotation", img_copy)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('n'):
            if image_index < len(image_paths) - 1:
                image_index += 1
                img, img_copy = load_image(image_index)
                cv2.imshow("Annotation", img_copy)
            else:
                break
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()
    return annotations


def save_annotations(annotations, format_choice, split_ratios):
    output_dir = "V:/DATASTRUCT/VIVA/annotations"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    format_dir = os.path.join(output_dir, format_choice, timestamp)
    os.makedirs(format_dir, exist_ok=True)

    total_images = len(set([ann[0] for ann in annotations]))
    train_split = int(total_images * (split_ratios[0] / 100))
    val_split = int(total_images * (split_ratios[1] / 100))
    test_split = total_images - train_split - val_split

    random.shuffle(annotations)
    train_annotations = annotations[:train_split]
    val_annotations = annotations[train_split:train_split + val_split]
    test_annotations = annotations[train_split + val_split:]

    splits = {'train': train_annotations, 'val': val_annotations, 'test': test_annotations}

    for split, anns in splits.items():
        split_dir = os.path.join(format_dir, split)
        os.makedirs(os.path.join(split_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(split_dir, 'labels'), exist_ok=True)

        for ann in anns:
            img_path, x1, y1, x2, y2, class_label = ann
            img_name = os.path.basename(img_path)
            label_name = os.path.splitext(img_name)[0] + '.txt'

            img_output_path = os.path.join(split_dir, 'images', img_name)
            label_output_path = os.path.join(split_dir, 'labels', label_name)

            shutil.copy(img_path, img_output_path)

            with open(label_output_path, 'w') as f:
                img = cv2.imread(img_path)
                x_center = (x1 + x2) / 2 / img.shape[1]
                y_center = (y1 + y2) / 2 / img.shape[0]
                width = abs(x2 - x1) / img.shape[1]
                height = abs(y2 - y1) / img.shape[0]
                f.write(f"{class_label} {x_center} {y_center} {width} {height}\n")


def annotation_format_split_window():
    layout = [
        [sg.Text("Select Annotation Format:")],
        [sg.Combo(['yolov5', 'yolov8', 'yolov10'], key="-FORMAT-")],
        [sg.Text("Enter Split Ratios (Train, Val, Test):")],
        [sg.Input(key="-TRAIN-", size=(5, 1)), sg.Text("% Train")],
        [sg.Input(key="-VAL-", size=(5, 1)), sg.Text("% Val")],
        [sg.Input(key="-TEST-", size=(5, 1)), sg.Text("% Test")],
        [sg.Button("Save"), sg.Button("Back")]
    ]
    return sg.Window("Annotation Format and Split", layout, finalize=True)


def main():
    main_window = create_main_window()
    options_window = None
    converter_window = None
    transformer_window = None
    annotator_window = None
    format_split_window = None
    annotations = None  # Initialize annotations to ensure it's defined

    while True:
        window, event, values = sg.read_all_windows()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            window.close()
            if window == main_window:
                break
            elif window == options_window:
                options_window = None
                main_window.un_hide()
            elif window == converter_window:
                converter_window = None
                options_window = hit_start()
            elif window == transformer_window:
                transformer_window = None
                options_window = hit_start()
            elif window == annotator_window:
                annotator_window = None
                options_window = hit_start()
            elif window == format_split_window:
                format_split_window = None
                options_window = hit_start()
        elif event == "Hit to Start :)":
            if options_window is None:
                main_window.hide()
                options_window = hit_start()
        elif event == "Help":
            pass
        elif event == "About":
            pass
        elif event == "Back":
            window.close()
            if window == options_window:
                options_window = None
                main_window.un_hide()
            elif window == converter_window:
                converter_window = None
                options_window = hit_start()
            elif window == transformer_window:
                transformer_window = None
                options_window = hit_start()
            elif window == annotator_window:
                annotator_window = None
                options_window = hit_start()
            elif window == format_split_window:
                format_split_window = None
                options_window = hit_start()
        elif event == "Video to Image Converter":
            options_window.close()
            converter_window = Video_Image_Converter()
        elif event == "Image Transformer":
            options_window.close()
            transformer_window = Image_transformer()
        elif event == "Annotate Images":
            options_window.close()
            annotator_window = annotate_images()
        elif event == "Convert" and window == converter_window:
            video_path = values["-FILE-"]
            if not video_path.endswith(".mp4"):
                sg.popup("Wrong formatted video was selected")
            else:
                output_dir = "V:/DATASTRUCT/VIVA/frames"
                convert_video_to_images(video_path, output_dir)
                sg.popup("Video converted to images successfully")
        elif event == "Convert" and window == transformer_window:
            folder_path = values["-FOLDER-"]
            if not folder_path:
                sg.popup("Please select a folder")
            else:
                convert_images_to_grayscale(folder_path)
                sg.popup("Images converted to grayscale successfully")
        elif event == "Next" and window == annotator_window:
            folder_path = values["-FOLDER-"]
            if not folder_path:
                sg.popup("Please select a folder")
            else:
                image_extensions = ('.jpg', '.jpeg', '.png')
                image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
                if not image_paths:
                    sg.popup("No images found in the selected folder")
                else:
                    annotator_window.close()
                    annotations = annotation_tool(image_paths)
                    format_split_window = annotation_format_split_window()
        elif event == "Save" and window == format_split_window:
            if annotations:
                format_choice = values["-FORMAT-"]
                train_ratio = int(values["-TRAIN-"])
                val_ratio = int(values["-VAL-"])
                test_ratio = int(values["-TEST-"])
                if not format_choice or train_ratio + val_ratio + test_ratio != 100:
                    sg.popup("Please select a format and ensure the split ratios add up to 100")
                else:
                    save_annotations(annotations, format_choice, (train_ratio, val_ratio, test_ratio))
                    sg.popup("Annotations saved successfully")
                    format_split_window.close()
                    options_window = hit_start()

    main_window.close()


if __name__ == "__main__":
    main()