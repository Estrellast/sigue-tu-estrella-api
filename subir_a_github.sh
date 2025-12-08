#!/bin/bash

# Script para subir código a GitHub automáticamente
# Ejecutar con: bash subir_a_github.sh

cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere

echo "🔧 Configurando Git..."
git config user.name "Estrellast"
git config user.email "tu-email@example.com"

echo "📦 Añadiendo archivos..."
git add .

echo "💾 Haciendo commit..."
git commit -m "Deploy completo - Sigue Tu Estrella API" || echo "Ya existe commit"

echo "🔗 Configurando remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Estrellast/sigue-tu-estrella-api.git

echo "📤 Subiendo a GitHub..."
echo "⚠️  Se te pedirá usuario y token:"
echo "   Username: Estrellast"
echo "   Password: [Pega tu Personal Access Token]"
echo ""

git push -u origin main

echo "✅ ¡Completado!"
