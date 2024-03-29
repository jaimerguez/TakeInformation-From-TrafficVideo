
# ANÁLISIS DEL TRÁFICO MEDIANTE VA

> *Project in process...*

## Objetivo 
El objetivo es extraer los datos de tráfico de un video usando técnicas de visión artificial para luego poder usarlo para: la creación de modelos de tráfico, análisis de los diferentes flujos... <br>
Poder entender cómo se comporta el tráfico de una ciudad, puede ayudar a optimizarlo, reduciendo los tiempos de atasco y reduciendo la contaminación. En este trabajo para extraer los datos, se utilizaron YOLOv5 y Sort como las principales técnicas de visión artificial. Una
de los objetivos alcanzados fue simplificar y reducir costos al hacer estudios de tráfico, en comparación casos técnicos utilizados actualmente; además de una flexibilidad mucho mayor.

## ¿Cómo usar? 

1) Instala los requisitos
2) Cambia las variabeis que consideres pertinentes en el script $./code/config.py.$
3) Lanza el codigo con el seguinte comando:  ```$ python main.py```
4) Todos los datos extraidos se guardan en el directorio $./output$
5) Postprocesa los datos obtenidos con los scripts del directorio $./code/analizar$

## Requisitos 

Los requisitos del proxecto están descritos en $./code/requirements.txt$. Para instalar todos:
```bash
$ pip install requirements.txt -r
```

## Demo

En el directorio del repositorio $./output\_example$ se encuentra una salida de ejemplo para un video de tráfico.<br>

<p align="center"><img src="https://github.com/jaimerguez/TakeInformation-From-TrafficVideo/blob/main/output_example/fluxo.jpg" width="50%"></p>
