# Verificación de Control de Congestión

## Test Sin Pérdidas (Actual) ✓

### Test 1: Mensaje de 16 bytes
```
Inicio (Slow Start):
  window_size = 1 MSS ✓
  
Después de 3 ACKs:
  window_size = 4 MSSs ✓
  
Comportamiento: CORRECTO
  - Inicia en 1 MSS
  - Crece +1 MSS por cada ACK enviado
  - Sigue fase Slow Start
```

### Test 2 y 3: Observaciones
- La ventana **NO reinicia** entre envíos (estado persistente)
- cwnd **persiste** del Test 1 al Test 2
- Esto es **CORRECTO** si cada `send()` es un contexto nuevamente creado

## Test CON PÉRDIDA (Pendiente)

Para verificar correctamente:

1. **Inducir TIMEOUT** con `sudo ./test/test_with_loss.sh 30`
2. **Verificar que en TIMEOUT:**
   ```
   [CC Debug] TIMEOUT
     cwnd: 8 bytes  (debe volver a 1 MSS)
     ssthresh: ? (debe ser mitad del cwnd anterior)
   ```

3. **Verificar transición a Congestion Avoidance:**
   - Si ssthresh se alcanza
   - cwnd debe crecer +1 MSS por ventana completa (no por ACK)

## Resumen de Reglas

| Situación | window_size | Regla |
|-----------|-------------|-------|
| Inicio | 1 MSS | Siempre |
| Slow Start + ACK | +1 MSS | Por cada ACK individual |
| Timeout | Reset a 1 MSS | ssthresh = cwnd_anterior / 2 |
| cwnd >= ssthresh | Congestion Avoidance | +1 MSS por ventana completa |

