from flask import Flask, render_template, request
from markupsafe import Markup
from kerykeion import KrInstance, MakeSvgInstance
from kerykeion.utilities.aspects import NatalAspects
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import os
import uuid
import tempfile
import time
import re
import json
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes to allow WordPress AJAX calls

# Initialize Geocoder and TimezoneFinder
geolocator = Nominatim(user_agent="astro_app_sigue_tu_estrella")
tf = TimezoneFinder()

# Helper for calculating time difference for progressions
def get_progressed_date(birth_dt, current_dt):
    """
    Secondary Progressions: 1 day after birth = 1 year of life.
    """
    age_in_years = (current_dt - birth_dt).days / 365.25
    days_to_add = age_in_years # 1 day per year
    
    # Create new date
    from datetime import timedelta
    prog_date = birth_dt + timedelta(days=days_to_add)
    return prog_date

def calculate_aspects_between_charts(chart1_objs, chart2_objs, chart1_name="Natal", chart2_name="Transit"):
    """
    Calculates aspects between two sets of planetary positions.
    chart1_objs: list of dicts {'name': 'Sun', 'position': 123.4} (Natal)
    chart2_objs: list of dicts {'name': 'Sun', 'position': 45.6} (Transit/Prog)
    """
    aspects = []
    
    # Orbs allowed for transits (very tight for significance)
    orb_map = {
        'conjunction': 1.0,
        'opposition': 1.0,
        'square': 1.0,
        'trine': 1.0,
        'sextile': 0.8
    }
    
    for p1 in chart1_objs:
        for p2 in chart2_objs:
            # CRITICAL: Skip same planet (e.g., Sun transit to Sun natal is not interesting)
            if p1['name'] == p2['name']:
                continue
            
            diff = abs(p1['position'] - p2['position'])
            diff = diff % 360
            if diff > 180:
                diff = 360 - diff
            
            aspect_type = None
            orb = 0
            
            # Check aspects with tight orbs
            if diff <= orb_map['conjunction']:
                aspect_type = 'conjuncion'
                orb = diff
            elif abs(diff - 180) <= orb_map['opposition']:
                aspect_type = 'oposicion'
                orb = abs(diff - 180)
            elif abs(diff - 90) <= orb_map['square']:
                aspect_type = 'cuadratura'
                orb = abs(diff - 90)
            elif abs(diff - 120) <= orb_map['trine']:
                aspect_type = 'trigono'
                orb = abs(diff - 120)
            elif abs(diff - 60) <= orb_map['sextile']:
                aspect_type = 'sextil'
                orb = abs(diff - 60)
                
            if aspect_type:
                aspects.append({
                    'p1_name': p1['name'],
                    'p2_name': p2['name'],
                    'type': aspect_type,
                    'orb': orb,
                    'is_transit': True
                })
                
    return aspects


