#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Programa principal de contador de coches
# Para modificar os parametros do programa, modificar o ficheiro config.py
# ---------------------------------------------------------------------------
# python main.py
# ---------------------------------------------------------------------------


from xml.etree.ElementTree import PI
import cv2
import numpy as np
import os
import sys
import config
import time



from yolov5 import yolov5
from drawlines import DrawLines
from counter import CounterVehicles, Vehicle
from sort import Sort
from util import *
from transformPoint import PixelMapper


if __name__ == "__main__":

    # cargamos o video de entrada
    try:
        video_input = cv2.VideoCapture(config.path_video_input)

    except  Exception as e:
        print(e)
        print("Error: Non se puido abrir o video de entrada")
        sys.exit()

    # comprobamos fora aberto de forma correcta
    if not video_input.isOpened():
        print("INFO | Video non atopado ou erro ao abrilo")
        sys.exit()

    total_frame = cv2.VideoCapture.get(video_input, cv2.CAP_PROP_FRAME_COUNT)
    primer_frame = True
    yolov5 = yolov5()
    tracker = Sort()
    # lista para gardar as instancias dos vehiculos
    dict_vehiculos = {}
    num_frame = 0
    time_inicio = time.time()

    while (video_input.isOpened()):
        ret, frame = video_input.read()
        if config.video_size != None and ret:
            frame = cv2.resize(
                frame, (config.video_size[1], config.video_size[0]))
        if ret == True:

            # debuxamos as linhas de entrada e de saida dos vehiculos
            if primer_frame:
                print("INFO | Introduce as linhas de ENTRADA dos vehiculos")
                lines_in, frame_lines_in = DrawLines(frame).run()
                print()
                print("INFO | Introduce as linhas de SAIDA dos vehiculos")
                lines_out, frame_lines_in = DrawLines(
                    frame_lines_in).run(color=(0, 0, 255))
                # gardamos imaxe das linhas de entrada e de saida
                cv2.imwrite(config.matriz_vehicles +
                            'posicion_entradas_saidas.jpg', frame_lines_in)
                # gardamos as posicions das linhas de entrada e saida
                write_poses_lines(lines_in, lines_out)
                primer_frame = False
                print()
                counter = CounterVehicles(lines_in, lines_out)
                #facemos as deteccions de vehiculos do primeiro frame
                boxes, confs, class_ids, centers_box, tracker_boxes = yolov5.detection(
                    frame)

                #creamos instancia da clase para transformar os puntos a real
                pm = PixelMapper(config.coor_pixel, config.coor_real)


            num_frame += 1

            if num_frame % config.skip_frames == 0:
                # obtemos as caixas delimitantes, as confianzas e clases do frame actual
                boxes, confs, class_ids, centers_box, tracker_boxes = yolov5.detection(
                    frame)
                # facemos as deteccions de vehiculos do frame actual
                tracks = tracker.update(tracker_boxes)

            if num_frame % config.skip_frames != 0:
                # actualizamos o tracker sen usar o detector
                tracks = tracker.update(tracker_boxes)

            # lista para saber os vehiculos que se actualizaron
            vehicles_update = []

            for j in range(len(tracks.tolist())):
                vehicle = tracks.tolist()[j]
                x1, y1, x2, y2 = int(vehicle[0]), int(
                    vehicle[1]), int(vehicle[2]), int(vehicle[3])
                if not vehicle[8] in dict_vehiculos.keys():
                    # instanciamos un novo vehiculo
                    instaVec = Vehicle(vehicle[8], vehicle[4], (int(
                        (x1+x2)/2), int((y1+y2)/2)), num_frame, counter)

                    # engadimos a instancia ao diccionario
                    dict_vehiculos[vehicle[8]] = instaVec
                    vehicles_update.append(vehicle[8])
                else:
                    # actualizamos a posicion do vehiculo
                    dict_vehiculos[vehicle[8]].update_vehicle(
                        (int((x1+x2)/2), int((y1+y2)/2)), num_frame,pm)
                    vehicles_update.append(vehicle[8])

            # comprobamos aqueles vehiculos que se perderon
            ids_eliminar = []
            for vehicle in dict_vehiculos.keys():
                # se non se atopa no frame actual e deixamos de velo durante X frames eliminamos o vehiculo
                if not vehicle in vehicles_update and (num_frame - dict_vehiculos[vehicle].ultimo_frame) >= config.num_frames_perder:
                    # so gardamos os datos no csv se estiveron na zona de estudo e se os datos son completos
                    if dict_vehiculos[vehicle].saida is not None:
                        dict_vehiculos[vehicle].save_data_csv()
                    ids_eliminar.append(vehicle)

            for vehicle in ids_eliminar:
                # eliminamos o vehiculo do diccionario
                # dict_vehiculos.pop(vehicle)
                del dict_vehiculos[vehicle]

            # debuxamos as caixas delimitantes no frame
            if config.screen_output:
                #frame_with_box = yolov5.draw_boxes(boxes, confs, class_ids)
                frame_with_box = DrawBoxes(tracks, frame, dict_vehiculos)
                frame_with_box = Drawlines(lines_in, lines_out, frame_with_box)
                cv2.imshow("Resultado", frame_with_box)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            os.system('cls' if os.name == 'nt' else 'clear')
            print("[INFO] Extraendo datos do video...")
            print("Numero de frame actual ",
                  num_frame, " de ", int(total_frame))
            print("Procesando feito:", round(
                num_frame/total_frame*100, 2), "%")
            print("Tempo restante:", round((time.time()-time_inicio) /
                  num_frame*(total_frame-num_frame), 2), "segundos")
            print("Frame por segundo:", round(
                num_frame/(time.time()-time_inicio), 2))
            print("Contador de entrada:", counter.cont_linhas_in)
            print("Contador de saida:", counter.cont_linhas_out)
            print(counter.matrix_total)

            tracks = tracker_boxes

        else:
            print("INFO | Final do video")
            break

        # gardamos as matrices de entrada e de saida
        np.savetxt(config.matriz_vehicles+"matriz_total_vehicles.csv",
                   counter.matrix_total, delimiter=",")

        # gardamos as matrices de entrada e de saida para cada clase
        for tipo in counter.dict_matrix_type.keys():
            np.savetxt(config.matriz_vehicles+"matriz_"+str(tipo) +
                       ".csv", counter.dict_matrix_type[tipo], delimiter=",")
