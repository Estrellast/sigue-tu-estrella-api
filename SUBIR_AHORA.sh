#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "  🚀 SUBIR CÓDIGO A GITHUB - PASO A PASO"
echo "════════════════════════════════════════════════════"
echo ""
echo "IMPORTANTE: Necesitas tu token de GitHub"
echo ""
echo "Si NO tienes el token:"
echo "  1. Ve a: https://github.com/settings/tokens"
echo "  2. Click en 'Generate new token (classic)'"
echo "  3. Nombre: 'Render Deploy'"
echo "  4. Marca SOLO: ✅ repo"
echo "  5. Click 'Generate token'"
echo "  6. COPIA el token (empieza con ghp_...)"
echo ""
echo "════════════════════════════════════════════════════"
echo ""
read -p "Pega tu token aquí: " TOKEN
echo ""
echo "Subiendo archivos a GitHub..."
echo ""

cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere

git push https://$TOKEN@github.com/Estrellast/sigue-tu-estrella-api.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ✅ ¡ÉXITO! Archivos subidos a GitHub"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "Ahora ve a Render y haz click en 'Manual Deploy'"
    echo "Render detectará los archivos y desplegará tu API"
    echo ""
else
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ❌ ERROR al subir"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "Verifica que el token sea correcto"
    echo ""
fi
