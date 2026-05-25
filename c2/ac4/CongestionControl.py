class CongestionControl():
    # current_state: Estado actual dentro de control de congestión, 
    # puede ser slow start o congestion avoidance. 

    # MSS: Tamaño max en bytes del área de datos de un segmento congestión.

    # cwnd: Tamaño de la ventana de congestión en bytes. 

    # ssthresh:  Slow Start threshold. Cuando current_state es slow start 
    # si cwnd >= ssthresh entonces cambia current_state a congestion avoidance.


    def __init__(self, MSS: int):
        self.MSS = MSS
        self.cwnd = 1 * MSS  # Comienza como 1 MSS
        self.current_state = "slow start"  # Comienza en slow start
        self.ssthresh = None  # Se define después del primer timeout

        
    def get_cwnd(self):
        # Retorna el valor cwnd almacenado en bytes.
        return self.cwnd
    

    def get_MSS_in_cwnd(self):
        # Retorna el tamaño de la ventana expresado como la cantidad 
        # de MSSs completos que caben en cwnd.
        return self.cwnd // self.MSS
    

    def event_ack_received(self):
        # Se encarga de manejar los cambios asociados a la recepción de ACKs
        if self.current_state == "slow start":
            self.cwnd += self.MSS

            # Verificar si debe cambiar a congestion avoidance
            if self.ssthresh is not None and self.cwnd >= self.ssthresh:
                self.current_state = "congestion avoidance"

        elif self.current_state == "congestion avoidance":
            # Aumentar cwnd en (1 / get_MSS_in_cwnd()) de MSS
            self.cwnd += self.MSS / self.get_MSS_in_cwnd()
    

    def event_timeout(self):
        # Maneja los cambios asociados a que ocurra timeout
        self.ssthresh = self.cwnd // 2
        
        # Resetear cwnd a 1 MSS
        self.cwnd = 1 * self.MSS
        
        # Volver a slow start
        self.current_state = "slow start"


    def is_state_slow_start(self):
        if self.current_state == "slow start":
            return True
        return False
    

    def is_state_congestion_avoidance(self):
        if self.current_state == "congestion avoidance":
            return True
        return False


    def get_ssthresh(self):
        return self.ssthresh