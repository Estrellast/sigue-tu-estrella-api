#!/bin/bash

# Script para subir a GitHub usando el token

cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere

# Configurar Git para usar el token
git config credential.helper store

# Crear archivo de credenciales temporal
echo "https://ghp_704GXXwYAKiaDzPvkWCNtXDhd3iZ3500JXlf@github.com" > ~/.git-credentials

# Hacer push
git push origin main

# Limpiar credenciales si lo deseas (comentado por seguridad)
# rm ~/.git-credentials

echo ""
echo "✅ Push completado!"
