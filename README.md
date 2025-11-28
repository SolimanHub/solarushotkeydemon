# Solarus Hotkey Fix para ArkOS (R36S)

Fix para el problema de la combinación de teclas FN+Start que no cierra el emulador Solarus en consolas retro con ArkOS.

## Descripción del Problema

En consolas retro como la **R36S** con sistema operativo **ArkOS**, al ejecutar juegos con el emulador **Solarus**, la combinación de teclas **FN+Start** (Select+Start) no cierra el emulador correctamente, quedando el usuario atrapado en el juego sin poder salir mediante controles.

### Causa Raíz

El script `solarushotkeydemon.py` original tiene varios errores:

1. **Código de evento incorrecto**: Busca el evento `f3` (código 705) en lugar del botón Start (botón 13)
2. **Mapeo erróneo de botones**: Los códigos definidos en la clase `Joypad` no corresponden con los botones reales del gamepad
3. **Bug en exit**: Usa `exit` en lugar de `exit()` o `break`

## Solución

Este repositorio proporciona un `solarushotkeydemon.py` corregido que:

- Detecta correctamente la combinación Select + Start
- Usa los códigos de evento correctos para el GO-Super Gamepad
- Cierra el emulador Solarus apropiadamente mediante `pkill solarus-run`

## Instalación

### Requisitos Previos

- Consola retro con ArkOS (probado en R36S con GO-Super Gamepad)
- Acceso SSH a la consola
- El servicio `solarushotkey` debe estar configurado

### Pasos de Instalación

#### Opción A: Via SSH (Recomendado)

1. **Conéctate a tu consola via SSH**:
```bash
ssh ark@<IP_DE_TU_CONSOLA>
# Contraseña por defecto: ark
```

2. **Detén el servicio actual**:
```bash
sudo systemctl stop solarushotkey
```

3. **Haz backup del archivo original** (recomendado):
```bash
sudo cp /usr/local/bin/solarushotkeydemon.py /usr/local/bin/solarushotkeydemon.py.backup
```

4. **Descarga el archivo corregido**:
```bash
sudo wget https://raw.githubusercontent.com/SolimanHub/solarushotkeydemon/refs/heads/main/solarushotkeydemon.py -O /usr/local/bin/solarushotkeydemon.py
```

O copia manualmente el contenido:
```bash
sudo nano /usr/local/bin/solarushotkeydemon.py
# Pega el contenido del archivo solarushotkeydemon.py
# Guarda con Ctrl+O, Enter, Ctrl+X
```

5. **Asegúrate de que el archivo sea ejecutable**:
```bash
sudo chmod +x /usr/local/bin/solarushotkeydemon.py
```

6. **Reinicia el servicio**:
```bash
sudo systemctl start solarushotkey
```

7. **Verifica que el servicio esté corriendo**:
```bash
sudo systemctl status solarushotkey
```

Deberías ver `active (running)` en el estado.

#### Opción B: Editando directamente en la tarjeta SD

Si no puedes conectarte via SSH (sin adaptador de red, problemas de conexión, etc.), puedes editar el archivo directamente:

1. **Apaga tu consola R36S completamente**

2. **Extrae la tarjeta SD del sistema** (normalmente la tarjeta donde está instalado ArkOS)

3. **Inserta la tarjeta SD en tu PC**
   - En Windows, es posible que solo veas algunas particiones. Necesitarás acceder a la partición Linux (ext4)
   - Puedes usar herramientas como [Linux File Systems for Windows](https://www.paragon-software.com/home/linuxfs-windows/) o [DiskInternals Linux Reader](https://www.diskinternals.com/linux-reader/)
   - En Linux o Mac, la partición se montará automáticamente

4. **Navega a la ruta del archivo**:
   - La ruta completa es: `/usr/local/bin/solarushotkeydemon.py`

5. **Haz backup del archivo original** (recomendado):
   - Copia `solarushotkeydemon.py` y renómbralo a `solarushotkeydemon.py.backup`

6. **Edita el archivo**:
   - Abre `solarushotkeydemon.py` con un editor de texto (Notepad++, VSCode, gedit, nano, etc.)
   - Reemplaza todo el contenido con el código del archivo `solarushotkeydemon.py` de este repositorio
   - **Importante**: Guarda el archivo con codificación UTF-8 y saltos de línea tipo Unix (LF, no CRLF)

7. **Expulsa la tarjeta SD de forma segura** de tu PC

8. **Reinserta la tarjeta SD en tu R36S** y enciéndela

9. **El fix debería aplicarse automáticamente** al iniciar el servicio

> **Nota para usuarios de Windows**: Si usas Notepad, asegúrate de guardar con codificación UTF-8. Se recomienda usar Notepad++ o VSCode para editar archivos de Linux.

## Prueba

1. Inicia un juego de Solarus desde EmulationStation
2. Una vez en el juego, presiona **Select + Start** simultáneamente
3. El juego debería cerrarse y regresar al menú de EmulationStation

## Troubleshooting

### El hotkey sigue sin funcionar

Si después de aplicar el fix la combinación aún no funciona, puede que tu gamepad use códigos de evento diferentes. Para identificarlos:

1. **Detén el juego y el servicio**:
```bash
sudo systemctl stop solarushotkey
```

2. **Ejecuta evtest para ver los códigos de tus botones**:
```bash
sudo evtest /dev/input/event2
```

3. **Presiona Select y anota el código** (ejemplo: `BTN_SELECT (312)`)
4. **Presiona Start y anota el código** (ejemplo: `BTN_START (313)`)

5. **Edita el archivo y actualiza los valores**:
```bash
sudo nano /usr/local/bin/solarushotkeydemon.py
```

Modifica estos valores según lo que obtuviste:
```python
class Joypad:
    start = 705  # Reemplaza con tu código
    select = 704  # Reemplaza con tu código
```

6. **Reinicia el servicio**:
```bash
sudo systemctl restart solarushotkey
```

### Ver logs del servicio

Para depurar problemas:
```bash
sudo journalctl -u solarushotkey -f
```

### Restaurar el archivo original

Si necesitas volver al archivo original:
```bash
sudo systemctl stop solarushotkey
sudo cp /usr/local/bin/solarushotkeydemon.py.backup /usr/local/bin/solarushotkeydemon.py
sudo systemctl start solarushotkey
```

## Dispositivos Compatibles

Este fix ha sido probado en:

- ✅ R36S con GO-Super Gamepad (190000004b4800000011000000010000)
- ✅ Dispositivos ArkOS con configuración similar

Si pruebas este fix en otro dispositivo, por favor reporta tu experiencia en los Issues.

## 🙏 Agradecimientos

- Comunidad de ArkOS por el sistema operativo
- Desarrolladores del emulador Solarus
- Comunidad de RetroHandhelds

---

**Nota**: Este fix es específico para el emulador Solarus en ArkOS. Otros emuladores usan diferentes métodos para manejar hotkeys de salida.
