#!/usr/bin/env python3
"""
Script para extraer el texto del PDF de Ali Aben Ragel 
"El Libro Conplido en los Iudizios de las Estrellas"

Fuente: Biblioteca Virtual Miguel de Cervantes
Edición: Madrid, Real Academia Española, 1954
"""

import pdfplumber
import json
import re
import os

PDF_PATH = "static/data/aben_ragel_libro_conplido.pdf"
OUTPUT_PATH = "static/data/aben_ragel_texto_completo.txt"
JSON_OUTPUT = "static/data/aben_ragel_capitulos.json"

def extract_text_from_pdf():
    """Extrae todo el texto del PDF"""
    print(f"Abriendo PDF: {PDF_PATH}")
    
    full_text = []
    
    with pdfplumber.open(PDF_PATH) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total de páginas: {total_pages}")
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"\n--- PÁGINA {i+1} ---\n")
                full_text.append(text)
            
            if (i + 1) % 10 == 0:
                print(f"  Procesadas {i+1}/{total_pages} páginas...")
    
    return "\n".join(full_text)

def save_text(text):
    """Guarda el texto extraído"""
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Texto guardado en: {OUTPUT_PATH}")
    print(f"Total caracteres: {len(text):,}")

def extract_chapters(text):
    """Intenta identificar los capítulos/secciones del libro"""
    chapters = {}
    
    # El libro tiene estructura en "Libros" y "Capítulos"
    # Buscar patrones como "Libro primero", "Capítulo I", etc.
    
    # Dividir por "libro" 
    libro_pattern = r'(libro\s+(?:primero|segundo|tercero|quarto|quinto|sesto|seteno|ocheno))'
    matches = re.finditer(libro_pattern, text.lower())
    
    positions = [(m.start(), m.group(1)) for m in matches]
    print(f"Encontrados {len(positions)} libros")
    
    return positions

def main():
    print("=" * 60)
    print("Extrayendo texto de Ali Aben Ragel")
    print("El Libro Conplido en los Iudizios de las Estrellas")
    print("=" * 60)
    
    # Extraer texto
    text = extract_text_from_pdf()
    
    # Guardar texto completo
    save_text(text)
    
    # Mostrar una muestra del texto
    print("\n" + "=" * 60)
    print("MUESTRA DEL TEXTO (primeros 2000 caracteres):")
    print("=" * 60)
    print(text[:2000])
    
    # Buscar capítulos
    print("\n" + "=" * 60)
    print("BUSCANDO ESTRUCTURA DEL LIBRO...")
    print("=" * 60)
    chapters = extract_chapters(text)
    for pos, name in chapters[:10]:
        print(f"  - {name} (posición: {pos})")

if __name__ == "__main__":
    main()