@app.route('/', methods=['GET', 'POST'])
def index():
    chart_data = None
    aspects_data = None
    error = None
    svg_content = None
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', 'Guest')
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            hour = int(request.form['hour'])
            minute = int(request.form['minute'])
            city_input = request.form.get('city', 'Madrid')
            
            # Geolocation with timeout and retry
            location = None
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    location = geolocator.geocode(city_input, timeout=10)
                    if location:
                        break
                except Exception as geo_error:
                    if attempt == max_retries - 1:
                        raise Exception(f"Error al buscar la ciudad '{city_input}': {str(geo_error)}")
                    time.sleep(1)  # Wait before retry
            
            if not location:
                raise Exception(f"No se encontró la ciudad: {city_input}")
            
            lat = location.latitude
            lng = location.longitude
            city_name = location.address.split(",")[0] # Use the first part of the address
            
            # Timezone Detection
            tz_str = tf.timezone_at(lng=lng, lat=lat)
            if not tz_str:
                tz_str = "UTC" # Fallback
            
            # Calculate UTC time from local time
            local_tz = pytz.timezone(tz_str)
            # Create timezone-aware datetime object for the local time
            # We use localize to handle DST correctly
            local_dt_naive = datetime(year, month, day, hour, minute)
            local_dt_aware = local_tz.localize(local_dt_naive)
            
            # Convert to UTC for kerykeion
            utc_dt = local_dt_aware.astimezone(pytz.utc)
            
            # Create Astrological Subject (KrInstance)
            subject = KrInstance(
                name, 
                utc_dt.year, 
                utc_dt.month, 
                utc_dt.day, 
                utc_dt.hour, 
                utc_dt.minute, 
                city=city_name,
                lat=lat,
                lon=lng,
                tz_str="UTC" 
            )
            
            # Calculate all data
            subject.get_all()
            
            # Calculate Aspects
            natal_aspects = NatalAspects(subject)
            aspects_list = natal_aspects.get_aspects()
            aspects_data = []
            for aspect in aspects_list:
                # Filter only major aspects or all? Let's show all relevant ones.
                # aspect is a dict with keys like 'p1_name', 'p2_name', 'aspect', 'orbit'
                aspects_data.append({
                    'p1': aspect['p1_name'],
                    'p2': aspect['p2_name'],
                    'type': aspect['aspect'],
                    'orb': f"{aspect['orbit']:.2f}"
                })
            
            # Generate SVG
            unique_id = str(uuid.uuid4())
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create subject with REAL name for the chart title
                subject_for_svg = KrInstance(
                    name, 
                    utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, 
                    city=city_name, lat=lat, lon=lng, tz_str="UTC"
                )
                subject_for_svg.get_all()
                
                svg_maker = MakeSvgInstance(subject_for_svg, new_output_directory=temp_dir, chart_type="Natal")
                
                # Customize Colors - Dark Mode for Ultra-Modern Look
                # Paper: Transparent to let the cosmic background show through
                svg_maker.colors_settings['paper_0'] = '#000000' 
                svg_maker.colors_settings['paper_1'] = '#000000' 
                
                # Zodiac Ring: Dark semi-transparent
                svg_maker.colors_settings['zodiac_bg_0'] = '#000000' 
                svg_maker.colors_settings['zodiac_bg_1'] = '#000000'
                
                # Icons & Text - WHITE/GOLD for visibility on dark
                svg_maker.colors_settings['zodiac_icon_0'] = '#ffffff'  # White for zodiac symbols
                svg_maker.colors_settings['zodiac_icon_1'] = '#ffffff'
                svg_maker.colors_settings['zodiac_num_0'] = '#ffd700'  # Gold for numbers
                svg_maker.colors_settings['zodiac_num_1'] = '#ffd700' 
                
                # Lines - Light grey/cyan for definition
                svg_maker.colors_settings['zodiac_radix_ring_0'] = '#00d2ff'  # Cyan
                svg_maker.colors_settings['zodiac_radix_ring_1'] = '#00d2ff'
                svg_maker.colors_settings['zodiac_transit_ring_0'] = '#444444'
                svg_maker.colors_settings['zodiac_transit_ring_1'] = '#444444'
                svg_maker.colors_settings['zodiac_transit_ring_2'] = '#444444'
                svg_maker.colors_settings['zodiac_transit_ring_3'] = '#444444'
                
                # Aspects lines - Neon colors
                svg_maker.colors_settings['aspect_0'] = '#00d2ff'  # Conjunction (Cyan)
                svg_maker.colors_settings['aspect_90'] = '#ff4444'  # Square (Red)
                svg_maker.colors_settings['aspect_180'] = '#ff4444'  # Opposition (Red)
                svg_maker.colors_settings['aspect_120'] = '#00ff88'  # Trine (Green)
                svg_maker.colors_settings['aspect_60'] = '#00d2ff'  # Sextile (Cyan)
                
                svg_maker.makeSVG()
                
                generated_files = os.listdir(temp_dir)
                if generated_files:
                    svg_path = os.path.join(temp_dir, generated_files[0])
                    with open(svg_path, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                        
                    # Tweak SVG for better visibility and contrast
                    if '<svg' in svg_content:
                        # Remove fixed width/height
                        svg_content = svg_content.replace('width="772.2"', 'width="100%"').replace('height="546.0"', 'height="100%"')
                        
                        # STEP 1: Make background transparent
                        svg_content = re.sub(
                            r'<rect x="0" y="0" width="100%" height="100%" style="fill:\s*#000000;"\s*/>',
                            '<rect x="0" y="0" width="100%" height="100%" style="fill: none;" />',
                            svg_content
                        )
                        
                        # STEP 2: Make zodiac ring background transparent/dark
                        svg_content = re.sub(
                            r'fill:#000000;\s*fill-opacity:\s*0\.[0-9]+',
                            'fill:none;', 
                            svg_content
                        )
                        
                        # STEP 3: Ensure text is white
                        svg_content = re.sub(
                            r'(<text[^>]*style="[^"]*fill:\s*)#000000',
                            r'\1#ffffff',
                            svg_content
                        )
                        
                        # STEP 4: Ensure planet symbols (paths) are white
                        svg_content = re.sub(
                            r'(<path[^>]*d="M[^M]{1,200}"[^>]*style="fill:)#000000',
                            r'\1#ffffff',
                            svg_content
                        )
                        
                        # STEP 5: House numbers to Gold
                        svg_content = re.sub(
                            r'(font-size:[^;]+;[^"]*fill:\s*)#000000',
                            r'\1#ffd700',
                            svg_content
                        )
            
            # Extract data for table
            chart_data = []
            
            def fmt_deg(deg):
                return f"{deg:.2f}"
            
            # Author Selection Logic
            author_id = request.form.get('author_id', 'ali_aben_ragel')
            
            # Load Interpretations from JSON - Try complete Heindel file first
            author_data = {}
            author_info = {}
            aspects_data_db = {}
            
            try:
                # For max_heindel, use the complete authentic texts
                if author_id == 'max_heindel':
                    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_heindel_completo.json')
                    with open(json_path, 'r', encoding='utf-8') as f:
                        heindel_db = json.load(f)
                        author_data = heindel_db.get('interpretaciones', {}).get('planetas_signos', {})
                        aspects_data_db = heindel_db.get('interpretaciones', {}).get('aspectos', {})
                        author_info = heindel_db.get('autor', {})
                
                # For ali_aben_ragel, use the medieval original texts
                elif author_id == 'ali_aben_ragel':
                    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_aben_ragel.json')
                    with open(json_path, 'r', encoding='utf-8') as f:
                        ragel_db = json.load(f)
                        author_data = ragel_db.get('interpretaciones', {}).get('planetas_signos', {})
                        author_info = ragel_db.get('autor', {})
                
                # For alan_leo, use the psychological/esoteric texts
                elif author_id == 'alan_leo':
                    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_alan_leo.json')
                    with open(json_path, 'r', encoding='utf-8') as f:
                        leo_db = json.load(f)
                        author_data = leo_db.get('interpretaciones', {}).get('planetas_signos', {})
                        author_info = leo_db.get('autor', {})
                
                else:
                    # Fallback to original schema for other authors
                    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'schema_interpretaciones.json')
                    with open(json_path, 'r', encoding='utf-8') as f:
                        interpretations_db = json.load(f)
                        
                        found_author = None
                        for entry in interpretations_db.get('examples', []):
                            if entry['autor']['id'] == author_id:
                                found_author = entry
                                break
                        
                        if not found_author and interpretations_db.get('examples'):
                            found_author = interpretations_db['examples'][0]
                        
                        if found_author:
                            author_data = found_author['interpretaciones']['planetas_signos']
                            author_info = found_author['autor']
                        
            except Exception as e:
                print(f"Warning: Could not load interpretations: {e}")
            
            # Mappers for sign names (Kerykeion abbreviations -> Spanish names for JSON lookup)
            sign_map = {
                'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Geminis', 'Can': 'Cancer', 
                'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio', 
                'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis'
            }
            
            # Planet names for JSON lookup
            planet_key_map = {
                'Sol': 'Sol', 'Luna': 'Luna', 'Ascendente': 'Ascendente',
                'Mercurio': 'Mercurio', 'Venus': 'Venus', 'Marte': 'Marte',
                'Júpiter': 'Jupiter', 'Saturno': 'Saturno', 'Urano': 'Urano',
                'Neptuno': 'Neptuno', 'Plutón': 'Pluton'
            }
            
            # Bodies list
            bodies = [
                ('Sol', subject.sun),
                ('Luna', subject.moon),
                ('Ascendente', subject.first_house),
                ('Mercurio', subject.mercury),
                ('Venus', subject.venus),
                ('Marte', subject.mars),
                ('Júpiter', subject.jupiter),
                ('Saturno', subject.saturn),
                ('Urano', subject.uranus),
                ('Neptuno', subject.neptune),
                ('Plutón', subject.pluto)
            ]
            
            for name_es, body_obj in bodies:
                # Get sign in Spanish
                s_english = body_obj['sign']
                s_key = sign_map.get(s_english, s_english)
                
                # Get planet key for JSON
                p_key = planet_key_map.get(name_es, name_es)
                
                # Build lookup key and get interpretation
                lookup_key = f"{p_key}_{s_key}"
                interpretation_text = author_data.get(lookup_key, {}).get('texto', "Interpretación no disponible para esta combinación.")
                
                chart_data.append({
                    'body': name_es,
                    'sign': s_key,  # Use Spanish sign name
                    'degree': fmt_deg(body_obj['position']),
                    'interpretation': interpretation_text,
                    'author_name': author_info.get('nombre', 'Fuente Clásica'),
                    'author_work': author_info.get('obra_principal', '')
                })
            
        except Exception as e:
            error = f"Error: {str(e)}"
            import traceback
            traceback.print_exc()

    return render_template('index.html', chart_data=chart_data, aspects_data=aspects_data, error=error, svg_content=Markup(svg_content) if svg_content else None)

