import cv2
import os

def img_to_vid(frame_rate):
    # Set the directory containing the images
    image_folder = 'C:/Users/asus/Desktop/Video to image sequence/models/ESRGAN/results'
    # image_folder = '../results'

    # Set the video name and format
    video_name = 'C:/Users/asus/Desktop/enhanced_video.mp4'
    # video_name = '../results/enhanced_video.mp4'

    # Get the frame size from the first image in the folder
    first_image = cv2.imread(os.path.join(image_folder, os.listdir(image_folder)[0]))
    frame_size = (first_image.shape[1], first_image.shape[0])

    # Create a list of all the image file names
    images = sorted([img for img in os.listdir(image_folder) if img.startswith('Snap')], key=lambda x: int(x.split('Snap')[1].split('.png')[0]))
    print(images)

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(video_name, fourcc, frame_rate, frame_size)

    # Loop through each image and add it to the video writer object
    for image in images:
        img_path = os.path.join(image_folder, image)
        img = cv2.imread(img_path)
        video.write(img)

    # Release the video writer object and close all windows
    video.release()
    cv2.destroyAllWindows()
