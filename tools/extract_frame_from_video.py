import cv2
import os
import fire
import numpy as np


def extract_frame(video_path, n_frame, output_dir):
    # Create VideoCapture and check if working
    vc = cv2.VideoCapture(video_path)
    try:
        ret, frame = vc.read()
        img_size = frame.shape
    except Exception as e:
        print("Issue with video", video_path, e)
        return

    # Randomly choose the frame_ids to export
    max_frame_nb = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_ids = np.random.randint(0, max_frame_nb, n_frame)
    print(frame_ids)

    # export frame
    for i in range(n_frame):
        vc.set(cv2.CAP_PROP_POS_FRAMES, frame_ids[i])
        ret, frame = vc.read()
        cv2.imwrite(os.path.join(output_dir, f"{i}.png"), frame)


if __name__ == '__main__':
    fire.Fire(extract_frame)
