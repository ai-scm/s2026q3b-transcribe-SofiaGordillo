
# Spanish Audio Transcriber

Herramienta local para transcribir archivos de audio y video en español utilizando Whisper dentro de Docker.

## 1. Objetivo

El proyecto permite convertir archivos `.mp3` y `.mp4` en archivos `.sub` con segmentos de texto y marcas de tiempo.

La transcripción se realiza localmente dentro de un contenedor Docker.

No se utilizan servicios externos de transcripción ni APIs de terceros.

## 2. Tecnologías

- Python 3.12
- faster-whisper 1.2.1
- Whisper
- FFmpeg
- Docker
- pytest

## 3. Arquitectura

El archivo multimedia del equipo anfitrión se monta dentro del contenedor mediante `/media`.

```text
Archivo MP3/MP4
       |
       v
   Docker /media
       |
       v
   transcribir
       |
       v
 faster-whisper
       |
       v
 segmentos + timestamps
       |
       v
 archivo .sub
````

## 4. Estructura del proyecto

```text
spanish-audio-transcriber/
├── src/
│   └── transcriber/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── output.py
│       ├── transcriber.py
│       └── validation.py
├── tests/
│   ├── test_output.py
│   └── test_validation.py
├── media/
├── Dockerfile
├── pyproject.toml
├── README.md
└── .gitignore
```

## 5. Construcción de la imagen Docker

Desde la carpeta del proyecto:

```bash
docker build -t spanish-audio-transcriber .
```

## 6. Crear el contenedor

Crear la carpeta para los archivos multimedia:

```bash
mkdir -p media
```

Crear el contenedor:

```bash
docker run -d \
  --name spanish-transcriber \
  -v "$PWD/media:/media" \
  spanish-audio-transcriber
```

El directorio `media` del equipo anfitrión queda disponible dentro del contenedor como `/media`.

## 7. Uso

El comando principal es:

```bash
docker exec spanish-transcriber transcribir /media/pelicula.mp4
```

Para un archivo MP3:

```bash
docker exec spanish-transcriber transcribir /media/audio.mp3
```

El archivo de salida se crea en la misma carpeta:

```text
/media/audio.mp3
/media/audio.sub
```

## 8. Opciones

### Cambiar el idioma

El idioma predeterminado es español (`es`).

```bash
docker exec spanish-transcriber transcribir \
  --language es \
  /media/audio.mp3
```

### Cambiar el modelo

El modelo predeterminado es `small`.

```bash
docker exec spanish-transcriber transcribir \
  --model small \
  /media/audio.mp3
```

### Sobrescribir un archivo existente

Si ya existe el archivo `.sub`, el programa solicita confirmación:

```text
El archivo ... ya existe. ¿Desea sobrescribirlo? [s/N]:
```

Para sobrescribir directamente:

```bash
docker exec spanish-transcriber transcribir \
  --force \
  /media/audio.mp3
```

## 9. Formato de salida

La transcripción se guarda utilizando extensión `.sub` y formato compatible con SRT:

```text
1
00:00:04,340 --> 00:00:09,340
Texto transcrito.

2
00:00:10,340 --> 00:00:15,340
Siguiente segmento.
```

Cada segmento contiene:

* Número de segmento.
* Tiempo inicial.
* Tiempo final.
* Texto transcrito.

Los timestamps se generan en orden y no pueden ser negativos.

## 10. Control de memoria

La aplicación no carga toda la transcripción en memoria.

`faster-whisper` proporciona los segmentos progresivamente y el programa los escribe en el archivo `.sub` conforme se procesan.

Esto permite trabajar con archivos de mayor duración sin almacenar toda la transcripción en memoria.

## 11. Procesamiento local

Todo el procesamiento de audio se realiza dentro del contenedor Docker.

El contenedor incluye:

* Python.
* faster-whisper.
* Whisper.
* FFmpeg.
* Dependencias necesarias.

No es necesario instalar Python, Whisper o FFmpeg en el equipo anfitrión para ejecutar la aplicación.

El modelo Whisper se descarga y utiliza dentro del entorno del contenedor.

## 12. Pruebas

Las pruebas unitarias se ejecutan con:

```bash
pytest
```

Las pruebas verifican principalmente:

* Validación de archivos MP3 y MP4.
* Archivos inexistentes.
* Extensiones no soportadas.
* Generación del archivo `.sub`.
* Formato de timestamps.
* Timestamps inválidos.
* Comportamiento cuando el archivo de salida ya existe.
* Uso de `--force`.

## 13. Criterio de éxito

El flujo principal del proyecto es:

```bash
docker exec spanish-transcriber transcribir /media/pelicula.mp4
```

y debe producir:

```text
/media/pelicula.sub
```

con segmentos de texto y timestamps válidos.

## 14. Limitaciones

La versión actual soporta únicamente:

* `.mp3`
* `.mp4`

El idioma predeterminado es español, aunque puede modificarse mediante `--language`.

El rendimiento depende de los recursos disponibles en el equipo donde se ejecuta Docker.

```

