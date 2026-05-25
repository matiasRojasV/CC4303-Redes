#!/bin/bash
# Script para probar GBN con pérdida de paquetes

set -e

LOSS_PERCENT=${1:-10}
DEVICE="enp0s3"  

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Test CON PÉRDIDA DE PAQUETES                                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configurando ${LOSS_PERCENT}% de pérdida en ${DEVICE}..."
echo "IP usada: 192.168.1.109"
echo ""

# Verificar que somos root
if [[ $EUID -ne 0 ]]; then
   echo "Este script necesita privilegios de root (sudo)"
   echo "Ejecuta: sudo ./run_test_with_loss.sh ${LOSS_PERCENT}"
   exit 1
fi

# Limpiar configuraciones previas
echo "[*] Limpiando configuraciones previas..."
tc qdisc del dev $DEVICE root 2>/dev/null || true
sleep 1

# Agregar pérdida
echo "[*] Aplicando ${LOSS_PERCENT}% de pérdida..."
tc qdisc add dev $DEVICE root netem loss ${LOSS_PERCENT}%
sleep 1

# Mostrar configuración
echo "[*] Verificando configuración:"
tc qdisc show dev $DEVICE
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ INSTRUCCIONES:                                                 ║"
echo "║ 1. En OTRA terminal: python3 servidor.py                       ║"
echo "║ 2. En OTRA terminal: python3 cliente.py                        ║"
echo "║                                                                ║"
echo "║ Deberías ver retransmisiones y timeouts, pero los archivos     ║"
echo "║ deben llegar correctamente.                                    ║"
echo "║                                                                ║"
echo "║ Cuando termines, presiona ENTER aquí para limpiar...           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

read -p "Presiona ENTER para limpiar la configuración..."

echo ""
echo "[*] Limpiando configuración..."
tc qdisc del dev $DEVICE root
sleep 1

echo "[✓] Configuración limpiada"
echo ""
echo "Para volver a ejecutar: sudo ./run_test_with_loss.sh ${LOSS_PERCENT}"
