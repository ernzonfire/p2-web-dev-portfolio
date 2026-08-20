#!/usr/bin/env python3
"""Build the portfolio resume PDF with a compact, ATS-friendly layout."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "resume" / "ErnieDemaluan_FullStackDeveloper_2026.pdf"

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#333333")


def link(label: str, url: str) -> str:
    return f'<link href="{url}" color="#111111"><u>{label}</u></link>'


def build_styles():
    sample = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=23,
            textColor=INK,
            spaceAfter=3,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=INK,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11,
            textColor=MUTED,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.6,
            leading=11.5,
            textColor=INK,
            spaceBefore=9,
            spaceAfter=3.5,
            uppercase=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.8,
            textColor=INK,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.9,
            leading=11.7,
            textColor=INK,
            spaceAfter=2,
        ),
        "project_title": ParagraphStyle(
            "ProjectTitle",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=INK,
            spaceBefore=3,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.9,
            leading=11.6,
            leftIndent=9,
            firstLineIndent=-7,
            textColor=INK,
            spaceAfter=1.6,
        ),
    }


def section_heading(text: str, styles):
    return Paragraph(text.upper(), styles["section"])


def project_block(title: str, details: list[str], styles):
    items = [Paragraph(title, styles["project_title"])]
    items.extend(Paragraph(f"- {detail}", styles["bullet"]) for detail in details)
    return KeepTogether(items)


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Ernie Demaluan Jr. - Full-Stack Developer Resume")
    canvas.setAuthor("Ernie Demaluan Jr.")
    canvas.setSubject("Full-stack developer resume and selected project experience")
    canvas.restoreState()


def build_resume():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=0.48 * inch,
        rightMargin=0.48 * inch,
        topMargin=0.52 * inch,
        bottomMargin=0.52 * inch,
        title="Ernie Demaluan Jr. - Full-Stack Developer Resume",
        author="Ernie Demaluan Jr.",
    )

    story = [
        Paragraph("ERNIE DEMALUAN JR.", styles["name"]),
        Paragraph("FULL-STACK DEVELOPER | CEBU, PHILIPPINES", styles["role"]),
        Paragraph(
            "ejdemaluan@gmail.com &nbsp;|&nbsp; "
            + link("Portfolio", "https://p2-web-dev-portfolio.vercel.app/")
            + " &nbsp;|&nbsp; "
            + link("GitHub", "https://github.com/ernzonfire")
            + " &nbsp;|&nbsp; "
            + link("LinkedIn", "https://www.linkedin.com/in/ernie-demaluan-b98673191/"),
            styles["contact"],
        ),
        Spacer(1, 3),
        section_heading("Professional Summary", styles),
        Paragraph(
            "Full-stack developer building responsive web applications and production mobile products. "
            "Experienced across React, Node.js, Express, MongoDB, Supabase, SwiftUI, Kotlin, REST APIs, "
            "authentication, deployment, and local-first data. Brings a creative production background and "
            "a strong focus on usability, execution, and clear problem-solving.",
            styles["body"],
        ),
        section_heading("Technical Skills", styles),
        Paragraph(
            "<b>Frontend:</b> HTML5, CSS3, JavaScript, TypeScript, React, Vite, responsive UI &nbsp;&nbsp; "
            "<b>Backend:</b> Node.js, Express, REST APIs, JWT authentication, Socket.IO",
            styles["small"],
        ),
        Paragraph(
            "<b>Data:</b> MongoDB, Mongoose, Supabase, IndexedDB, local-first storage &nbsp;&nbsp; "
            "<b>Mobile:</b> SwiftUI, Kotlin, Jetpack Compose, Capacitor",
            styles["small"],
        ),
        Paragraph(
            "<b>Workflow:</b> Git, GitHub, Postman, Vercel, Render, testing, debugging, accessibility",
            styles["small"],
        ),
        section_heading("Selected Projects", styles),
        project_block(
            "ERN FINANCE | INDEPENDENT PRODUCT | SWIFTUI, KOTLIN, REACT | "
            + link("App Store", "https://apps.apple.com/ph/app/ern-finance/id6789468096")
            + " | "
            + link("Google Play", "https://play.google.com/store/apps/details?id=com.ern.finance"),
            [
                "Designed and shipped a privacy-first finance product across native iOS, native Android, and React/PWA surfaces.",
                "Built local-first tracking for accounts, expenses, budgets, card dues, goals, and safe-to-spend planning.",
                "Released on the App Store and Google Play with public listings and cross-platform release workflows.",
            ],
            styles,
        ),
        project_block(
            "PAYNEAR (P6) | MERN GROUP PROJECT | "
            + link("Live", "https://paynear.vercel.app/")
            + " | "
            + link("Code", "https://github.com/ernzonfire/paynear-p6"),
            [
                "Collaborated in a four-person team on a map-first platform for finding nearby establishments by accepted payment method.",
                "The product includes role-based accounts, owner submissions, admin verification, reviews, Socket.IO chat, notifications, and AI-assisted filters.",
            ],
            styles,
        ),
        project_block(
            "KUSINAMATE (P5) | REACT, NODE.JS, EXPRESS, MONGODB | "
            + link("Live", "https://kusina-mate-p5.vercel.app/")
            + " | "
            + link("Code", "https://github.com/ernzonfire/kusina-mate-p5"),
            [
                "Extended a React meal planner with a REST API, JWT accounts, recipe CRUD, and persistent user data.",
                "Implemented favorites, weekly meal plans, grocery aggregation, filtering, analytics, and production deployment.",
            ],
            styles,
        ),
        project_block(
            "ADDITIONAL SHIPPED WORK",
            [
                link("KusinaMate React (P4)", "https://kusina-mate.vercel.app/")
                + " - Responsive client-side meal planner with search, budget filters, favorites, and weekly planning.",
                link("ExplainIt AI (P3)", "https://explainit-ai-app.vercel.app/")
                + " - JavaScript and REST API learning tool with structured, beginner-friendly explanations.",
                link("Personal Portfolio (P2)", "https://p2-web-dev-portfolio.vercel.app/")
                + " - Responsive, accessible portfolio with documented project and contact links.",
            ],
            styles,
        ),
        project_block(
            "NEXT INTERNAL PLATFORM | NEXT.JS, SUPABASE, VERCEL | ONGOING",
            [
                "Built an employee engagement platform with authentication, events, QR attendance validation, points, rewards, and admin workflows.",
                "Structured multi-user product flows and real-time validation for scalable internal operations.",
            ],
            styles,
        ),
        section_heading("Professional Experience", styles),
        Paragraph(
            "<b>VOC ANALYST / TECHNICAL &amp; CREATIVE SUPPORT</b> &nbsp;|&nbsp; ResultsCX - Newtown &nbsp;|&nbsp; 2024 - Present",
            styles["project_title"],
        ),
        Paragraph(
            "- Analyze customer feedback to identify recurring product, system, and workflow improvements.",
            styles["bullet"],
        ),
        Paragraph(
            "- Translate customer and operational data into clear findings for service and experience improvements.",
            styles["bullet"],
        ),
        Paragraph(
            "- Troubleshoot operational and event systems, support livestream setups, and communicate issues clearly across teams.",
            styles["bullet"],
        ),
        Paragraph(
            "- Recognized as NPS Champion (2024 - Present); apply structured problem-solving to improve service and execution.",
            styles["bullet"],
        ),
        section_heading("Education and Training", styles),
        Paragraph(
            "<b>UPLIFT CODE CAMP</b> &nbsp;|&nbsp; Full-Stack Web Development Bootcamp &nbsp;|&nbsp; 2026",
            styles["project_title"],
        ),
        Paragraph(
            "Project-based training in JavaScript, React, Node.js, Express, MongoDB, APIs, Git, testing, and production deployment.",
            styles["small"],
        ),
    ]

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    print(OUTPUT)


if __name__ == "__main__":
    build_resume()
