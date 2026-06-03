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
Bash

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

## ¿Cuántos saltos dan los paquetes?

Los paquetes realizan **3 o 5 saltos**, dependiendo de la ruta utilizada.

## ¿Siempre dan la misma cantidad de saltos?

No. Algunos paquetes recorren **3 saltos** y otros **5 saltos**, por lo que la cantidad de saltos varía según la ruta seleccionada.

## ¿Cómo se compara con la cantidad mínima de saltos?

La ruta mínima entre R1 y R5 es de **3 saltos**. Algunos paquetes siguen esta ruta óptima, mientras que otros toman rutas alternativas de **5 saltos**, superando el mínimo.

## Observación

Como existen múltiples rutas hacia el destino, algunos paquetes siguen el camino más corto y otros toman rutas más largas, lo que sugiere un balanceo de carga o decisiones de enrutamiento alternativas.
