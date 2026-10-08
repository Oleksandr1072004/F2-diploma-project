from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from datetime import datetime


# Шлях до шрифтів (поруч з цим файлом)
FONTS_DIR = Path(__file__).parent / "fonts"


def register_fonts():
    """Реєстрація TTF-шрифтів з підтримкою кирилиці"""
    pdfmetrics.registerFont(
        TTFont("AutoSpark", str(FONTS_DIR / "DejaVuSans.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("AutoSpark-Bold", str(FONTS_DIR / "DejaVuSans-Bold.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("AutoSpark-Italic", str(FONTS_DIR / "DejaVuSans-Oblique.ttf"))
    )
    # Реєструємо сімейство шрифтів (щоб <b> та <i> працювали)
    pdfmetrics.registerFontFamily(
        "AutoSpark",
        normal="AutoSpark",
        bold="AutoSpark-Bold",
        italic="AutoSpark-Italic",
        boldItalic="AutoSpark-Bold",
    )


async def generate_diagnostic_report(car_id: int, diagnostics: list) -> str:
    """Генерація PDF звіту діагностики з підтримкою кирилиці"""

    # Реєструємо шрифти
    register_fonts()

    # Папка для звітів
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    filename = f"diagnostic_{car_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = reports_dir / filename

    # Створюємо документ
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Стилі з нашим шрифтом
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='AutoSpark-Bold',
        fontSize=18,
        textColor=colors.HexColor('#E32929'),
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName='AutoSpark-Bold',
        fontSize=14,
        textColor=colors.HexColor('#111111'),
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='AutoSpark',
        fontSize=11,
        leading=16,
    )

    footer_style = ParagraphStyle(
        'CustomFooter',
        parent=styles['Normal'],
        fontName='AutoSpark-Italic',
        fontSize=9,
        textColor=colors.grey,
    )

    elements = []

    # Заголовок
    elements.append(Paragraph("AutoSpark — Звіт діагностики", title_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Інформація про авто
    elements.append(Paragraph(
        f"<b>Автомобіль ID:</b> {car_id}",
        normal_style
    ))
    elements.append(Paragraph(
        f"<b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        normal_style
    ))
    elements.append(Spacer(1, 1 * cm))

    # Таблиця діагностик
    for diag in diagnostics:
        elements.append(Paragraph(
            f"<b>Діагностика #{diag.id}</b> — {diag.ecu_type or 'Загальна'}",
            heading_style
        ))

        if diag.dtc_codes:
            elements.append(Paragraph("<b>Коди помилок:</b>", normal_style))
            for code in diag.dtc_codes:
                elements.append(Paragraph(f"• {code}", normal_style))

        if diag.diagnosis:
            elements.append(Paragraph(
                f"<b>Висновок:</b> {diag.diagnosis}",
                normal_style
            ))

        if diag.recommendations:
            elements.append(Paragraph(
                f"<b>Рекомендації:</b> {diag.recommendations}",
                normal_style
            ))

        elements.append(Spacer(1, 0.5 * cm))

    # Футер
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        "AutoSpark — вул. Олександра Маланчука, 49, Чернівці<br/>"
        "Тел: +380 95 212 02 35",
        footer_style
    ))

    # Генеруємо PDF
    doc.build(elements)

    return str(filepath)