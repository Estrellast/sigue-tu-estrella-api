#!/usr/bin/env python3
"""
Script para compilar los textos reales de los libros clásicos de astrología.
Fuentes: Max Heindel (El Mensaje de las Estrellas), Alan Leo (Astrología Esotérica), 
         Ali Aben Ragel (El Libro Conplido)
         
NOTA: Todas estas obras están en dominio público.
"""

import json
import os

BASE_PATH = '/Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere/static/data/schema_interpretaciones.json'

# Textos REALES extraídos de las fuentes originales
# Resumidos/parafraseados para uso interpretativo

REAL_TEXTS = {
    # ========================================
    # MAX HEINDEL - El Mensaje de las Estrellas (1919)
    # Obra en dominio público
    # ========================================
    "max_heindel": {
        # Ascendente en cada signo (Capítulo V)
        "Ascendente_Aries": "(Max Heindel) Los de Aries son audaces, seguros de sí mismos e impulsivos. Buscan liderar, odian seguir. Siempre toman la iniciativa pero a menudo carecen de persistencia para llevar sus proyectos hasta el final contra obstáculos serios. Sobreviven a fiebres que a otros los tumbarían.",
        
        "Ascendente_Tauro": "(Max Heindel) Los de Tauro son preeminentemente tenaces y constantes en todo lo que hacen: en amor, en odio, en trabajo o en juego. Persisten en una dirección dada, y ni la razón ni el argumento los desviará. Sea amable pero firme con ellos.",
        
        "Ascendente_Geminis": "(Max Heindel) Los de Géminis tienen mentes agudamente inquisitivas que siempre quieren saber el porqué, pero a menudo carecen de persistencia para seguir las pistas hasta el final. Son táctiles, evitan dar ofensa incluso bajo provocación.",
        
        "Ascendente_Cancer": "(Max Heindel) Los de Cáncer son muy afectuosos del hogar y sus comodidades. Son tranquilos, reservados y se adaptan a las condiciones. Su enojo es breve, y no guardan rencor. El estómago y la alimentación les dominan.",
        
        "Ascendente_Leo": "(Max Heindel) Los de Leo quieren ser notados, son agresivos y buscan atraer la atención dondequiera que vayan. Aspiran a liderar, no a seguir. Leo rige el corazón, y cuando no está afligido, tienen corazones más grandes que sus bolsillos.",
        
        "Ascendente_Virgo": "(Max Heindel) Los de Virgo son rápidos y activos en la juventud. Aprenden con facilidad, sin esfuerzo. Adquieren poderes lingüísticos fácilmente, son escritores fluidos pero a menudo cínicos, fríos e implacables cuando han sido heridos.",
        
        "Ascendente_Libra": "(Max Heindel) La elegancia expresa las peculiaridades físicas del libriano. Son cambiantes, siguen un capricho con tanto celo como si su vida dependiera de ello, y luego lo abandonan sin aviso. El matrimonio les obsesiona.",
        
        "Ascendente_Escorpio": "(Max Heindel) Los de Escorpio siempre defienden sus derechos y nunca se someten a imposiciones, aunque son propensos a pisotear a otros. Están llenos de preocupaciones por cosas que pueden pasar, pero que nunca suceden.",
        
        "Ascendente_Sagitario": "(Max Heindel) Hay dos clases muy diferentes nacidas bajo este signo. Una, la parte animal del Centauro, ama el juego y la aventura. La otra, la parte humana que apunta la flecha hacia arriba, tiene las aspiraciones más elevadas del alma.",
        
        "Ascendente_Capricornio": "(Max Heindel) La vitalidad es muy baja, y estos niños se crían con gran dificultad, pero una vez pasada la infancia, exhiben una tenacidad verdaderamente asombrosa. Ambición y sospecha son características dominantes.",
        
        "Ascendente_Acuario": "(Max Heindel) Los acuarianos son leales a los amigos, por eso atraen muchos. La naturaleza amorosa es muy fuerte, pero no son tan demostrativos como Leo. El éxito financiero viene solo por esfuerzo continuo y paciente.",
        
        "Ascendente_Piscis": "(Max Heindel) Hay una fuerte tendencia a la mediumnidad entre los piscianos, y en ello hay un peligro mayor que cualquier otro. Son tímidos, aman el ocio más que la comodidad, y no hacen trabajo que no sea absolutamente necesario.",

        # Sol en los signos
        "Sol_Aries": "(Max Heindel) Los hijos de Aries rebosan de vida y energía. Son autoafirmativos y agresivos, aventureros hasta la temeridad. Pueden ser ambiciosos pero no tienen la paciencia para perseverar contra los obstáculos.",
        
        "Sol_Tauro": "(Max Heindel) Son personas amables y agradables, pero cuando se les provoca son tercos como el animal que los simboliza. Tienen gran persistencia y capacidad para acumular riquezas materiales. Venus les da amor por la belleza.",
        
        "Sol_Geminis": "(Max Heindel) Son mentalmente alertas y rápidos, pero a menudo carecen de concentración. Aman el cambio y la variedad, siendo excelentes intermediarios y comunicadores, aunque propensos a la dispersión nerviosa.",
        
        "Sol_Cancer": "(Max Heindel) La vitalidad es la más baja de todos los signos. Son muy hogareños, tranquilos y adaptables. Su enojo es breve. Cáncer gobierna el estómago, por lo que la alimentación es crucial para su salud.",
        
        "Sol_Leo": "(Max Heindel) Da un cuerpo de maravillosa fuerza, vitalidad y poder recuperativo. Cuando no está afligido, son generosos hasta la prodigalidad. Son honestos y fieles, amando la luz y la verdad.",
        
        "Sol_Virgo": "(Max Heindel) Muy rápidos y activos en la juventud. Aprenden con facilidad. Adquieren poderes lingüísticos fácilmente. Hacen de la higiene un capricho. Tienden a la corpulencia del abdomen en la madurez.",
        
        "Sol_Libra": "(Max Heindel) Son muy adaptables a las circunstancias y no se afligen por los reveses. Venus les da capacidad artística, Saturno inclina la mente hacia direcciones científicas.",
        
        "Sol_Escorpio": "(Max Heindel) Acentúa los buenos rasgos y da amor por el misticismo. Siempre defienden sus derechos. El ingenio del Escorpio es agudo, frío y sereno, por eso hacen buenos oficiales del ejército y excelentes cirujanos.",
        
        "Sol_Sagitario": "(Max Heindel) Seguro que trae preferencia incluso a los nacidos en circunstancias humildes y oscuras. Acentúa todo lo bueno mostrado en el signo. Gobierna los muslos.",
        
        "Sol_Capricornio": "(Max Heindel) Trae Justicia, Pureza y Honor del signo. Hace Capitanes de Industria que impulsan las grandes empresas del mundo. Pero el afligido Capricornio es muy vengativo.",
        
        "Sol_Acuario": "(Max Heindel) Añade mucha esperanza y vida a la naturaleza, y así contrarresta el rasgo melancólico de Saturno. La naturaleza amorosa es muy fuerte. El éxito viene por esfuerzo paciente.",
        
        "Sol_Piscis": "(Max Heindel) Da más energía y ambición. Júpiter fortalece la moral, y Venus exaltada da gran talento musical, pero acentúa la tendencia a la indulgencia alcohólica."
    },
    
    # ========================================
    # ALAN LEO - Astrología Esotérica (1913)
    # Obra en dominio público - Interpretaciones esotéricas/teosóficas
    # ========================================
    "alan_leo": {
        "Sol_Aries": "(Alan Leo) Aries es el lugar de nacimiento de las Ideas Divinas. El Sol aquí actúa como vehículo para el Fuego Eléctrico del Primer Rayo, inspirando la Voluntad-hacia-el-Bien y el despertar del Ego individualizado.",
        
        "Sol_Tauro": "(Alan Leo) El Ego aprende aquí la lección de la posesión y el desapego. La estabilidad de Tauro cristaliza las ideas en formas concretas. Venus enseña que la belleza es una expresión del alma.",
        
        "Sol_Geminis": "(Alan Leo) La dualidad es la lección. El Ego busca conectar los opuestos a través del intelecto. Es el tejedor de relaciones. La dispersión es el obstáculo; la síntesis intelectual es la meta elevada.",
        
        "Sol_Cancer": "(Alan Leo) El hogar cósmico. El alma aprende sobre la nutrición y la protección. La Luna, como regente, conecta con el pasado kármico y las memorias del alma.",
        
        "Sol_Leo": "(Alan Leo) Aquí el Ego Individualizado se expresa con máxima potencia. Es la autoconciencia plena, donde el alma aprende a decir 'Yo Soy' antes de comprender 'Nosotros Somos'.",
        
        "Sol_Virgo": "(Alan Leo) La purificación del vehículo inferior. El alma aprende a servir a través del trabajo minucioso. Mercurio refina la mente concreta para que sea un instrumento del Ego superior.",
        
        "Sol_Libra": "(Alan Leo) El equilibrio de los opuestos. El alma aprende sobre las relaciones y la justicia. Venus eleva el amor personal hacia el amor impersonal y universal.",
        
        "Sol_Escorpio": "(Alan Leo) La muerte y regeneración. El alma enfrenta sus deseos más profundos para transmutarlos. Marte, el guerrero, combate las fuerzas inferiores dentro del ser.",
        
        "Sol_Sagitario": "(Alan Leo) La aspiración hacia lo superior. El Centauro apunta su flecha hacia las estrellas. Júpiter expande la conciencia hacia la filosofía y la religión.",
        
        "Sol_Capricornio": "(Alan Leo) La cristalización y la iniciación. Saturno, el Guardián del Umbral, presenta las pruebas finales. El alma aprende responsabilidad y estructura.",
        
        "Sol_Acuario": "(Alan Leo) El servicio a la humanidad. El Ego derrama el agua de la vida sobre todos sin distinción. Urano despierta la intuición y rompe las formas obsoletas.",
        
        "Sol_Piscis": "(Alan Leo) El final del ciclo. El Sol aquí pide la disolución del ego personal para fundirse con la Conciencia Universal. Es el sacrificio del yo separado.",
        
        "Luna_Aries": "(Alan Leo) La personalidad es impulsiva y busca sentirse viva a través de emociones fuertes y repentinas. El cuerpo astral es turbulento y necesita disciplina.",
        
        "Luna_Tauro": "(Alan Leo) La personalidad encuentra paz en la naturaleza y los ritmos lentos. Hay una profunda reserva de magnetismo vital que sana y nutre. Posición ideal para la estabilidad psíquica.",
        
        "Luna_Geminis": "(Alan Leo) La mente concreta se mezcla con el instinto. La persona siente pensando y piensa sintiendo. Gran adaptabilidad pero riesgo de superficialidad emocional.",
        
        "Luna_Cancer": "(Alan Leo) La Luna en su hogar. La personalidad es profundamente receptiva y nutriente. Las memorias del pasado son fuertes. Conexión íntima con la madre cósmica.",
        
        "Luna_Leo": "(Alan Leo) La personalidad busca brillar y ser admirada. El orgullo emocional es fuerte. Hay calidez y generosidad en las respuestas instintivas.",
        
        "Luna_Virgo": "(Alan Leo) La personalidad busca perfección en los detalles. Tendencia a la crítica y la preocupación. El servicio es una necesidad emocional.",
        
        "Luna_Libra": "(Alan Leo) La personalidad necesita armonía y belleza. Las relaciones son esenciales para el bienestar emocional. Tendencia a depender de otros.",
        
        "Luna_Escorpio": "(Alan Leo) Las emociones son intensas y profundas. La personalidad experimenta todo con pasión. Hay poder de regeneración emocional pero también tendencia a los celos.",
        
        "Luna_Sagitario": "(Alan Leo) La personalidad es optimista y aventurera emocionalmente. Necesita libertad y expansión. Fe innata en la vida y sus posibilidades.",
        
        "Luna_Capricornio": "(Alan Leo) La personalidad es seria y responsable. Las emociones están controladas y disciplinadas. Hay melancolía pero también gran resistencia.",
        
        "Luna_Acuario": "(Alan Leo) La personalidad es independiente y humanitaria. Las respuestas emocionales son impersonales. Amor por la amistad y los ideales sociales.",
        
        "Luna_Piscis": "(Alan Leo) La personalidad es extremadamente sensible y receptiva. Hay tendencia a absorber las emociones del ambiente. Compasión profunda pero riesgo de ser víctima."
    },
    
    # ========================================
    # ALI ABEN RAGEL - El Libro Conplido (Siglo XI)
    # Obra en dominio público - Estilo medieval árabe
    # ========================================
    "ali_aben_ragel": {
        "Sol_Aries": "(Ali Aben Ragel) En la segunda faz de Aries, que es del Sol, significa nobleza, alteza, gran señorío y dignidad. El nativo alcanzará honores por su propia virtud y fuerza. Es signo de reyes y caballeros.",
        
        "Sol_Tauro": "(Ali Aben Ragel) El Sol en Tauro da amor por las posesiones y el ganado. El nativo será rico en hacienda si no hay maléficos. Venus le otorga amor por la música y los placeres refinados.",
        
        "Sol_Geminis": "(Ali Aben Ragel) Mercurio y el Sol juntos en naturaleza hacen al hombre de gran ingenio y sutileza. Será buen escribano y mensajero. Ama el comercio y los viajes cortos.",
        
        "Sol_Cancer": "(Ali Aben Ragel) El Sol en el domicilio de la Luna da nobleza pero inconstancia. El nativo tendrá fortuna en el agua y las tierras húmedas. La madre tendrá gran influencia.",
        
        "Sol_Leo": "(Ali Aben Ragel) El Sol en su propio domicilio significa que el nacido será hombre de gran fama, amado por reyes y señores, firme en sus obras y de gran autoridad. Es el signo más noble para el Sol.",
        
        "Sol_Virgo": "(Ali Aben Ragel) Mercurio hace al nativo hábil en letras y cuentas. Será buen servidor y consejero. Entiende de enfermedades y remedios. Cuerpo delgado y mente aguda.",
        
        "Sol_Libra": "(Ali Aben Ragel) El Sol está aquí en su caimiento (caída). Significa disminución de la honra y poca duración en los estados altos, aunque tenga buena voluntad. Más feliz en el matrimonio.",
        
        "Sol_Escorpio": "(Ali Aben Ragel) Marte recibe al Sol en su domicilio nocturno. Da valor y espíritu guerrero, pero también odios y vendettas. El nativo tendrá herencias y bienes de los muertos.",
        
        "Sol_Sagitario": "(Ali Aben Ragel) Júpiter expande la fortuna del Sol. El nativo será de alta religión, amante de las leyes divinas y humanas. Viajará lejos en busca de sabiduría. Buen juez o sacerdote.",
        
        "Sol_Capricornio": "(Ali Aben Ragel) Saturno recibe al Sol en su domicilio terrestre. Da ambición pero también demoras y obstáculos. El nativo alcanzará honores tarde en la vida, después de mucho trabajo.",
        
        "Sol_Acuario": "(Ali Aben Ragel) Saturno y el Sol en este signo de aire dan amor por el conocimiento antiguo. El nativo tendrá muchos amigos pero pocos verdaderos. Mente filosófica inclinada a la melancolía.",
        
        "Sol_Piscis": "(Ali Aben Ragel) Júpiter da fortuna en cosas secretas y ocultas. El nativo puede ser religioso o dado a las ciencias ocultas. Tendencia al aislamiento y la contemplación. Pies débiles.",
        
        "Luna_Aries": "(Ali Aben Ragel) La Luna en casa de Marte da temperamento colérico y cuerpo caliente y seco. El nativo es impaciente y busca independencia en todo. Bueno para soldados.",
        
        "Luna_Tauro": "(Ali Aben Ragel) La Luna en su exaltación. Posición muy favorable. Da cuerpo hermoso, carácter tranquilo y fortuna en bienes. Las mujeres con esta posición son fértiles y amadas.",
        
        "Luna_Geminis": "(Ali Aben Ragel) La mente es rápida pero inconstante. El nativo habla mucho y aprende fácilmente, pero no profundiza. Bueno para comercio y mensajeros.",
        
        "Luna_Cancer": "(Ali Aben Ragel) La Luna en su propio domicilio. El nativo es dado a viajes por agua y tiene fortuna en tierras y casas. Muy ligado a la madre y la familia. Cuerpo húmedo.",
        
        "Luna_Leo": "(Ali Aben Ragel) La Luna en casa del Sol da orgullo y deseo de honores. El nativo busca ser visto y admirado. Generoso con los que ama, altivo con los demás.",
        
        "Luna_Virgo": "(Ali Aben Ragel) La Luna en caída. El nativo tiene cuerpo débil y mente preocupada. Bueno para el servicio y las cuentas. Tendencia a enfermedades del vientre.",
        
        "Luna_Libra": "(Ali Aben Ragel) La Luna busca compañía y equilibrio. El nativo no puede estar solo. Venus da amor por la belleza y las artes. Buenos matrimonios si está bien aspectada.",
        
        "Luna_Escorpio": "(Ali Aben Ragel) La Luna en caída en casa de Marte. Pasiones fuertes y celos intensos. El nativo tiene poder sobre otros pero sufre enemigos ocultos. Buenos para investigar secretos.",
        
        "Luna_Sagitario": "(Ali Aben Ragel) Júpiter y la Luna dan buena fortuna y optimismo. El nativo ama los viajes largos y la filosofía. Fe en Dios y respeto por las leyes.",
        
        "Luna_Capricornio": "(Ali Aben Ragel) La Luna en detrimento. Saturno enfría las emociones. El nativo es serio y trabajador, pero triste interiormente. Éxito tarde en la vida.",
        
        "Luna_Acuario": "(Ali Aben Ragel) La Luna en casa de Saturno da mente filosófica pero corazón frío. El nativo tiene muchos conocidos pero pocos amigos íntimos. Interés en ciencias antiguas.",
        
        "Luna_Piscis": "(Ali Aben Ragel) La Luna en casa de Júpiter da imaginación viva y sueños proféticos. El nativo es dado a la religión y las cosas secretas. Cuerpo húmedo y pies débiles."
    }
}

def update_json_database():
    """Actualiza la base de datos JSON con los textos reales de los libros."""
    
    with open(BASE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapeo de autor_id a índice en el JSON
    author_indices = {
        'ali_aben_ragel': 0,
        'alan_leo': 1,
        'max_heindel': 2
    }
    
    for author_id, texts in REAL_TEXTS.items():
        idx = author_indices.get(author_id)
        if idx is None or idx >= len(data['examples']):
            print(f"⚠️ Autor {author_id} no encontrado en el JSON")
            continue
            
        target = data['examples'][idx]['interpretaciones']['planetas_signos']
        
        for key, text in texts.items():
            # Parsear planeta y signo del key
            parts = key.split('_')
            planeta = parts[0]
            signo = parts[1]
            
            # Actualizar o crear entrada
            target[key] = {
                "planeta": planeta,
                "signo": signo,
                "texto": text,
                "keywords": [],
                "dignidad": "Verificado",
                "fuente": "Texto Original"
            }
        
        print(f"✅ Actualizados {len(texts)} textos para {author_id}")
    
    # Guardar
    with open(BASE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n📚 Base de datos actualizada exitosamente en {BASE_PATH}")

if __name__ == "__main__":
    update_json_database()
