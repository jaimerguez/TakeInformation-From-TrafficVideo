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


from time import time
import cv2
import argparse
import sys
import numpy as np
import csv



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debuxar fluxo de vehiculos')
    parser.add_argument(
        '-c', '--csv', help='Path o csv dos datos dos vehiculos')
    parser.add_argument(
        '-e', '--entrada', help='Entrada a ter en conta', type = int)
    parser.add_argument(
        '-s', '--saida', help='Saida a ter en conta', type = int)

    args = parser.parse_args()

    clases = ['bus']
    entrada = int(args.entrada)
    saida = int(args.saida)

    
    # cargamos o csv
    try:
        csv1 = open(args.csv, "r")
    except:
        print("Error: Non se pode ler o csv")
        sys.exit()

    csvReader = csv.reader(csv1)
    primera = True
    vel = []
    for row in csvReader:
    
        if not primera and int(row[4]) == saida and int(row[3]) == entrada:
        #if not primera and row[1] in clases:
            traxectorias = row[7].replace('(', "").replace(')', '').replace(
                '[', '').replace(']', '').replace(' ', '').split(',')
            suma = 0            
            for i in range(0, len(traxectorias)):
                suma += float(traxectorias[i])
            vel.append(suma/len(traxectorias))

        primera = False

    print("Media:", sum(vel)/len(vel))