# --- Holistic Synthesis Engine ---
def generate_holistic_synthesis(chart_data, author_id, aspects_list=None, aspects_interpretations=None):
    """
    Generates a holistic synthesis of the chart based on the chosen author.
    Now includes analysis of aspects and thematic synthesis (love, money, health).
    
    Args:
        chart_data: List of planet positions with interpretations
        author_id: The selected author's ID
        aspects_list: List of actual aspects from the chart (from Kerykeion)
        aspects_interpretations: Dict of aspect interpretations from JSON
    """
@app.route('/')
def home():
    return jsonify({
        "message": "Sigue Tu Estrella API - Carta Natal Completa",
        "version": "1.0.0",
        "status": "active",
        "author": "Francisco Manuel (Pacoastrologo) - Sigue Tu Estrella",
        "copyright": "Concepto original, diseño y lógica astrológica por Francisco Manuel. Todos los derechos reservados.",
        "website": "https://siguetuestrella.com"
    })
    synthesis = {
        "title": "",
        "content": "",
        "method": "",
        "themes": {}  # Add thematic analysis
    }

    # Extract key planets
    sun = next((p for p in chart_data if p['body'] == 'Sol'), None)
    moon = next((p for p in chart_data if p['body'] == 'Luna'), None)
    asc = next((p for p in chart_data if p['body'] == 'Ascendente'), None)
    venus = next((p for p in chart_data if p['body'] == 'Venus'), None)
    mars = next((p for p in chart_data if p['body'] == 'Marte'), None)
    jupiter = next((p for p in chart_data if p['body'] == 'Júpiter'), None)
    saturn = next((p for p in chart_data if p['body'] == 'Saturno'), None)

    if not sun or not moon:
        return synthesis

    # Analyze aspects for each theme
    def get_aspect_type(aspect_name):
        """Convert aspect name to type for lookup"""
        aspect_map = {
            'conjunction': 'conjuncion',
            'sextile': 'sextil',
            'square': 'cuadratura', 
            'trine': 'trigono',
            'opposition': 'oposicion'
        }
        return aspect_map.get(aspect_name.lower(), aspect_name)
    
    # Count beneficial vs challenging aspects
    beneficial_count = 0
    challenging_count = 0
    love_indicators = []
    money_indicators = []
    
    if aspects_list:
        for aspect in aspects_list:
            aspect_type = aspect.get('type', '').lower()
            p1 = aspect.get('p1', '')
            p2 = aspect.get('p2', '')
            
            # Count aspect types
            if aspect_type in ['sextile', 'trine', 'conjunction']:
                beneficial_count += 1
            elif aspect_type in ['square', 'opposition']:
                challenging_count += 1
            
            # Love indicators (Venus, Moon, Mars aspects)
            if 'Venus' in p1 or 'Venus' in p2 or 'Moon' in p1 or 'Moon' in p2:
                if aspect_type in ['sextile', 'trine']:
                    love_indicators.append('positive')
                elif aspect_type in ['square', 'opposition']:
                    love_indicators.append('challenging')
            
            # Money indicators (Jupiter, Saturn, Venus, 2nd house)
            if 'Jupiter' in p1 or 'Jupiter' in p2:
                if aspect_type in ['sextile', 'trine', 'conjunction']:
                    money_indicators.append('positive')
                elif aspect_type in ['square', 'opposition']:
                    money_indicators.append('challenging')

    # Generate synthesis based on author style
    
    # 1. ALI ABEN RAGEL (Medieval - Temperament & Dignity)
    if author_id == 'ali_aben_ragel':
        synthesis["title"] = "Juicio General de la Natividad"
        synthesis["method"] = "Cálculo del Temperamento según los Signos y Dignidades Planetarias"
        
        # Determine temperament based on signs
        fire_signs = ['Aries', 'Leo', 'Sagitario']
        earth_signs = ['Tauro', 'Virgo', 'Capricornio']
        air_signs = ['Geminis', 'Libra', 'Acuario']
        water_signs = ['Cancer', 'Escorpio', 'Piscis']
        
        sun_element = 'fuego' if sun['sign'] in fire_signs else 'tierra' if sun['sign'] in earth_signs else 'aire' if sun['sign'] in air_signs else 'agua'
        moon_element = 'fuego' if moon['sign'] in fire_signs else 'tierra' if moon['sign'] in earth_signs else 'aire' if moon['sign'] in air_signs else 'agua'
        
        # Build coherent synthesis
        content_parts = []
        content_parts.append(f"Según los antiguos aforismos de las estrellas traducidos por Ali Aben Ragel:")
        content_parts.append(f"El Sol hallándose en {sun['sign']}, signo de naturaleza {sun_element}, infunde en el nativo las cualidades propias de este elemento.")
        content_parts.append(f"La Luna en {moon['sign']}, de naturaleza {moon_element}, modifica estas cualidades según su disposición.")
        
        if beneficial_count > challenging_count:
            content_parts.append("Los luminares se hallan favorablemente aspectados, lo cual augura fortuna y larga vida si no hay maléficos en ángulos.")
        else:
            content_parts.append("Los aspectos difíciles entre los planetas advierten de obstáculos que el nativo deberá superar con prudencia.")
        
        # Add love analysis
        love_positive = love_indicators.count('positive')
        love_challenging = love_indicators.count('challenging')
        if love_positive > love_challenging:
            synthesis["themes"]["amor"] = "Venus y la Luna bien dispuestas indican felicidad en el matrimonio y uniones fructíferas."
        elif love_challenging > love_positive:
            synthesis["themes"]["amor"] = "Los maléficos afligiendo a Venus o Luna advierten de dificultades en el amor y posibles separaciones."
        else:
            synthesis["themes"]["amor"] = "El juicio sobre el amor requiere examinar la séptima casa y su señor con mayor detenimiento."
            
        synthesis["content"] = " ".join(content_parts)

    # 2. ALAN LEO (Esoteric - Soul Purpose)
    elif author_id == 'alan_leo':
        synthesis["title"] = "El Propósito del Alma en Esta Encarnación"
        synthesis["method"] = "Síntesis Esotérica de la Tríada Sol-Luna-Ascendente"
        
        content_parts = []
        content_parts.append("Desde la perspectiva esotérica de Alan Leo:")
        content_parts.append(f"El Sol en {sun['sign']} representa el PROPÓSITO del Ego - la cualidad que el alma busca desarrollar en esta vida.")
        content_parts.append(f"La Luna en {moon['sign']} simboliza el PASADO - las tendencias kármicas traídas de vidas anteriores que deben ser transmutadas.")
        
        if asc:
            content_parts.append(f"El Ascendente en {asc['sign']} es la MÁSCARA - el vehículo físico a través del cual el alma se expresa.")
        
        # Spiritual lesson based on aspects
        if beneficial_count > challenging_count:
            content_parts.append("La preponderancia de aspectos armónicos indica que el alma ha ganado mérito en vidas pasadas y tiene ahora oportunidades de avance espiritual.")
        else:
            content_parts.append("Los aspectos desafiantes señalan lecciones kármicas pendientes. El dolor es el maestro que impele al alma hacia la luz.")
        
        synthesis["themes"]["proposito"] = "La tarea es armonizar la voluntad solar (futuro) con los hábitos lunares (pasado), elevando la conciencia hacia el Yo Superior."
        synthesis["content"] = " ".join(content_parts)

    # 3. MAX HEINDEL (Rosicrucian - Health & Moral Development)
    elif author_id == 'max_heindel':
        synthesis["title"] = "El Mensaje de las Estrellas para Esta Natividad"
        synthesis["method"] = "Análisis Rosacruz según Max Heindel"
        
        content_parts = []
        content_parts.append("Siguiendo las enseñanzas rosacruces de Max Heindel:")
        
        # Add actual interpretations from the database
        if sun.get('interpretation'):
            content_parts.append(f"Respecto al Sol: {sun['interpretation'][:200]}...")
        
        if moon.get('interpretation'):
            content_parts.append(f"Sobre la Luna: {moon['interpretation'][:200]}...")
        
        # Health analysis based on signs
        content_parts.append("En cuanto a la salud: El Sol es el dador de vida y su posición indica la vitalidad general.")
        
        if beneficial_count > challenging_count:
            content_parts.append("Los aspectos favorables fortalecen la constitución y prometen buena recuperación ante enfermedades.")
            synthesis["themes"]["salud"] = "Constitución fuerte con buenos poderes de recuperación."
        else:
            content_parts.append("Los aspectos desafiantes requieren mayor cuidado de la salud, especialmente en las áreas regidas por los signos afectados.")
            synthesis["themes"]["salud"] = "Se aconseja moderación y cuidado preventivo de la salud."
        
        # Moral development
        synthesis["themes"]["desarrollo"] = "El propósito moral es elevar la naturaleza inferior hacia la superior, transmutando los deseos en aspiraciones espirituales."
        
        synthesis["content"] = " ".join(content_parts)
    
    return synthesis

