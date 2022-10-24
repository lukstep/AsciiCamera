import cv2
import numpy as np
import os

# density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{[]?-_+~<>i!lI;:,^`'. "
density = "@%#*+=:. "
density_len = len(density)
density_scaler = 255 / density_len


def render(vc, frame, terminal_columns, terminal_rows):
    frame_shape = np.shape(frame)
    y = int(np.ceil(frame_shape[0] / terminal_rows)) - 1
    x = int(np.ceil(frame_shape[1] / terminal_columns)) - 1
    ascii_frame = np.chararray([terminal_rows, terminal_columns])
    rval, frame = vc.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for row in range(0, terminal_rows):
        for column in range(0, terminal_columns):
            tmp = frame[
                (row * y) : (row * y) + (y - 1), column * x : (column * x) + (x - 1)
            ]
            try:
                ascii_frame[row, column] = density[
                    density_len - int(np.floor(np.mean(tmp) / density_scaler)) - 1
                ]
            except:
                print(
                    f"index:{len(density) - int(np.floor(np.mean(tmp) / len(density))) - 1}"
                )
                return
    os.system("clear")
    for row in ascii_frame:
        print(row.tostring().decode("utf-8"))


def run():
    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        return
    while rval:
        terminal_columns, terminal_rows = os.get_terminal_size()
        render(vc, frame, terminal_columns, terminal_rows)
    vc.release()
    cv2.destroyWindow("preview")


if __name__ == "__main__":
    run()
