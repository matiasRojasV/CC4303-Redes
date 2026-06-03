# Describir brevemente las similitudes y diferencias entre la tabla de rutas utilizadas para esta actividad vs tabla de rutas real
## Similitudes

* **Propósito:** Ambas determinan el siguiente salto (*gateway*) necesario para redirigir un paquete hacia su destino final.
* **Autonomía:** Cada router gestiona su propia tabla de manera independiente.

## Diferencias

* **Criterio de enrutamiento:** La simulación decide la ruta según **rangos de puertos** (sobre la IP local `127.0.0.1`). En la realidad, se decide exclusivamente por **rangos de direcciones IP** (subredes CIDR).
* **Función de los puertos:** En la actividad, los puertos se usan para simular diferentes dispositivos (*hosts*). En la realidad, los routers no los miran para enrutar; se usan para identificar **procesos o aplicaciones** dentro de una misma máquina.
* **Soporte de almacenamiento:** La simulación emplea un archivo de texto plano (`.txt`). Un router real utiliza estructuras de datos dinámicas en su memoria interna (RAM/TCAM) actualizadas por protocolos de red.



# Mecanismo de Recepción de Información:
Para la interacción con el script emisor, se optó por una interfaz de línea de comandos basada en argumentos posicionales (sys.argv). La sintaxis definida para la ejecución del programa es la siguiente:

% python3 sender.py IP_final puerto_final "mensaje" IP_envio puerto_envio

Justificación técnica de la elección:

    Separación de direccionamiento lógico y físico: El script permite diferenciar claramente el Destino Final (IP_final, puerto_final) —el cual viaja oculto y encapsulado dentro de los primeros 6 bytes del paquete— del Destino de Envío inmediato (IP_envio, puerto_envio), que representa el nodo o router adyacente que recibirá el paquete en primera instancia para procesar su enrutamiento.

    Automatización: El uso de parámetros por consola evita las interrupciones por bloqueos de entrada interactiva (input()), facilitando la creación posterior de scripts automatizados (archivos .sh o .bat) que levanten múltiples emisores en paralelo dentro del escenario del mini-Internet.

    Manejo de strings complejos: Al encerrar el mensaje entre comillas dobles, el sistema operativo interpreta la cadena de texto completa como un único argumento, permitiendo el envío seguro de mensajes que contengan espacios.






# **Manejo de Round-Robin**

Para el balanceo de carga se utilizó Programación Orientada a Objetos mediante la clase `RouterState`, la cual centraliza y aísla el historial de reenvíos en un diccionario interno llamado `areas_state`:

* **Identificación por Área:** Cada zona o subred se registra de forma independiente usando una tupla `(cidr, puerto_inicio, puerto_final)` como clave del diccionario. Esto permite al router escalar y memorizar rutas en paralelo para un número arbitrario de destinos independientes.
* **Algoritmo de Rotación:** Al resolver el siguiente salto en `check_routes`, el método `get_next_route` selecciona el camino correspondiente al índice actual de esa subred y actualiza la posición usando aritmética modular: `(current_index + 1) % len(matching_routes)`.

Este diseño distribuye el tráfico de manera estrictamente equitativa y cíclica entre los enlaces redundantes disponibles, evitando la sobrecarga y prescindiendo del uso de variables globales complejas.




# Pruebas Mini-Internet sin TTL (Informe 1pto):

### Análisis de Saltos en la Red

Los paquetes realizaron entre **4 y 8 saltos**, dependiendo de la ruta seguida. La 
cantidad de saltos no fue constante, evidenciando que el enrutamiento varía entre pruebas.

La ruta más corta observada requirió **4 saltos** (1 → 2 → 4 → 5). Sin embargo, la 
mayoría de los paquetes recorrió más saltos debido a que pasaron varias veces por 
los mismos routers antes de llegar al destino.

### Conclusión

Los resultados sugieren la presencia de **bucles de enrutamiento** o una convergencia 
incompleta de las tablas de rutas, lo que provoca que algunos paquetes sigan caminos 
más largos que la ruta óptima y aumenten la cantidad de saltos necesarios para alcanzar 
el destino.



### Observaciones de las Pruebas

Se repitieron las pruebas utilizando una topología de **7 routers**, correspondiente a la 
estructura solicitada en el Test 2 del Paso 8. Al comparar los resultados con la red anterior, 
se observó que la cantidad de saltos aumentó debido al mayor número de nodos y rutas posibles 
dentro de la red.

Los paquetes realizaron entre **4 y 12 saltos**, dependiendo de la ruta seguida. La cantidad de 
saltos no fue constante, ya que algunos paquetes recorrieron caminos más largos y pasaron varias 
veces por los mismos routers antes de llegar al destino.

La ruta mínima observada requirió **4 saltos**, mientras que otras alcanzaron hasta **12 saltos**, 
evidenciando la presencia de rutas alternativas y posibles bucles de enrutamiento.

### Conclusión

Los resultados muestran que, al aumentar el tamaño de la red a 7 routers, también aumenta la variabilidad 
en las rutas y la cantidad de saltos que realizan los paquetes. Esto sugiere la existencia de múltiples 
caminos hacia el destino y posibles períodos de convergencia de las tablas de rutas, provocando que 
algunos paquetes sigan trayectorias más largas que la ruta óptima.

Además, se incluyen en el informe los contenidos de los distintos archivos de rutas utilizados para 
la configuración de la red.


# ¿En que posición (línea) de la tabla debería ir la ruta default? Añada en su informe cómo queda su nueva tabla de rutas y la respuesta a esta pregunta.
La ruta default (0.0.0.0/0) debe ir al final de la tabla de rutas, después de todas las rutas específicas.

Razón: Las tablas de rutas se procesan de arriba hacia abajo. Al tener la ruta default al final, se garantiza que:

Primero se intenten las rutas específicas (más precisas)
Solo si no coincide ninguna ruta específica, se usa la ruta default como "catch-all"