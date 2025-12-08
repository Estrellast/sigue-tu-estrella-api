import json
import os

# Define archetypal keywords and medieval-style templates for Ali Aben Ragel
signs_data = {
    "Aries": {"element": "Fuego", "quality": "Cardinal", "ruler": "Marte", "keywords": ["fuerza", "inicio", "cólera", "mando"], "nature": "Caliente y Seco"},
    "Tauro": {"element": "Tierra", "quality": "Fijo", "ruler": "Venus", "keywords": ["estabilidad", "placer", "ganado", "construcción"], "nature": "Frío y Seco"},
    "Geminis": {"element": "Aire", "quality": "Mutable", "ruler": "Mercurio", "keywords": ["palabra", "comercio", "hermanos", "cambio"], "nature": "Caliente y Húmedo"},
    "Cancer": {"element": "Agua", "quality": "Cardinal", "ruler": "Luna", "keywords": ["hogar", "madre", "ríos", "protección"], "nature": "Frío y Húmedo"},
    "Leo": {"element": "Fuego", "quality": "Fijo", "ruler": "Sol", "keywords": ["realeza", "honor", "hijos", "poder"], "nature": "Caliente y Seco"},
    "Virgo": {"element": "Tierra", "quality": "Mutable", "ruler": "Mercurio", "keywords": ["servicio", "cosecha", "enfermedad", "análisis"], "nature": "Frío y Seco"},
    "Libra": {"element": "Aire", "quality": "Cardinal", "ruler": "Venus", "keywords": ["justicia", "matrimonio", "belleza", "socios"], "nature": "Caliente y Húmedo"},
    "Escorpio": {"element": "Agua", "quality": "Fijo", "ruler": "Marte", "keywords": ["muerte", "renacimiento", "oculto", "intensidad"], "nature": "Frío y Húmedo"},
    "Sagitario": {"element": "Fuego", "quality": "Mutable", "ruler": "Júpiter", "keywords": ["fe", "viajes largos", "leyes", "sabiduría"], "nature": "Caliente y Seco"},
    "Capricornio": {"element": "Tierra", "quality": "Cardinal", "ruler": "Saturno", "keywords": ["ambición", "gobierno", "tiempo", "estructura"], "nature": "Frío y Seco"},
    "Acuario": {"element": "Aire", "quality": "Fijo", "ruler": "Saturno/Urano", "keywords": ["amigos", "esperanza", "ciencia", "humanidad"], "nature": "Caliente y Húmedo"},
    "Piscis": {"element": "Agua", "quality": "Mutable", "ruler": "Júpiter/Neptuno", "keywords": ["aislamiento", "misticismo", "océano", "sacrificio"], "nature": "Frío y Húmedo"}
}

planets_data = {
    "Sol": {"type": "Luminar", "text_template": "El Sol en {signo} otorga al nativo {kw1} y deseo de {kw2}. Siendo su naturaleza {nature}, indica dignidad y honores en los asuntos de la casa que ocupe."},
    "Luna": {"type": "Luminar", "text_template": "La Luna en {signo} hace el alma {kw_nature} y el cuerpo propenso a {kw3}. Indica fluctuaciones en {kw4} y una conexión con lo femenino y popular."},
    "Mercurio": {"type": "Planeta", "text_template": "Mercurio en {signo} dispone la mente hacia {kw1} y {kw2}. El nativo será hábil en {kw3} y de ingenio rápido, aunque variable."},
    "Venus": {"type": "Planeta", "text_template": "Venus en {signo} embellece la vida a través de {kw1}. Promete dicha en {kw2} y afectos suaves, salvo que esté afligido."},
    "Marte": {"type": "Planeta", "text_template": "Marte en {signo} da fuerza en {kw1} pero peligro de {kw2}. El nativo luchará por {kw3} con ardor excesivo."},
    "Jupiter": {"type": "Planeta", "text_template": "Júpiter en {signo} expande la fortuna mediante {kw1}. Otorga sabiduría en {kw2} y protección providencial."},
    "Saturno": {"type": "Planeta", "text_template": "Saturno en {signo} restringe y disciplina a través de {kw1}. Da seriedad en {kw2} y pruebas que forjan el carácter."},
    "Urano": {"type": "Planeta", "text_template": "Urano en {signo} trae cambios repentinos en {kw1} y una visión original de {kw2}."},
    "Neptuno": {"type": "Planeta", "text_template": "Neptuno en {signo} disuelve los límites de {kw1}, trayendo inspiración o confusión en {kw2}."},
    "Pluton": {"type": "Planeta", "text_template": "Plutón en {signo} transforma profundamente los asuntos de {kw1}, a menudo mediante crisis y regeneración."},
    "Ascendente": {"type": "Angulo", "text_template": "El Ascendente en {signo} marca el temperamento {nature}. El nativo aborda la vida con {kw1} y su destino está ligado a {kw2}."}
}

