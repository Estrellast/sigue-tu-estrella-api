#!/usr/bin/env bash
# Script para instalar dependencias del sistema en Render

# Instalar herramientas de compilación necesarias para pyswisseph
apt-get update
apt-get install -y build-essential

# Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt
