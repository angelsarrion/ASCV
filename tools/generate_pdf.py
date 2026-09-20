#!/usr/bin/env python3
"""
tools/generate_pdf.py
High-precision Vector PDF and Preview Image Generator using PyCairo for Ángel Sarrión's CV.
Produces:
  - docs/AngelSarrion-CV.pdf (English)
  - docs/AngelSarrion-CV-es.pdf (Spanish)
  - docs/assets/cv-preview.png (English preview thumbnail)
  - docs/assets/cv-preview-es.png (Spanish preview thumbnail)
Icons are drawn as native scalable vector shapes — 0% tofu, 100% vector precision.
"""

import os
import json
import math
import cairo

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_JSON_PATH = os.path.join(ROOT_DIR, "content", "cv.json")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")

PAGE_WIDTH = 595.28   # A4 Width in points
PAGE_HEIGHT = 841.89  # A4 Height in points
MARGIN_X = 40.0
MARGIN_Y = 36.0
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN_X

# Color definitions
C_PINK = (0.88, 0.05, 0.48)      # Neon Pink / Magenta
C_BLUE = (0.01, 0.48, 0.72)      # Deep Cyan / Synth Blue
C_DARK = (0.08, 0.10, 0.16)      # Slate Dark Text
C_MUTED = (0.35, 0.40, 0.48)     # Muted Gray