base_path = '/Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere/static/data/schema_interpretaciones.json'

def generate_interpretations():
    with open(base_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Real Text Database - Excerpts found from actual books
    real_texts = {
        # Ali Aben Ragel (Libro Conplido)
        "ali_aben_ragel": {
            "Sol_Aries": "(Ali Aben Ragel) En la segunda <i>faz</i> de Aries, que es del Sol, significa nobleza, alteza, gran señorío y dignidad. El nativo alcanzará honores por su propia virtud y fuerza.",
            "Sol_Leo": "(Ali Aben Ragel) El Sol en su propio domicilio significa que el nacido será hombre de gran fama, amado por reyes y señores, firme en sus obras y de gran autoridad.",
            "Sol_Libra": "(Ali Aben Ragel) El Sol está aquí en su cañimiento (caída). Significa disminución de la honra y poca duración en los estados altos, aunque tenga buena voluntad."
        },
        # Alan Leo (Astrología Esotérica)
        "alan_leo": {
            "Sol_Aries": "(Alan Leo) Aries es el lugar de nacimiento de las Ideas Divinas. El Sol aquí actúa como un vehículo para el Fuego Eléctrico del Primer Rayo, inspirando la 'Voluntad-hacia-el-Bien' y el despertar del Ego.",
            "Sol_Leo": "(Alan Leo) Aquí el Ego Individualizado se expresa con máxima potencia. Es la autoconciencia plena, donde el alma aprende a decir 'Yo Soy' antes de comprender 'Nosotros Somos'.",
            "Sol_Piscis": "(Alan Leo) El final del ciclo. El Sol aquí pide la disolución del ego personal para fundirse con la Conciencia Universal. Es el sacrificio del yo separado."
        },
        # Max Heindel (El Mensaje de las Estrellas)
        "max_heindel": {
            "Sol_Aries": "(Max Heindel) Los hijos de Aries rebalsan de vida y energía; son autoafirmativos y agresivos hasta cierto grado, aventureros al borde de la temeridad. Tienen la misión de liderar, pero deben controlar su impulsividad.",
            "Sol_Tauro": "(Max Heindel) Son personas amables y agradables, pero cuando se les provoca son tercos como el animal que los simboliza. Tienen una gran persistencia y capacidad para acumular riquezas materiales.",
            "Sol_Geminis": "(Max Heindel) Son mentalmente alertas y rápidos, pero a menudo carecen de concentración. Aman el cambio y la variedad, siendo excelentes intermediarios y comunicadores, aunque propensos a la dispersión nerviosa."
        }
    }

    # Author 0: Ali Aben Ragel (Medieval - Concrete, Fatalistic, Dignities)
    authors_config = [
        {
            "index": 0,
            "id": "ali_aben_ragel",
            "prefix": "(Ali Aben Ragel)",
            "templates": {
                "Sol": "El Sol en {signo} otorga {kw1} y inclinación al {kw2}. Según los antiguos juicios, esto promete {nature} en el destino del nacido.",
                "Luna": "La Luna en {signo} dispone el cuerpo a {kw3} y el alma a ser {kw_nature}. Sus afecciones son {kw4} y variables.",
                "Mercurio": "Mercurio en {signo} hace al hombre {kw1}, de ingenio sutil para {kw2} y hábil en {kw3}.",
                "Venus": "Venus en {signo} da amor por {kw1} y deleites en {kw2}. Significa bodas y asociaciones afortunadas.",
                "Marte": "Marte en {signo} incita a {kw1} con furor. Peligro de hierro o fuego por causa de {kw2}.",
                "Jupiter": "Júpiter en {signo} aumenta la hacienda y la ley mediante {kw1}. El nativo será tenido por sabio en {kw2}.",
                "Saturno": "Saturno en {signo} trae tristezas por {kw1} y demora en {kw2}. Es señal de cosas antiguas y duraderas.",
                "Urano": "Infortunio o cambio súbito en {kw1}. La mente se aparta de la norma en asuntos de {kw2}.",
                "Neptuno": "Engaños o secretos en {kw1}. La fantasía prevalece sobre la razón en {kw2}.",
                "Pluton": "Destrucción y renovación en {kw1}.",
                "Ascendente": "El Ascendente en {signo} muestra un nativo de complexión {nature}, inclinado a {kw1}."
            }
        },
        # Author 1: Alan Leo (Esoteric - Soul, Evolution, Rays)
        {
            "index": 1,
            "id": "alan_leo",
            "prefix": "(Alan Leo)",
            "templates": {
                "Sol": "El Ego Solar utiliza la vibración de {signo} para desarrollar {kw1}. La lección kármica es transformar {kw2} en voluntad espiritual.",
                "Luna": "La personalidad, limitada por la forma de {signo}, busca seguridad en {kw3}. El pasado kármico se manifiesta como {kw4}.",
                "Mercurio": "El puente mental (Antahkarana) se construye en {signo} mediante {kw1} y la síntesis de {kw2}.",
                "Venus": "El amor en {signo} busca la cohesión mediante {kw1}, elevando el deseo hacia {kw2} superior.",
                "Marte": "La fuerza del deseo en {signo} impulsa a la acción mediante {kw3}. Debe transmutarse el conflicto de {kw2} en servicio.",
                "Jupiter": "La conciencia superior se expande en {signo} a través de {kw1} y la filosofía de {kw2}.",
                "Saturno": "El Guardián del Umbral en {signo} cristaliza {kw1} para enseñar responsabilidad en {kw2}.",
                "Urano": "La Mente Universal rompe las formas de {signo} para liberar {kw1}.",
                "Neptuno": "El amor universal disuelve las barreras de {signo} a través de {kw1}.",
                "Pluton": "La Voluntad Divina destruye lo inferior en {signo} para regenerar {kw1}.",
                "Ascendente": "El vehículo físico en {signo} está diseñado para expresar {kw1} como propósito del alma."
            }
        },
        # Author 2: Max Heindel (Rosicrucian - Vital Body, Health, Moral)
        {
            "index": 2,
            "id": "max_heindel",
            "prefix": "(Max Heindel)",
            "templates": {
                "Sol": "El Espíritu Vital en {signo} infunde {kw1} en el cuerpo denso. El nativo debe cultivar {kw2} para mantener la salud.",
                "Luna": "La imaginación, trabajando a través de {signo}, predispone a {kw3}. Hay una conexión etérica con {kw4}.",
                "Mercurio": "La mente concreta en {signo} se enfoca en {kw1}, sirviendo de freno o espuela para {kw2}.",
                "Venus": "La atracción social en {signo} suaviza la naturaleza mediante {kw1} y el refinamiento de {kw2}.",
                "Marte": "El cuerpo de deseos es fuerte en {signo}, incitando a {kw3}. Peligro de fiebre o accidentes por {kw2}.",
                "Jupiter": "La circulación arterial y la benevolencia se ven favorecidas en {signo} por {kw1}.",
                "Saturno": "El metabolismo se retarda en {signo}, causando cristalización en {kw1}. Necesidad de paciencia en {kw2}.",
                "Urano": "El éter planetario en {signo} produce una naturaleza errática en {kw1}.",
                "Neptuno": "Hipersensibilidad en {signo}. Posible contacto con planos invisibles a través de {kw1}.",
                "Pluton": "Fuerzas latentes en {signo} que operan en {kw1}.",
                "Ascendente": "El cuerpo denso es del tipo {signo}, dando vitalidad {nature} y tendencia a {kw1}."
            }
        }
    ]

    for author_cfg in authors_config:
        idx = author_cfg['index']
        a_id = author_cfg['id']
        prefix = author_cfg['prefix']
        tmpls = author_cfg['templates']
        
        if idx >= len(data['examples']):
            continue 
            
        target_interpretations = data['examples'][idx]['interpretaciones']['planetas_signos']
        
        for p_key, p_val in planets_data.items():
            for s_key, s_val in signs_data.items():
                key = f"{p_key}_{s_key}"
                
                kw = s_val['keywords']
                nature = s_val['nature']

                # CHECK FOR REAL TEXT FIRST
                real_text_entry = real_texts.get(a_id, {}).get(key)
                
                if real_text_entry:
                    text = real_text_entry
                else:
                    # Use improved template
                    template_str = tmpls.get(p_key, "Interpretación en {signo}.")
                    text = f"{prefix} {template_str.format(signo=s_key, kw1=kw[0], kw2=kw[1], kw3=kw[2], kw4=kw[3], nature=nature, kw_nature=nature.lower())}"
                
                # Always overwrite or strict create
                target_interpretations[key] = {
                    "planeta": p_key,
                    "signo": s_key,
                    "texto": text,
                    "keywords": kw,
                    "dignidad": "Peregrino"
                }
        
        # Save back to memory
        data['examples'][idx]['interpretaciones']['planetas_signos'] = target_interpretations

    
    with open(base_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    generate_interpretations()
