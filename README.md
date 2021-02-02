# Annie Asistente de voz virtual
Annie es un asistente virtual que responde a distintos comandos dictados por voz, como podría ser consultar el tiempo en una ciudad, hacer búsquedas por internet o reproducir vídeos. 
En el mercado existen proyectos similares como [goolge Assistant](https://assistant.google.com/ "google Assistant") o [alexa](https://www.amazon.com/b?ie=UTF8&node=17934671011 "alexa") que aunque
la complejidad y número de comandos que contemplan es mucho más alta, el objetivo que persiguen es el mismo.  
Annie está pensada para ejecutarse en ordenadores, sin importar su sistema operativo mientras puedan ejecutar scripts en Python
## Recursos utilizados
Para desarrollar la aplicación hemos utilizado el lenguaje Python y sus librerias, no hemos utilizado funciones dependientes del sistema operativo con el objetivo de que sea multiplataforma. Para hablar de los recursos utilizados resulta más cómodo dividir las distintas funcionalidades de nuestro asistente de voz
### Reconocimiento de Voz
La primera parte que hubo que afrontar en el desarrollo de Annie es la grabación del audio y la conversión de este a texto para poder procesarlo luego. La librería SpeechRecognition de Python nos permite realizar las dos tareas, para el reconocimiento de voz a texto además podemos seleccionar que algoritmo queremos utilizar para ello, Google_recognizer, Sphinx, Wit.ai...
### Procesamiento del lenguaje natural
En la segunda parte hay que procesar el texto para "entender" el comando que el usuario pide, para ello debemos de utilizar algoritmos de procesamiento del lenguaje natural. Se han explorado distintas librerías como Spacy o Nltk, en nuestro caso hemos optado por usar Nltk, hacemos uso de distintas funciones de la librería como 'punkt' o 'stopwords' para eliminar signos de puntuación y palabras con poco significado semántico, para obtener el lema usamos WordNetLemmatizer, averaged_perceptron_tagger para determinar el tag de cada palabra o maxent_ne_chunker para identificar las entidades de la frase, entre otras muchas funcionalidades de nltk.
### Texto a voz
En la última parte una vez hemos conseguido conocer el comando que el usuario quiere ejecutar debemos devolverle una respuesta utilizando la voz, para ello probamos dos librerías gTTs y pyttsx3, preferíamos las voces que se incluían en pyttsx3, para llevar acabo está función cada comando devuelve un string una vez se ejecuta, este string se usa posteriormente para dar voz a nuestro asistente.
