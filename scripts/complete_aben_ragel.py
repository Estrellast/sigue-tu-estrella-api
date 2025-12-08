#!/usr/bin/env python3
"""
Script para crear el archivo JSON completo de interpretaciones de Ali Aben Ragel
basado en el texto extraído del Libro Conplido.

Este script extrae las descripciones generales de cada planeta y sus interpretaciones
en cada signo según el texto medieval.
"""

import json
import re

# Interpretaciones extraídas manualmente del texto auténtico de Aben Ragel
# Libro Conplido en los Iudizios de las Estrellas (siglo XIII)

interpretaciones_aben_ragel = {
    "source": {
        "book": "El Libro Conplido en los Iudizios de las Estrellas",
        "author": "Ali Aben Ragel (Ibn Abi 'l-Ridjal)",
        "translator": "Corte de Alfonso el Sabio",
        "year_original": "Siglo XIII",
        "edition": "Real Academia Española, 1954",
        "source_url": "https://www.cervantesvirtual.com/obra/el-libro-conplido-de-los-iudizios-de-las-estrellas--0/",
        "license": "Dominio Público",
        "notes": "Texto en castellano medieval, capítulo cuarto del Libro Primero sobre las naturas de las planetas"
    },
    "autor": {
        "id": "ali_aben_ragel",
        "nombre": "Ali Aben Ragel",
        "nombre_arabe": "Abu'l-Hasan 'Ali ibn Abi'r-Rijal",
        "obra_principal": "El Libro Conplido en los Iudizios de las Estrellas",
        "enfoque": "Astrología Medieval Árabe - Dignidades, Faces y Temperamentos"
    },
    "interpretaciones": {
        "planetas": {
            "Sol": {
                "descripcion_general": "El Sol es lumbre del cielo e su candela e gouernador del mundo e fazedor de los tiempos. E por el se fazen las planetas orientales e occidentales e por el seran parecidas e escondidas e por el se mueue toda cosa mouiente e por el nace toda cosa naciente e crece toda cosa creciente. E el es el espirito del cielo grant e con el se abiuan los signos. E el Sol es mas noble e meior que todas las otras planetas e mas alto en nobleza; que su natura obra en todas las naturas e ninguna de las otras naturas non obran en el.",
                "naturaleza": "Luminar mayor, planeta de grant sennorio e poderio e nobleza e alteza e grandez. Es fortuna por catamiento e infortuna por ayuntamiento de cuerpo.",
                "significados": "Significa los padres, el regno, la alteza, el sennorio."
            },
            "Luna": {
                "descripcion_general": "La Luna es luminar menor e es sennor del ascendente del mundo e semeia al omne mas que todas las otras cosas en conpençamiento de su engendramiento e en su menguamiento después. Ca ella conpieça chica e ua creciendo recibiendo la lumbre del Sol tro ques para en su opposicion.",
                "naturaleza": "Su natura de la Luna es fria e vmida. Es rey de la noche e su governador e poderosa en la mar en so crecer e en so menguar. Es aparcera del ascendente e de su sennor en toda nacencia e en toda question.",
                "significados": "Por la Luna es la fermosura de las estrellas e su feeldat. Significa la criança, las lluuias, la rafecia e carestia del precio del pan."
            },
            "Saturno": {
                "descripcion_general": "Saturno es la planeta uieio, grant, cansado, planeta de despreciamiento e de cuydados e de tristezas e de enfermedades luengas. Su natura es fria e seca, semeia a melanconia, ques gouierna de todas las vmores. Es seco e enuidioso, tiene luenga sanna, de poca fabla, non quiere conpanna, quiere estar sennero e apartado. A profundos asmamientos e sotil memoria, piensa e cata en las cosas antiguas.",
                "naturaleza": "Frio e seco, melancólico. Non a entendimiento ligero, es mintroso e traydor, faze fechizos de legar e nigromancias e marauillas. Con los reyes es semeiante de rey.",
                "significados": "Ama edificar e sembrar e plantar e poblar. Non a solaz con ninguno, pesado de andar e de mouer, de poco usar de mugeres, sterle."
            },
            "Jupiter": {
                "descripcion_general": "Jupiter es planeta de la egualdad e de la comunaleza e del bien e de ameioramiento e del entendimiento e del seso e piedat; que es temprado e egual e fortuna por catamiento e por corporal ayuntamiento. Significa el bien e la meiorança e la ley e la simplicidat e la castidat, e endereça e non danna, puebla e non yerma.",
                "naturaleza": "Temprado e egual, fortuna por catamiento. Es de fermoso parecer e de apuesta persona, obediente, manso, fiel, leal, piadoso, manda el bien e muestralo e uieda el mal e aborrecelo, ayuda a los pobres e gouierna a los que lo an menester.",
                "significados": "Es uerdadero en sus fechos e en sus dichos, de buen solaz e de buen amor e de buena amiztat e uerdadera e sin enganno, conplido e sano en su cuerpo e en sus miembros, bien andante en sus fechos e en sus obras, ama alcaldias e decretos e iudizios."
            },
            "Marte": {
                "descripcion_general": "Mars es planeta caliente e seca, igneo, de malhetria natural, nocturno, feminino, gastador, malhetrero, sannudo, uencedor, porfidioso, ama matar e matanças e uaraias e pleytos e contrallar, ligera mient infortuna, loco e non sufre, ensannas ayna de fuerte sanna.",
                "naturaleza": "Caliente e seco, igneo. Mete todo su coraçon en fazer sus cosas, non manda a ssi quando es sannudo ni torna su mano de fazer lo ques le antoia, mueue guerras e faziendas, faze batallas, yerma poblados.",
                "significados": "Es necio e oluidoso, de poco entendimiento, menguado de seso, non para mientes en las fines de las cosas. Suya es ladronia e furtar e robar caminos e ferir e afogar."
            },
            "Venus": {
                "descripcion_general": "Venus es fortuna, fria e vmida, nocturna, alegre, gozosa, risuenna, de buen parecer, afeytada, limpia, fermosa, ama ioglerias e alegrias e cantares e comer e beuer e uicios, mansa, de poco mouimiento.",
                "naturaleza": "Fria e vmida, nocturna. Es significador de las mugieres e de amor e de iazer con mugieres e de amiztat e de conpannia. Es de buena uoluntat e de sabrosas palabras e franca e de mansos dichos.",
                "significados": "Sos maestrias e sus saberes son en fazer cantos e en adobar sones e en tanner estrumentos. Della es el debuxar e el pintar e la sotileza de mano e de las maestrias. Non puede sofrir mal nin sanna nin uaraia nin infortunio porque su natura es natura de las mugeres."
            },
            "Mercurio": {
                "descripcion_general": "Mercurio es planeta de malhetrias e de forçamientos e de ensennamientos e de escriuanias e de cuentas e de sciencias. Es caliente e seco, conuertible de forma e de natura, masculino con masculino e feminino con feminino, fortuna con fortuna e infortuna con infortuna.",
                "naturaleza": "Caliente e seco, conuertible. Bien razonado e bien fablante, osado en fablar, de fermoso parecer e apuesta persona, mancebo, ama los libros e las cuentas, pagas de las maestrias e de las cosas bien fechas e de las fermosas razones e de romançes e de uersificar.",
                "significados": "Es ligero de mouer e de ardiente propriedat e alegre, mouedizo en todas las cosas. Es flaco de coraçon e mintroso e mesturero, sotil e sabidor de mannas engannosas. El su estado es escontra el Sol estado de escriuano ligero e mannoso."
            }
        },
        "planetas_signos": {
            # SOL en signos
            "Sol_Aries": {
                "texto": "(Ali Aben Ragel) E el Sol quando es en todos los grados de Aries, faze uiles los altos e abaxa los sennores e a poder en malhetrias e en cruezas e en uictorias e en fazer mal."
            },
            "Sol_Tauro": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Tauro es rey que da uoluntat de matanças e de batallas e de uencer e de fazer algaras e de conquirir."
            },
            "Sol_Geminis": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Gemini es rey de flaco espirito e de chico poder e guias por su uoluntat e por su sabor e faze cosas quel auiltan e quel abaxan."
            },
            "Sol_Cancer": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Cancer es sennor que ama cantares e ioglerias e iuegos e oyr romances e fablielas e amar afeytamientos e limpiedat e apartamiento e esquiuamiento de los omnes."
            },
            "Sol_Leo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Leon es rey que demuestra sus armas e desuayna sus espadas e guisa sos cauallos e sus cauallinas por uencer e lidiar los reyes sos uezinos."
            },
            "Sol_Virgo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Virgo es rey que ama ioglerias e cantares e estarse quedo. So uoluntat es en comer e en beuer e en cosas odoriferas e en folgar e en todos los uicios del cuerpo."
            },
            "Sol_Libra": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Libra es rey quel uencieron e quel tomaron su regno e mataron sos cauallerias e ua fuyendo desnuyo; que a miedo grant de perder el cuerpo."
            },
            "Sol_Escorpio": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Escorpion es omne alto de grant fermosura e de conplido cuerpo e de limpiedat e de fermosos uestidos e de apuesto parecer e temudo."
            },
            "Sol_Sagitario": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Sagitario es rey apoderado, malfechor. Faze mal a los omnes e roba e toma sin derecho e mata los omnes sin derecho e yerma las poblaciones."
            },
            "Sol_Capricornio": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Capricorno es rey de grant fama e de grant nombradia e buena. Tuelle los omnes malos e arriedra los malos fechos e uieda los poderosos de fazer mal a los flacos e a la yente menuda."
            },
            "Sol_Acuario": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Aquario es rey de chica nombradia e de poca fama e de pocos siruientes. Faze sus cosas el por si, pero es poderoso sobre su yente e de fuerte mandado e precias mas que non uale."
            },
            "Sol_Piscis": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Piscis es sennor de iuegos e de ioglerias e de risos e de pereza e de estar quedo e de seguir sus uoluntades e de malas mannas e de malas naturas."
            },
            
            # LUNA en signos
            "Luna_Aries": {
                "texto": "(Ali Aben Ragel) La Luna quando es en todas las partes de Aries, es rey alto e de grant forma e de grant poder e fermoso e conplido de cuerpo e de apuesto parecer e temido."
            },
            "Luna_Tauro": {
                "texto": "(Ali Aben Ragel) E quando es en todas las partes de Tauro, es rey de ancho regno e bien puesto e sus faziendas eguales e bien puestas, amado de sos omnes e de sos pueblos, conplido e abastado, ama folguras e alegrias e uicios."
            },
            "Luna_Geminis": {
                "texto": "(Ali Aben Ragel) E quando es en todas las partes de Gemini, es pobre e mezquino e dannado de mienbros e sus faziendas malas e mal puestas, e de malos uestidos e malas qualidades en su cuerpo e en su uicto."
            },
            "Luna_Cancer": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Cancer es de grant alteza e de alto grado e de ancho regnado, sennor de poder e de mandar e de uedar e de buen parecer e limpiedat e fermosura e grant persona e temudo e a sennorio."
            },
            "Luna_Leo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Leon es rey noble coronado, desprecianle su yente e sus pueblos e mandan e uiedan en el regno sin el e fazen lo que quieren a menos de su mandado."
            },
            "Luna_Virgo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Virgo es triste e con muchos cuedados e cuytado con cuetas e de pannos rotos. Sirue a los omnes predicando e diziendo romançes e fablielas, trae los malos e los enpeecimientos a ssi."
            },
            "Luna_Libra": {
                "texto": "(Ali Aben Ragel) En las partes de Libra es rey coronado ques entremete de comer e de beuer e de folgar. Non piensa de sus faziendas ni a cuedado dellas. Ama alegrias e cantares e mugieres e oyr fablielas e trebeiar."
            },
            "Luna_Escorpio": {
                "texto": "(Ali Aben Ragel) E en las partes de Escorpion es de muchos cuedados e de muchas tristezas. Trae el mal a ssi por su mal seso e acaecenle enpeecimientos por sos malos asmamientos."
            },
            "Luna_Sagitario": {
                "texto": "(Ali Aben Ragel) En las partes de Sagitario es rey coronado muy necio, non piensa de ninguna cosa ni entiende su bien ni su mal ni a cuedado de su regno ni de su pueblo."
            },
            "Luna_Capricornio": {
                "texto": "(Ali Aben Ragel) En las partes de Capricorno es omne noble e alto e de grant prez e buena nombradia e buena fama e fermoso e apuesta persona e de buenos uestidos e limpio."
            },
            "Luna_Acuario": {
                "texto": "(Ali Aben Ragel) En las partes de Aquario es açorero que ama seguir a omnes que fuyen e ama caçar e ama mucho andar e uenir. E es de mucho mouimiento, faze cosas que nol tienen pro en sus faziendas ni en sus uictos."
            },
            "Luna_Piscis": {
                "texto": "(Ali Aben Ragel) En las partes de Piscis es semeiante de sieruo e despreciado en su abito e en sus uestidos. Ama caçar e trebeiar e iogar iuegos en que pierde e estarse quedo e non pensar de ninguna su fazienda."
            },
            
            # SATURNO en signos (ya tenemos algunos, agregamos los faltantes)
            "Saturno_Aries": {
                "texto": "(Ali Aben Ragel) Quando Saturno es en la primera faz de Aries, es de afeytado parecer e de pintada uista e precias de matanças e de batallas. E en la segunda faz de Aries aciende los fuegos e mete guerras entre los omnes e mal querencias entre unos e otros. E en la tercera faz de Aries danna las cosas sembradas e arranca los arboles e yerma las poblaciones."
            },
            "Saturno_Tauro": {
                "texto": "(Ali Aben Ragel) En la primera faz de Tauro es enfeminado en sus fechos, iaze con los moços e con los ninnos chicos e con las ninnas chicas. E en amas las otras fazes de Tauro es uieio, flaco, de miembros dannados, de cuerpo cansado e dannada fuerça e llama bozes de fazer duelo sobre si mismo."
            },
            "Saturno_Geminis": {
                "texto": "(Ali Aben Ragel) E en todo Gemini es de mala qualidat e triste e endolorido e de angosta uida e de mal parada fazienda."
            },
            "Saturno_Cancer": {
                "texto": "(Ali Aben Ragel) E en todo Cancer es de muy feo rostro e de marauillosa criatura en su forma e en su parecer que se espantan de su figura e marauillan-se quantos le ueen e quantos oen del fablar."
            },
            "Saturno_Leo": {
                "texto": "(Ali Aben Ragel) En la primera faz de Leon muestra treuença e fuerça e sofrimiento e el ama duelos e miedos. E en la segunda faz de Leon muestra ley e llora sos pecados, e en la tercera faz de Leon es pobre, despreciado e medroso."
            },
            "Saturno_Virgo": {
                "texto": "(Ali Aben Ragel) En la primera faz de Virgo es dolorido, de miembros dannados, de muchos cuedados e tristezas, non a fuerça ninguna ni mouimiento ninguno. En la segunda faz de Virgo precias e gabas de las cosas que non puede fazer nin conplir. En la tercera faz de Virgo es de mala fazienda e parecida pobreza, pide a los omnes por mercet que coma."
            },
            "Saturno_Libra": {
                "texto": "(Ali Aben Ragel) En la primera faz de Libra es sennor de regno e de alteza e corona e nobleza e sermono. En la segunda faz de Libra es sennor de matanças e de batallas e de uencimientos e de cauallos e de armas e de guisamientos. E en la tercera faz de Libra es pobre e mezquino, triste, cuetoso, desnuyo, descubierta su uerguença."
            },
            "Saturno_Escorpio": {
                "texto": "(Ali Aben Ragel) En la primera faz de Escorpion ama tirar de ballesta e caçar e caualleria. En la segunda faz de Escorpion es matador e afogador e afrontador e enuidioso. En la tercera faz de Escorpion es de marauillosa criatura e fea e de mucho mal e de mucha uaraia."
            },
            "Saturno_Sagitario": {
                "texto": "(Ali Aben Ragel) E en todas las fazes de Sagitario es grant, cansado, de mienbros dannados, de espinazo coruo, de parecida pobreza e de manifiesta mezquindat."
            },
            "Saturno_Capricornio": {
                "texto": "(Ali Aben Ragel) En la primera faz de Capricorno es dolorido e cuetoso de grandes cuetas, despreciado, triste, caydo, llora e messa sus cabellos. En la segunda faz e en la tercera de Capricorno ama cauar e edificar e trabaiarse de sembrar e de fazer correr rrios e fazer pozos e sacar aguas e plantar e poblar."
            },
            "Saturno_Acuario": {
                "texto": "(Ali Aben Ragel) En todas las partes de Aquario ama luchar e matar e attreuimiento e aforçamiento en las cosas fuertes e medrosas."
            },
            "Saturno_Piscis": {
                "texto": "(Ali Aben Ragel) En la primera parte de Piscis ama matanças e malhetrias e sannas e lazarias. E en la segunda faz de Piscis e en la tercera guia los ciegos e aconpanna los pobres e sirue a los que an los mienbros dannados e a los enfermos."
            },
            
            # JUPITER en signos
            "Jupiter_Aries": {
                "texto": "(Ali Aben Ragel) Es Jupiter en todas las partes de Aries noble. Ama uicios e abondanças e comer e uestir e afeytarse."
            },
            "Jupiter_Tauro": {
                "texto": "(Ali Aben Ragel) En la primera faz de Tauro es omne de saber e de iudgar e de buenas mannas e de escreuir. E en la segunda e en la tercera faz de Tauro es hadrubado e de mienbros dannados e de pezcueço quebrantado e coruo espinazo e de mala qualidat e parecida pobreza e es uil."
            },
            "Jupiter_Geminis": {
                "texto": "(Ali Aben Ragel) En la primera faz de Gemini es de pintado parecer e de fermoso solaz, entremetés de libros e de escreuir e de leer e de saber e de buenas mannas e de philosofia. En la segunda faz de Gemini es farto e abastado, demanda iazer con las mugieres por fuerça. En la tercera faz de Gemini es desuergonçado e descubierto, parecida su licherria, sabidor de engarrano e de traycion."
            },
            "Jupiter_Cancer": {
                "texto": "(Ali Aben Ragel) En la primera faz de Cancer es omne pleytes e bozero e contrallador de las cosas, ama matanças e seguir sos uoluntades. En la segunda faz de Cancer es rey alto e noble e de alto poder, guarnido con sus armas, guisado e presto pora matar e lidiar. En la tercera faz de Cancer ama caçar e seguir los bestiglos e ama matanças por mannas e por engannos."
            },
            "Jupiter_Leo": {
                "texto": "(Ali Aben Ragel) En todas las partes de Leon es omne de caça e tirador de ballesta e ama matanças e caualleria e demandar los enemigos."
            },
            "Jupiter_Virgo": {
                "texto": "(Ali Aben Ragel) En la primera faz de Virgo es escriuano e contador e ama sciencias e philosophia e es de buen solaz e renunciador de departimientos. En la segunda faz es sannudo e malfetrero e dannador. En la tercera es flaco e cansado, perezoso, triste, dannado de sus mienbros."
            },
            "Jupiter_Libra": {
                "texto": "(Ali Aben Ragel) En la primera faz de Libra ayunta aues e guardalas e fazelas maneras e caça con ellas. En la segunda faz es pobre e uil e menguado. En la tercera faz es rey noble e ondrado e alto e de grant sennorio."
            },
            "Jupiter_Escorpio": {
                "texto": "(Ali Aben Ragel) En la primera faz de Escorpion es tirador de ballesta e guiador de caualleria e omne de sennorio e de nobleza e ama matanças e cauallerias. En la segunda faz e en la tercera es auenturado en caçar e en ganar e en allegar auer e en conplir sus uoluntades e sus desseos e es desuergonçado en seguir sus uoluntades."
            },
            "Jupiter_Sagitario": {
                "texto": "(Ali Aben Ragel) En todas las partes de Sagitario ama caualgar e guisarse pora lidiar e guarnirse de todas armas e de omnes e de todo guarnimiento e guisamiento bueno e fermoso."
            },
            "Jupiter_Capricornio": {
                "texto": "(Ali Aben Ragel) En todas las partes de Capricorno es de mala fazienda e flaco e pobre e dolorido e de dannados mienbros."
            },
            "Jupiter_Acuario": {
                "texto": "(Ali Aben Ragel) En la primera faz de Aquario es caçador e uestidor de buenos pannos e fermosos e fermoso e apuesto e temudo e afeytado. En la segunda faz de Aquario ama comer e beuer e folgar en uicio e en abondancia. E en la tercera faz tal como en la primera."
            },
            "Jupiter_Piscis": {
                "texto": "(Ali Aben Ragel) En la primera faz de Piscis es maestro, demostrador de sciencias e de decretos e leedor de libros e pensar e estudiar en las cosas profundas e fuertes de entender. En la segunda faz de Piscis es noble e alegre e gozoso, ama cantares e ioglerias e uicios e abondancias. En la tercera faz de Piscis es matado echado entre uestiglos quel comen."
            },
            
            # MARTE en signos
            "Marte_Aries": {
                "texto": "(Ali Aben Ragel) En la primera faz de Aries faze roydos e marauillas e ama furtos e engannos e pleytos e alçase sobre los malos e los escassos e los uaraiosos. E en la segunda faz de Aries es de parecidas armas e guisado pora varaiar. Temenle quantos le ueen. Mata ligera miente a qui quier quel contralla. En la tercera faz es temido e afeytado de fermoso afeytamiento, tiene en su mano espada tirada, menaza con ella a los omnes e meteles miedo."
            },
            "Marte_Tauro": {
                "texto": "(Ali Aben Ragel) En la primera faz de Tauro es desuergonçado que sigue su uoluntat, celoso, ama e busca iazer con mugieres por fuerça e por uencimientos. En la segunda faz de Tauro saca espadas e mueue uaraias e uierte sangres e mata omnes. En la tercera faz de Tauro es de forma fea marauillosa, rostro dannado, ama ioglerias e alegrias e cantares e uicios."
            },
            "Marte_Geminis": {
                "texto": "(Ali Aben Ragel) En la primera faz e en la segunda de Gemini es cauallero que tiene su espada colgada e trae sus guarnimientos e sus armas e anda en semeiante de qui busca cosa que fuyo e quel salió de mano. En la tercera faz de Gemini es uil e pobre, menguado, sirue a los pobres e a los de miembros dannados e a los que piden por Dios."
            },
            "Marte_Cancer": {
                "texto": "(Ali Aben Ragel) En la primera faz de Cancer es caualgador, tiene bestias, e tirador con ballesta e entremetés de caualleria e es temudo. En la segunda faz de Cancer es de rostro dannado e marauillosa forma e marauillan-se los omnes del. En la tercera faz de Cancer es caçador de culuebras e de otras reptilias, escantador de culuebras, melezina los omnes por escantos e por palabras."
            },
            "Marte_Leo": {
                "texto": "(Ali Aben Ragel) En la primera faz de Leon es tirador de ballesta e tenedor de armas, podiente e attreuido e fuerte. En la segunda e en la tercera faz de Leon es triste e a cuedados e dolorido, fiere su cabeça e messa su barua con su mano."
            },
            "Marte_Virgo": {
                "texto": "(Ali Aben Ragel) En la primera faz de Virgo es de feo catamiento e de rostro dannado, tenedor de sanna, ligero pora matar qui quiere, non dubda cometer las cosas malas e esquiuadas de los omnes. En la segunda e en la tercera faz de Virgo es hadrubado, de miembros dannados, de mala fazienda e pobre e menguado e uil e uieio."
            },
            "Marte_Libra": {
                "texto": "(Ali Aben Ragel) En la primera faz e en la segunda de Libra es tenedor de armas e tirador de ballesta e es temudo e de buen parecer e afeytado. En la tercera faz ama ioglerias e uicios e alegrias e cantares e folgura e comer e beuer."
            },
            "Marte_Escorpio": {
                "texto": "(Ali Aben Ragel) En la primera faz de Escorpion es ualiente, guardador de lo suyo, parecido, nombrado, llega a lo que quiere e faze de sos enemigos lo que quiere. En la segunda faz de Escorpion es desnuyo e descubierto, de mala obra, sirue a los enuidiosos e a los uaraiosos e a los guerreros. En la tercera faz de Escorpion es muy amador de las mugieres e demándalas forçandolas, sannudo, ensannase sobre si mismo."
            },
            "Marte_Sagitario": {
                "texto": "(Ali Aben Ragel) En la primera faz de Sagitario e en la segunda es temudo, sofridor e ualiente e attreuido e alegre. En la tercera faz de Sagitario es enfeminado, chufador, semeia a las mugieres en flaqueza e en pereza e en fablar e en uestir e en afeytar."
            },
            "Marte_Capricornio": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Capricorno es sennor de regnado e de nobleza e de uictoria e de sennorio, uencedor de sus enemigos, entremeteos en las cosas fuertes e de que an miedo los omnes."
            },
            "Marte_Acuario": {
                "texto": "(Ali Aben Ragel) En la primera faz de Aquario anda metiendo uaraias e mueue a los malos por fazer mal a los omnes. En la segunda faz de Aquario caualga bestias e mueue batallas e matanças e comete los enemigos e sirue a los malos e endereça los cauallos. En la tercera faz de Aquario es hadrubado, de miembros dannados, non a poder en si de fazer bien ni mal."
            },
            "Marte_Piscis": {
                "texto": "(Ali Aben Ragel) En la primera faz de Piscis es donneador e ama ioglerias e chufar con mugieres e iazer con ellas e seguir sus sabores. En la segunda faz de Piscis es uencedor e matador de los omnes por fuerça sin razon. En la tercera faz de Piscis faze miraglos e marauillas e cosas temudas e sonadas."
            },
            
            # VENUS en signos
            "Venus_Aries": {
                "texto": "(Ali Aben Ragel) E Venus quando fuere en todas las partes de Aries, es triste e dolorida e pobre e menguada e cuydadosa e acaecel enpeecimientos e occasiones e pesares e duelos."
            },
            "Venus_Tauro": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Tauro es muy noble e alta, de grant fama e de grant nombradia e de alto estado escontra los reyes e sos fijos e escontra los nobles e los altos e los ensennoreados."
            },
            "Venus_Geminis": {
                "texto": "(Ali Aben Ragel) E en las partes de Gemini es de buen talant e piadosa, busca bien a los omnes, entremetés de fazer bien a los flacos omnes e a los pobres e a los cuetados."
            },
            "Venus_Cancer": {
                "texto": "(Ali Aben Ragel) E quando fuere en todas las partes de Cancer, ama deportar e comer e beuer con los omnes e ama aliofar e piedras preciadas e maneras de afeytamientos e pannos."
            },
            "Venus_Leo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Leon es dannada de miembros e pobre e menguada, de malas faziendas e de diuersa forma e natura."
            },
            "Venus_Virgo": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Virgo es dolorida e cuetosa e triste, de mienbros dannados, aconpannas con los pobres e con los menguados e con los de los mienbros dannados."
            },
            "Venus_Libra": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Libra es sennora de cauallerias e de alcaydias e de armas e de guarnimientos, comete a los enemigos con caualleros e armas e guarnimientos."
            },
            "Venus_Escorpio": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Escorpion ama matanças e sannas e malhetrias e demanda sus cosas por fuerça que faze a aquellos que las tienen."
            },
            "Venus_Sagitario": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Sagitario ama tirar de ballesta e bofordar e torneos."
            },
            "Venus_Capricornio": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Capricorno ama ioglerias e beuer e enbebdarse e ama limpiedat e cantar e fermosas casas e uicios e conpannia."
            },
            "Venus_Acuario": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Aquario ama caçar e seguir e tener acores e falcones e aguilas."
            },
            "Venus_Piscis": {
                "texto": "(Ali Aben Ragel) E en todas las partes de Piscis es rey ensennado e sabio, de grant regno e de conplido sennorio, faze sus cosas por seso e por asmamiento, mantiene su regno e su pueblo por sabiduria e por sciencias e buenas mannas e alabadas."
            },
            
            # MERCURIO en signos
            "Mercurio_Aries": {
                "texto": "(Ali Aben Ragel) E quando Mercurio fuere en todas las partes de Aries, es matador e uaraiador e contrallador e bozero."
            },
            "Mercurio_Tauro": {
                "texto": "(Ali Aben Ragel) E en las partes de Tauro es beuedor e ioglar e ama alegria e cantar e folgura e uicio."
            },
            "Mercurio_Geminis": {
                "texto": "(Ali Aben Ragel) En las partes de Gemini cobdicia lidiar e aguisase a matarse, condura los omnes a las cosas celadas e cubiertas."
            },
            "Mercurio_Cancer": {
                "texto": "(Ali Aben Ragel) En todas las partes de Cancer es dolorido e cuetoso e triste e de mala fazienda."
            },
            "Mercurio_Leo": {
                "texto": "(Ali Aben Ragel) En todas las partes de Leon es ualiente cauallero, matador, busca las cosas por fuerça e por uencimiento, ama almogauerias e batallas."
            },
            "Mercurio_Virgo": {
                "texto": "(Ali Aben Ragel) En todas las partes de Virgo es ualiente, tirador con ballesta e tenedor de armas e de bestias e cauallos e caualleros e omnes e peones e buenos guisamientos."
            },
            "Mercurio_Libra": {
                "texto": "(Ali Aben Ragel) En todas las partes de Libra es tenedor de libros e leedor e contador e entremetes de los saberes."
            },
            "Mercurio_Escorpio": {
                "texto": "(Ali Aben Ragel) En todas las partes de Escorpion es fermoso e apuesto e de buen parecer, temudo e de fermosos uestidos e de buenas caualgaduras e afeytado e limpio."
            },
            "Mercurio_Sagitario": {
                "texto": "(Ali Aben Ragel) En todas las partes de Sagitario es matador e tenedor de guarnimientos e de armas e guisado pora lidiar."
            },
            "Mercurio_Capricornio": {
                "texto": "(Ali Aben Ragel) En todas las partes de Capricorno es pobre, menguado, desnuyo, lazrado, enfermo, dannado de mienbros, de paladino mal e de paladina uileza."
            },
            "Mercurio_Acuario": {
                "texto": "(Ali Aben Ragel) En todas las partes de Aquario es astrologo e agurero e geomanciano e entremetés de soluer suennos e adeuinancias."
            },
            "Mercurio_Piscis": {
                "texto": "(Ali Aben Ragel) En todas las partes de Piscis es fermoso e agudo e entendudo, de afeytado parecer, de fermosos uestidos, conplido de cuerpo e de miembros, limpio e ondrado e loçano."
            }
        }
    }
}

# Guardar el archivo JSON
output_path = "/Users/franciscomanuel/.gemini/antigravity/playground/spectral-photosphere/static/data/interpretaciones_aben_ragel.json"

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(interpretaciones_aben_ragel, f, ensure_ascii=False, indent=2)

print(f"✅ Archivo guardado en: {output_path}")
print(f"📊 Total de interpretaciones de planetas: {len(interpretaciones_aben_ragel['interpretaciones']['planetas'])}")
print(f"📊 Total de interpretaciones planeta-signo: {len(interpretaciones_aben_ragel['interpretaciones']['planetas_signos'])}")
