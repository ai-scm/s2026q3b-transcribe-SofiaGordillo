# Spanish Audio Transcriber

Herramienta local para transcribir archivos de audio y video en español utilizando Whisper dentro de Docker.

## 1. Objetivo

El proyecto permite convertir archivos `.mp3` y `.mp4` en archivos `.sub` con segmentos de texto y marcas de tiempo.

La transcripción se realiza localmente dentro de un contenedor Docker.

No se utilizan servicios externos de transcripción ni APIs de terceros.

## 2. Tecnologías

- Python 3.12
- faster-whisper
- Whisper
- FFmpeg
- Docker
- Docker Compose (opcional)

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

