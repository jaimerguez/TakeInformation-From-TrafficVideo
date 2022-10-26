#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Script para contar vehiculos e identificar varias medidas:
# - Entrada de vehículos e saída (contadores independentes)
# - Tempo de permanencia
# - Matriz de entradas e saidas
# - Numero de vehiculos totais e de cada tipoloxia
# - Traxectoria de cada vehículo
# Isto despois e gardado en varios ficheiros csv
# ---------------------------------------------------------------------------

import config
import sys
import numpy as np
import csv
import cv2


class CounterVehicles():

    def __init__(self, lines_in, lines_out):
        # definimos contadores de entrada e saida dos vehiculos en total
        self.entrar = 0
        self.sair = 0
        # contadores de para cada entrada e para cada saida
        self.cont_linhas_in = [0]*len(lines_in)
        self.cont_linhas_out = [0]*len(lines_out)
        # definimos matriz de entrada e saida
        self.matrix_total = np.zeros(
            (len(lines_in), len(lines_out)), dtype=int)

        # definimos as linhas
        self.lines_in = lines_in
        self.lines_out = lines_out

        # variabeis do video para calcular o tempo de permanencia
        video = cv2.VideoCapture(config.path_video_input)
        self.fps = video.get(cv2.CAP_PROP_FPS)

        # abrimos archivo csv para gardar os datos

        try:
            # cargamos as clases de yolo
            self.classes = []
            with open(config.path_yolo_labels, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]

        except Exception as error:
            print("INFO | Erro ao importar clases de Yolo")
            print(error)
            sys.exit()

        # abrimos o ficheiro para escribir os datos
        csv_vehicles = open(config.data_vehicles, 'w')
        self.csv_vehicles = csv.writer(csv_vehicles)
        self.csv_vehicles.writerow(
            ['ID', 'Clase', 'Tempo', 'Entrada', 'Saida', 'TraxectoriaVideo','TraxectoriaReal','Velocidade'])

        # creamos un diccionario para gardar as matrices de entrada e saida para cada clase
        self.dict_matrix_type = {}
        for tipo in config.whatdetect:
            self.dict_matrix_type[tipo] = np.zeros(
                (len(lines_in), len(lines_out)), dtype=int)


class Vehicle(CounterVehicles):
    def __init__(self, ID, clase, center_box, num_frame, contador):
        # definimos as variabeis de cada vehiculo
        self.ID = ID
        self.contador = contador
        self.clase = clase
        self.center_box = center_box
        self.time = None
        self.entrada = None
        self.saida = None
        self.traxectoria = [center_box]
        self.traxectoria_in = [center_box]
        self.velocidade = []
        self.traxectoria_real = []
        self.primer_frame = None  # frame que o vehiculo se encontra dentro da zona de estudio
        self.ultimo_frame = num_frame  # ultimo frame que o vehiculo se encontra
        # valor booleano para saber se xa temos toda a informacion sobre o vehiculo
        self.completo = False
        #self.update_vehicle(center_box, num_frame)

    def update_vehicle(self, center_box, num_frame, pm):
        """
        Funcion para actualizar os datos de cada vehiculo
        """
        #! TODO: podese engadir so a traxectoria do vehiculo so dentro da zona de estudio
        # if not self.completo:
        #    self.center_box = center_box
        #    self.ultimo_frame = num_frame
        #    self.traxectoria.append(self.center_box)
        self.center_box = center_box
        self.ultimo_frame = num_frame
        self.traxectoria.append(self.center_box)

        # comprobamos se entrou
        if not self.completo:
            if self.entrada is None and (len(self.traxectoria) > config.frame_update_inout):
                for i, line in enumerate(self.contador.lines_in):
                    if self.intersect(self.center_box, self.traxectoria[-config.frame_update_inout], line[0], line[1]):
                        self.entrada = i
                        self.traxectoria_in = []
                        self.traxectoria_in.append(self.center_box)
                        self.contador.cont_linhas_in[i] += 1
                        self.contador.entrar += 1
                        self.primer_frame = num_frame
                        self.traxectoria_real.append(tuple(pm.pixel_to_lonlat(self.center_box)[0]))
                        break

            if self.entrada is not None and self.saida is None:
                self.traxectoria_in.append(self.center_box)
                self.traxectoria_real.append(tuple(pm.pixel_to_lonlat(self.center_box)[0]))
                num_frames_vel = config.num_frames_vel
                if len(self.traxectoria_real)>num_frames_vel:
                    self.velocidade.append(pm.calculate_speed(self.traxectoria_real[-1],self.traxectoria_real[-num_frames_vel])/(num_frames_vel/self.contador.fps))

            # comprobamos se saiu
            if self.saida is None and self.entrada is not None and (len(self.traxectoria) > config.frame_update_inout):
                for i, line in enumerate(self.contador.lines_out):
                    if self.intersect(self.center_box, self.traxectoria[-config.frame_update_inout], line[0], line[1]):
                        self.saida = i
                        self.time = (self.ultimo_frame -
                                     self.primer_frame)/self.contador.fps
                        self.completo = True
                        self.contador.cont_linhas_out[i] += 1
                        self.contador.sair += 1
                        # self.save_data_csv()
                        self.contador.matrix_total[self.entrada,
                                                   self.saida] += 1
                        self.contador.dict_matrix_type[str(
                            self.contador.classes[int(self.clase)])][self.entrada, self.saida] += 1
                        break

    def intersect(self, A, B, C, D):
        # funcion que comproba se as rectas AB e CD intersecan
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def save_data_csv(self):
        """
        Funcion para gardar os datos en formato csv, gardamos o eliminar de memoria a instancia no programa principal (main.py)
        """
        self.contador.csv_vehicles.writerow([int(self.ID), str(self.contador.classes[int(
            self.clase)]), round(abs(self.time), 3), self.entrada, self.saida, self.traxectoria, self.traxectoria_real,self.velocidade])
