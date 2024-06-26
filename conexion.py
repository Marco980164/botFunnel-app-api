from openai import OpenAI
# USAR CON RESPONSABILIDAD LA API DEBIDO A QUE SOLO TIENE 10 DLS DE SALDO
# API KEY CON SALDO: ""


# Cliente para conectarse a OpenAI
client = OpenAI(api_key="")

# Variables para configurar el chatbot
name = "Juan"
purpose = "ayudar a calificar clientes prospectos"
enviroment = "una empresa desarrolladora de software"
company = "Cantera Digital"
extra_context = "sin contexto extra"

complexity = "Coloquial"
conversation_purpose = "Entrevistar"
emotion = "Asertividad"
analogies = "False"
empathy = "Baja"
length = "Corta"
feedback = "Medio"
tone = "Formal"

# Prompt para configurar el chatbot en las conversaciones
config = (
    f"Eres un chatbot que se llama {name} con el propósito de {purpose} dentro del entorno de {enviroment} llamada {company}."
    "Dentro de esta conversación tendrás las siguientes características:"
    f"Complejidad del lenguaje: {complexity}."
    f"Propósito de la conversación: {conversation_purpose}."
    f"Emoción de la conversación: {emotion}."
    f"Uso de analogías: {analogies}."
    f"Nivel de empatía: {empathy}."
    f"Longitud de respuestas: {length}."
    f"Nivel de retroalimentación por parte del cliente: {feedback}."
    f"Tono de la conversación: {tone}."
    f"Contexto extra: {extra_context}"
)

# Diccionario para correccion de pregunta y adecuacion de la misma
# Se usara la variable pregunta_corregida para guardar la respuesta del chatbot
questions = [
    {"role": "system",
     "content": config
     },
]

# Diccionario para separar las respuestas
# Se usara la variable clasificacion para guardar la respuesta del chatbot
answer_classification = [
    {"role": "system",
     "content": "Evalua la pregunta y respuesta. Si la respuesta es correcta con respecto a la pregunta, escribe OK. Si la respuesta es incorrecta o si el usuario esta preguntando una duda escribe ERROR."
     },
]

# Diccionario para corregir respuestas erroneas
# Se usara la variable correccion_del_usuario para guardar la respuesta del chatbot
answer_correction = [
    {"role": "system",
     "content": "Dile al usuario de forma educada que la respuesta que nos dio no es correcta y repitele la pregunta. Si esta preguntando una duda contestala de forma educada y pide que repita la pregunta."
    },
]


# Diccionario para calificar las preguntas y respuestas
# Se usara la variable evaluacion para guardar la respuesta del chatbot
answers_evaluation = [
    {
        "role": "system",
        "content": "Evalua la pregunta y respuesta en un rango de 0 a 10. Siendo 0 la peor calificación y 10 la mejor calificación. Solamente regresa el número de la calificación.",
    },
]


# Lista de preguntas por hacer al chatbot
preguntas = [
    {
        "pregunta": "A que se dedica tu empresa",
        "descripcion": "Pregunta para obtener cual es el giro de la empresa del cliente",
        "tonopregunta": "Formal",
        "lenguaje": "Formal"
    },
    {
        "pregunta": "De donde es originaria tu empresa?",
        "descripcion": "Pregunta para obtener de que ciudad, estado o pais es la empresa del cliente",
        "tonopregunta": "Informal",
        "lenguaje": "Informal"
    },
]

# Lista de preguntas y respuestas finales
final_answers = []

# Lista de calificaciones finales
calificaciones = []

# POR ESTA SECCION DEBERIA DE EMPEZAR UN CICLO FOR PARA RECORRER TODAS LAS PREGUNTAS

for pregunta in preguntas:
    # Escribir un prompt para corregir la pregunta y configurarla con los parametros deseados
    question_prompt = "Reescribe la pregunta de la forma deseada y correcta ortograficamente siguiendo los parametros: Pregunta: " + pregunta["pregunta"] + " Descripcion: " + pregunta["descripcion"] + " Tono de la pregunta: " + pregunta["tonopregunta"] + " Lenguaje: " + pregunta["lenguaje"] + "."
    print(question_prompt)
    # Pasarle la pregunta y los parametros necesarios al bot para reescribir la pregunta de la forma deseada y correcta ortograficamente al diccionario questions
    questions.append({"role": "user", "content": question_prompt})
    # Guardar la respuesta del chatbot en content y despues en la variable pregunta_corregida

    content = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=questions,
        temperature=1,
        max_tokens=200
    )

    pregunta_corregida = content.choices[0].message.content

    # Mostrar la pregunta corregida al usuario
    print(pregunta_corregida)

    respuesta_buena = False
    # Inicio de un ciclo while para clasificar la pregunta y respuesta
    while respuesta_buena == False:
        # Solicitar respuesta al usuario
        input_message = input()

        # Creacion de prompt para clasificar pregunta y respuesta
        classification_prompt = "Pregunta: " + pregunta_corregida + " Respuesta: " + input_message
        # Pasarle la pregunta y respuesta al bot para clasificarla al diccionario answer_classification
        answer_classification.append({"role": "user", "content": classification_prompt})
        # Guardar la respuesta del chatbot en content y despues en la variable clasificacion

        content = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=answer_classification,
            temperature=1,
            max_tokens=200
        )
        clasificacion = "Modifica este valor"  # Quitar esta linea cuando se tenga el codigo completo
        clasificacion = content.choices[0].message.content

        # Logica para saber como responder de acuerdo con la clasificacion
        if clasificacion == "ERROR":
            print("Respuesta incorrecta. Aqui debe ir el prompt para respuesta erronea")

            prompt_correction = "Respuesta incorrecta que dio el usuario: " + input_message + " Pregunta por repetir: " + pregunta_corregida
            # Pasarle la pregunta corregida al bot para que le pida al usuario que repita la pregunta
            answer_correction.append({"role": "user", "content": prompt_correction})
            # Guardar la respuesta del chatbot en content y despues en la variable correccion_del_usuario

            content = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=answer_correction,
                temperature=1,
                max_tokens=200
            )

            correccion_del_usuario = content.choices[0].message.content
            print(correccion_del_usuario)


        else:
            print("Respuesta correcta. Aqui debe ir el prompt para respuesta correcta")
            final_answers.append({"pregunta": pregunta_corregida, "respuesta": input_message})
            respuesta_buena = True

        # FIN DEL CICLO WHILE FOR QUE CLASIFICA PREGUNTA Y RESPUESTA

    # FIN DEL CICLO FOR QUE RECORRE TODAS LAS PREGUNTAS


# Creacion de prompt para evaluar pregunta y respuesta dentro de un ciclo for seguido de la respuesta con su calificacion
for pregunta in final_answers:
    evaluation_prompt = (
        "Pregunta: " + pregunta["pregunta"] + " Respuesta: " + pregunta["respuesta"]
    )

    # Pasarle la pregunta y respuesta al bot para evaluarla al diccionario answers_evaluation
    answers_evaluation.append({"role": "user", "content": evaluation_prompt})
    # Guardar la respuesta del chatbot en content y despues en la variable evaluacion

    content = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=answers_evaluation,
        temperature=1,
        max_tokens = 200
    )

    evaluacion = content.choices[0].message.content

    # Append al diccionario calificaciones el elemento con la pregunta, respuesta y calificacion
    calificaciones.append({"pregunta": pregunta["pregunta"], "respuesta": pregunta["respuesta"], "calificacion": evaluacion})

# Mostrar todas las calificaciones al usuario
print(calificaciones)
