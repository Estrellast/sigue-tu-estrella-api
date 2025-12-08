#!/usr/bin/env python3
"""
Script para descargar y estructurar los textos completos de 
"The Message of the Stars" de Max Heindel desde rosicrucian.com

Este libro está en dominio público (1918) y contiene interpretaciones
de todos los planetas en signos y aspectos entre planetas.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.rosicrucian.com/mos/"

# URLs de los capítulos relevantes
CHAPTERS = {
    "moseng03.htm": ["Sun", "Venus"],  # Sol en signos, Venus en signos
    "moseng04.htm": ["Mercury", "Moon", "Saturn"],  # Mercurio, Luna, Saturno
    "moseng05.htm": ["Jupiter", "Mars_Houses"],  # Júpiter en signos
    "moseng06.htm": ["Mars", "Uranus"],  # Marte en signos, Urano
}

def download_chapter(filename):
    """Descarga un capítulo del libro"""
    url = BASE_URL + filename
    print(f"Descargando: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return None

def extract_planet_in_signs(html_content, planet_name):
    """Extrae las interpretaciones de un planeta en los 12 signos"""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    sign_map = {
        "Aries": "Aries", "Taurus": "Tauro", "Gemini": "Geminis", 
        "Cancer": "Cancer", "Leo": "Leo", "Virgo": "Virgo",
        "Libra": "Libra", "Scorpio": "Escorpio", "Sagittarius": "Sagitario",
        "Capricorn": "Capricornio", "Aquarius": "Acuario", "Pisces": "Piscis"
    }
    
    interpretations = {}
    
    for i, sign in enumerate(signs):
        # Buscar el patrón "PLANET in SIGN"
        pattern = rf'{planet_name}\s+in\s+{sign}[.,\s]+'
        
        # Buscar el inicio del texto
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = match.end()
            
            # Buscar el final (siguiente sección o planeta)
            if i < len(signs) - 1:
                next_sign = signs[i + 1]
                end_pattern = rf'{planet_name}\s+in\s+{next_sign}'
                end_match = re.search(end_pattern, text[start:], re.IGNORECASE)
                if end_match:
                    end = start + end_match.start()
                else:
                    end = start + 2000  # Fallback
            else:
                end = start + 2000
            
            interpretation = text[start:end].strip()
            # Limpiar el texto
            interpretation = re.sub(r'\s+', ' ', interpretation)
            interpretation = interpretation[:1500]  # Limitar longitud
            
            spanish_sign = sign_map[sign]
            interpretations[spanish_sign] = interpretation
    
    return interpretations

def extract_aspects(html_content, planet1, planet2):
    """Extrae las interpretaciones de aspectos entre dos planetas"""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    aspects = {}
    
    # Buscar diferentes tipos de aspectos
    aspect_patterns = [
        (rf'{planet1}\s+(sextile|trine)\s+(to\s+)?{planet2}', "sextile_trine"),
        (rf'{planet1}\s+(square|opposition)\s+(to\s+)?{planet2}', "square_opposition"),
        (rf'{planet1}\s+conjunction\s+(to\s+)?{planet2}', "conjunction"),
        (rf'{planet1}\s+parallel\s+(to\s+)?{planet2}', "parallel"),
    ]
    
    for pattern, aspect_type in aspect_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = match.end()
            # Obtener siguiente párrafo
            interpretation = text[start:start+1000].strip()
            interpretation = re.sub(r'\s+', ' ', interpretation)
            aspects[aspect_type] = interpretation[:800]
    
    return aspects

def main():
    """Función principal"""
    print("=" * 60)
    print("Descargando 'The Message of the Stars' de Max Heindel")
    print("Fuente: rosicrucian.com (Dominio Público)")
    print("=" * 60)
    
    all_data = {
        "source": {
            "book": "The Message of the Stars",
            "author": "Max Heindel and Augusta Foss Heindel",
            "year": 1918,
            "source_url": "https://www.rosicrucian.com/mos/moseng11.htm",
            "license": "Public Domain"
        },
        "planets_in_signs": {},
        "aspects": {}
    }
    
    # Descargar cada capítulo
    for filename, planets in CHAPTERS.items():
        html = download_chapter(filename)
        if html:
            for planet in planets:
                if planet == "Mars_Houses":
                    continue  # Solo necesitamos signos
                print(f"  Extrayendo: {planet} en signos...")
                interpretations = extract_planet_in_signs(html, planet)
                if interpretations:
                    all_data["planets_in_signs"][planet] = interpretations
                    print(f"    Encontrado: {len(interpretations)} signos")
        time.sleep(0.5)  # Ser amable con el servidor
    
    # Guardar resultados
    output_path = "../static/data/heindel_complete.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Datos guardados en: {output_path}")
    print(f"   Planetas procesados: {len(all_data['planets_in_signs'])}")

if __name__ == "__main__":
    main()
