# Antonia – Universidad

Herramientas para el informe de Valoración Geriátrica Integral (Internado de Geriatría).

- `fuente/grafico_arana.py`: genera el gráfico de araña (radar) de la VGI, con cada escala expresada como % de desempeño
  (100 % = mejor resultado; escalas inversas como (máx − puntaje)/máx) y la línea de umbral de normalidad.
  Uso: `python3 fuente/grafico_arana.py salida.png`
- `fuente/docx_helpers.py`: utilidades para generar documentos Word (Calibri 10, texto justificado).

Los informes y los scripts que contienen datos clínicos del residente se excluyen del repositorio (ver `.gitignore`),
ya que este repositorio es público.
