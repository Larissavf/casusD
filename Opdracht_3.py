import os
from PIL import Image
import random
import shutil

mypath = "C:/Users/btnap/Documents/School/Thema_10"
os.chdir(mypath)

def create_dataset_structure(base_path):
    """
    Creates the specified dataset directory structure, starting with the dataset directory.

    Args:
        base_path (str): The root path where the dataset directory will be created.
    """
    dataset_path = os.path.join(base_path, "dataset")
    shutil.rmtree(f'{base_path}/dataset', ignore_errors=True)
    os.makedirs(dataset_path, exist_ok=True)

    paths = [
        "images/train",
        "images/val",
        "labels/train",
        "labels/val"
    ]

    for sub_path in paths:
        dir_path = os.path.join(dataset_path, sub_path)
        os.makedirs(dir_path, exist_ok=True)

def normalize_coordinates(xmin, ymin, xmax, ymax, w, h):
    """
    Normalize the bounding box coordinates according to YOLO format.
    """
    x_center = (xmin + xmax) / 2 / w
    y_center = (ymin + ymax) / 2 / h
    width = (xmax - xmin) / w
    height = (ymax - ymin) / h
    return x_center, y_center, width, height

def process_annotations(coords_file, images_folder, output_folder):
    """
    Process annotations from a text file and convert them to YOLO format.

    coords_file: Path to the coordinates file (coords-idc.txt).
    images_folder: Folder containing the images.
    output_folder: Folder to store the YOLO annotation files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(coords_file, 'r') as f:
        lines = f.readlines()

    # Group the annotations by patient ID (image file name)
    annotations = {}
    for line in lines:
        patient_id, xmin, ymin, xmax, ymax = map(int, line.strip().split(','))
        image_name = f"{patient_id}.jpeg"  # Assuming .jpeg, adjust as needed

        if image_name not in annotations:
            annotations[image_name] = []

        annotations[image_name].append((xmin, ymin, xmax, ymax))

    # Process each image
    for image_name, bboxes in annotations.items():
        # Open the image to get its dimensions
        image_path = os.path.join(images_folder, image_name)

        try:
            with Image.open(image_path) as img:
                w, h = img.size  # Image width and height
        except FileNotFoundError:
            print(f"Warning: Image {image_name} not found in the folder {images_folder}. Skipping.")
            continue

        # Prepare the annotation text file for this image
        annotation_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}.txt")

        with open(annotation_file, 'w') as annotation_f:
            for xmin, ymin, xmax, ymax in bboxes:
                # Normalize bounding box coordinates to YOLO format
                x_center, y_center, width, height = normalize_coordinates(xmin, ymin, xmax, ymax, w, h)

                # Write the normalized values to the text file (class is 0 for simplicity)
                annotation_f.write(f"0 {x_center} {y_center} {width} {height}\n")

        print(f"Processed {image_name} -> {annotation_file}")

def coords_list_maker(coords_file):
    coords_list = []
    with open(coords_file, 'r') as f:
        for line in f:
            coords_list.append(line.strip().split(','))
    return coords_list

def pick_random_files(directory, num_files):
    """
    Picks random files from the specified directory.

    directory: Path to the directory where files are located.
    num_files: Number of random files to pick.

    Returns a list of random file paths.
    """
    # List all files in the directory
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Ensure the number of files requested is not greater than the available files
    num_files = min(num_files, len(all_files))

    # Pick random files
    random_files = random.sample(all_files, num_files)

    # Return the full paths of the selected files
    return [os.path.join(directory, file) for file in random_files]

def trainingdata_chooser(mypath):
    #select text files
    training_list = []
    validation_list = []
    path = f'{mypath}/annotations/'
    picked_training_files = pick_random_files(path, 150)
    picked_validation_files = pick_random_files(path, 50)
    for file in picked_training_files:
        training_list.append(f'{mypath}/complete_images/{file.split("/")[-1].strip(".txt")}.jpeg')
        shutil.copy(file, f"{mypath}/dataset/labels/train")
    for file in picked_validation_files:
        validation_list.append(f'{mypath}/complete_images/{file.split("/")[-1].strip(".txt")}.jpeg')
        shutil.copy(file, f"{mypath}/dataset/labels/val")

    return training_list, validation_list


def img_copy(mypath, img_list, good_dir):
    for file in img_list:
        try:
            # Check if the file exists before copying
            if os.path.isfile(file):
                # Get the destination path for the file
                destination = os.path.join(f"{mypath}/dataset/images/{good_dir}", os.path.basename(file))
                # Copy the file to the destination directory
                shutil.copy(file, destination)
                print(f"Copied {file} to {destination}")
            else:
                print(f"File {file} does not exist, skipping.")
        except Exception as e:
            print(f"Error copying {file}: {e}")



# Example usage:
coords_file = 'coords-idc.txt'  # Path to your coordinates file
images_folder = 'complete_images/'  # Folder containing your images (adjust as needed)
output_folder = 'annotations/'  # Folder to store the YOLO annotation files

create_dataset_structure(mypath)
process_annotations(coords_file, images_folder, output_folder)
training_list, validation_list = trainingdata_chooser(mypath)
img_copy(mypath, training_list, good_dir="train")
img_copy(mypath, validation_list, good_dir="val")
