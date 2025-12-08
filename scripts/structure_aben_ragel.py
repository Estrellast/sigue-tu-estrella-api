#!/usr/bin/env python3
"""
Script para estructurar el texto de Ali Aben Ragel
y extraer las interpretaciones de planetas en signos/fazes

El libro tiene la siguiente estructura:
- Libro Primero: Naturaleza de los signos y planetas
- Libro Segundo: Juicios sobre natividades  
- Libro Tercero: Revoluciones de años
- Libro Quarto: Elecciones
- Libro Quinto: Interrogaciones
"""

import re
import json

INPUT_FILE = "static/data/aben_ragel_texto_completo.txt"
OUTPUT_FILE = "static/data/interpretaciones_aben_ragel.json"

def load_text():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def extract_planet_descriptions(text):
    """Extrae las descripciones de los planetas"""
    planets = {}
    
    # Patrones para encontrar descripciones de planetas
    planet_patterns = [
        (r'De Saturno\.(.*?)(?=De Jupiter|De Mars|De Sol|De Venus|De Mercurio|De Luna|\Z)', 'Saturno'),
        (r'De Jupiter\.(.*?)(?=De Saturno|De Mars|De Sol|De Venus|De Mercurio|De Luna|\Z)', 'Jupiter'),
        (r'De Mars\.(.*?)(?=De Saturno|De Jupiter|De Sol|De Venus|De Mercurio|De Luna|\Z)', 'Marte'),
        (r'De Sol\.(.*?)(?=De Saturno|De Jupiter|De Mars|De Venus|De Mercurio|De Luna|\Z)', 'Sol'),
        (r'De Venus\.(.*?)(?=De Saturno|De Jupiter|De Mars|De Sol|De Mercurio|De Luna|\Z)', 'Venus'),
        (r'De Mercurio\.(.*?)(?=De Saturno|De Jupiter|De Mars|De Sol|De Venus|De Luna|\Z)', 'Mercurio'),
        (r'De Luna\.(.*?)(?=De Saturno|De Jupiter|De Mars|De Sol|De Venus|De Mercurio|\Z)', 'Luna'),
    ]
    
    for pattern, planet_name in planet_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            # Limpiar el texto
            description = re.sub(r'\s+', ' ', description)
            description = description[:3000]  # Limitar longitud
            planets[planet_name] = description
            print(f"  Encontrado: {planet_name} ({len(description)} caracteres)")
    
    return planets

def extract_planet_in_signs(text, planet_name):
    """Extrae las interpretaciones de un planeta en cada signo"""
    signs = {}
    
    # Patrones para signos
    sign_names = {
        'Aries': ['Aries', 'aries'],
        'Tauro': ['Tauro', 'Tauru'],
        'Geminis': ['Gemini', 'Geminis'],
        'Cancer': ['Cancer', 'Cancar'],
        'Leo': ['Leon', 'Leo'],
        'Virgo': ['Virgo'],
        'Libra': ['Libra'],
        'Escorpio': ['Escorpi', 'Escorpion'],
        'Sagitario': ['Sagitar'],
        'Capricornio': ['Capricor', 'Capricorno'],
        'Acuario': ['Aquari', 'Aquario'],
        'Piscis': ['Pisc', 'Piscis']
    }
    
    # Buscar menciones de cada signo cerca del planeta
    planet_section_start = text.lower().find(f"de {planet_name.lower()}")
    if planet_section_start == -1:
        return signs
    
    planet_section = text[planet_section_start:planet_section_start + 5000]
    
    for sign_spanish, sign_variants in sign_names.items():
        for variant in sign_variants:
            pattern = rf'(?:en|de)\s+(?:la\s+)?(?:primara|segunda|tercera)?\s*(?:faz\s+de\s+)?{variant}'
            matches = list(re.finditer(pattern, planet_section, re.IGNORECASE))
            if matches:
                # Obtener contexto alrededor de la primera mención
                first_match = matches[0]
                start = max(0, first_match.start() - 50)
                end = min(len(planet_section), first_match.end() + 200)
                context = planet_section[start:end].strip()
                context = re.sub(r'\s+', ' ', context)
                signs[sign_spanish] = context
    
    return signs

