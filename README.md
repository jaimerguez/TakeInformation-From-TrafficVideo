
# ANÁLISIS DEL TRÁFICO MEDIANTE VA
# *Project in process...*

Jaime Rodríguez Rodríguez
Martín Sánchez López

Universidade de Santiago de Compostela

-------------------- Introducción --------------------
O obxectivo é extraer os datos de  tráfico 
dun vídeo usando visión por computadora para despois poder usala para: a creación de modelos de tráfico, 
análise dos diferentes fluxos... Poder entender como se comporta o tráfico dunha cidade, pode axudar a 
optimizalo, conseguindo reducir os tempos de atascos e reducindo a contaminación. Neste traballo para 
conseguir extraer os datos usouse YOLOv5 e Sort como principais técnicas de visión por computadora. Un
dos obxectivos conseguidos foi simplificar e reducir costes a hora de facer estudos de tráfico, comparado 
cás técnicas usadas actualmente; ademais de moita maior flexibilidade.

--------------------- Cómo usar? ---------------------

1) Instala os requisitos
2) Cambia as variabeis que consideres pertinentes no script ./code/config.py.
3) Lanza o codigo co seguinte comando: $ python main.py
4) Todos os datos ontidos gardanse no directorio ./output
5) Postprocesa os datos obtidos cos scripts do directorio ./code/analizar

--------------------- Requisitos ---------------------

Os requisitos do proxecto están descritos en ./code/requirements.txt. Para instalar todos:
$ pip install requirements.txt -r
