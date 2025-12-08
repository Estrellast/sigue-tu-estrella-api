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
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

geolocator = Nominatim(user_agent="astro_app_sigue_tu_estrella")
tf = TimezoneFinder()

def get_progressed_date(birth_dt, current_dt):
    """Secondary Progressions: 1 day after birth = 1 year of life."""
    age_in_years = (current_dt - birth_dt).days / 365.25
    days_to_add = age_in_years
    prog_date = birth_dt + timedelta(days=days_to_add)
    return prog_date

def calculate_aspects_between_charts(chart1_objs, chart2_objs, chart1_name="Natal", chart2_name="Transit"):
    """Calculates aspects between two sets of planetary positions."""
    aspects = []
    orb_map = {
        'conjunction': 2.0,
        'opposition': 2.0,
        'square': 2.0,
        'trine': 2.0,
        'sextile': 1.5
    }
    
    for p1 in chart1_objs:
        for p2 in chart2_objs:
            if p1['name'] == p2['name']:
    continue            diff = abs(p1['position'] - p2['position'])
            diff = diff % 360
            if diff > 180:
                diff = 360 - diff
            
            aspect_type = None
            orb = 0
            
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

@app.route('/')
def home():
    return jsonify({
        "message": "Sigue Tu Estrella API - Carta Natal Completa",
        "version": "2.0.0",
        "status": "active",
        "author": "Francisco Manuel (Pacoastrologo) - Sigue Tu Estrella",
        "copyright": "Concepto original, diseño y lógica astrológica por Francisco Manuel.",
        "website": "https://siguetuestrella.com"
    })

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', 'Guest')
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        hour = int(data.get('hour'))
        minute = int(data.get('minute'))
        city_input = data.get('city', 'Madrid')
        
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
        
        tz_str = tf.timezone_at(lng=lng, lat=lat) or "UTC"
        local_tz = pytz.timezone(tz_str)
        local_dt_naive = datetime(year, month, day, hour, minute)
        local_dt_aware = local_tz.localize(local_dt_naive)
        utc_dt = local_dt_aware.astimezone(pytz.utc)
        
        subject = KrInstance(name, utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
        subject.get_all()
        
        natal_aspects = NatalAspects(subject)
        aspects_list = natal_aspects.get_aspects()
        aspects_data = [{'p1': a['p1_name'], 'p2': a['p2_name'], 'type': a['aspect'], 'orb': f"{a['orbit']:.2f}"} for a in aspects_list]
        
        svg_content = ""
        with tempfile.TemporaryDirectory() as temp_dir:
            subject_for_svg = KrInstance(name, utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
            subject_for_svg.get_all()
            svg_maker = MakeSvgInstance(subject_for_svg, new_output_directory=temp_dir, chart_type="Natal")
            
            svg_maker.colors_settings['paper_0'] = '#ffffff'
            svg_maker.colors_settings['paper_1'] = '#ffffff'
            svg_maker.colors_settings['zodiac_bg_0'] = '#ffffff'
            svg_maker.colors_settings['zodiac_bg_1'] = '#ffffff'
            svg_maker.colors_settings['zodiac_icon_0'] = '#000000'
            svg_maker.colors_settings['zodiac_icon_1'] = '#000000'
            svg_maker.colors_settings['zodiac_num_0'] = '#000000'
            svg_maker.colors_settings['zodiac_num_1'] = '#000000'
            
            svg_maker.colors_settings['zodiac_radix_ring_0'] = '#444444'
            svg_maker.colors_settings['zodiac_radix_ring_1'] = '#444444'
            
            svg_maker.colors_settings['aspect_0'] = '#0000FF'
            svg_maker.colors_settings['aspect_90'] = '#FF0000'
            svg_maker.colors_settings['aspect_180'] = '#FF0000'
            svg_maker.colors_settings['aspect_120'] = '#00AA00'
            svg_maker.colors_settings['aspect_60'] = '#0000FF'
            
            svg_maker.makeSVG()
            
            generated_files = os.listdir(temp_dir)
            if generated_files:
                with open(os.path.join(temp_dir, generated_files[0]), 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                svg_content = svg_content.replace('width="772.2"', 'width="100%"').replace('height="546.0"', 'height="100%" viewBox="0 0 772 546"')

        author_id = data.get('author_id', 'ali_aben_ragel')
        
        author_data = {}
        author_info = {}
        aspects_interpretations = {}

        try:
            if author_id == 'max_heindel':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_heindel_completo.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    heindel_db = json.load(f)
                    author_data = heindel_db.get('interpretaciones', {}).get('planetas_signos', {})
                    aspects_interpretations = heindel_db.get('interpretaciones', {}).get('aspectos', {})
                    author_info = heindel_db.get('autor', {})
            
            elif author_id == 'ali_aben_ragel':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_aben_ragel.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    ragel_db = json.load(f)
                    author_data = ragel_db.get('interpretaciones', {}).get('planetas_signos', {})
                    author_info = ragel_db.get('autor', {})
            
            elif author_id == 'alan_leo':
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data', 'interpretaciones_alan_leo.json')
                with open(json_path, 'r', encoding='utf-8') as f:
                    leo_db = json.load(f)
                    author_data = leo_db.get('interpretaciones', {}).get('planetas_signos', {})
                    author_info = leo_db.get('autor', {})
                    
        except Exception as e:
            print(f"Warning: Could not load interpretations: {e}")

        sign_map = {
             'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Geminis', 'Can': 'Cancer', 
             'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio', 
             'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis'
        }
        
        planet_key_map = {
            'Sol': 'Sol', 'Luna': 'Luna', 'Ascendente': 'Ascendente',
            'Mercurio': 'Mercurio', 'Venus': 'Venus', 'Marte': 'Marte',
            'Júpiter': 'Jupiter', 'Saturno': 'Saturno', 'Urano': 'Urano',
            'Neptuno': 'Neptuno', 'Plutón': 'Pluton'
        }

        chart_data = []
        bodies = [('Sol', subject.sun), ('Luna', subject.moon), ('Ascendente', subject.first_house), ('Mercurio', subject.mercury), ('Venus', subject.venus), ('Marte', subject.mars), ('Júpiter', subject.jupiter), ('Saturno', subject.saturn), ('Urano', subject.uranus), ('Neptuno', subject.neptune), ('Plutón', subject.pluto)]
        
        for name_es, body_obj in bodies:
            s_english = body_obj['sign']
            s_key = sign_map.get(s_english, s_english)
            p_key = planet_key_map.get(name_es, name_es)
            
            lookup_key = f"{p_key}_{s_key}"
            interpretation_text = author_data.get(lookup_key, {}).get('texto', "Interpretación no encontrada.")
            
            chart_data.append({
                'body': name_es, 
                'sign': s_key, 
                'degree': f"{body_obj['position']:.2f}",
                'interpretation': interpretation_text
            })
        
        holistic_synthesis = {
            "title": "Síntesis Astrológica",
            "content": "Interpretación holística basada en el autor seleccionado.",
            "method": "Análisis Tradicional",
            "themes": {}
        }

        # TRANSITS & PROGRESSIONS
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        transits_subject = KrInstance("Transits Now", now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
        transits_subject.get_all()
        
        transit_bodies = [
            {'name': 'Sol', 'position': transits_subject.sun['position']},
            {'name': 'Luna', 'position': transits_subject.moon['position']},
            {'name': 'Mercurio', 'position': transits_subject.mercury['position']},
            {'name': 'Venus', 'position': transits_subject.venus['position']},
            {'name': 'Marte', 'position': transits_subject.mars['position']},
            {'name': 'Jupiter', 'position': transits_subject.jupiter['position']},
            {'name': 'Saturno', 'position': transits_subject.saturn['position']},
            {'name': 'Urano', 'position': transits_subject.uranus['position']},
            {'name': 'Neptuno', 'position': transits_subject.neptune['position']},
            {'name': 'Pluton', 'position': transits_subject.pluto['position']}
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
        
        transit_aspects_list = calculate_aspects_between_charts(natal_bodies_struct, transit_bodies)
        
        transits_data = []
        for ta in transit_aspects_list:
            p1 = ta['p2_name']
            p2 = ta['p1_name']
            aspect_name = ta['type']
            
            key1 = f"{p1}_{aspect_name}_{p2}"
            key2 = f"{p2}_{aspect_name}_{p1}"
            
            text = aspects_interpretations.get(key1, {}).get('texto') or aspects_interpretations.get(key2, {}).get('texto')
            
            if not text:
                text = f"El planeta {p1} en tránsito forma {aspect_name} con tu {p2} natal."

            transits_data.append({
                'planet_transit': p1,
                'planet_natal': p2,
                'aspect': aspect_name,
                'orb': f"{ta['orb']:.2f}",
                'interpretation': text
            })

        prog_date = get_progressed_date(utc_dt, now_utc)
        
        prog_subject = KrInstance("Progressed", prog_date.year, prog_date.month, prog_date.day, prog_date.hour, prog_date.minute, city=city_name, lat=lat, lon=lng, tz_str="UTC")
        prog_subject.get_all()
        
        prog_data = []
        prog_bodies_list = [
            ('Sol', prog_subject.sun), ('Luna', prog_subject.moon), 
            ('Mercurio', prog_subject.mercury), ('Venus', prog_subject.venus), ('Marte', prog_subject.mars)
        ]
        
        for name_es, body_obj in prog_bodies_list:
             s_english = body_obj['sign']
             s_key = sign_map.get(s_english, s_english)
             p_key = planet_key_map.get(name_es, name_es)
             
             lookup_key = f"{p_key}_{s_key}"
             interp = author_data.get(lookup_key, {}).get('texto', "")
             
             prog_data.append({
                 'body': name_es,
                 'sign': s_key,
                 'degree': f"{body_obj['position']:.2f}",
                 'interpretation': interp
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
        now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        sky_subject = KrInstance("Sky Now", now_utc.year, now_utc.month, now_utc.day, now_utc.hour, now_utc.minute, city="Greenwich", lat=51.48, lon=0.0, tz_str="UTC")
        sky_subject.get_all()
        
        def get_sign_info(sign_abbr):
            sign_map = {
                 'Ari': ('Aries', '♈'), 'Tau': ('Tauro', '♉'), 'Gem': ('Géminis', '♊'), 
                 'Can': ('Cáncer', '♋'), 'Leo': ('Leo', '♌'), 'Vir': ('Virgo', '♍'), 
                 'Lib': ('Libra', '♎'), 'Sco': ('Escorpio', '♏'), 'Sag': ('Sagitario', '♐'), 
                 'Cap': ('Capricornio', '♑'), 'Aqu': ('Acuario', '♒'), 'Pis': ('Piscis', '♓')
            }
            return sign_map.get(sign_abbr, (sign_abbr, ''))

        sky_data = []
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
                 'degree': int(body['position'])
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
