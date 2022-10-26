#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 10/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Script con funciones auxiliares para mostrar resultados en tiempo real
# por pantalla para el usuario
# - Debuxar as caixas delimitantas do tracker
# - Debuxar centro de masas de cada caixa delimitadora
# - Debuxar linha de traxectoria
# - Debuxar as linhas de entrada e saida
# - Gardar as linhas de entrada e saida en csv
# ---------------------------------------------------------------------------


import cv2
import config
import numpy as np
import csv

# cargamos as clases de yolo
classes = []
with open(config.path_yolo_labels, 'r') as f:
    classes = [line.strip() for line in f.readlines()]


def Drawlines(lines_in, lines_out, frame):
    # Debuxamos as linhas
    for i, line in enumerate(lines_in):
        cv2.line(frame, line[0], line[1], (255, 0, 0), 2)
        cv2.putText(frame, "IN "+str(i), (line[0][0], line[0][1]-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    for i, line in enumerate(lines_out):
        cv2.line(frame, line[0], line[1], (0, 0, 255), 2)
        cv2.putText(frame, "OUT "+str(i), (line[0][0], line[0][1]-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return frame


def DrawBoxes(tracks, frame, dict_vehiculos):
    # debuxar as caixas delimitantes do tracker
    for j in range(len(tracks.tolist())):
        coords = tracks.tolist()[j]
        x1, y1, x2, y2 = int(coords[0]), int(
            coords[1]), int(coords[2]), int(coords[3])
        name_idx = int(coords[8])
        clase = classes[int(coords[4])]
        color = compute_color_for_labels(coords[8])
        name = "ID: {}, {}".format(str(name_idx), str(clase))
        cv2.rectangle(frame, (x1, y1), (x2, y2),
                      color, 2)
        cv2.rectangle(frame, (x1, y1), (x2, y1+25),
                      color, -1)

        if len(dict_vehiculos[name_idx].velocidade)>0: 
            vel = int(dict_vehiculos[name_idx].velocidade[-1])

            cv2.putText(frame, name+' '+str(vel), (x1+1, y1+15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)

        else:
            cv2.putText(frame, name, (x1+1, y1+15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)
        # debuxar centro de masas de cada caixa delimitadora
        pointx = int((x1+x2)/2)
        pointy = int((y1+y2)/2)
        cv2.circle(frame, (pointx, pointy), 5, (0, 0, 255), -1)
        # debuxar linha de traxectoria
        pts_traxectoria = dict_vehiculos[name_idx].traxectoria[-int(
            config.num_points_traxectoria):]
        cv2.polylines(frame, [np.array(pts_traxectoria)],
                      False, color, 2)
    return frame


def compute_color_for_labels(label):
    # variabel para as cores de cada clase, graficos
    palette = (3 ** 11 - 1, 2 ** 15 - 1, 3 ** 2 - 1)
    # funcion para obter a cor para cada clase
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def write_poses_lines(linesin, linesout):
    # escribir as linhas de entrada e saida
    csv_linhas = open(config.matriz_vehicles+"linhas_posicion.csv", 'w')
    csv_linhas = csv.writer(csv_linhas)
    csv_linhas.writerow(
        ['Tipo', 'Punto1', 'Punto2'])

    for line in linesin:
        csv_linhas.writerow(['Entrada', line[0], line[1]])
    for line in linesout:
        csv_linhas.writerow(['Saida', line[0], line[1]])
