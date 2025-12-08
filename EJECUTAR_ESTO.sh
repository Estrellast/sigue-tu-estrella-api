#!/bin/bash

echo "════════════════════════════════════════════════════"
echo "  🚀 SUBIR A GITHUB - INSTRUCCIONES FINALES"
echo "════════════════════════════════════════════════════"
echo ""
echo "Cuando ejecutes 'git push origin main', Git te pedirá:"
echo ""
echo "  Username: Estrellast"
echo "  Password: [PEGA TU TOKEN AQUÍ]"
echo ""
echo "Tu token es:"
echo "  ghp_704GXXwYAKiaDzPvkWCNtXDhd3iZ3500JXlf"
echo ""
echo "════════════════════════════════════════════════════"
echo ""
echo "Presiona ENTER para continuar..."
read

cd /Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  ✅ ¡ÉXITO! Código subido a GitHub"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "Ahora ve a Render y haz click en 'Manual Deploy'"
    echo ""
else
    echo ""
    echo "❌ Hubo un error. Verifica el token."
    echo ""
fi
