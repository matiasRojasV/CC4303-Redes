# Ejemplo 1
## Levantar los Routers
python3 router.py 127.0.0.1 8881 tabla_de_rutas/rutas_R1_v1.txt
python3 router.py 127.0.0.1 8882 tabla_de_rutas/rutas_R2_v1.txt


## Caso A: Mandar un mensaje a R1 cuyo destino final es el mismo R1
python3 sender.py 127.0.0.1 8881 "Hola R1, eres mi destino final" 127.0.0.1 8881

## Caso B: Mandar un mensaje a R1 pero cuyo destino final es R2 (Enrutamiento)
python3 sender.py 127.0.0.1 8882 "hola R2!" 127.0.0.1 8881


# Ejemplo 2
## Levantar los Routers
python3 router.py 127.0.0.1 8881 tabla_de_rutas/rutas_R1_v2.txt
python3 router.py 127.0.0.1 8882 tabla_de_rutas/rutas_R2_v2.txt
python3 router.py 127.0.0.1 8883 tabla_de_rutas/rutas_R3_v2.txt

## Caso A: Encriptar y enviar un mensaje desde R1 hacia el extremo R3 (Multi-salto)
python3 sender.py 127.0.0.1 8883 "Mensaje cruzando todo el mini-Internet" 127.0.0.1 8881

## Caso B: Enviar un paquete a un destino fuera de rango (Descarte de paquetes)
python3 sender.py 127.0.0.1 8884 "Hola, ¿hay alguien ahí?" 127.0.0.1 8881