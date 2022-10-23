import cv2
import numpy as np
import os

density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{[]?-_+~<>i!lI;:,^`'. "
# density = "@%#*+=:. "
density_len = len(density)
density_scaler = 256 / density_len


def run(vc, terminal_rows, terminal_columns):
    x = 0
    y = 0
    if vc.isOpened():
        rval, frame = vc.read()
        frame_shape = np.shape(frame)
        y = int(np.ceil(frame_shape[0] / terminal_rows)) - 1
        x = int(np.ceil(frame_shape[1] / terminal_columns)) - 1
    else:
        return

    asci_frame = np.chararray([terminal_rows, terminal_columns])
    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for row in range(0, terminal_rows):
            for column in range(0, terminal_columns):
                tmp = frame[
                    (row * y) : (row * y) + (y - 1), column * x : (column * x) + (x - 1)
                ]
                try:
                    asci_frame[row, column] = density[
                        density_len - int(np.floor(np.mean(tmp) / density_scaler)) - 1
                    ]
                except:
                    print(
                        f"index:{len(density) - int(np.floor(np.mean(tmp) / len(density))) - 1}"
                    )
                    return
        os.system("clear")
        for row in asci_frame:
            print(row.tostring())


if __name__ == "__main__":
    terminal_columns, terminal_rows = os.get_terminal_size()
    cv2.namedWindow("ASCI CAM")
    vc = cv2.VideoCapture(0)
    run(vc, terminal_rows, terminal_columns - 3)
    vc.release()
    cv2.destroyWindow("preview")
