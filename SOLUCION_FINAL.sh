#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "  🔑 CREAR TOKEN Y SUBIR A GITHUB"
echo "════════════════════════════════════════════════════"
echo ""
echo "PASO 1: Crear un nuevo token"
echo "----------------------------"
echo "1. Abre Safari y ve a: https://github.com/settings/tokens/new"
echo "2. Note: 'Render Deploy'"
echo "3. Expiration: '90 days'"
echo "4. Marca SOLO: ✅ repo (todos los sub-permisos)"
echo "5. Click 'Generate token'"
echo "6. COPIA el token (ghp_...)"
echo ""
echo "════════════════════════════════════════════════════"
echo ""
read -p "Pega el token aquí y presiona ENTER: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ No ingresaste ningún token"
    exit 1
fi

echo "Configurando Git..."
cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere

# Remover y recrear remote con token
git remote remove origin 2>/dev/null
git remote add origin https://${TOKEN}@github.com/Estrellast/sigue-tu-estrella-api.git

echo "Subiendo archivos a GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ✅ ¡ÉXITO! Archivos subidos a GitHub"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "Ahora:"
    echo "1. Ve a Render en Safari"
    echo "2. Click en 'Manual Deploy' → 'Deploy latest commit'"
    echo "3. Espera 2-3 minutos"
    echo "4. Copia la URL que te dé Render"
    echo ""
else
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ❌ ERROR"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "El token puede ser inválido. Verifica que:"
    echo "- Copiaste el token completo"
    echo "- Marcaste el permiso 'repo'"
    echo ""
fi