def load_data():
    with open(CV_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_text(val, lang="en"):
    if isinstance(val, dict):
        return val.get(lang, val.get("en", ""))
    return str(val)

def wrap_text(ctx, text, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        extents = ctx.text_extents(test_line)
        if extents.width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# =========================================================================
# Native Cairo Vector Icon Drawers (No Unicode Font Dependencies)
# =========================================================================

def draw_email_icon(ctx, x, y, size=8.5, color=C_DARK):
    ctx.save()
    ctx.set_source_rgb(*color)
    w = size * 1.3
    h = size * 0.82
    ctx.rectangle(x, y - h, w, h)
    ctx.fill()
    # White inner flap
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(0.9)
    ctx.move_to(x + 1, y - h + 1)
    ctx.line_to(x + w / 2, y - h * 0.45)
    ctx.line_to(x + w - 1, y - h + 1)
    ctx.stroke()
    ctx.restore()
    return w

def draw_pin_icon(ctx, x, y, size=8.5, color=C_DARK):
    ctx.save()
    ctx.set_source_rgb(*color)
    r = size * 0.36
    cx = x + r
    cy = y - size * 0.65
    ctx.arc(cx, cy, r, 0, math.pi * 2)
    ctx.fill()
    ctx.move_to(cx - r * 0.85, cy + r * 0.2)
    ctx.line_to(cx, y)
    ctx.line_to(cx + r * 0.85, cy + r * 0.2)
    ctx.fill()
    # Inner hole
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(cx, cy, r * 0.4, 0, math.pi * 2)
    ctx.fill()
    ctx.restore()
    return size * 0.8

def draw_linkedin_icon(ctx, x, y, size=8.5, color=C_DARK):
    ctx.save()
    ctx.set_source_rgb(*color)
    w = size
    h = size
    ctx.rectangle(x, y - h, w, h)
    ctx.fill()
    # White 'in'
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size * 0.7)
    ctx.move_to(x + size * 0.16, y - size * 0.22)
    ctx.show_text('in')
    ctx.restore()
    return w

def draw_github_icon(ctx, x, y, size=8.5, color=C_DARK):
    ctx.save()
    ctx.set_source_rgb(*color)
    r = size * 0.45
    cx = x + r
    cy = y - r
    ctx.arc(cx, cy, r, 0, math.pi * 2)
    ctx.fill()
    # Ears
    ctx.move_to(cx - r * 0.7, cy - r * 0.5)
    ctx.line_to(cx - r * 0.45, cy - r * 1.05)
    ctx.line_to(cx - r * 0.15, cy - r * 0.75)
    ctx.fill()
    ctx.move_to(cx + r * 0.7, cy - r * 0.5)
    ctx.line_to(cx + r * 0.45, cy - r * 1.05)
    ctx.line_to(cx + r * 0.15, cy - r * 0.75)
    ctx.fill()
    # Inner face cutout
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(cx, cy + r * 0.22, r * 0.42, 0, math.pi * 2)
    ctx.fill()
    ctx.restore()
    return size

def draw_globe_icon(ctx, x, y, size=8.5, color=C_DARK):
    ctx.save()
    ctx.set_source_rgb(*color)
    ctx.set_line_width(0.85)
    r = size * 0.45
    cx = x + r
    cy = y - r
    ctx.arc(cx, cy, r, 0, math.pi * 2)
    ctx.stroke()
    ctx.move_to(cx - r, cy)
    ctx.line_to(cx + r, cy)
    ctx.stroke()
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(0.5, 1.0)
    ctx.arc(0, 0, r, 0, math.pi * 2)
    ctx.stroke()
    ctx.restore()
    ctx.restore()
    return size

class PDFCanvas:
    def __init__(self, filename, total_pages=2, surface_type="pdf"):
        self.filename = filename
        self.total_pages = total_pages
        self.current_page = 1
        self.surface_type = surface_type
        if surface_type == "image":
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(PAGE_WIDTH), int(PAGE_HEIGHT))
        else:
            self.surface = cairo.PDFSurface(filename, PAGE_WIDTH, PAGE_HEIGHT)
        
        self.ctx = cairo.Context(self.surface)
        if surface_type == "image":
            self.ctx.set_source_rgb(1, 1, 1)
            self.ctx.paint()
            
        self.y = MARGIN_Y

    def next_page(self):
        self.draw_footer()
        self.surface.show_page()
        self.current_page += 1
        self.y = MARGIN_Y

    def draw_footer(self):
        ctx = self.ctx
        ctx.save()
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8)
        ctx.set_source_rgb(*C_MUTED)
        
        # Left footer
        ctx.move_to(MARGIN_X, PAGE_HEIGHT - 22)
        ctx.show_text("Ángel Sarrión · Senior Business Analyst Lead & IT Specialist · github.com/angelsarrion/ASCV")
        
        # Right footer
        page_str = f"Page {self.current_page} of {self.total_pages}"
        ext = ctx.text_extents(page_str)
        ctx.move_to(PAGE_WIDTH - MARGIN_X - ext.width, PAGE_HEIGHT - 22)
        ctx.show_text(page_str)
        ctx.restore()

    def draw_header(self, profile, lang="en"):
        ctx = self.ctx
        name = profile["name"].upper()
        role = get_text(profile["role"], lang).upper()
        loc = get_text(profile["location"], lang)
        email = profile["email"]
        portfolio_text = "angelsarrion.github.io/ASCV"

        # Name
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(20)
        ctx.set_source_rgb(*C_DARK)
        ext = ctx.text_extents(name)
        ctx.move_to(PAGE_WIDTH / 2 - ext.width / 2, self.y + 16)
        ctx.show_text(name)
        self.y += 24

        # Role
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(10)
        ctx.set_source_rgb(*C_BLUE)
        ext = ctx.text_extents(role)
        ctx.move_to(PAGE_WIDTH / 2 - ext.width / 2, self.y + 10)
        ctx.show_text(role)
        self.y += 18

        # --- LINE 1: [Envelope] email · [Pin] location ---
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8.5)
        email_ext = ctx.text_extents(email)
        loc_ext = ctx.text_extents(loc)
        dot_ext = ctx.text_extents("  ·  ")

        icon_sz = 8.5
        w_email_icon = icon_sz * 1.3
        w_pin_icon = icon_sz * 0.8

        line1_w = (w_email_icon + 4 + email_ext.width + 
                   dot_ext.width + 
                   w_pin_icon + 4 + loc_ext.width)
        
        cur_x = (PAGE_WIDTH - line1_w) / 2
        line1_y = self.y + 4

        # Draw Email Icon & Text
        draw_email_icon(ctx, cur_x, line1_y, icon_sz, C_DARK)
        cur_x += w_email_icon + 4
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(cur_x, line1_y)
        ctx.show_text(email)
        cur_x += email_ext.width

        # Dot
        ctx.set_source_rgb(*C_MUTED)
        ctx.move_to(cur_x, line1_y)
        ctx.show_text("  ·  ")
        cur_x += dot_ext.width

        # Draw Pin Icon & Location
        draw_pin_icon(ctx, cur_x, line1_y, icon_sz, C_DARK)
        cur_x += w_pin_icon + 4
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(cur_x, line1_y)
        ctx.show_text(loc)
        self.y += 14

        # --- LINE 2: [in] LinkedIn · [GitHub] GitHub · [Globe] Portfolio ---
        li_text = "LinkedIn"
        gh_text = "GitHub"
        port_text = "Portfolio"

        li_ext = ctx.text_extents(li_text)
        gh_ext = ctx.text_extents(gh_text)
        port_ext = ctx.text_extents(port_text)

        w_li_icon = icon_sz
        w_gh_icon = icon_sz
        w_wb_icon = icon_sz

        line2_w = (w_li_icon + 4 + li_ext.width + 
                   dot_ext.width + 
                   w_gh_icon + 4 + gh_ext.width + 
                   dot_ext.width + 
                   w_wb_icon + 4 + port_ext.width)
        
        cur_x2 = (PAGE_WIDTH - line2_w) / 2
        line2_y = self.y + 3

        # LinkedIn
        draw_linkedin_icon(ctx, cur_x2, line2_y, icon_sz, C_DARK)
        cur_x2 += w_li_icon + 4
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(cur_x2, line2_y)
        ctx.show_text(li_text)
        cur_x2 += li_ext.width

        # Dot
        ctx.set_source_rgb(*C_MUTED)
        ctx.move_to(cur_x2, line2_y)
        ctx.show_text("  ·  ")
        cur_x2 += dot_ext.width

        # GitHub
        draw_github_icon(ctx, cur_x2, line2_y, icon_sz, C_DARK)
        cur_x2 += w_gh_icon + 4
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(cur_x2, line2_y)
        ctx.show_text(gh_text)
        cur_x2 += gh_ext.width

        # Dot
        ctx.set_source_rgb(*C_MUTED)
        ctx.move_to(cur_x2, line2_y)
        ctx.show_text("  ·  ")
        cur_x2 += dot_ext.width

        # Portfolio
        draw_globe_icon(ctx, cur_x2, line2_y, icon_sz, C_DARK)
        cur_x2 += w_wb_icon + 4
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(cur_x2, line2_y)
        ctx.show_text(port_text)
        self.y += 12

        # Dual-tone rule line (Synthwave Magenta to Cyan)
        ctx.save()
        ctx.set_line_width(1.5)
        pat = cairo.LinearGradient(MARGIN_X, self.y, PAGE_WIDTH - MARGIN_X, self.y)
        pat.add_color_stop_rgb(0.0, *C_PINK)
        pat.add_color_stop_rgb(1.0, *C_BLUE)
        ctx.set_source(pat)
        ctx.move_to(MARGIN_X, self.y + 4)
        ctx.line_to(PAGE_WIDTH - MARGIN_X, self.y + 4)
        ctx.stroke()
        ctx.restore()
        self.y += 14

    def draw_section_title(self, title):
        ctx = self.ctx
        self.y += 6
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(9.5)
        ctx.set_source_rgb(*C_PINK)
        ctx.move_to(MARGIN_X, self.y)
        ctx.show_text(title.upper())

        # Fine rule line under title
        ctx.save()
        ctx.set_line_width(0.8)
        ctx.set_source_rgb(*C_BLUE)
        ctx.move_to(MARGIN_X, self.y + 4)
        ctx.line_to(PAGE_WIDTH - MARGIN_X, self.y + 4)
        ctx.stroke()
        ctx.restore()
        self.y += 14

    def draw_paragraph(self, text, font_size=8.5, line_spacing=11.5, color=C_DARK, italic=False):
        ctx = self.ctx
        slant = cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL
        ctx.select_font_face("Sans", slant, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(font_size)
        ctx.set_source_rgb(*color)
        lines = wrap_text(ctx, text, CONTENT_WIDTH)
        for l in lines:
            ctx.move_to(MARGIN_X, self.y + font_size)
            ctx.show_text(l)
            self.y += line_spacing

    def draw_bullet(self, text, indent=14, font_size=8, line_spacing=10.5):
        ctx = self.ctx
        
        # Draw native vector triangle bullet (0% tofu, 100% vector precision)
        ctx.save()
        ctx.set_source_rgb(*C_PINK)
        bx = MARGIN_X + 2
        by = self.y + font_size * 0.55
        ctx.move_to(bx, by - 2.8)
        ctx.line_to(bx + 3.8, by)
        ctx.line_to(bx, by + 2.8)
        ctx.close_path()
        ctx.fill()
        ctx.restore()
        
        # Text
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(font_size)
        ctx.set_source_rgb(*C_DARK)
        available_w = CONTENT_WIDTH - indent
        lines = wrap_text(ctx, text, available_w)
        for i, l in enumerate(lines):
            ctx.move_to(MARGIN_X + indent, self.y + font_size)
            ctx.show_text(l)
            self.y += line_spacing

    def finish(self):
        if self.surface_type == "image":
            self.surface.write_to_png(self.filename)
        else:
            self.draw_footer()
            self.surface.finish()

def render_page1(canvas, data, lang="en"):
    profile = data["profile"]
    summary = get_text(data["summary"], lang)
    top_projects = data["topProjects"]
    is_es = (lang == "es")

    t_summary = "Perfil Ejecutivo & Alcance" if is_es else "Executive Profile & Scope"
    t_top = "Iniciativas Estratégicas Destacadas" if is_es else "Strategic Initiatives (Featured)"

    canvas.draw_header(profile, lang)
    
    # Executive Summary
    canvas.draw_section_title(t_summary)
    canvas.draw_paragraph(summary, font_size=8.5, line_spacing=11.5)
    canvas.y += 6

    # Top Projects
    canvas.draw_section_title(t_top)
    for p in top_projects:
        ctx = canvas.ctx
        p_title = get_text(p["title"], lang)
        p_period = p["period"]
        p_role = get_text(p["role"], lang)
        p_comp = p["company"]
        p_overview = get_text(p["overview"], lang)
        p_impact = get_text(p["impact"], lang)
        p_stack = ", ".join(p["stack"])

        # Project Header Row (No "TOP #" tag)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(9.5)
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(MARGIN_X, canvas.y + 8)
        ctx.show_text(p_title)

        # Period & Company
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(8.5)
        ctx.set_source_rgb(*C_BLUE)
        right_str = f"{p_comp} · {p_period}"
        ext = ctx.text_extents(right_str)
        ctx.move_to(PAGE_WIDTH - MARGIN_X - ext.width, canvas.y + 8)
        ctx.show_text(right_str)
        canvas.y += 12

        # Role Subtitle
        ctx.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8.5)
        ctx.set_source_rgb(*C_PINK)
        ctx.move_to(MARGIN_X, canvas.y + 6)
        ctx.show_text(f"Role: {p_role}")
        canvas.y += 10

        # Overview
        canvas.draw_paragraph(p_overview, font_size=8, line_spacing=10.5, color=C_MUTED)
        
        # 2 Key Bullets
        for b in p_impact[:2]:
            canvas.draw_bullet(b, font_size=7.8, line_spacing=10)

        # Tech Stack Tag Line
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(7.5)
        ctx.set_source_rgb(*C_BLUE)
        ctx.move_to(MARGIN_X + 14, canvas.y + 6)
        ctx.show_text(f"Stack: {p_stack}")
        canvas.y += 12

