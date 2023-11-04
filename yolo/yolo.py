import cv2 as cv
import numpy as np

# Cargar el modelo YOLOv8 y sus pesos (debes tener estos archivos en tu sistema)
modelo_yolo = cv.dnn.readNet('ruta_al_archivo.weights', 'ruta_al_archivo.cfg')

# Inicializar la captura de video
cap = cv.VideoCapture('rtsp://homeland:Homeland2019@10.10.1.253:3454/Media/Live/Normal?camera=C_3&streamindex=1')

while True:
    ret, img = cap.read()
    if ret:
        # Redimensionar la imagen
        img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)

        # Realizar la detección de objetos en la imagen
        height, width, _ = img.shape
        blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        modelo_yolo.setInput(blob)
        detections = modelo_yolo.forward()

        # Procesar las detecciones y dibujar los cuadros delimitadores en la imagen (similar al código anterior)

        # Mostrar la imagen con los cuadros delimitadores
        cv.imshow('cap', img)

        key = cv.waitKey(1)
        if key == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break

cap.release()
cv.destroyAllWindows()