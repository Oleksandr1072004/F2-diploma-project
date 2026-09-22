from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from datetime import datetime


async def generate_diagnostic_report(car_id: int, diagnostics: list) -> str:
    """Генерація PDF звіту діагностики"""

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

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#E32929'),
        spaceAfter=20,
    )

    elements = []

    # Заголовок
    elements.append(Paragraph("AutoSpark — Звіт діагностики", title_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Інформація про авто
    elements.append(Paragraph(f"<b>Автомобіль ID:</b> {car_id}", styles['Normal']))
    elements.append(Paragraph(
        f"<b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 1 * cm))

    # Таблиця діагностик
    for diag in diagnostics:
        elements.append(Paragraph(
            f"<b>Діагностика #{diag.id}</b> — {diag.ecu_type or 'Загальна'}",
            styles['Heading2']
        ))

        if diag.dtc_codes:
            elements.append(Paragraph("<b>Коди помилок:</b>", styles['Normal']))
            for code in diag.dtc_codes:
                elements.append(Paragraph(f"• {code}", styles['Normal']))

        if diag.diagnosis:
            elements.append(Paragraph(f"<b>Висновок:</b> {diag.diagnosis}", styles['Normal']))

        if diag.recommendations:
            elements.append(Paragraph(
                f"<b>Рекомендації:</b> {diag.recommendations}",
                styles['Normal']
            ))

        elements.append(Spacer(1, 0.5 * cm))

    # Футер
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        "<i>AutoSpark — вул. Олександра Маланчука, 49, Чернівці<br/>"
        "Тел: +380 95 212 02 35</i>",
        styles['Normal']
    ))

    # Генеруємо PDF
    doc.build(elements)

    return str(filepath)