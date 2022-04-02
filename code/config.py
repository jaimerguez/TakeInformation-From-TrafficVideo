#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Arquivo config.py para establecer as variabeis do sistema
# ---------------------------------------------------------------------------


# path do video de entrada para o analise
path_video_input = "../video/IMG_1839.MOV"

# tamanho do video para traballar
video_size = (1080, 1920)
# video_size = None # None para tomar tamanho por defecto

# variabel booleana para mostrar o resultado por pantalla
screen_output = True


##############################################################
#################### PARAMETROS DE YOLOv5 ####################
##############################################################
# path os pesos de Yolo
path_yolo_weights = "../data/yolov5s.onnx"  # version pequena
# path_yolo_weights = "../data/yolov5m.onnx" #version media
# path_yolo_weights = "../data/yolov5l.onnx" #version grande

# path as clases de Yolo
path_yolo_labels = "../data/coco.names"
# tamanho da imagen de entrada para o Yolo (alto, largo)
size_yolo = (640, 640)
# confianza minima para detectar
confidence = 0.5
# score minimo para detectar (https://docs.opencv.org/4.x/d6/d0f/group__dnn.html#ga9d118d70a1659af729d01b10233213ee)
score = 0.5
# nms_threshold (https://docs.opencv.org/4.x/d6/d0f/group__dnn.html#ga9d118d70a1659af729d01b10233213ee)
nms_threshold = 0.6
# obxetos a detectar
whatdetect = ["bicicleta", "coche", "moto", "persoa", "semaforo", "bus"]
# cor da caixa delimitadora
cor_box = (0, 255, 0)
