#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Programa principal de contador de coches
# Para modificar os parametros do programa, modificar o ficheiro config.py
# ---------------------------------------------------------------------------
# python main.py
# ---------------------------------------------------------------------------


import cv2
import numpy as np
import os
import sys
import config

from yolov5 import yolov5
from drawlines import DrawLines


def Drawlines(lines_in, lines_out, frame):
    # Draw the lines
    for i, line in enumerate(lines_in):
        cv2.line(frame, line[0], line[1], (255, 0, 0), 2)
        cv2.putText(frame, str(i), (line[0][0], line[0][1]-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    for i, line in enumerate(lines_out):
        cv2.line(frame, line[0], line[1], (0, 0, 255), 2)
        cv2.putText(frame, str(i), (line[0][0], line[0][1]-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame


if __name__ == "__main__":
    # cargamos o video de entrada
    video_input = cv2.VideoCapture(config.path_video_input)

    # comprobamos fora aberto de forma correcta
    if not video_input.isOpened():
        print("INFO | Video non atopado ou erro ao abrilo")
        sys.exit()

    primer_frame = True
    yolov5 = yolov5()

    while (video_input.isOpened()):
        ret, frame = video_input.read()
        if config.video_size != None:
            frame = cv2.resize(
                frame, (config.video_size[1], config.video_size[0]))
        if ret == True:

            # debuxamos as linhas de entrada e de saida dos vehiculos
            if primer_frame:
                print("INFO | Introduce as linhas de entrada dos vehiculos")
                lines_in, frame_lines_in = DrawLines(frame).run()
                print()
                print("INFO | Introduce as linhas de saida dos vehiculos")
                lines_out, _ = DrawLines(frame_lines_in).run(color=(0, 0, 255))
                primer_frame = False
                print()

            # obtemos as caixas delimitantes, as confianzas e clases do frame actual
            boxes, confs, class_ids = yolov5.detection(frame)
            # debuxamos as caixas delimitantes no frame
            if config.screen_output:
                frame_with_box = yolov5.draw_boxes(boxes, confs, class_ids)
                frame_with_box = Drawlines(lines_in, lines_out, frame_with_box)
                cv2.imshow("Resultado", frame_with_box)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            print("INFO | Final do video")
            break
