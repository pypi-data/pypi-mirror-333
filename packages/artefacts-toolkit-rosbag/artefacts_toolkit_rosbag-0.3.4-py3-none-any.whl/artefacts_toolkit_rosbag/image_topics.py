import cv2
import subprocess

from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore
from rosbags.image import message_to_cvimage
from pathlib import Path


def _get_last_image_from_rosbag(rosbag_filepath, topic_name, output_dest):
    # Create a typestore and get the string class.
    typestore = get_typestore(Stores.LATEST)

    formatted_name = topic_name.replace("/", "_")
    filename = f"{output_dest}/{formatted_name}.last.png"
    for p in Path(output_dest).glob(f"{formatted_name}.last.png"):
        p.unlink()
    img = None
    # Create reader instance and open for reading.
    with Reader(rosbag_filepath) as reader:
        # Topic and msgtype information is available on .connections list.
        for connection in reader.connections:
            print(connection.topic, connection.msgtype)
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_name:
                msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                img = message_to_cvimage(msg, "bgr8")
    if img is not None:
        cv2.imwrite(filename, img)
    return filename


def extract_camera_image(rosbag_filepath, camera_topic, output_dir="output"):
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)
    try:
        _get_last_image_from_rosbag(rosbag_filepath, camera_topic, output_dir)
    except Exception as e:
        print("error")
        print(e)


def extract_video(bag_path, topic_name, output_path, frame_rate=20):
    # Change the output path to a .webm file if not already:
    if not output_path.endswith(".webm"):
        print("Output path must be a .webm file, changing file extension...")
        output_path = output_path + ".webm"
    
    typestore = get_typestore(Stores.LATEST)
    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*"vp80")
    frame_size = None  # Set after reading frame 1
    video_writer = None

    print("Opening bag file and extracting image topics...")

    try:
        with Reader(bag_path) as reader:
            for connection, timestamp, rawdata in reader.messages():
                if connection.topic == topic_name:
                    msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
                    # Convert ROS Image message to OpenCV image
                    try:
                        frame = message_to_cvimage(msg, "bgr8")
                    except Exception as e:
                        print(f"Error converting message to image: {e}")
                        continue

                    if frame_size is None:
                        frame_size = (frame.shape[1], frame.shape[0])
                        video_writer = cv2.VideoWriter(
                            output_path, fourcc, frame_rate, frame_size
                        )

                    video_writer.write(frame)

    except Exception as e:
        print(f"Error extracting video from rosbag: {bag_path}. Error: {e}")
    finally:
        if video_writer is not None:
            video_writer.release()
            print(f"Video saved to {output_path}")
