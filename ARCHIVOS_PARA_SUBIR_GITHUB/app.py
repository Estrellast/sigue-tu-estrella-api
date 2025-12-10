from flask import Flask, render_template, request, jsonify
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
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (WordPress)

# Initialize Geocoder and TimezoneFinder (Global to avoid re-init overhead)
geolocator = Nominatim(user_agent="astro_app_sigue_tu_estrella_v2")
tf = TimezoneFinder()

@app.route('/', methods=['GET'])
def index():
    return "Sigue Tu Estrella API is Running. Use POST /api/calculate for chart generation."

def get_author_data(author_id):
    """Efficiently load author data with caching mechanism in mind (simple dict for now)"""
    # Note: In production, we'd cache this in memory to avoid disk I/O on every request
    base_path = os.path.dirname(os.path.abspath(__file__))
    author_data = {}
    author_info = {}
    aspects_interpretations = {}
    
    try:
        if author_id == 'max_heindel':
            json_path = os.path.join(base_path, 'static', 'data', 'interpretaciones_heindel_completo.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                author_data = db.get('interpretaciones', {}).get('planetas_signos', {})
                aspects_interpretations = db.get('interpretaciones', {}).get('aspectos', {})
                author_info = db.get('autor', {})
        elif author_id == 'ali_aben_ragel':
            json_path = os.path.join(base_path, 'static', 'data', 'interpretaciones_aben_ragel.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                author_data = db.get('interpretaciones', {}).get('planetas_signos', {})
                author_info = db.get('autor', {})
        elif author_id == 'alan_leo':
            json_path = os.path.join(base_path, 'static', 'data', 'interpretaciones_alan_leo.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                author_data = db.get('interpretaciones', {}).get('planetas_signos', {})
                author_info = db.get('autor', {})
        else:
             # Fallback
            json_path = os.path.join(base_path, 'static', 'data', 'schema_interpretaciones.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                example = db.get('examples', [])[0] if db.get('examples') else {}
                if example:
                    author_data = example.get('interpretaciones', {}).get('planetas_signos', {})
                    author_info = example.get('autor', {})
    except Exception as e:
        print(f"Error loading author data: {e}")
        
    return author_data, author_info, aspects_interpretations

def generate_holistic_synthesis(chart_data, author_id, aspects_list, aspects_interpretations, subject):
    """
    Generates a structured holistic synthesis.
    Optimized for speed: Single pass through data.
    """
    synthesis = {
        "title": "Síntesis Astrológica",
        "content": "",
        "method": "Análisis General",
        "themes": {}
    }
    
    # Quick planetary lookups
    planets = {p['body']: p for p in chart_data}
    sun = planets.get('Sol')
    moon = planets.get('Luna')
    asc = planets.get('Ascendente')
    
    if not sun or not moon: return synthesis

    # --- ALI ABEN RAGEL (Medieval) ---
    if author_id == 'ali_aben_ragel':
        synthesis["title"] = "Juicio de la Natividad (Aben Ragel)"
        synthesis["method"] = "Temperamento y Dignidades"
        
        # Simple Element Logic for Speed
        fire = ['Aries', 'Leo', 'Sagitario']
        earth = ['Tauro', 'Virgo', 'Capricornio']
        air = ['Geminis', 'Libra', 'Acuario']
        water = ['Cancer', 'Escorpio', 'Piscis']
        
        sun_sign = sun['sign']
        sun_elem = 'Fuego' if sun_sign in fire else 'Tierra' if sun_sign in earth else 'Aire' if sun_sign in air else 'Agua'
        
        synthesis["content"] = f"Nacido bajo el Sol en {sun_sign} ({sun_elem}). "
        
        # Aspect Balance
        positive_aspects = sum(1 for a in aspects_list if a['type'] in ['sextile', 'trine', 'conjunction'])
        hard_aspects = sum(1 for a in aspects_list if a['type'] in ['square', 'opposition'])
        
        if positive_aspects > hard_aspects:
            synthesis["content"] += "La configuración general muestra armonía y facilidades naturales. "
        else:
             synthesis["content"] += "La configuración sugiere desafíos que forjarán el carácter. "
             
    # --- ALAN LEO (Esoteric) ---
    elif author_id == 'alan_leo':
        synthesis["title"] = "Propósito del Alma (Alan Leo)"
        synthesis["method"] = "Lectura Esotérica"
        synthesis["content"] = f"El Sol en {sun['sign']} indica el propósito vital actual. La Luna en {moon['sign']} refleja el pasado kármico."
        if asc:
             synthesis["content"] += f" El Ascendente en {asc['sign']} es la personalidad visible."
             
    # --- MAX HEINDEL (Rosicrucian) ---
    elif author_id == 'max_heindel':
         synthesis["title"] = "Mensaje de las Estrellas (Max Heindel)"
         synthesis["method"] = "Filosofía Rosacruz"
         synthesis["content"] = f"Posición solar vital: {sun['sign']}. "
         if sun.get('interpretation'):
             # Limit text length for speed/display
             clean_text = sun['interpretation'].split('.')[0] + "."
             synthesis["content"] += f"Influencia clave: {clean_text}"

    return synthesis

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    start_time = time.time()
    try:
        data = request.get_json() if request.is_json else request.form
        
        # 1. Parsing Inputs
        try:
            name = data.get('name', 'Consultante')
            date_str = data.get('date', '') # Expecting YYYY-MM-DD or parts
            time_str = data.get('time', '') # Expecting HH:MM
            
            if date_str and time_str:
                # Flexible parsing if full string provided
                d_parts = date_str.split('-')
                t_parts = time_str.split(':')
                year, month, day = int(d_parts[0]), int(d_parts[1]), int(d_parts[2])
                hour, minute = int(t_parts[0]), int(t_parts[1])
            else:
                # Fallback to individual fields
                year = int(data['year'])
                month = int(data['month'])
                day = int(data['day'])
                hour = int(data['hour'])
                minute = int(data['minute'])
                
            city_input = data.get('city', 'Madrid')
            author_id = data.get('author_id', 'ali_aben_ragel')
        except KeyError as e:
            return jsonify({'success': False, 'error': f"Faltan datos requeridos: {e}"}), 400

        # 2. Geolocation (Optimized: Fast Fail)
        try:
            location = geolocator.geocode(city_input, timeout=5)
            if not location:
                 return jsonify({'success': False, 'error': f"Ciudad desconocida: {city_input}"}), 400
        except Exception:
             # Fallback simple hardcoded checks if geo fails (robustness)
             if city_input.lower() == 'madrid':
                 lat, lng, city_name = 40.4168, -3.7038, "Madrid"
             else:
                 return jsonify({'success': False, 'error': "Error de conexión geolocalización"}), 500
        else:
             lat = location.latitude
             lng = location.longitude
             city_name = location.address.split(",")[0]

        # 3. Timezones
        try:
            tz_str = tf.timezone_at(lng=lng, lat=lat) or "UTC"
            local_tz = pytz.timezone(tz_str)
            local_dt_naive = datetime(year, month, day, hour, minute)
            local_dt_aware = local_tz.localize(local_dt_naive)
            utc_dt = local_dt_aware.astimezone(pytz.utc)
        except Exception as e:
            return jsonify({'success': False, 'error': f"Error zona horaria: {e}"}), 400

        # 4. ONE Kerykeion Calculation (SINGLE PASS)
        subject = KrInstance(name, utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
        subject.get_all() # Calculates everything
        
        # 5. Aspects
        natal_aspects = NatalAspects(subject)
        aspects_list = natal_aspects.get_aspects()
        # Clean aspects for JSON
        aspects_json = [{
            'p1': a['p1_name'], 
            'p2': a['p2_name'], 
            'type': a['aspect'], 
            'orb': round(a['orbit'], 2)
        } for a in aspects_list]

        # 6. Load Interpretations
        author_data, author_info, aspects_interpretations = get_author_data(author_id)
        
        # 7. Map Data & Interpretations
        planet_map_es = {
            'Sun': 'Sol', 'Moon': 'Luna', 'Mercury': 'Mercurio', 'Venus': 'Venus', 
            'Mars': 'Marte', 'Jupiter': 'Jupiter', 'Saturn': 'Saturno', 
            'Uranus': 'Urano', 'Neptune': 'Neptuno', 'Pluto': 'Pluton',
            'First House': 'Ascendente', 'Node': 'Nodo Norte'
        }
        sign_map_es = {
             'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Geminis', 'Can': 'Cancer', 
             'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio', 
             'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis'
        }

        chart_data = []
        # Precompute bodies list to ensure ORDER (Lights -> Personal -> Social -> Trans)
        bodies_order = ['Sun', 'Moon', 'First House', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
        
        # Access internal data stores safely
        for p_eng in bodies_order:
            if p_eng == 'First House':
                body_data = subject.first_house
                p_name_k = 'First House'
            else:
                 # Kerykeion stores planets as attributes lowercased usually, but let's lookup
                 body_data = getattr(subject, p_eng.lower().replace(' ', '_'), None)
                 p_name_k = p_eng
            
            if not body_data: continue

            p_es = planet_map_es.get(p_name_k, p_name_k)
            s_es = sign_map_es.get(body_data['sign'], body_data['sign'])
            
            # Lookup Interpretation
            key = f"{p_es}_{s_es}"
            interp = author_data.get(key, {}).get('texto', "Interpretación no disponible.")
            
            chart_data.append({
                'body': p_es,
                'sign': s_es,
                'degree': round(body_data['position'], 2),
                'house': body_data.get('house', ''), # Might vary depending on Kr version
                'interpretation': interp
            })

        # ... (Previous code) ...
        # 8. Holistic Synthesis
        synthesis = generate_holistic_synthesis(chart_data, author_id, aspects_json, aspects_interpretations, subject)

        # ------------------------------------------------------------------
        # NEW: TRANSITS CALCULATION (Fixing the "Lost Functionality")
        # ------------------------------------------------------------------
        transits_data = []
        try:
            from kerykeion.utilities.aspects import CompositeAspects
            
            # 1. Create Transit Chart (Current Time)
            now_utc = datetime.utcnow()
            transit_subject = KrInstance(
                "Transits", now_utc.year, now_utc.month, now_utc.day, 
                now_utc.hour, now_utc.minute, 
                city=city_name, lat=lat, lon=lng, tz_str="UTC"
            )
            
            # 2. Calculate Aspects (Natal vs Transit)
            # Kerykeion CompositeAspects compares two charts
            transit_aspects_list = CompositeAspects(subject, transit_subject).get_aspects()
            
            # 3. Format for JSON
            transits_data = [{
                'p_natal': a['p1_name'],     # Planet in Natal Chart
                'p_transit': a['p2_name'],   # Planet in Transit Chart
                'type': a['aspect'],         # Conjunction, Square, etc.
                'orb': round(a['orbit'], 2)
            } for a in transit_aspects_list]
            
        except Exception as e:
            print(f"Error calculating transits: {e}")
            # Non-blocking error, allow natal to return even if transits fail

        # 9. SVG Generation (Using same subject instance!)
        svg_content = ""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                svg_maker = MakeSvgInstance(subject, new_output_directory=temp_dir, chart_type="Natal")
                
                # Styles (White on Black or White High Contrast)
                paper_color = "#1a1a1a"
                gold = "#D4AF37"
                cyan = "#00F0FF"
                white = "#FFFFFF"
                
                svg_maker.colors_settings['paper_0'] = paper_color
                svg_maker.colors_settings['paper_1'] = paper_color
                svg_maker.colors_settings['zodiac_bg_0'] = paper_color
                svg_maker.colors_settings['zodiac_bg_1'] = paper_color
                svg_maker.colors_settings['zodiac_icon_0'] = white
                svg_maker.colors_settings['zodiac_icon_1'] = white
                svg_maker.colors_settings['zodiac_num_0'] = gold
                svg_maker.colors_settings['zodiac_num_1'] = gold
                svg_maker.colors_settings['zodiac_radix_ring_0'] = cyan
                svg_maker.colors_settings['zodiac_radix_ring_1'] = cyan
                
                svg_maker.makeSVG()
                
                generated = os.listdir(temp_dir)
                if generated:
                    with open(os.path.join(temp_dir, generated[0]), 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                        
                    # Inject CSS for responsiveness
                    svg_content = svg_content.replace('width="772.2"', 'width="100%"').replace('height="546.0"', 'height="100%" viewBox="0 0 772 546"')
                    
        except Exception as e:
            print(f"SVG Error: {e}")

        process_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'processing_time': f"{process_time:.3f}s",
            'author_info': author_info,
            'chart_data': chart_data,
            'aspects_data': aspects_json,
            'transits_data': transits_data, # <--- Added to Response
            'holistic_synthesis': synthesis,
            'svg': svg_content
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
