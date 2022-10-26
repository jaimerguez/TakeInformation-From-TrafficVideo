#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jaime Rodríguez Rodríguez
#               Martin Sanchez Lopez
# Created Date: 10/04/2022
# version ='1.0'
# ---------------------------------------------------------------------------
# Programa para debuxar de maneira grafica as traxectoias de cada vehiculo (fluxos)
# ---------------------------------------------------------------------------
# python drawFlow.py -i ../../exemplo_saida/1/posicion_entradas_saidas.jpg -c ../../exemplo_saida/1/data_vehicles.csv -d ../../exemplo_saida/1/
# python drawFlow.py -i ../../exemplo_saida/4/posicion_entradas_saidas.jpg -c ../../exemplo_saida/4/data_vehicles.csv -d ../../exemplo_saida/4/
# ---------------------------------------------------------------------------


import cv2
import argparse
import sys
import numpy as np
import csv


def compute_color_for_labels(label):
    # variabel para as cores de cada clase, graficos
    palette = (3 ** 11 - 1, 2 ** 15 - 1, 3 ** 2 - 1)
    # funcion para obter a cor para cada clase
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debuxar fluxo de vehiculos')
    parser.add_argument('-d', '--directorio', type=str,
                        help='Directorio onde gardar a imaxe de saida')
    parser.add_argument(
        '-i', '--imaxe', help='Path da imaxe sobre que dibuxar')
    parser.add_argument(
        '-c', '--csv', help='Path o csv dos datos dos vehiculos')

    args = parser.parse_args()

    clases = ['bus','coche']

    # cargamos a imaxe
    try:
        image = cv2.imread(args.imaxe)
    except:
        print("Error: Non se pode ler a imaxe")
        sys.exit()

    # cargamos o csv
    try:
        csv1 = open(args.csv, "r")
    except:
        print("Error: Non se pode ler o csv")
        sys.exit()

    csvReader = csv.reader(csv1)
    primera = True
    for row in csvReader:
        if not primera and row[1] in clases:
            tra = []
            traxectorias = row[5].replace('(', "").replace(')', '').replace(
                '[', '').replace(']', '').replace(' ', '').split(',')
            for i in range(0, len(traxectorias), 2):
                tra.append((int(traxectorias[i]), int(traxectorias[i+1])))

            cv2.polylines(image, [np.array(tra)], False,
                          compute_color_for_labels(int(row[0])), 2)
        primera = False

    cv2.imwrite(args.directorio + '/fluxo_bus.jpg', image)
    cv2.imshow("image", image)
    cv2.waitKey(0)
