#!/usr/bin/env python3
"""
tools/build.py
Single-source-of-truth compiler for Ángel Sarrión's CV & Personal Space.
Reads content/cv.json and generates:
  - docs/index.html (EN website)
  - docs/es/index.html (ES website)
  - docs/cv.json & docs/es/cv.json (Raw JSON endpoints)
  - docs/cv.txt & docs/es/cv.txt (Plain text ATS endpoints)
  - main.tex (EN LaTeX document)
  - main-es.tex (ES LaTeX document)
"""

import json
import os
import sys
import html
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_JSON_PATH = os.path.join(ROOT_DIR, "content", "cv.json")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
DOCS_ES_DIR = os.path.join(DOCS_DIR, "es")

def load_data():
    with open(CV_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_text(val, lang="en"):
    if isinstance(val, dict):
        return val.get(lang, val.get("en", ""))
    return str(val)

def generate_html(data, lang="en"):
    profile = data["profile"]
    summary = data["summary"]
    top_projects = data["topProjects"]
    experience = data["experience"]
    skills = data["skills"]
    education = data["education"]
    languages = data["languages"]
    meta = data["meta"]

    is_es = (lang == "es")
    base_prefix = "../" if is_es else "./"
    
    # Explicit file paths for flawless navigation across file://, localhost, and GitHub Pages
    lang_switch_url = "../index.html" if is_es else "es/index.html"
    lang_switch_label = "Switch to English" if is_es else "Cambiar a Español"
    lang_switch_flag = "🇬🇧 English" if is_es else "🇪🇸 Español"
    
    preview_img = f"{base_prefix}assets/cv-preview-es.png" if is_es else f"{base_prefix}assets/cv-preview.png"
    pdf_filename = "AngelSarrion-CV-es.pdf" if is_es else "AngelSarrion-CV.pdf"
    tex_filename = "main-es.tex" if is_es else "main.tex"

    # Localized labels
    L = {
        "skip": "Saltar al contenido principal" if is_es else "Skip to main content",
        "nav_about": "Perfil" if is_es else "About",
        "nav_top": "Iniciativas" if is_es else "Initiatives",
        "nav_exp": "Experiencia" if is_es else "Experience",
        "nav_skills": "Competencias" if is_es else "Skills",
        "nav_edu": "Educación" if is_es else "Education",
        "nav_cv": "CV y Contacto" if is_es else "CV & Contact",
        "status_tag": "Riesgo de Crédito · Arquitectura de Soluciones · Liderazgo TI" if is_es else "Credit Risk · Enterprise Architecture · Technical Leadership",
        "btn_dl_pdf": "Descargar CV (PDF)" if is_es else "Download CV (PDF)",
        "btn_email": "Enviar Email" if is_es else "Send Email",
        "btn_print_page": "Imprimir esta página" if is_es else "Print this page",
        "sec_abstract": "Perfil Ejecutivo y Alcance" if is_es else "Executive Profile & Scope",
        "sec_top": "Iniciativas Estratégicas Destacadas" if is_es else "Strategic Initiatives (Featured)",
        "sec_exp": "Trayectoria Profesional" if is_es else "Professional Career History",
        "sec_skills": "Matriz de Competencias y Gobernanza" if is_es else "Technical Taxonomy & Governance",
        "sec_edu": "Credenciales Académicas e Idiomas" if is_es else "Academic Credentials & Languages",
        "sec_cv": "CV y Contacto" if is_es else "CV & Contact",
        "key_impact": "Hitos Técnicos y de Negocio:" if is_es else "Key Architectural & Business Impact:",
        "pitch": "Abierto a oportunidades en liderazgo técnico, arquitectura de sistemas y riesgo de crédito — conversemos." if is_es else "Open to conversations about technical leadership, enterprise architecture, and credit risk systems — feel free to reach out.",
        "local_time": "hora local en España" if is_es else "local time in Spain",
        "auto_gen": "Generado automáticamente a partir de este repositorio, siempre actualizado." if is_es else "Auto-generated from this repository, always up to date.",
        "compiled_note": "Este PDF fue compilado con LaTeX — compilación verificada" if is_es else "This PDF was compiled with LaTeX — verified build",
        "data_label": "Este CV como datos:" if is_es else "This CV as data:",
        "theme_toggle": "📄 Modo Claro" if is_es else "📄 LaTeX Paper"
    }

    # Top Projects HTML (Clean, no TOP# badges)
    top_projects_html = []
    for proj in top_projects:
        title = get_text(proj["title"], lang)
        role = get_text(proj["role"], lang)
        overview = get_text(proj["overview"], lang)
        impact_items = "".join([f"<li>{html.escape(item)}</li>" for item in get_text(proj["impact"], lang)])
        stack_tags = "".join([f'<span class="tech-tag pink">{html.escape(t)}</span>' for t in proj["stack"]])
        
        top_projects_html.append(f"""
        <article class="project-card" id="project-{proj['id']}">
          <div class="project-header-row">
            <h3 class="project-title">{html.escape(title)}</h3>
            <span class="project-period">{html.escape(proj['period'])} · {html.escape(proj['company'])}</span>
          </div>
          <div class="project-role-badge">💼 {html.escape(role)}</div>
          <p class="project-overview">{html.escape(overview)}</p>
          <ul class="project-impact-list">
            {impact_items}
          </ul>
          <div class="project-stack-wrap">
            {stack_tags}
          </div>
        </article>
        """)

    # Experience Timeline HTML
    exp_html = []
    for exp in experience:
        company = html.escape(exp["company"])
        pos = html.escape(get_text(exp["position"], lang))
        dates = f"{html.escape(get_text(exp['start'], lang))} – {html.escape(get_text(exp['end'], lang))}"
        loc = html.escape(get_text(exp["location"], lang))
        bullets = "".join([f"<li>{html.escape(b)}</li>" for b in get_text(exp["bullets"], lang)])
        stack_tags = "".join([f'<span class="tech-tag">{html.escape(t)}</span>' for t in exp.get("stack", [])])

        exp_html.append(f"""
        <div class="timeline-item">
          <div class="timeline-card">
            <div class="experience-header">
              <h3 class="experience-company">{company}</h3>
              <span class="experience-dates">{dates}</span>
            </div>
            <div class="experience-position">{pos}</div>
            <div class="experience-location">📍 {loc}</div>
            <ul class="experience-bullets">
              {bullets}
            </ul>
            <div class="project-stack-wrap">
              {stack_tags}
            </div>
          </div>
        </div>
        """)

    # Skills HTML
    skills_html = []
    for cat in skills:
        cat_title = html.escape(get_text(cat["category"], lang))
        items = "".join([f'<div class="skill-item">{html.escape(item)}</div>' for item in cat["items"]])
        skills_html.append(f"""
        <div class="skill-category-card">
          <h3 class="skill-category-title">⚙ {cat_title}</h3>
          <div class="skill-items-list">
            {items}
          </div>
        </div>
        """)

    # Education HTML
    edu_html = []
    for edu in education:
        deg = html.escape(get_text(edu["degree"], lang))
        inst = html.escape(edu["institution"])
        period = html.escape(edu["period"])
        field = html.escape(get_text(edu["field"], lang))
        loc = html.escape(edu["location"])
        edu_html.append(f"""
        <div class="timeline-card" style="margin-bottom: 16px;">
          <div class="experience-header">
            <h3 class="experience-company">{inst}</h3>
            <span class="experience-dates">{period}</span>
          </div>
          <div class="experience-position">{deg}</div>
          <div class="experience-location">📍 {loc} · {field}</div>
        </div>
        """)

    # Languages HTML
    lang_html = []
    for l in languages:
        name = html.escape(get_text(l["language"], lang))
        prof = html.escape(get_text(l["proficiency"], lang))
        lang_html.append(f'<span class="tech-tag" style="font-size: 0.95rem; padding: 6px 14px;"><strong>{name}:</strong>&nbsp;{prof}</span>')

    # Direct Language Switcher Pill in Navbar
    if is_es:
        lang_pill = f"""
        <div class="lang-switcher-pill" aria-label="Idioma">
          <a href="../index.html" class="lang-btn" title="Switch to English">EN</a>
          <span class="lang-btn active">ES</span>
        </div>
        <a href="../index.html" class="btn-control lang-toggle-btn" title="Switch to English">{lang_switch_flag}</a>
        """
    else:
        lang_pill = f"""
        <div class="lang-switcher-pill" aria-label="Language">
          <span class="lang-btn active">EN</span>
          <a href="es/index.html" class="lang-btn" title="Cambiar a Español">ES</a>
        </div>
        <a href="es/index.html" class="btn-control lang-toggle-btn" title="Cambiar a Español">{lang_switch_flag}</a>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(get_text(profile['title'], lang))}</title>
  <meta name="description" content="{html.escape(get_text(profile['metaDescription'], lang))}">
  <meta name="theme-color" content="{meta['themeColor']['dark']}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{html.escape(get_text(profile['title'], lang))}">
  <meta property="og:description" content="{html.escape(get_text(profile['metaDescription'], lang))}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="{meta['siteUrl']}">
  
  <link rel="icon" type="image/svg+xml" href="{base_prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{base_prefix}styles.css">
</head>
<body>
  <div class="synth-grid-bg"></div>
  <a href="#main-content" class="skip-link">{L['skip']}</a>

  <!-- Navigation Header -->
  <header class="site-header">
    <div class="container nav-container">
      <a href="#about" class="brand" aria-label="{profile['name']}">
        <img src="{base_prefix}assets/brand-mark.svg" alt="Logo" class="brand-mark">
        <span class="brand-text">{profile['name']}</span>
      </a>

      <nav aria-label="Main Navigation">
        <ul class="nav-menu" id="nav-menu">
          <li><a href="#about" class="nav-link">{L['nav_about']}</a></li>
          <li><a href="#top-projects" class="nav-link">{L['nav_top']}</a></li>
          <li><a href="#experience" class="nav-link">{L['nav_exp']}</a></li>
          <li><a href="#skills" class="nav-link">{L['nav_skills']}</a></li>
          <li><a href="#education" class="nav-link">{L['nav_edu']}</a></li>
          <li><a href="#cv" class="nav-link cv-link">{L['nav_cv']}</a></li>
        </ul>
      </nav>

      <div class="nav-actions">
        {lang_pill}
        <button id="theme-toggle" class="btn-control" aria-label="Toggle Theme">
          {L['theme_toggle']}
        </button>
        <button id="mobile-menu-toggle" class="mobile-toggle" aria-label="Toggle navigation menu">
          ☰
        </button>
      </div>
    </div>
  </header>

  <main id="main-content">
    <!-- Hero Section -->
    <section class="hero-section" id="about">
      <div class="container">
        <div class="hero-terminal-prompt">
          <span class="pulse-dot"></span>
          <span>santander-uk/credit-risk/lead-analyst:~$ {L['status_tag']}</span>
        </div>
        
        <h1 class="hero-title">{profile['name']}</h1>
        <div class="hero-subtitle">{html.escape(get_text(profile['role'], lang))}</div>
        <p class="hero-positioning">"{html.escape(get_text(profile['positioning'], lang))}"</p>

        <div class="hero-meta-bar">
          <div class="hero-meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>{html.escape(get_text(profile['location'], lang))}</span>
          </div>
          <div class="hero-meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <a href="mailto:{profile['email']}">{profile['email']}</a>
          </div>
          <div class="hero-meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
            <a href="{profile['links']['linkedin']}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          </div>
          <div class="hero-meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/></svg>
            <a href="{profile['links']['github']}" target="_blank" rel="noopener noreferrer">GitHub</a>
          </div>
        </div>

        <div class="hero-cta-group">
          <a href="{base_prefix}{pdf_filename}" class="btn-primary" download>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>{L['btn_dl_pdf']}</span>
          </a>
          <a href="mailto:{profile['email']}" class="btn-secondary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span>{L['btn_email']}</span>
          </a>
          <a href="#cv" class="btn-outline-pink">
            <span>{L['nav_cv']}</span>
          </a>
        </div>
      </div>
    </section>

    <!-- Section 1: Abstract & Summary (Clean single-line header) -->
    <section class="section-block">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">01.</span>
            <span>{L['sec_abstract']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div class="abstract-card">
          <p class="abstract-text">{html.escape(get_text(summary, lang))}</p>
        </div>
      </div>
    </section>

    <!-- Section 2: Top Featured Projects (Clean single-line header) -->
    <section class="section-block" id="top-projects">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">02.</span>
            <span>{L['sec_top']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div class="projects-grid">
          {"".join(top_projects_html)}
        </div>
      </div>
    </section>

    <!-- Section 3: Professional Experience (Clean single-line header) -->
    <section class="section-block" id="experience">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">03.</span>
            <span>{L['sec_exp']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div class="experience-timeline">
          {"".join(exp_html)}
        </div>
      </div>
    </section>

    <!-- Section 4: Skills Matrix (Clean single-line header) -->
    <section class="section-block" id="skills">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">04.</span>
            <span>{L['sec_skills']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div class="skills-grid">
          {"".join(skills_html)}
        </div>
      </div>
    </section>

    <!-- Section 5: Education & Languages (Clean single-line header) -->
    <section class="section-block" id="education">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">05.</span>
            <span>{L['sec_edu']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;">
          <div>
            <h3 style="font-family: var(--font-mono); font-size: 1.05rem; color: var(--neon-pink); margin-bottom: 14px;">🎓 {'Educación' if is_es else 'Education'}</h3>
            {"".join(edu_html)}
          </div>
          <div>
            <h3 style="font-family: var(--font-mono); font-size: 1.05rem; color: var(--neon-blue); margin-bottom: 14px;">🌐 {'Idiomas' if is_es else 'Languages'}</h3>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              {"".join(lang_html)}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 6: CV & CONTACT (Exact layout matching user screenshot) -->
    <section class="section-block" id="cv">
      <div class="container">
        <header class="section-header">
          <h2 class="section-title">
            <span class="tex-cmd">\\section</span>
            <span class="section-num">06.</span>
            <span>{L['sec_cv']}</span>
          </h2>
          <hr class="latex-hrule">
        </header>

        <div class="cv-contact-container">
          <!-- Left Column: Document Thumbnail -->
          <a href="{base_prefix}{pdf_filename}" class="cv-preview-card" download title="{L['btn_dl_pdf']}">
            <img src="{preview_img}" alt="{profile['name']} - CV Preview" class="cv-preview-img">
          </a>

          <!-- Right Column: Contact Pitch, Actions & Links -->
          <div class="cv-contact-details">
            <p class="cv-contact-pitch">{L['pitch']}</p>

            <div class="cv-action-row">
              <a href="{base_prefix}{pdf_filename}" class="btn-cv-download" download>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                <span>{L['btn_dl_pdf']}</span>
              </a>
              <a href="mailto:{profile['email']}" class="btn-cv-email">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                <span>{L['btn_email']}</span>
              </a>
              <button class="btn-cv-print action-print-cv">
                {L['btn_print_page']}
              </button>
            </div>

            <div class="cv-contact-list">
              <div class="cv-contact-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                <a href="mailto:{profile['email']}">{profile['email']}</a>
              </div>
              <div class="cv-contact-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>{html.escape(get_text(profile['location'], lang))}</span>
              </div>
              <div class="cv-contact-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span><span id="live-spain-time" class="live-time-indicator">--:--</span> {L['local_time']}</span>
              </div>
              <div class="cv-contact-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                <a href="{profile['links']['linkedin']}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
              </div>
              <div class="cv-contact-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/></svg>
                <a href="{profile['links']['github']}" target="_blank" rel="noopener noreferrer">GitHub</a>
              </div>
            </div>

            <div class="cv-meta-block">
              <div><em>{L['auto_gen']}</em></div>
              <div class="cv-meta-badge">{L['compiled_note']}</div>
              <div>{L['data_label']} <a href="{base_prefix}cv.json">JSON</a> · <a href="{base_prefix}cv.txt">plain text</a> · <a href="{base_prefix}{tex_filename}">LaTeX (.tex)</a></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <strong>{profile['name']}</strong> — {html.escape(get_text(profile['role'], lang))}
        </div>

        <div class="footer-data-links">
          <span>{L['data_label']}</span>
          <a href="{base_prefix}cv.json" class="footer-data-pill">JSON</a>
          <a href="{base_prefix}cv.txt" class="footer-data-pill">PLAIN TEXT</a>
          <a href="{base_prefix}{tex_filename}" class="footer-data-pill">LATEX (.TEX)</a>
          <a href="{meta['repoUrl']}" target="_blank" rel="noopener noreferrer" class="footer-data-pill">GITHUB REPO</a>
        </div>
      </div>

      <div class="footer-copyright">
        © {datetime.now().year} {profile['name']} · Senior Business Analyst Lead & IT Specialist
      </div>
    </div>
  </footer>

  <script src="{base_prefix}app.js"></script>
</body>
</html>
"""
    return html_content

def generate_plain_text(data, lang="en"):
    profile = data["profile"]
    summary = data["summary"]
    top_projects = data["topProjects"]
    experience = data["experience"]
    skills = data["skills"]
    education = data["education"]
    languages = data["languages"]

    lines = []
    lines.append(f"{profile['name'].upper()} — {get_text(profile['role'], lang).upper()}")
    lines.append("=" * 70)
    lines.append(f"Email:    {profile['email']}")
    lines.append(f"Location: {get_text(profile['location'], lang)}")
    lines.append(f"LinkedIn: {profile['links']['linkedin']}")
    lines.append(f"GitHub:   {profile['links']['github']}")
    lines.append("\n" + ("=" * 70))
    lines.append("01. EXECUTIVE SUMMARY / EXTRACTO")
    lines.append("=" * 70)
    lines.append(get_text(summary, lang))
    lines.append("\n" + ("=" * 70))
    lines.append("02. STRATEGIC INITIATIVES (FEATURED)")
    lines.append("=" * 70)
    for p in top_projects:
        lines.append(f"\n* {get_text(p['title'], lang)} | {p['period']} | {p['company']}")
        lines.append(f"  Role: {get_text(p['role'], lang)}")
        lines.append(f"  Overview: {get_text(p['overview'], lang)}")
        lines.append("  Key Impact:")
        for b in get_text(p['impact'], lang):
            lines.append(f"    - {b}")
        lines.append(f"  Stack: {', '.join(p['stack'])}")

    lines.append("\n" + ("=" * 70))
    lines.append("03. PROFESSIONAL CAREER HISTORY")
    lines.append("=" * 70)
    for e in experience:
        lines.append(f"\n* {e['company']} | {get_text(e['start'], lang)} – {get_text(e['end'], lang)}")
        lines.append(f"  Position: {get_text(e['position'], lang)} ({get_text(e['location'], lang)})")
        for b in get_text(e['bullets'], lang):
            lines.append(f"    - {b}")
        if "stack" in e and e["stack"]:
            lines.append(f"  Stack: {', '.join(e['stack'])}")

    lines.append("\n" + ("=" * 70))
    lines.append("04. TECHNICAL MATRIX & SKILLS")
    lines.append("=" * 70)
    for s in skills:
        lines.append(f"* {get_text(s['category'], lang)}: {', '.join(s['items'])}")

    lines.append("\n" + ("=" * 70))
    lines.append("05. EDUCATION & LANGUAGES")
    lines.append("=" * 70)
    for ed in education:
        lines.append(f"* {ed['institution']}: {get_text(ed['degree'], lang)} ({ed['period']}) — {ed['location']}")
    for l in languages:
        lines.append(f"* {get_text(l['language'], lang)}: {get_text(l['proficiency'], lang)}")

    return "\n".join(lines)

def escape_tex(text):
    if not text:
        return ""
    replacements = [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
        ("·", "\\textbullet{}"),
        ("—", "---"),
        ("–", "--")
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def generate_latex(data, lang="en"):
    profile = data["profile"]
    summary = data["summary"]
    top_projects = data["topProjects"]
    experience = data["experience"]
    skills = data["skills"]
    education = data["education"]
    languages = data["languages"]

    is_es = (lang == "es")

    sec_summary = "Perfil Ejecutivo" if is_es else "Executive Profile"
    sec_top = "Iniciativas Estratégicas Destacadas" if is_es else "Strategic Initiatives (Featured)"
    sec_exp = "Trayectoria Profesional" if is_es else "Professional Career History"
    sec_skills = "Matriz de Competencias" if is_es else "Technical Competencies"
    sec_edu = "Formación Académica e Idiomas" if is_es else "Academic Credentials & Languages"

    top_proj_tex = []
    for p in top_projects:
        title = escape_tex(get_text(p["title"], lang))
        period = escape_tex(p["period"])
        role = escape_tex(get_text(p["role"], lang))
        overview = escape_tex(get_text(p["overview"], lang))
        stack = escape_tex(", ".join(p["stack"]))
        bullet_items = "\n".join(["    \\item " + escape_tex(b) for b in get_text(p["impact"], lang)])
        
        block = (
            "\\noindent\\textbf{\\large " + title + "} \\hfill {\\color{SynthBlue}\\textbf{" + period + "}} \\\\\n"
            "{\\color{SynthPink}\\textbf{" + role + " $\\cdot$ " + p['company'] + "}} \\\\\n"
            "\\vspace{2pt}\n"
            + overview + "\n"
            "\\begin{itemize}[leftmargin=1.5em, itemsep=1.5pt, topsep=2pt]\n"
            + bullet_items + "\n"
            "\\end{itemize}\n"
            "\\noindent\\textit{\\footnotesize \\textbf{Tech Stack:} " + stack + "}\n"
            "\\vspace{10pt}\n"
        )
        top_proj_tex.append(block)

    exp_tex = []
    for e in experience:
        company = escape_tex(e["company"])
        pos = escape_tex(get_text(e["position"], lang))
        dates = escape_tex(get_text(e['start'], lang)) + " -- " + escape_tex(get_text(e['end'], lang))
        loc = escape_tex(get_text(e["location"], lang))
        bullet_items = "\n".join(["    \\item " + escape_tex(b) for b in get_text(e["bullets"], lang)])
        stack_str = ""
        if e.get("stack"):
            stack_str = "\\\\\\noindent\\textit{\\footnotesize \\textbf{Stack:} " + escape_tex(', '.join(e['stack'])) + "}"
        
        block = (
            "\\noindent\\textbf{\\large " + company + "} \\hfill {\\color{SynthBlue}\\textbf{" + dates + "}} \\\\\n"
            "{\\color{SynthPink}\\textbf{" + pos + "}} $\\cdot$ {\\color{SlateGray}" + loc + "}\n"
            "\\begin{itemize}[leftmargin=1.5em, itemsep=1.5pt, topsep=2pt]\n"
            + bullet_items + "\n"
            "\\end{itemize}\n"
            + stack_str + "\n"
            "\\vspace{10pt}\n"
        )
        exp_tex.append(block)

    skills_tex = []
    for s in skills:
        cat = escape_tex(get_text(s["category"], lang))
        items = escape_tex(", ".join(s["items"]))
        skills_tex.append("\\item \\textbf{" + cat + ":} " + items)

    edu_tex = []
    for ed in education:
        deg = escape_tex(get_text(ed["degree"], lang))
        inst = escape_tex(ed["institution"])
        period = escape_tex(ed["period"])
        field = escape_tex(get_text(ed["field"], lang))
        block = (
            "\\noindent\\textbf{" + inst + "} \\hfill {\\textbf{" + period + "}} \\\\\n"
            + deg + " -- \\textit{" + field + "}\\\\\n"
        )
        edu_tex.append(block)

    lang_tex = ", ".join(["\\textbf{" + escape_tex(get_text(l['language'], lang)) + ":} " + escape_tex(get_text(l['proficiency'], lang)) for l in languages])

    header_title = escape_tex(get_text(profile['title'], lang))
    role_str = escape_tex(get_text(profile['role'], lang))
    loc_str = escape_tex(get_text(profile['location'], lang))
    sum_str = escape_tex(get_text(summary, lang))

    tex_doc = f"""% =========================================================================
% Ángel Sarrión — Curriculum Vitae
% Design: LaTeX Technical Precision + Synthwave Palette (Neon Pink & Cyan)
% =========================================================================
\\documentclass[10pt,a4paper]{{article}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}
\\usepackage[margin=1.4cm, top=1.4cm, bottom=1.4cm]{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{tikz}}
\\usepackage{{fontawesome5}}

% --- Synthwave Color Palette ---
\\definecolor{{SynthPink}}{{HTML}}{{FF2A85}}
\\definecolor{{SynthBlue}}{{HTML}}{{008CB4}}
\\definecolor{{DarkVoid}}{{HTML}}{{0A0B16}}
\\definecolor{{SlateGray}}{{HTML}}{{475569}}

% --- Hyperref Setup ---
\\hypersetup{{
    colorlinks=true,
    linkcolor=SynthBlue,
    urlcolor=SynthBlue,
    pdftitle={{{header_title}}},
    pdfauthor={{{profile['name']}}}
}}

% --- Section Styling ---
\\titleformat{{\\section}}
  {{\\large\\bfseries\\color{{SynthPink}}}}
  {{}}
  {{0em}}
  {{}}[{{\\color{{SynthBlue}}\\titlerule[1.2pt]}}]

\\titlespacing*{{\\section}}{{0pt}}{{12pt}}{{8pt}}

\\begin{{document}}
\\pagestyle{{empty}}

% --- Header with Vector Icons (Matching Screenshot) ---
\\begin{{center}}
    {{\\Huge\\textbf{{\\scshape {profile['name']}}}}} \\\\[4pt]
    {{\\large\\color{{SynthBlue}}\\textbf{{{role_str}}}}} \\\\[6pt]
    {{\\small
        \\faEnvelope~\\href{{mailto:{profile['email']}}}{{{profile['email']}}} \\ $\\cdot$ \\ 
        \\faMapMarker*~{{{loc_str}}} \\\\[3pt]
        \\faLinkedin~\\href{{{profile['links']['linkedin']}}}{{LinkedIn}} \\ $\\cdot$ \\ 
        \\faGithub~\\href{{{profile['links']['github']}}}{{GitHub}} \\ $\\cdot$ \\ 
        \\faGlobe~\\href{{https://angelsarrion.github.io/ASCV/}}{{Portfolio}}
    }}
\\end{{center}}

\\vspace{{-4pt}}

% --- Section: Summary ---
\\section{{{sec_summary}}}
\\noindent {sum_str}

% --- Section: Top Projects ---
\\section{{{sec_top}}}
{"".join(top_proj_tex)}

% --- Section: Professional Experience ---
\\section{{{sec_exp}}}
{"".join(exp_tex)}

% --- Section: Skills ---
\\section{{{sec_skills}}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=2pt, topsep=2pt]
{"".join(skills_tex)}
\\end{{itemize}}

% --- Section: Education & Languages ---
\\section{{{sec_edu}}}
{"".join(edu_tex)}
\\vspace{{6pt}}
\\noindent {lang_tex}

\\end{{document}}
"""
    return tex_doc

def main():
    data = load_data()
    
    # 1. Generate HTML
    print("Generating docs/index.html (EN)...")
    html_en = generate_html(data, "en")
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_en)

    print("Generating docs/es/index.html (ES)...")
    html_es = generate_html(data, "es")
    with open(os.path.join(DOCS_ES_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_es)

    # 2. Raw JSON endpoints
    print("Generating docs/cv.json & docs/es/cv.json...")
    with open(os.path.join(DOCS_DIR, "cv.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(os.path.join(DOCS_ES_DIR, "cv.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 3. Plain Text ATS endpoints
    print("Generating docs/cv.txt & docs/es/cv.txt...")
    with open(os.path.join(DOCS_DIR, "cv.txt"), "w", encoding="utf-8") as f:
        f.write(generate_plain_text(data, "en"))
    with open(os.path.join(DOCS_ES_DIR, "cv.txt"), "w", encoding="utf-8") as f:
        f.write(generate_plain_text(data, "es"))

    # 4. LaTeX files
    print("Generating main.tex (EN) & main-es.tex (ES)...")
    with open(os.path.join(ROOT_DIR, "main.tex"), "w", encoding="utf-8") as f:
        f.write(generate_latex(data, "en"))
    with open(os.path.join(ROOT_DIR, "main-es.tex"), "w", encoding="utf-8") as f:
        f.write(generate_latex(data, "es"))
    
    with open(os.path.join(DOCS_DIR, "main.tex"), "w", encoding="utf-8") as f:
        f.write(generate_latex(data, "en"))
    with open(os.path.join(DOCS_DIR, "main-es.tex"), "w", encoding="utf-8") as f:
        f.write(generate_latex(data, "es"))

    print("Build complete! All files generated successfully.")

if __name__ == "__main__":
    main()
