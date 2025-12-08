#!/bin/bash

# Configurar Git para no pedir credenciales
export GIT_TERMINAL_PROMPT=0

# Cambiar remote a usar formato que no requiere autenticación para repos públicos
cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere

git remote remove origin
git remote add origin https://github.com/Estrellast/sigue-tu-estrella-api.git

# Intentar push
git push -u origin main --verbose

echo ""
echo "Estado del push:"
git log --oneline -3
