# Describir brevemente las similitudes y diferencias entre la tabla de rutas utilizadas para esta actividad vs tabla de rutas real
## Similitudes

* **Propósito:** Ambas determinan el siguiente salto (*gateway*) necesario para redirigir un paquete hacia su destino final.
* **Autonomía:** Cada router gestiona su propia tabla de manera independiente.

## Diferencias

* **Criterio de enrutamiento:** La simulación decide la ruta según **rangos de puertos** (sobre la IP local `127.0.0.1`). En la realidad, se decide exclusivamente por **rangos de direcciones IP** (subredes CIDR).
* **Función de los puertos:** En la actividad, los puertos se usan para simular diferentes dispositivos (*hosts*). En la realidad, los routers no los miran para enrutar; se usan para identificar **procesos o aplicaciones** dentro de una misma máquina.
* **Soporte de almacenamiento:** La simulación emplea un archivo de texto plano (`.txt`). Un router real utiliza estructuras de datos dinámicas en su memoria interna (RAM/TCAM) actualizadas por protocolos de red.



Mecanismo de Recepción de Información:
Para la interacción con el script emisor, se optó por una interfaz de línea de comandos basada en argumentos posicionales (sys.argv). La sintaxis definida para la ejecución del programa es la siguiente:
Bash

% python3 sender.py IP_final puerto_final "mensaje" IP_envio puerto_envio

Justificación técnica de la elección:

    Separación de direccionamiento lógico y físico: El script permite diferenciar claramente el Destino Final (IP_final, puerto_final) —el cual viaja oculto y encapsulado dentro de los primeros 6 bytes del paquete— del Destino de Envío inmediato (IP_envio, puerto_envio), que representa el nodo o router adyacente que recibirá el paquete en primera instancia para procesar su enrutamiento.

    Automatización: El uso de parámetros por consola evita las interrupciones por bloqueos de entrada interactiva (input()), facilitando la creación posterior de scripts automatizados (archivos .sh o .bat) que levanten múltiples emisores en paralelo dentro del escenario del mini-Internet.

    Manejo de strings complejos: Al encerrar el mensaje entre comillas dobles, el sistema operativo interpreta la cadena de texto completa como un único argumento, permitiendo el envío seguro de mensajes que contengan espacios.