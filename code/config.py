#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Arquivo config.py para establecer as variabeis do sistema
# ---------------------------------------------------------------------------

##############################################################
#################### Datos de entrada ########################
##############################################################
# path do video de entrada para o analise
# pode ser un enlace a un video de youtube ou unha ruta de ficheiro
# o video pode ser en directo
#path_video_input = "https://www.youtube.com/watch?v=rQ55zQZjUro"
path_video_input = "../video/VIDEO_PROBA.mp4"

# tamanho do video para traballar
video_size = (1080, 1920)
# video_size = None # None para tomar tamanho por defecto

# ruta o ficheiro de saida dos datos
path_output_file = "../video/output.csv"


##############################################################
#################### SAIDA data - grafico ####################
##############################################################
# variabel booleana para mostrar o resultado por pantalla
screen_output = True

# numero de puntos para debuxar traxectoria do vehiculo
# no caso de querer debuxar todos ponher o valor a cero
# NOTE: Este valor non influe nas traxectorias gardadas no csv
num_points_traxectoria = 0

##############################################################
#################### Transformacion puntos ###################
##############################################################

import numpy as np

#coordenadas no video
coor_pixel = np.array([
            [1142, 979], # Third lampost top right
            [663, 975], # Corner of white rumble strip top left
            [716, 381], # Corner of rectangular road marking bottom left
            [1124, 337] # Corner of dashed line bottom right
        ])

#coordenadas reais
coor_real = np.array([
            [43.01016, -7.55302], # Third lampost top right
            [43.01020, -7.55298], # Corner of white rumble strip top left
            [43.01000, -7.55254], # Corner of rectangular road marking bottom left
            [43.00985, -7.55260] # Corner of dashed line bottom right
        ])

#numero de frames para ter en conta a hora de calcular a velocidade
num_frames_vel = 10

##############################################################
#################### SAIDA data - csv ########################
##############################################################
# ¡¡¡¡IMPORTANTE!!!!:
# Os ficheiros de saidas son borrados cada vez que se inicia 
# o programa
data_vehicles = "../output/data_vehicles.csv"
matriz_vehicles = "../output/"

# NOTE: explicacion das matrices de datos
# columnas -> saida
# filas    -> entrada

##############################################################
#################### PARAMETROS DO Tracker ###################
##############################################################
# numero de frame que non detectamos e eliminamos vehiculo de 
# seguimento
num_frames_perder = 40

# numero de frame pasado que comparamos co actual para saber 
# por onde entra e sae
frame_update_inout = 3

# numero de frames que seguimos un vehiculo sen usar o detector
skip_frames = 8

#iou threshold de SORT (default: 0.3)
iou_sort = 0.2


##############################################################
#################### PARAMETROS DE YOLOv5 ####################
##############################################################
#GPU para usar 
device = 0

# numero de frames sen facer deteccions, usando tracker
num_frames_track = 3

# path os pesos de Yolo no caso de usar OpenCV para facer as 
# inferencias
#path_yolo_weights = "../data/yolov5s.onnx"  # version pequena
#path_yolo_weights = "../data/yolov5m.onnx"  # version media
path_yolo_weights = "../data/yolov5l.onnx" #version grande


# path as clases de Yolo
path_yolo_labels = "../data/coco.names"
# tamanho da imagen de entrada para o Yolo (alto, largo)
size_yolo = (640, 640)
# confianza minima para detectar
confidence = 0.4
# score minimo para detectar (https://docs.opencv.org/4.x/d6/d0f/group__dnn.html#ga9d118d70a1659af729d01b10233213ee)
score = 0.4
# nms_threshold (https://docs.opencv.org/4.x/d6/d0f/group__dnn.html#ga9d118d70a1659af729d01b10233213ee)
nms_threshold = 0.6
# obxetos a detectar
#whatdetect = ["bicicleta", "coche", "moto", "persoa", "semaforo", "bus"]
whatdetect = ["coche", "moto", "bus"]
# cor da caixa delimitadora e texto
cor_box = (0, 255, 0)