@app.route('/api/calculate', methods=['POST'])
def api_calculate():

    try:
        # Handle both JSON and Form data
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', 'Guest')
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        hour = int(data.get('hour'))
        minute = int(data.get('minute'))
        city_input = data.get('city', 'Madrid')
        
        # Geolocation
        location = None
        max_retries = 2
        for attempt in range(max_retries):
            try:
                location = geolocator.geocode(city_input, timeout=10)
                if location:
                    break
            except Exception:
                time.sleep(1)
        
        if not location:
            return jsonify({'error': f"No se encontró la ciudad: {city_input}"}), 400
        
        lat = location.latitude
        lng = location.longitude
        city_name = location.address.split(",")[0]
        
        # Timezone
        tz_str = tf.timezone_at(lng=lng, lat=lat) or "UTC"
        local_tz = pytz.timezone(tz_str)
        local_dt_naive = datetime(year, month, day, hour, minute)
        local_dt_aware = local_tz.localize(local_dt_naive)
        utc_dt = local_dt_aware.astimezone(pytz.utc)
        
        # Kerykeion Instance
        subject = KrInstance(name, utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
        subject.get_all()
        
        # Aspects
        natal_aspects = NatalAspects(subject)
        aspects_list = natal_aspects.get_aspects()
        aspects_data = [{'p1': a['p1_name'], 'p2': a['p2_name'], 'type': a['aspect'], 'orb': f"{a['orbit']:.2f}"} for a in aspects_list]
        
        # SVG Generation (Reusing logic - ideally refactor to function, but inline for now)
        svg_content = ""
        with tempfile.TemporaryDirectory() as temp_dir:
            subject_for_svg = KrInstance(name, utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
            subject_for_svg.get_all()
            svg_maker = MakeSvgInstance(subject_for_svg, new_output_directory=temp_dir, chart_type="Natal")
            
            # High Visibility / Classic Paper Style Settings
            # Based on user reference image: White background, clear lines.
            svg_maker.colors_settings['paper_0'] = '#ffffff' 
            svg_maker.colors_settings['paper_1'] = '#ffffff' 
            svg_maker.colors_settings['zodiac_bg_0'] = '#ffffff' 
            svg_maker.colors_settings['zodiac_bg_1'] = '#ffffff'
            svg_maker.colors_settings['zodiac_icon_0'] = '#000000' # Black icons
            svg_maker.colors_settings['zodiac_icon_1'] = '#000000'
            svg_maker.colors_settings['zodiac_num_0'] = '#000000' # Black numbers
            svg_maker.colors_settings['zodiac_num_1'] = '#000000' 
            
            # Rings & Lines
            svg_maker.colors_settings['zodiac_radix_ring_0'] = '#444444' # Dark Grey
            svg_maker.colors_settings['zodiac_radix_ring_1'] = '#444444'
            svg_maker.colors_settings['zodiac_transit_ring_0'] = '#444444'
            svg_maker.colors_settings['zodiac_transit_ring_1'] = '#444444'
            svg_maker.colors_settings['zodiac_transit_ring_2'] = '#444444'
            svg_maker.colors_settings['zodiac_transit_ring_3'] = '#444444'
            
            # Aspects - Classic High Contrast
            svg_maker.colors_settings['aspect_0'] = '#0000FF' # Conjunction (Blue)
            svg_maker.colors_settings['aspect_90'] = '#FF0000' # Square (Red)
            svg_maker.colors_settings['aspect_180'] = '#FF0000' # Opposition (Red)
            svg_maker.colors_settings['aspect_120'] = '#00AA00' # Trine (Green)
            svg_maker.colors_settings['aspect_60'] = '#0000FF' # Sextile (Blue)
            
            svg_maker.makeSVG()
            
            generated_files = os.listdir(temp_dir)
            if generated_files:
                with open(os.path.join(temp_dir, generated_files[0]), 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                    
                # Post-processing for MAX VISIBILITY & RESPONSIVENESS
                # We want the chart to take full width but respect aspect ratio
                svg_content = svg_content.replace('width="772.2"', 'width="100%"').replace('height="546.0"', 'height="100%" viewBox="0 0 772 546"')
                
                # Make lines thicker for clearer reading on mobile
                svg_content = re.sub(r'stroke-width:[^;]+;', 'stroke-width: 1.5px;', svg_content)
                
                # Ensure text is large enough
                # (Simple regex to boost font size slightly if possible, or trust full screen zoom)



        # Author Selection Logic
        author_id = data.get('author_id', 'ali_aben_ragel')
        
        # Load Interpretations - Use complete files where available
        author_data = {}
        author_info = {}
        aspects_interpretations = {}

        try:
            # For max_heindel, use the complete authentic texts
            if author_id == 'max_heindel':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_heindel_completo.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    heindel_db = json.load(f)
                    author_data = heindel_db.get('interpretaciones', {}).get('planetas_signos', {})
                    aspects_interpretations = heindel_db.get('interpretaciones', {}).get('aspectos', {})
                    author_info = heindel_db.get('autor', {})
            
            # For ali_aben_ragel, use the medieval original texts
            elif author_id == 'ali_aben_ragel':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_aben_ragel.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    ragel_db = json.load(f)
                    author_data = ragel_db.get('interpretaciones', {}).get('planetas_signos', {})
                    author_info = ragel_db.get('autor', {})
            
            # For alan_leo, use the psychological/esoteric texts
            elif author_id == 'alan_leo':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_alan_leo.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    leo_db = json.load(f)
                    author_data = leo_db.get('interpretaciones', {}).get('planetas_signos', {})
                    author_info = leo_db.get('autor', {})
            
            else:
                # Fallback to original schema for other authors (alan_leo, etc.)
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'schema_interpretaciones.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    interpretations_db = json.load(f)
                    
                    found_author = None
                    for entry in interpretations_db.get('examples', []):
                        if entry['autor']['id'] == author_id:
                            found_author = entry
                            break
                    
                    if not found_author and interpretations_db.get('examples'):
                        found_author = interpretations_db['examples'][0]
                    
                    if found_author:
                        author_data = found_author['interpretaciones']['planetas_signos']
                        author_info = found_author['autor']
                    
        except Exception as e:
            print(f"Warning: Could not load interpretations: {e}")

        # Mappers for Kerykeion (English) -> JSON Keys (Spanish)
        planet_map = {
            'Sun': 'Sol', 'Moon': 'Luna', 'Mercury': 'Mercurio', 'Venus': 'Venus', 
            'Mars': 'Marte', 'Jupiter': 'Jupiter', 'Saturn': 'Saturno', 
            'Uranus': 'Urano', 'Neptune': 'Neptuno', 'Pluto': 'Pluton',
            'First House': 'Ascendente' # Kerykeion might call it First House or Ascendant
        }
        # Mappers for sign names (Kerykeion abbreviations -> Spanish names for JSON lookup)
        sign_map = {
             'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Geminis', 'Can': 'Cancer', 
             'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio', 
             'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis'
        }
        
        # Planet keys for JSON lookup (handling accents)
        planet_key_map = {
            'Sol': 'Sol', 'Luna': 'Luna', 'Ascendente': 'Ascendente',
            'Mercurio': 'Mercurio', 'Venus': 'Venus', 'Marte': 'Marte',
            'Júpiter': 'Jupiter', 'Saturno': 'Saturno', 'Urano': 'Urano',
            'Neptuno': 'Neptuno', 'Plutón': 'Pluton'
        }

        # Chart Data
        chart_data = []
        bodies = [('Sol', subject.sun), ('Luna', subject.moon), ('Ascendente', subject.first_house), ('Mercurio', subject.mercury), ('Venus', subject.venus), ('Marte', subject.mars), ('Júpiter', subject.jupiter), ('Saturno', subject.saturn), ('Urano', subject.uranus), ('Neptuno', subject.neptune), ('Plutón', subject.pluto)]
        
        for name_es, body_obj in bodies:
            
            p_english = body_obj.get('name', '')
            if name_es == 'Ascendente': p_english = 'First House' 
            
            s_english = body_obj['sign']
            
            p_key = planet_map.get(p_english, p_english)
            s_key = sign_map.get(s_english, s_english)
            
            lookup_key = f"{p_key}_{s_key}"
            interpretation_text = author_data.get(lookup_key, {}).get('texto', "Interpretación no encontrada en los textos digitalizados actuales de este autor.")
            
            chart_data.append({
                'body': name_es, 
                'sign': s_key, 
                'degree': f"{body_obj['position']:.2f}",
                'interpretation': interpretation_text
            })
            
        # GENERATE HOLISTIC SYNTHESIS with aspects analysis
        holistic_synthesis = generate_holistic_synthesis(
            chart_data, 
            author_id, 
            aspects_list=aspects_data,
            aspects_interpretations=aspects_interpretations
        )

        # --- PREDICTIVE ASTROLOGY: TRANSITS & PROGRESSIONS ---
        
        # 1. Current Transits (Now)
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        transits_subject = KrInstance(
            "Transits Now", 
            now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute,
            city=city_name, lat=lat, lon=lng, tz_str="UTC"
        )
        transits_subject.get_all()
        
        transit_bodies = [
            {'name': 'Sol', 'position': transits_subject.sun['position'], 'sign': transits_subject.sun['sign']},
            {'name': 'Luna', 'position': transits_subject.moon['position'], 'sign': transits_subject.moon['sign']},
            {'name': 'Mercurio', 'position': transits_subject.mercury['position'], 'sign': transits_subject.mercury['sign']},
            {'name': 'Venus', 'position': transits_subject.venus['position'], 'sign': transits_subject.venus['sign']},
            {'name': 'Marte', 'position': transits_subject.mars['position'], 'sign': transits_subject.mars['sign']},
            {'name': 'Jupiter', 'position': transits_subject.jupiter['position'], 'sign': transits_subject.jupiter['sign']},
            {'name': 'Saturno', 'position': transits_subject.saturn['position'], 'sign': transits_subject.saturn['sign']},
            {'name': 'Urano', 'position': transits_subject.uranus['position'], 'sign': transits_subject.uranus['sign']},
            {'name': 'Neptuno', 'position': transits_subject.neptune['position'], 'sign': transits_subject.neptune['sign']},
            {'name': 'Pluton', 'position': transits_subject.pluto['position'], 'sign': transits_subject.pluto['sign']}
        ]
        
        natal_bodies_struct = [
            {'name': 'Sol', 'position': subject.sun['position']},
            {'name': 'Luna', 'position': subject.moon['position']},
            {'name': 'Mercurio', 'position': subject.mercury['position']},
            {'name': 'Venus', 'position': subject.venus['position']},
            {'name': 'Marte', 'position': subject.mars['position']},
            {'name': 'Jupiter', 'position': subject.jupiter['position']},
            {'name': 'Saturno', 'position': subject.saturn['position']},
            {'name': 'Urano', 'position': subject.uranus['position']},
            {'name': 'Neptuno', 'position': subject.neptune['position']},
            {'name': 'Pluton', 'position': subject.pluto['position']}
        ]
        
        # Calculate Transit Aspects
        transit_aspects_list = calculate_aspects_between_charts(natal_bodies_struct, transit_bodies, chart1_name="Natal", chart2_name="Transit")
        
        # Interpret Transits (Using Heindel's Aspect Interpretations as Base)
        transits_data = []
        for ta in transit_aspects_list:
            # Look up interpretation: "Saturn_conjunction_Sun" (Transit_Aspect_Natal)
            # We reuse natal texts but frame them as current influences
            
            p1 = ta['p2_name'] # Transit Planet (Active Force)
            p2 = ta['p1_name'] # Natal Planet (Receiving Point)
            aspect_name = ta['type'] # 'conjuncion', 'cuadratura', etc.
            
            # Map Spanish to Key format if needed
            # For simplicity, we search: "{p1}_{aspect_name}_{p2}" in DB
            # Or reversed: "{p2}_{aspect_name}_{p1}" since conjunctions are symmetric in text usually
            
            # Try keys
            key1 = f"{p1}_{aspect_name}_{p2}"
            key2 = f"{p2}_{aspect_name}_{p1}"
            
            text = aspects_interpretations.get(key1, {}).get('texto') or aspects_interpretations.get(key2, {}).get('texto')
            
            if not text:
                # Fallback to general nature of transit
                text = f"El planeta {p1} en tránsito forma un(a) {aspect_name} con tu {p2} natal. Este es un período significativo para los temas de {p2}."

            transits_data.append({
                'planet_transit': p1,
                'planet_natal': p2,
                'aspect': aspect_name,
                'orb': f"{ta['orb']:.2f}",
                'interpretation': text
            })

        # 2. Secondary Progressions (Day for a Year)
        prog_date = get_progressed_date(utc_dt, now_utc)
        
        prog_subject = KrInstance(
            "Progressed", 
            prog_date.year, prog_date.month, prog_date.day, prog_date.hour, prog_date.minute,
            city=city_name, lat=lat, lon=lng, tz_str="UTC"
        )
        prog_subject.get_all()
        
        prog_data = []
        # Key Progressed Planets (Sun, Moon, Asc, MC, Mercury, Venus, Mars) 
        # Outer planets usually don't move much in progressions
        prog_bodies_list = [
            ('Sol', prog_subject.sun), ('Luna', prog_subject.moon), 
            ('Mercurio', prog_subject.mercury), ('Venus', prog_subject.venus), ('Marte', prog_subject.mars)
        ]
        
        for name_es, body_obj in prog_bodies_list:
             # Interpret Sign Position of Progressed Planet
             s_english = body_obj['sign']
             s_key = sign_map.get(s_english, s_english)
             p_key = planet_key_map.get(name_es, name_es)
             
             lookup_key = f"{p_key}_{s_key}"
             interp = author_data.get(lookup_key, {}).get('texto', "")
             
             prog_data.append({
                 'body': name_es,
                 'sign': s_key,
                 'degree': f"{body_obj['position']:.2f}",
                 'interpretation': interp # Reusing natal sign interp for progressed sign is valid in classical astro (the nature is the same)
             })

        return jsonify({
            'success': True,
            'svg': svg_content,
            'chart_data': chart_data,
            'aspects_data': aspects_data,
            'author_info': author_info,
            'holistic_synthesis': holistic_synthesis,
            'transits': {
                'date': now_utc.strftime("%Y-%m-%d"),
                'aspects': transits_data
            },
            'progressions': {
                'date': prog_date.strftime("%Y-%m-%d"),
                'planets': prog_data
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sky_now', methods=['GET'])
def api_sky_now():
    try:
        # Use UTC for universal time
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        # Generic location for calculations (Greenwich) - Signs are global
        sky_subject = KrInstance(
            "Sky Now", 
            now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute,
            city="Greenwich", lat=51.48, lon=0.0, tz_str="UTC"
        )
        sky_subject.get_all()
        
        # Helper to get Spanish sign name and emoji
        def get_sign_info(sign_abbr):
            sign_map = {
                 'Ari': ('Aries', '♈'), 'Tau': ('Tauro', '♉'), 'Gem': ('Géminis', '♊'), 
                 'Can': ('Cáncer', '♋'), 'Leo': ('Leo', '♌'), 'Vir': 'Virgo', '♍', 
                 'Lib': ('Libra', '♎'), 'Sco': ('Escorpio', '♏'), 'Sag': ('Sagitario', '♐'), 
                 'Cap': ('Capricornio', '♑'), 'Aqu': ('Acuario', '♒'), 'Pis': ('Piscis', '♓')
            }
            return sign_map.get(sign_abbr, (sign_abbr, ''))

        sky_data = []
        # Key planets for general interest
        bodies_list = [
            ('Sol', sky_subject.sun, '☀️'), 
            ('Luna', sky_subject.moon, '🌙'), 
            ('Mercurio', sky_subject.mercury, '☿️'), 
            ('Venus', sky_subject.venus, '♀️'), 
            ('Marte', sky_subject.mars, '♂️'),
            ('Júpiter', sky_subject.jupiter, '♃'),
            ('Saturno', sky_subject.saturn, '♄')
        ]
        
        for name, body, icon in bodies_list:
             sign_name, sign_icon = get_sign_info(body['sign'])
             sky_data.append({
                 'planet': name,
                 'planet_icon': icon,
                 'sign': sign_name,
                 'sign_icon': sign_icon,
                 'degree': int(body['position']) # Simplified degree
             })

        return jsonify({
            'success': True,
            'date': now_utc.strftime("%d/%m/%Y"),
            'planets': sky_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