def render_page2(canvas, data, lang="en"):
    experience = data["experience"]
    skills = data["skills"]
    education = data["education"]
    languages = data["languages"]
    is_es = (lang == "es")

    t_exp = "Trayectoria Profesional" if is_es else "Professional Career History"
    t_skills = "Matriz de Competencias" if is_es else "Technical Taxonomy & Governance"
    t_edu = "Formación Académica e Idiomas" if is_es else "Academic Credentials & Languages"

    canvas.draw_section_title(t_exp)
    for e in experience:
        ctx = canvas.ctx
        comp = e["company"]
        pos = get_text(e["position"], lang)
        dates = f"{get_text(e['start'], lang)} – {get_text(e['end'], lang)}"
        loc = get_text(e["location"], lang)
        bullets = get_text(e["bullets"], lang)
        stack = ", ".join(e.get("stack", []))

        # Company & Dates
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(9)
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(MARGIN_X, canvas.y + 8)
        ctx.show_text(comp)

        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(8)
        ctx.set_source_rgb(*C_BLUE)
        ext = ctx.text_extents(dates)
        ctx.move_to(PAGE_WIDTH - MARGIN_X - ext.width, canvas.y + 8)
        ctx.show_text(dates)
        canvas.y += 11

        # Position & Location
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8.5)
        ctx.set_source_rgb(*C_PINK)
        ctx.move_to(MARGIN_X, canvas.y + 6)
        ctx.show_text(f"{pos} · {loc}")
        canvas.y += 9

        # Bullets
        bullet_count = 3 if "Santander" in comp else 2
        for b in bullets[:bullet_count]:
            canvas.draw_bullet(b, font_size=7.8, line_spacing=9.8)

        if stack:
            ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(7.5)
            ctx.set_source_rgb(*C_MUTED)
            ctx.move_to(MARGIN_X + 14, canvas.y + 5)
            ctx.show_text(f"Stack: {stack}")
            canvas.y += 8
        canvas.y += 4

    # Skills Matrix
    canvas.draw_section_title(t_skills)
    for s in skills:
        cat = get_text(s["category"], lang)
        items = ", ".join(s["items"])
        ctx = canvas.ctx
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(7.8)
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(MARGIN_X, canvas.y + 7)
        cat_str = f"• {cat}: "
        ctx.show_text(cat_str)
        ext = ctx.text_extents(cat_str)

        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(7.8)
        ctx.set_source_rgb(*C_MUTED)
        ctx.move_to(MARGIN_X + ext.width, canvas.y + 7)
        ctx.show_text(items)
        canvas.y += 10

    # Education & Languages
    canvas.draw_section_title(t_edu)
    for ed in education:
        inst = ed["institution"]
        deg = get_text(ed["degree"], lang)
        period = ed["period"]
        field = get_text(ed["field"], lang)
        loc = ed["location"]
        
        ctx = canvas.ctx
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(8.5)
        ctx.set_source_rgb(*C_DARK)
        ctx.move_to(MARGIN_X, canvas.y + 7)
        ctx.show_text(f"{inst} — {deg}")
        
        ctx.set_font_size(8)
        ctx.set_source_rgb(*C_BLUE)
        ext = ctx.text_extents(period)
        ctx.move_to(PAGE_WIDTH - MARGIN_X - ext.width, canvas.y + 7)
        ctx.show_text(period)
        canvas.y += 10

        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(7.8)
        ctx.set_source_rgb(*C_MUTED)
        ctx.move_to(MARGIN_X, canvas.y + 6)
        ctx.show_text(f"{field} · {loc}")
        canvas.y += 12

    # Languages
    lang_str = " | ".join([f"{get_text(l['language'], lang)}: {get_text(l['proficiency'], lang)}" for l in languages])
    ctx = canvas.ctx
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(8)
    ctx.set_source_rgb(*C_PINK)
    ctx.move_to(MARGIN_X, canvas.y + 6)
    ctx.show_text(f"Languages: {lang_str}")
    canvas.y += 10

def generate_pdf(data, lang="en", outfile="output.pdf"):
    canvas = PDFCanvas(outfile, total_pages=2, surface_type="pdf")
    render_page1(canvas, data, lang)
    canvas.next_page()
    render_page2(canvas, data, lang)
    canvas.finish()
    print(f"Generated PDF: {outfile}")

def generate_preview_image(data, lang="en", outfile="preview.png"):
    canvas = PDFCanvas(outfile, total_pages=1, surface_type="image")
    render_page1(canvas, data, lang)
    canvas.finish()
    print(f"Generated Preview Image: {outfile}")

def main():
    data = load_data()
    out_en = os.path.join(DOCS_DIR, "AngelSarrion-CV.pdf")
    out_es = os.path.join(DOCS_DIR, "AngelSarrion-CV-es.pdf")
    generate_pdf(data, "en", out_en)
    generate_pdf(data, "es", out_es)

    # Generate Page 1 PNG Previews
    prev_en = os.path.join(ASSETS_DIR, "cv-preview.png")
    prev_es = os.path.join(ASSETS_DIR, "cv-preview-es.png")
    generate_preview_image(data, "en", prev_en)
    generate_preview_image(data, "es", prev_es)

if __name__ == "__main__":
    main()
