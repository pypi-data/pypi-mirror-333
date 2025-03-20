import FreeSimpleGUI as sg
import cv2
import gui
import os

# Function to resize the image maintaining aspect ratio
resized_image = gui.resize_image("V:/DATASTRUCT/VIVA/assets/annotated_bgi.png", 1100, 700)
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
                options_window = gui.hit_start()
            elif window == transformer_window:
                transformer_window = None
                options_window = gui.hit_start()
            elif window == annotator_window:
                annotator_window = None
                options_window = gui.hit_start()
            elif window == format_split_window:
                format_split_window = None
                options_window = gui.hit_start()
        elif event == "Hit to Start :)":
            if options_window is None:
                main_window.hide()
                options_window = gui.hit_start()
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
                options_window = gui.hit_start()
            elif window == transformer_window:
                transformer_window = None
                options_window = gui.hit_start()
            elif window == annotator_window:
                annotator_window = None
                options_window = gui.hit_start()
            elif window == format_split_window:
                format_split_window = None
                options_window = gui.hit_start()
        elif event == "Video to Image Converter":
            options_window.close()
            converter_window = gui.Video_Image_Converter()
        elif event == "Image Transformer":
            options_window.close()
            transformer_window = gui.Image_transformer()
        elif event == "Annotate Images":
            options_window.close()
            annotator_window = gui.annotate_images()
        elif event == "Convert" and window == converter_window:
            video_path = values["-FILE-"]
            if not video_path.endswith(".mp4"):
                sg.popup("Wrong formatted video was selected")
            else:
                output_dir = "V:/DATASTRUCT/VIVA/frames"
                gui.convert_video_to_images(video_path, output_dir)
                sg.popup("Video converted to images successfully")
        elif event == "Convert" and window == transformer_window:
            folder_path = values["-FOLDER-"]
            if not folder_path:
                sg.popup("Please select a folder")
            else:
                gui.convert_images_to_grayscale(folder_path)
                sg.popup("Images converted to grayscale successfully")
        elif event == "Next" and window == annotator_window:
            folder_path = values["-FOLDER-"]
            if not folder_path:
                sg.popup("Please select a folder")
            else:
                image_extensions = ('.jpg', '.jpeg', '.png')
                image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                               f.lower().endswith(image_extensions)]
                if not image_paths:
                    sg.popup("No images found in the selected folder")
                else:
                    annotator_window.close()
                    annotations = gui.annotation_tool(image_paths)
                    format_split_window = gui.annotation_format_split_window()
        elif event == "Save" and window == format_split_window:
            if annotations:
                format_choice = values["-FORMAT-"]
                train_ratio = int(values["-TRAIN-"])
                val_ratio = int(values["-VAL-"])
                test_ratio = int(values["-TEST-"])
                if not format_choice or train_ratio + val_ratio + test_ratio != 100:
                    sg.popup("Please select a format and ensure the split ratios add up to 100")
                else:
                    gui.save_annotations(annotations, format_choice, (train_ratio, val_ratio, test_ratio))
                    sg.popup("Annotations saved successfully")
                    format_split_window.close()
                    options_window = gui.hit_start()

    main_window.close()


if __name__ == "__main__":
    main()
