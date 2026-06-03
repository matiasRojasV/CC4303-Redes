# Ejemplo 1
## Levantar los Routers
python3 router.py 127.0.0.1 8881 tabla_de_rutas/v1/rutas_R1_v1.txt
python3 router.py 127.0.0.1 8882 tabla_de_rutas/v1/rutas_R2_v1.txt


## Caso A: Mandar un mensaje a R1 cuyo destino final es el mismo R1
python3 sender.py 127.0.0.1 8881 "Hola R1, eres mi destino final" 127.0.0.1 8881

## Caso B: Mandar un mensaje a R1 pero cuyo destino final es R2 (Enrutamiento)
python3 sender.py 127.0.0.1 8882 "hola R2!" 127.0.0.1 8881


# Ejemplo 2
## Levantar los Routers
python3 router.py 127.0.0.1 8881 tabla_de_rutas/v2/rutas_R1_v2.txt
python3 router.py 127.0.0.1 8882 tabla_de_rutas/v2/rutas_R2_v2.txt
python3 router.py 127.0.0.1 8883 tabla_de_rutas/v2/rutas_R3_v2.txt

## Caso A: Encriptar y enviar un mensaje desde R1 hacia el extremo R3 (Multi-salto)
python3 sender.py 127.0.0.1 8883 "Mensaje cruzando todo el mini-Internet" 127.0.0.1 8881

## Caso B: Enviar un paquete a un destino fuera de rango (Descarte de paquetes)
python3 sender.py 127.0.0.1 8884 "Hola, ¿hay alguien ahí?" 127.0.0.1 8881



# test roundrobin
python3 c3/ac5/router.py 127.0.0.1 8881 c3/ac5/tabla_de_rutas/v3/rutas_R1_v3.txt &
python3 c3/ac5/router.py 127.0.0.1 8882 c3/ac5/tabla_de_rutas/v3/rutas_R2_v3.txt &
python3 c3/ac5/router.py 127.0.0.1 8883 c3/ac5/tabla_de_rutas/v3/rutas_R3_v3.txt &
python3 c3/ac5/router.py 127.0.0.1 8884 c3/ac5/tabla_de_rutas/v3/rutas_R4_v3.txt &
python3 c3/ac5/router.py 127.0.0.1 8885 c3/ac5/tabla_de_rutas/v3/rutas_R5_v3.txt 
killall python3

python3 c3/ac5/sender.py 127.0.0.1 8881 "cruzando todo el Internet" 127.0.0.1 8885
5421
5321
54535421
5321
54535421
5321
54535421
5321
54535421


# test roundrobin v2
python3 c3/ac5/router.py 127.0.0.1 8880 c3/ac5/tabla_de_rutas/v4/rutas_R0_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8881 c3/ac5/tabla_de_rutas/v4/rutas_R1_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8882 c3/ac5/tabla_de_rutas/v4/rutas_R2_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8883 c3/ac5/tabla_de_rutas/v4/rutas_R3_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8884 c3/ac5/tabla_de_rutas/v4/rutas_R4_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8885 c3/ac5/tabla_de_rutas/v4/rutas_R5_v4.txt &
python3 c3/ac5/router.py 127.0.0.1 8886 c3/ac5/tabla_de_rutas/v4/rutas_R6_v4.txt 

killall python3

python3 c3/ac5/sender.py 127.0.0.1 8881 "cruzando todo el mini-Internet" 127.0.0.1 8885
54201
5321
545354201
53621
5453201
5421
53545363201

python3 c3/ac5/sender.py 127.0.0.1 8885 "cruzando todo el mini-Internet" 127.0.0.1 8881
101232426235
10245
1263623242635
101236245
10263235
124262363245

# test roundrobin default router
python3 c3/ac5/router.py 127.0.0.1 8880 c3/ac5/tabla_de_rutas/v5/rutas_R0_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8881 c3/ac5/tabla_de_rutas/v5/rutas_R1_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8882 c3/ac5/tabla_de_rutas/v5/rutas_R2_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8883 c3/ac5/tabla_de_rutas/v5/rutas_R3_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8884 c3/ac5/tabla_de_rutas/v5/rutas_R4_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8885 c3/ac5/tabla_de_rutas/v5/rutas_R5_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 8886 c3/ac5/tabla_de_rutas/v5/rutas_R6_v5.txt &
python3 c3/ac5/router.py 127.0.0.1 7000 c3/ac5/tabla_de_rutas/v5/rutas_RD_v5.txt


python3 c3/ac5/sender.py 127.0.0.1 7000 "cruzando todo el mini-Internet" 127.0.0.1 8885




# test v2 modificado
Usando las rutas del ejemplo 2 de la sección anterior, pruebe qué ocurre si alguien configura mal una de las tablas de rutas y coméntelo brevemente en su informe. Para ello, cambie la configuración de la tabla de rutas del archivo rutas_R2_v2.txt  por: 

bucle entre r1 y r2
[2] redirigiendo paquete hacia ('127.0.0.1', 8881)
[1] redirigiendo paquete hacia ('127.0.0.1', 8882)
[2] redirigiendo paquete hacia ('127.0.0.1', 8881)
[1] redirigiendo paquete hacia ('127.0.0.1', 8882)
[2] redirigiendo paquete hacia ('127.0.0.1', 8881)
[1] redirigiendo paquete hacia ('127.0.0.1', 8882)
[2] redirigiendo paquete hacia ('127.0.0.1', 8881)