def main():
    print("=" * 60)
    print("Estructurando el texto de Ali Aben Ragel")
    print("El Libro Conplido en los Iudizios de las Estrellas")
    print("=" * 60)
    
    text = load_text()
    print(f"Texto cargado: {len(text):,} caracteres")
    
    # Buscar secciones de planetas
    print("\nBuscando descripciones de planetas...")
    planets = extract_planet_descriptions(text)
    
    # Crear estructura JSON
    output = {
        "source": {
            "book": "El Libro Conplido en los Iudizios de las Estrellas",
            "author": "Ali Aben Ragel (Ibn Abi 'l-Ridjal)",
            "translator": "Corte de Alfonso el Sabio",
            "year_original": "Siglo XIII",
            "edition": "Real Academia Española, 1954",
            "source_url": "https://www.cervantesvirtual.com/obra/el-libro-conplido-de-los-iudizios-de-las-estrellas--0/",
            "license": "Dominio Público"
        },
        "autor": {
            "id": "ali_aben_ragel",
            "nombre": "Ali Aben Ragel",
            "nombre_arabe": "Ibn Abi 'l-Ridjal",
            "obra_principal": "El Libro Conplido en los Iudizios de las Estrellas",
            "enfoque": "Astrología Medieval Árabe - Dignidades y Temperamentos"
        },
        "interpretaciones": {
            "planetas": planets,
            "planetas_signos": {}
        }
    }
    
    # Extraer interpretaciones específicas de Saturno en signos (como ejemplo)
    print("\nExtrayendo interpretaciones de Saturno en signos...")
    
    # Buscar la sección de Saturno en el texto
    saturno_start = text.find("De Saturno.")
    if saturno_start != -1:
        saturno_section = text[saturno_start:saturno_start + 6000]
        
        # Extraer cada faz/signo
        fazes = {
            "Saturno_Aries": "En la primara faz de Aries",
            "Saturno_Tauro": "En la primara faz de Tauro",
            "Saturno_Geminis": "En todo Gemini",
            "Saturno_Cancer": "En todo Cancar",
            "Saturno_Leo": "En la primara faz de Leon",
            "Saturno_Virgo": "En la primara faz de Virgo",
            "Saturno_Libra": "En la primara faz de Libra",
            "Saturno_Escorpio": "En la primara faz de Escorpión",
            "Saturno_Sagitario": "En todas las fazes de Sagitario",
            "Saturno_Capricornio": "En la primara faz de Capricorno",
            "Saturno_Acuario": "En todas las partes de Aquavio",
            "Saturno_Piscis": "En la primera parte de Piscis"
        }
        
        for key, pattern in fazes.items():
            idx = saturno_section.lower().find(pattern.lower())
            if idx != -1:
                # Obtener texto hasta el siguiente "En la" o "En todo"
                end_idx = idx + 300
                interpretation = saturno_section[idx:end_idx]
                interpretation = re.sub(r'\s+', ' ', interpretation).strip()
                output["interpretaciones"]["planetas_signos"][key] = {
                    "texto": f"(Ali Aben Ragel) {interpretation}"
                }
                print(f"  ✓ {key}")
    
    # Hacer lo mismo para Júpiter
    print("\nExtrayendo interpretaciones de Júpiter en signos...")
    jupiter_start = text.find("De Jupiter.")
    if jupiter_start != -1:
        jupiter_section = text[jupiter_start:jupiter_start + 6000]
        
        fazes_jupiter = {
            "Jupiter_Aries": "Es en todas las partes de Aries",
            "Jupiter_Tauro": "En la primara faz de Tauro",
            "Jupiter_Geminis": "En la primera faz de Gemini",
            "Jupiter_Cancer": "En la primaza faz de Cancer",
            "Jupiter_Leo": "En la primara faz de Leon",
            "Jupiter_Virgo": "En la primara faz de Virgo",
            "Jupiter_Libra": "En la primara faz de Libra",
            "Jupiter_Escorpio": "En la primara faz de Escorpión",
            "Jupiter_Sagitario": "En todas las fazes de Sagitario",
            "Jupiter_Capricornio": "En la primara faz de Capricorno",
            "Jupiter_Acuario": "En todas las partes de Aquario",
            "Jupiter_Piscis": "En la primera parte de Piscis"
        }
        
        for key, pattern in fazes_jupiter.items():
            idx = jupiter_section.lower().find(pattern.lower())
            if idx != -1:
                end_idx = idx + 300
                interpretation = jupiter_section[idx:end_idx]
                interpretation = re.sub(r'\s+', ' ', interpretation).strip()
                output["interpretaciones"]["planetas_signos"][key] = {
                    "texto": f"(Ali Aben Ragel) {interpretation}"
                }
                print(f"  ✓ {key}")
    
    # Guardar JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON guardado en: {OUTPUT_FILE}")
    print(f"   Planetas extraídos: {len(planets)}")
    print(f"   Interpretaciones planeta-signo: {len(output['interpretaciones']['planetas_signos'])}")

if __name__ == "__main__":
    main()
