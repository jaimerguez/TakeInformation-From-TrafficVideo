#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Implementacion de YoloV5 en python e con OpenCV
# Para configurar os parametros no archivo config.py
# ---------------------------------------------------------------------------
# python yolov5.py
# ---------------------------------------------------------------------------



import cv2
import config
import sys
import numpy as np


class yolov5():
    def __init__(self):
        # cargamos pesos de yolo
        try:
            self.net = cv2.dnn.readNetFromONNX(config.path_yolo_weights)

            # cargamos as clases de yolo
            self.classes = []
            with open(config.path_yolo_labels, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]

        except Exception as error:
            print("INFO | Erro ao cargar pesos de yolo ou clases")
            print(error)
            sys.exit()

        # obtemos a informacion das diferentes capas da rede
        ln = self.net.getLayerNames()
        # obtemos os indeces que non saida sen conectar
        for i in self.net.getUnconnectedOutLayers():
            self.output_layers = ln[i-1]

        # intentamos cargar o modelo na GPU
        try:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
            print("INFO | Cargado modelo de Yolo en GPU")
        except:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            print("INFO | Cargado modelo de Yolo en CPU, non se puido cargar en GPU")

    def detection(self, frame):
        self.frame = frame

        # preprocesamos o frame e obtemos as saidas
        outputs = self.preprocesado()
        # obtemos as caixas delimitantes, as confianzas e clases
        boxes, confs, class_ids, center_boxes, tracker = self.get_boxes_dimensions(outputs)
        return boxes, confs, class_ids, center_boxes, tracker

    def get_boxes_dimensions(self, outputs):
        class_ids = []  # lista para gardar as clases as que pertencen
        confs = []  # lista para gardar as confianzas
        boxes = []  # lista para gardar as caixas delimitantes
        centers = []  # lista para gardar os centros das caixas delimitantes
        tracker = [] #lista para gardar os datos das caixas para o tracker

        for detection in outputs[0]:
            confidence = detection[4]  # obtemos a confianza
            scores = detection[5:]  # obtemos as confianzas para cada clase
            class_id = np.argmax(scores)  # obtemos a clase con mais confianza
            # comprobamos que sexa maior que o umbral e que a clase con maior probabilidade sexa a que se quere detectar
            if confidence > config.confidence and (self.classes[class_id] in config.whatdetect):
                x_factor = self.frame.shape[1] / config.size_yolo[1]
                y_factor = self.frame.shape[0] / config.size_yolo[0]
                # obtemos as coordenadas das caixas delimitantes
                center_x = int(detection[0] * x_factor)  # centro x da caixa
                center_y = int(detection[1] * y_factor)  # centro y da caixa
                w = int(detection[2] * x_factor)  # ancho da caixa
                h = int(detection[3] * y_factor)  # alto da caixa
                # coordenadas das caixas delimitantes
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                # gardamos as caixas delimitantes
                boxes.append([x, y, w, h])
                # gardamos as confianzas
                confs.append(float(confidence))
                # gardamos as clases
                class_ids.append(class_id)
                # gardamos os centros das caixas delimitantes
                centers.append([center_x, center_y])
                #gardamos os datos para o tracker
                tracker.append([x, y, x+w, y+h, confidence, class_id])

        # supresion de non maximos
        indexes = cv2.dnn.NMSBoxes(
            boxes, confs, score_threshold=config.score, nms_threshold=config.nms_threshold)

        # definimos novas listas para o resultado final despois da MNS
        result_class_ids = []
        result_boxes = []
        result_confidences = []
        result_centers = []
        result_tracker = [] # lista para gardar introducir as caixas no tracker
        for i in indexes:
            # introucimos o resultado nas listas finais
            result_class_ids.append(class_ids[i])
            result_boxes.append(boxes[i])
            result_confidences.append(confs[i])
            result_centers.append(centers[i])
            result_tracker.append(tracker[i])
        return result_boxes, result_confidences, result_class_ids, result_centers, np.asarray(result_tracker)

    def preprocesado(self):
        # empregando a funcion blob de openCV para pre-procesar a imaxe
        blob = cv2.dnn.blobFromImage(
            self.frame, 1/255.0, config.size_yolo, swapRB=True, crop=False)

        # pasamos o frame a traves da rede
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        return outputs

    def draw_boxes(self, boxes, confs, class_ids):
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            label = self.classes[class_ids[i]]
            # caixa delimitadora
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), config.cor_box, 2)
            # caixa delimitadora con texto
            cv2.rectangle(self.frame, (x, y), (x+w, y-25), config.cor_box, -1)
            cv2.putText(self.frame, f'{label}: {int(confs[i]*100)}%', (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        return self.frame


if __name__ == "__main__":
    # cargamos o video de entrada
    video_input = cv2.VideoCapture(config.path_video_input)

    # creamos instancia da clase yolv5
    yolov5 = yolov5()

    # comprobamos fora aberto de forma correcta
    if not video_input.isOpened():
        print("INFO | Video non atopado ou erro ao abrilo")
        sys.exit()

    while (video_input.isOpened()):
        ret, frame = video_input.read()
        frame = cv2.resize(frame, (config.video_size[1], config.video_size[0]))
        if ret == True:
            # obtemos as caixas delimitantes, as confianzas e clases do frame actual
            boxes, confs, class_ids, center_boxes, _ = yolov5.detection(frame)
            # debuxamos as caixas delimitantes no frame
            if config.screen_output:
                frame_output = yolov5.draw_boxes(boxes, confs, class_ids)
                cv2.imshow("Yolo", frame_output)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            print("INFO | Final do video")
            break
