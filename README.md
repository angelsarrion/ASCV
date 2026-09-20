# Ángel Sarrión — Personal Space & CV

[![Deploy to GitHub Pages](https://github.com/angelsarrion/ASCV/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/angelsarrion/ASCV/actions/workflows/deploy-pages.yml)
[![Compile LaTeX to PDF](https://github.com/angelsarrion/ASCV/actions/workflows/compile-latex.yml/badge.svg)](https://github.com/angelsarrion/ASCV/actions/workflows/compile-latex.yml)

> **Live Site:** [https://angelsarrion.github.io/ASCV/](https://angelsarrion.github.io/ASCV/)  
> **Versión en Español:** [https://angelsarrion.github.io/ASCV/es/](https://angelsarrion.github.io/ASCV/es/)

Espacio personal y portafolio profesional interactivo de **Ángel Sarrión**, Senior Business Analyst Lead y Especialista en TI con más de 18 años de trayectoria en banca de misión crítica, motores de riesgo de crédito (Credit Risk) y arquitectura de sistemas en Santander UK y Santander Digital Services.

Diseñado con una estética híbrida única: **Rigor y maquetación de LaTeX + Diseño Retro-Ochentero Futurista (Synthwave / Outrun)** con paleta de rosa neón (`#ff2a85`) y azul eléctrico (`#00f0ff`).

---

## ⚡ Características Principales

- **Fuente Única de Verdad (`content/cv.json`)**: Todo el contenido curricular y técnico se gestiona en un único archivo JSON bilingüe. El sitio web (inglés y español), los textos planos para ATS, los endpoints de datos JSON y los documentos LaTeX se compilan automáticamente.
- **Proyectos TOP Resaltados**:
  1. 🏆 **RDS (Risk Decision Service)** (Santander UK, 2021–2025) — Rediseño del motor central de decisión de riesgo crediticio en tiempo real, soporte On-Call 24/7 y coordinación de releases BAU con Agile.
  2. 🥈 **Risk PCSM Project** (Santander UK, 2016–2017) — Reestructuración integral del riesgo crediticio minorista para tarjetas de crédito, cuentas personales y préstamos comerciales.
  3. 🥉 **Project Spectrum** (Santander UK, 2018) — Hito insignia del programa Santander DIGITAL para el onboarding digital de empresas mediante IBM API Gateway, Data Lake Near Real-Time y CI/CD en PaaS.
- **Generación y Descarga de CV Multi-Formato**:
  - 📥 **PDF Vectorial Compilado**: Descarga directa de `AngelSarrion-CV.pdf` (inglés) y `AngelSarrion-CV-es.pdf` (español).
  - 🖨️ **Impresión / Generación en Vivo (`window.print()`)**: Hoja de estilos `@media print` optimizada para producir un documento A4 LaTeX ultra nítido directamente desde el navegador.
  - 📜 **Código Fuente LaTeX (`.tex`)**: Descarga directa de `main.tex` y `main-es.tex`.
  - 💾 **Datos estructurados**: Endpoints disponibles en `cv.json` y `cv.txt` (formato compatible con ATS).
- **Diseño Dual**:
  - **Synthwave Dark (por defecto)**: Fondo noche cósmica, cuadrícula sutil ochentera, neones brillantes y badges vectoriales.
  - **LaTeX Paper (alternativo)**: Modo papiro marfil con tipografía académica serif y acentos sobrios.
- **Automatización CI/CD con GitHub Actions**:
  - `deploy-pages.yml`: Despliegue automático a GitHub Pages en cada push a `main`.
  - `compile-latex.yml`: Compilación de `main.tex` y `main-es.tex` con TeXLive en los servidores de GitHub.

---

## 🚀 Inicio Rápido

### Estructura de Archivos

```text
ASCV/
├── content/
│   └── cv.json               # 📌 Fuente única de verdad (editar aquí)
├── tools/
│   ├── build.py              # Compilador web, LaTeX y formatos de datos
│   └── generate_pdf.py       # Generador de PDFs vectoriales con PyCairo
├── docs/                     # 🌐 Directorio publicado en GitHub Pages
│   ├── index.html            # Sitio en inglés
│   ├── es/
│   │   └── index.html        # Sitio en español
│   ├── styles.css            # Estilos LaTeX + Synthwave
│   ├── app.js                # Lógica interactiva (temas, print, idioma)
│   ├── AngelSarrion-CV.pdf   # PDF compilado (EN)
│   ├── AngelSarrion-CV-es.pdf# PDF compilado (ES)
│   ├── cv.json / cv.txt      # Endpoints de datos
│   └── assets/               # Marca personal ÁS y favicon SVG
├── main.tex                  # Código fuente LaTeX (EN)
├── main-es.tex               # Código fuente LaTeX (ES)
├── .github/workflows/        # Flujos de trabajo de GitHub Actions
└── build.sh                  # Script de compilación rápida
```

### Cómo Actualizar tu CV

1. Edita el archivo `content/cv.json`.
2. Ejecuta la compilación:
   ```bash
   ./build.sh
   # o bien:
   python3 tools/build.py && python3 tools/generate_pdf.py
   ```
3. Prueba en local:
   ```bash
   python3 -m http.server 8080 --directory docs
   ```
   Abre [http://localhost:8080](http://localhost:8080) en tu navegador.
4. Sube los cambios a GitHub:
   ```bash
   git add .
   git commit -m "feat: update career experience and projects"
   git push origin main
   ```

---

## 🛠️ Cómo Publicar en GitHub Pages

1. En GitHub, crea el repositorio `ASCV` (o renómbralo a `angelsarrion.github.io` si deseas que sea tu página raíz de usuario).
2. Conecta tu repositorio local:
   ```bash
   git remote add origin https://github.com/angelsarrion/ASCV.git
   git branch -M main
   git push -u origin main
   ```
3. En GitHub ve a **Settings** > **Pages**:
   - Bajo **Build and deployment** > **Source**:
     - Selecciona **Deploy from a branch** y elige la carpeta `/docs` de la rama `main`.
     - *O bien*, selecciona **GitHub Actions** para usar el workflow automatizado `.github/workflows/deploy-pages.yml`.
4. ¡Listo! Tu sitio estará activo en `https://angelsarrion.github.io/ASCV/`.

---

© 2026 Ángel Sarrión · Senior Business Analyst Lead & IT Specialist
