#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
# Created Date: 01/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Script para debuxar linhas sobre unha imaxe ca axuda do rato
# Servira para establecer as zonas de entrada e saida do vehiculo
# ---------------------------------------------------------------------------
# python drawlines.py --image path_image
# ---------------------------------------------------------------------------

import cv2
import sys
import argparse


class DrawLines():
    def __init__(self, frame):
        self.image = frame.copy()
        self.without_lines = frame.copy()
        self.window_name = "Introduce as linhas de entrada e saida"
        self.done = False
        self.points_coord = []
        self.cont_linha = 0

    def on_mouse(self, event, x, y, buttons, user_param):
        # funcion que captura os eventos do rato
        if self.done:
            return

        # boton dereito: collemos puntos
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x, y)]

        # boton esquerdo: debuxamos unha linha
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x, y))
            print('Inicio: {}, Final: {}'.format(
                self.image_coordinates[0], self.image_coordinates[1]))

            # Debuxamos unha linha entre os puntos
            cv2.line(
                self.image, self.image_coordinates[0], self.image_coordinates[1], self.color, 2)
            cv2.putText(self.image, str(self.cont_linha), (self.image_coordinates[0][0], self.image_coordinates[0][1]-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, self.color, 2)
            self.cont_linha += 1
            cv2.imshow(self.window_name, self.image)
            self.points_coord.append(self.image_coordinates)

        # limpar as linhas
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.image = self.without_lines
            self.cont_linhas = 0

    def run(self, color=(255, 0, 0)):
        print("INFO | Introduce as linhas de entrada e saida dos vehiculos")
        print("INFO | Presiona o boton dereito para limpar as linhas")
        print("INFO | Pressiona 'q' para sair")
        self.color = color
        cv2.namedWindow(self.window_name)
        cv2.imshow(self.window_name, self.image)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while (not self.done):
            # Bucle de debuxo
            # actualizamos a imaxe
            cv2.imshow(self.window_name, self.image)
            if cv2.waitKey(1) == ord("q"):  # 'q' presionamos para sair
                self.done = True
        cv2.destroyWindow(self.window_name)
        return self.points_coord, self.image


if __name__ == "__main__":
    # cargamos a imaxe de entrada
    parser = argparse.ArgumentParser(
        description="Introduce o path da imaxe de entrada")
    parser.add_argument("-i", "--image", required=True,
                        help="Introduce o path da imaxe de entrada")
    args = parser.parse_args()
    try:
        image = cv2.imread(args.image)
    except:
        print("INFO | Imaxe non atopada ou erro ao abrilo")
        sys.exit()

    lines, _ = DrawLines(image).run()
    print(lines)
