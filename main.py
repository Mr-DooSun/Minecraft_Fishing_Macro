import win32gui
import pynput

import numpy

from time import sleep

import cv2

from PIL import ImageGrab

def Search_image_on_image(frame,template,threshold=1) :
    h,w = template.shape[:-1]

    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)

    loc = numpy.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        return (int(w / 2 + pt[0])+left,int(h / 2 + pt[1])+top)

    return None

def Search_red_on_image(frame):
    # lower_color=(0, 0, 44)
    # upper_color=(40, 33, 84)
    
    lower_color=(31, 31, 198)
    upper_color=(51, 51, 218)

    img_mask = cv2.inRange(frame, lower_color, upper_color)

    cv2.imshow("img_mask",img_mask)

    for x in range(0,len(img_mask)):
        for y in range(0,len(img_mask[x])):
            if img_mask[x][y] == 255 :
                return True
    return False

def get_window_image_by_opencv(
    x: int,
    y: int,
    w: int,
    h: int
):
    center_x = x + int((w - x)/2)
    center_y = y + int((h - y)/2)

    # img = ImageGrab.grab(bbox=(x, y, w, h))
    img = ImageGrab.grab(bbox=(center_x-100, center_y-100, center_x+100, center_y+100))
    img_np = numpy.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)

    return frame
  

def get_window_list():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)

        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True

    output = []

    win32gui.EnumWindows(callback, output)
    
    return output

if __name__ == '__main__' :
    mouse_drag = pynput.mouse.Controller()
    mouse_button = pynput.mouse.Button

    window_list = get_window_list()

    for tmp_title, tmp_hwnd in window_list:
        if "minecraft 1.19.2" in tmp_title.lower() :
            hwnd = tmp_hwnd
            break

    template = cv2.imread("image/detect.png")

    while True :
        left, top, right, bot = win32gui.GetWindowRect(hwnd)

        frame = get_window_image_by_opencv(
            x=left,
            y=top,
            w=right,
            h=bot,
        )

        status = Search_red_on_image(frame=frame)
        if not status :
            print("HIT!")
            mouse_drag.press(mouse_button.right)
            mouse_drag.release(mouse_button.right)

            sleep(1)

            print("Casting!")
            mouse_drag.press(mouse_button.right)
            mouse_drag.release(mouse_button.right)
            
            sleep(3)
        else :
            print("Wait....")

        cv2.imshow("frame1",frame)

        # q 버튼을 누르면 종료
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break