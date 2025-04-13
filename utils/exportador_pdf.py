
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from modelos.curso import Curso
from modelos.docente import Docente
from modelos.salon import Salon
from individuo import Individuo

def exportar_horario_pdf(nombre_archivo: str, individuo: Individuo, cursos: list[Curso]):
    cursos_por_codigo = {c.codigo: c for c in cursos}
    horarios_ordenados = sorted(set(h for _, h, _ in individuo.asignaciones.values()))

    data = [["Código", "Curso", "Carrera", "Semestre", "Sección", "Tipo", "Salón", "Horario", "Docente"]]

    # Agrupar por horario
    for horario in horarios_ordenados:
        for codigo, (salon, hora, docente) in individuo.asignaciones.items():
            if hora != horario:
                continue
            curso = cursos_por_codigo[codigo]
            data.append([
                curso.codigo,
                curso.nombre,
                curso.carrera,
                str(curso.semestre),
                curso.seccion,
                curso.tipo.capitalize(),
                salon.nombre,
                hora,
                docente.nombre if docente else "No asignado"
            ])

    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Horario Generado - Mejor Individuo", styles['Title']))
    elements.append(Spacer(1, 12))

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a90e2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f1f1")]),
    ]))

    elements.append(table)
    doc.build(elements)

    print(f"Horario exportado exitosamente como PDF: {nombre_archivo}")
