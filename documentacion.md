## ⚙️ Ejecutar test
para ejecutar los tests hay que ejecutar el comando: `python3 -m unittest ./tests/Test_clinica.py a la altura del directorio: computaci-n-2025-05-27-gesti-n-cl-nica-MateK12/`

## ⚙️ Ejecutar programa
para ejecutar el programa: `python3 app.py en` el mismo directorio


## 📦 Organización del Código

- `src/models/`: contiene las clases principales
- `app.py`: archivo para ejecutar el sistema que maneja la entrada y salida de informacion del usuario. Este archivo llama a los metodos de la clase clinica, y muestra los resultados.
- `src/exceptions/`: define las excepciones personalizadas
- `tests/`:estan todos los tests, para cada clase 
- `Clinica`: clase central que maneja las operaciones principales

La clase principal `Clinica` tiene todos los metodos para que funcione el sistema, incluida validaciones que levantaran excepciones en caso de ser necesarios

## 🧱 Tests
El archivo `Test_clinica.py` tiene los test de todas las clases (una para cada una) estos testean que se den los resultados correctos, pero tambien que se levanten las excepciones correctas

## 🛑 Manejo de Errores
Se usan las siguientes excepciones para validar reglas de negocio:
- `MedicoNoDisponibleException` 
- `PacienteNoEncontradoException`
- `TurnoOcupadoException`
- `RecetaInvalidaException`
Las excepciones se manejas con bloques `try` `except` en el archivo app.py 