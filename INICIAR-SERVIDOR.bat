@echo off
title Pixelverso — Servidor Local
echo.
echo  ==========================================
echo   PIXELVERSO — Servidor corriendo en:
echo   http://localhost:8765
echo  ==========================================
echo.
echo  Mantene esta ventana abierta mientras usas la web.
echo  Para cerrar el servidor: presiona Ctrl+C
echo.
start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" "http://localhost:8765"
python -m http.server 8765 --directory "%~dp0"
pause
