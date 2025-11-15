# reportes/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from django.contrib.staticfiles import finders
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

import pandas as pd
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Image,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

from plantas.models import plantaArbol
from mantenimiento.models import TareaMantenimiento


# --------- 1) Página principal de reportes ---------
@login_required
def reportes_inicio(request):
    """
    Página principal para elegir qué reporte generar: especies o mantenimiento.
    """
    return render(request, "reportes/inicio_reportes.html")


# --------- 2) Helper simple para obtener rol ---------
def _rol(user) -> str:
    """
    Regresa el rol en minúsculas para comparar más fácil.
    Se asume que user.rol puede ser: 'administrador', 'gestor', 'mantenimiento'.
    """
    r = getattr(user, "rol", None) or getattr(user, "tipo_usuario", None) or ""
    return str(r).lower()


# --------- 3) REPORTE DE ESPECIES ---------
@login_required
def reporte_especies(request):
    usuario = request.user
    rol = _rol(usuario)

    # =========================
    # 1) Query base según rol
    # =========================
    if rol == "administrador":
        # Administrador general: acceso completo a todos los reportes
        qs = plantaArbol.objects.all()
    elif rol == "gestor":
        # Gestor de especies:
        # acceso a reportes relacionados con las especies y tareas que haya registrado.
        plantas_ids = (
            TareaMantenimiento.objects.filter(
                Q(usuario_responsable=usuario) | Q(modificado_por=usuario)
            )
            .values("planta_id")
        )
        qs = plantaArbol.objects.filter(id_planta__in=plantas_ids).distinct()
    elif rol == "mantenimiento":
        # Usuario de mantenimiento:
        # acceso restringido a reportes de tareas asignadas o completadas por él mismo.
        plantas_ids = (
            TareaMantenimiento.objects.filter(usuario_responsable=usuario)
            .values("planta_id")
        )
        qs = plantaArbol.objects.filter(id_planta__in=plantas_ids).distinct()
    else:
        # Si el rol no coincide, por seguridad no mostramos nada
        qs = plantaArbol.objects.none()

    # =========================
    # 2) Filtros dinámicos (buscador + rango de fechas)
    # =========================
    q = request.GET.get("q", "").strip()
    f_ini = parse_date(request.GET.get("f_ini")) if request.GET.get("f_ini") else None
    f_fin = parse_date(request.GET.get("f_fin")) if request.GET.get("f_fin") else None

    if q:
        qs = qs.filter(
            Q(nombre_comun__icontains=q)
            | Q(nombre_cientifico__icontains=q)
            | Q(descripcion__icontains=q)
        )

    if f_ini:
        qs = qs.filter(fecha_plantacion__gte=f_ini)
    if f_fin:
        qs = qs.filter(fecha_plantacion__lte=f_fin)

    total = qs.count()

    # Campos que usaremos en tabla/Excel/PDF
    columnas = [
        "nombre_comun",
        "nombre_cientifico",
        "descripcion",
        "fecha_plantacion",
        "periodicidad_riego",
        "periodicidad_poda",
        "periodicidad_fumigacion",
    ]
    valores = list(qs.values(*columnas))

    # =========================
    # 3) Datos para gráficas (para Excel/PDF)
    # =========================

    # Gráfica 1: frecuencia por nombre científico (Top 10)
    freq_por_cientifico = (
        qs.values("nombre_cientifico")
        .annotate(c=Count("id_planta"))
        .order_by("-c")[:10]
    )
    chart1_labels = [x["nombre_cientifico"] for x in freq_por_cientifico]
    chart1_data = [x["c"] for x in freq_por_cientifico]

    # Gráfica 2: distribución por periodicidad de riego
    freq_riego = (
        qs.values("periodicidad_riego")
        .annotate(c=Count("id_planta"))
        .order_by("-c")
    )
    chart2_labels = [x["periodicidad_riego"] or "Sin dato" for x in freq_riego]
    chart2_data = [x["c"] for x in freq_riego]

    # =========================
    # 4) Exportar a Excel (logo + tabla + hoja de gráficas)
    # =========================
    if "excel" in request.GET:
        from openpyxl.drawing.image import Image as XLImage
        from openpyxl.chart import BarChart, PieChart, Reference

        df = pd.DataFrame(valores)
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Hoja 1: Especies (tabla)
            df.to_excel(
                writer, sheet_name="Especies", index=False, startrow=6
            )  # tabla comienza en fila 7
            workbook = writer.book
            sheet = writer.sheets["Especies"]

            # Logo
            logo_path = finders.find("img/upemor-logo.png")
            if logo_path:
                logo = XLImage(logo_path)
                logo.width = 180
                logo.height = 90
                sheet.add_image(logo, "A1")

            # Título y total
            sheet["A5"] = "Reporte General de Especies"
            sheet["A5"].font = sheet["A5"].font.copy(bold=True, size=14)

            sheet["A6"] = f"Total de especies registradas: {total}"
            sheet["A6"].font = sheet["A6"].font.copy(bold=True)

            # Hoja 2: Datos + gráficas
            sheet2 = workbook.create_sheet(title="Gráficas")

            # Datos para gráfica 1
            sheet2["A1"] = "Nombre científico"
            sheet2["B1"] = "Frecuencia"
            for i, (lbl, val) in enumerate(zip(chart1_labels, chart1_data), start=2):
                sheet2[f"A{i}"] = lbl
                sheet2[f"B{i}"] = val

            # Datos para gráfica 2
            sheet2["D1"] = "Periodicidad riego"
            sheet2["E1"] = "Frecuencia"
            for i, (lbl, val) in enumerate(zip(chart2_labels, chart2_data), start=2):
                sheet2[f"D{i}"] = lbl
                sheet2[f"E{i}"] = val

            # Gráfica 1: BarChart
            if chart1_labels:
                bar_chart = BarChart()
                bar_chart.title = "Frecuencia por nombre científico"
                bar_chart.y_axis.title = "Cantidad"
                bar_chart.x_axis.title = "Especie"

                data_ref = Reference(
                    sheet2,
                    min_col=2,
                    min_row=1,
                    max_row=1 + len(chart1_data),
                )
                cats_ref = Reference(
                    sheet2,
                    min_col=1,
                    min_row=2,
                    max_row=1 + len(chart1_data),
                )
                bar_chart.add_data(data_ref, titles_from_data=True)
                bar_chart.set_categories(cats_ref)

                bar_chart.width = 20
                bar_chart.height = 12
                sheet2.add_chart(bar_chart, "A10")

            # Gráfica 2: PieChart
            if chart2_labels:
                pie_chart = PieChart()
                pie_chart.title = "Distribución por periodicidad de riego"

                data_ref2 = Reference(
                    sheet2,
                    min_col=5,
                    min_row=1,
                    max_row=1 + len(chart2_data),
                )
                cats_ref2 = Reference(
                    sheet2,
                    min_col=4,
                    min_row=2,
                    max_row=1 + len(chart2_data),
                )
                pie_chart.add_data(data_ref2, titles_from_data=True)
                pie_chart.set_categories(cats_ref2)

                pie_chart.width = 20
                pie_chart.height = 12
                sheet2.add_chart(pie_chart, "J10")

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="reporte_especies.xlsx"'
        return response

    # =========================
    # 5) Exportar a PDF (membrete + 2 gráficas + tabla)
    # =========================
    if "pdf" in request.GET:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=36,
            leftMargin=36,
            rightMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        story = []

        # Logo
        logo_path = finders.find("img/upemor-logo.png")
        if logo_path:
            img = Image(logo_path, width=120, height=60)
            story.append(img)
            story.append(Spacer(1, 8))

        story.append(Paragraph("Reporte General de Especies", styles["Title"]))
        story.append(Paragraph(f"Total de especies: {total}", styles["Normal"]))
        story.append(Spacer(1, 10))

        # Gráfica 1: BarChart en PDF
        if chart1_labels:
            drawing1 = Drawing(400, 200)
            bc = VerticalBarChart()
            bc.x = 50
            bc.y = 30
            bc.height = 150
            bc.width = 300
            bc.data = [chart1_data]
            bc.categoryAxis.categoryNames = chart1_labels
            bc.barWidth = 10
            bc.valueAxis.valueMin = 0
            bc.groupSpacing = 5
            drawing1.add(bc)

            story.append(
                Paragraph(
                    "Frecuencia por nombre científico (Top 10)",
                    styles["Heading3"],
                )
            )
            story.append(drawing1)
            story.append(Spacer(1, 12))

        # Gráfica 2: Pie en PDF
        if chart2_labels:
            drawing2 = Drawing(400, 200)
            pie = Pie()
            pie.x = 100
            pie.y = 15
            pie.width = 200
            pie.height = 200
            pie.data = chart2_data
            pie.labels = chart2_labels
            drawing2.add(pie)

            story.append(
                Paragraph(
                    "Distribución por periodicidad de riego",
                    styles["Heading3"],
                )
            )
            story.append(drawing2)
            story.append(Spacer(1, 12))

        # Tabla de especies
        headers = [
            "Nombre común",
            "Nombre científico",
            "Fecha plantación",
            "Riego",
            "Poda",
            "Fumigación",
        ]
        data = [headers]

        for p in valores[:300]:
            data.append(
                [
                    p.get("nombre_comun", ""),
                    p.get("nombre_cientifico", ""),
                    str(p.get("fecha_plantacion", "") or ""),
                    p.get("periodicidad_riego", ""),
                    p.get("periodicidad_poda", ""),
                    p.get("periodicidad_fumigacion", ""),
                ]
            )

        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d0f0d0")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.whitesmoke, colors.lightgrey],
                    ),
                ]
            )
        )

        story.append(table)
        doc.build(story)

        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_value, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reporte_especies.pdf"'
        return response

    # =========================
    # 6) Render en pantalla (solo filtros + tabla)
    # =========================
    context = {
        "total": total,
        "plantas": valores,
        "q": q,
        "f_ini": request.GET.get("f_ini", ""),
        "f_fin": request.GET.get("f_fin", ""),
    }
    return render(request, "reportes/reportes_especies.html", context)


# --------- 4) REPORTE DE MANTENIMIENTO ---------
@login_required
def reporte_mantenimiento(request):
    usuario = request.user
    rol = _rol(usuario)

    # =========================
    # 1) Query base según rol
    # =========================
    if rol == "administrador":
        # Admin: todas las tareas
        qs = TareaMantenimiento.objects.select_related("planta", "usuario_responsable")
    elif rol == "gestor":
        # Gestor: tareas donde aparece como responsable o modificador
        qs = (
            TareaMantenimiento.objects.select_related("planta", "usuario_responsable")
            .filter(Q(usuario_responsable=usuario) | Q(modificado_por=usuario))
        )
    elif rol == "mantenimiento":
        # Mantenimiento: solo tareas asignadas a él
        qs = (
            TareaMantenimiento.objects.select_related("planta", "usuario_responsable")
            .filter(usuario_responsable=usuario)
        )
    else:
        qs = TareaMantenimiento.objects.none()

    # =========================
    # 2) Filtros (buscador + rango de fechas programadas)
    # =========================
    q = request.GET.get("q", "").strip()
    f_ini = parse_date(request.GET.get("f_ini")) if request.GET.get("f_ini") else None
    f_fin = parse_date(request.GET.get("f_fin")) if request.GET.get("f_fin") else None

    if q:
        qs = qs.filter(
            Q(planta__nombre_comun__icontains=q)
            | Q(planta__nombre_cientifico__icontains=q)
            | Q(usuario_responsable__matricula__icontains=q)
            | Q(usuario_responsable__nombre_completo__icontains=q)
            | Q(observaciones__icontains=q)
        )

    if f_ini:
        qs = qs.filter(fecha_programada__date__gte=f_ini)
    if f_fin:
        qs = qs.filter(fecha_programada__date__lte=f_fin)

    total_tareas = qs.count()
    realizadas = qs.filter(estado=TareaMantenimiento.ESTADO_REALIZADA).count()
    cumplimiento_global = (
        round(realizadas * 100 / total_tareas, 2) if total_tareas > 0 else 0.0
    )

    # =========================
    # 3) Datos tabulares para HTML/Excel/PDF
    # =========================
    filas = []
    for t in qs:
        if t.usuario_responsable:
            usuario_nombre = (
                t.usuario_responsable.nombre_completo
                or t.usuario_responsable.matricula
                or t.usuario_responsable.email
            )
        else:
            usuario_nombre = ""

        filas.append({
            "especie": t.planta.nombre_comun if t.planta else "",
            "tipo": t.get_tipo_display(),
            "fecha_programada": t.fecha_programada,
            "fecha_realizacion": t.fecha_realizacion,
            "estado": t.get_estado_display(),
            "usuario": usuario_nombre,
            "observaciones": t.observaciones or "",
        })


    # =========================
    # 4) Cumplimiento por usuario y por especie (para % y gráficas)
    # =========================
    # Por usuario
    por_usuario = (
        qs.values("usuario_responsable__nombre_completo", "usuario_responsable__matricula")
        .annotate(
            total=Count("id"),
            realizadas=Count("id", filter=Q(estado=TareaMantenimiento.ESTADO_REALIZADA))
        )
    )
    chart1_labels = []
    chart1_data = []  # porcentaje de cumplimiento por usuario

    for r in por_usuario:
        nombre = (
            r["usuario_responsable__nombre_completo"]
            or r["usuario_responsable__matricula"]
            or "Sin asignar"
        )
        total_u = r["total"] or 0
        realizadas_u = r["realizadas"] or 0
        pct = round(realizadas_u * 100 / total_u, 2) if total_u > 0 else 0.0
        chart1_labels.append(nombre)
        chart1_data.append(pct)

    # Por especie
    por_especie = (
        qs.values("planta__nombre_comun")
        .annotate(
            total=Count("id"),
            realizadas=Count(
                "id",
                filter=Q(estado=TareaMantenimiento.ESTADO_REALIZADA),
            ),
        )
        .order_by("-total")[:10]
    )
    chart2_labels = []
    chart2_data = []  # porcentaje de cumplimiento por especie

    for r in por_especie:
        nombre_e = r["planta__nombre_comun"] or "Sin especie"
        total_e = r["total"] or 0
        realizadas_e = r["realizadas"] or 0
        pct_e = round(realizadas_e * 100 / total_e, 2) if total_e > 0 else 0.0
        chart2_labels.append(nombre_e)
        chart2_data.append(pct_e)

    # =========================
    # 5) Exportar a Excel
    # =========================
    if "excel" in request.GET:
        from openpyxl.drawing.image import Image as XLImage
        from openpyxl.chart import BarChart, Reference

        df = pd.DataFrame(filas)
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Hoja 1: Tareas
            df.to_excel(
                writer, sheet_name="Mantenimiento", index=False, startrow=6
            )
            workbook = writer.book
            sheet = writer.sheets["Mantenimiento"]

            # Logo
            logo_path = finders.find("img/upemor-logo.png")
            if logo_path:
                logo = XLImage(logo_path)
                logo.width = 180
                logo.height = 90
                sheet.add_image(logo, "A1")

            # Encabezado
            sheet["A5"] = "Reporte de mantenimiento programado y realizado"
            sheet["A5"].font = sheet["A5"].font.copy(bold=True, size=14)

            sheet[
                "A6"
            ] = f"Total de tareas: {total_tareas} | Cumplimiento global: {cumplimiento_global}%"
            sheet["A6"].font = sheet["A6"].font.copy(bold=True)

            # Hoja 2: Gráficas
            sheet2 = workbook.create_sheet(title="Gráficas")

            # Datos para gráfica 1 (por usuario)
            sheet2["A1"] = "Usuario"
            sheet2["B1"] = "% Cumplimiento"
            for i, (lbl, val) in enumerate(
                zip(chart1_labels, chart1_data), start=2
            ):
                sheet2[f"A{i}"] = lbl
                sheet2[f"B{i}"] = float(val)

            # Datos para gráfica 2 (por especie)
            sheet2["D1"] = "Especie"
            sheet2["E1"] = "% Cumplimiento"
            for i, (lbl, val) in enumerate(
                zip(chart2_labels, chart2_data), start=2
            ):
                sheet2[f"D{i}"] = lbl
                sheet2[f"E{i}"] = float(val)

            # Gráfica 1: BarChart cumplimiento por usuario
            if chart1_labels:
                bar1 = BarChart()
                bar1.title = "Cumplimiento por usuario (%)"
                bar1.y_axis.title = "% Cumplimiento"
                bar1.x_axis.title = "Usuario"

                data_ref1 = Reference(
                    sheet2,
                    min_col=2,
                    min_row=1,
                    max_row=1 + len(chart1_data),
                )
                cats_ref1 = Reference(
                    sheet2,
                    min_col=1,
                    min_row=2,
                    max_row=1 + len(chart1_data),
                )
                bar1.add_data(data_ref1, titles_from_data=True)
                bar1.set_categories(cats_ref1)
                bar1.width = 20
                bar1.height = 12
                sheet2.add_chart(bar1, "A10")

            # Gráfica 2: BarChart cumplimiento por especie
            if chart2_labels:
                bar2 = BarChart()
                bar2.title = "Cumplimiento por especie (%)"
                bar2.y_axis.title = "% Cumplimiento"
                bar2.x_axis.title = "Especie"

                data_ref2 = Reference(
                    sheet2,
                    min_col=5,
                    min_row=1,
                    max_row=1 + len(chart2_data),
                )
                cats_ref2 = Reference(
                    sheet2,
                    min_col=4,
                    min_row=2,
                    max_row=1 + len(chart2_data),
                )
                bar2.add_data(data_ref2, titles_from_data=True)
                bar2.set_categories(cats_ref2)
                bar2.width = 20
                bar2.height = 12
                sheet2.add_chart(bar2, "J10")

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_mantenimiento.xlsx"'
        )
        return response

    # =========================
    # 6) Exportar a PDF
    # =========================
    if "pdf" in request.GET:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=36,
            leftMargin=36,
            rightMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        story = []

        # Logo
        logo_path = finders.find("img/upemor-logo.png")
        if logo_path:
            img = Image(logo_path, width=120, height=60)
            story.append(img)
            story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                "Reporte de mantenimiento programado y realizado",
                styles["Title"],
            )
        )
        story.append(
            Paragraph(
                f"Total de tareas: {total_tareas} | Cumplimiento global: {cumplimiento_global}%",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 10))

        # Gráfica 1: cumplimiento por usuario
        if chart1_labels:
            drawing1 = Drawing(400, 200)
            bc1 = VerticalBarChart()
            bc1.x = 50
            bc1.y = 30
            bc1.height = 150
            bc1.width = 300
            bc1.data = [chart1_data]
            bc1.categoryAxis.categoryNames = chart1_labels
            bc1.valueAxis.valueMin = 0
            drawing1.add(bc1)

            story.append(
                Paragraph("Cumplimiento por usuario (%)", styles["Heading3"])
            )
            story.append(drawing1)
            story.append(Spacer(1, 12))

        # Gráfica 2: cumplimiento por especie
        if chart2_labels:
            drawing2 = Drawing(400, 200)
            bc2 = VerticalBarChart()
            bc2.x = 50
            bc2.y = 30
            bc2.height = 150
            bc2.width = 300
            bc2.data = [chart2_data]
            bc2.categoryAxis.categoryNames = chart2_labels
            bc2.valueAxis.valueMin = 0
            drawing2.add(bc2)

            story.append(
                Paragraph(
                    "Cumplimiento por especie (%) (Top 10)",
                    styles["Heading3"],
                )
            )
            story.append(drawing2)
            story.append(Spacer(1, 12))

        # Tabla de tareas (resumen)
        headers = [
            "Especie",
            "Tipo",
            "Fecha programada",
            "Fecha realización",
            "Estado",
            "Usuario responsable",
            "Observaciones",
        ]
        data = [headers]
        for f in filas[:300]:
            data.append(
                [
                    f["especie"],
                    f["tipo"],
                    str(f["fecha_programada"] or ""),
                    str(f["fecha_realizacion"] or ""),
                    f["estado"],
                    f["usuario"],
                    f["observaciones"],
                ]
            )

        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d0f0d0")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.whitesmoke, colors.lightgrey],
                    ),
                ]
            )
        )

        story.append(table)
        doc.build(story)

        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(
            pdf_value, content_type="application/pdf"
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_mantenimiento.pdf"'
        )
        return response

    # =========================
    # 7) Render HTML (filtros + tabla)
    # =========================
    context = {
        "total_tareas": total_tareas,
        "realizadas": realizadas,
        "cumplimiento_global": cumplimiento_global,
        "tareas": filas,
        "q": q,
        "f_ini": request.GET.get("f_ini", ""),
        "f_fin": request.GET.get("f_fin", ""),
    }
    return render(request, "reportes/reportes_mantenimiento.html", context)

# --------- 5) REPORTE DE CUMPLIMIENTO DE TAREAS POR USUARIOS ---------
@login_required
def reportes_cumplimiento_usuarios(request):
    usuario = request.user
    rol = _rol(usuario)

    # Solo Admin y Gestor tienen acceso
    if rol not in ("administrador", "gestor"):
        return HttpResponseForbidden("No tiene permiso para ver este reporte.")

    User = get_user_model()

    # =========================
    # 1) Base de tareas: solo usuarios de rol mantenimiento
    # =========================
    qs = TareaMantenimiento.objects.select_related("usuario_responsable").filter(
        usuario_responsable__rol="mantenimiento"
    )

    # =========================
    # 2) Filtros (buscador por usuario + rango de fechas programadas)
    # =========================
    q = request.GET.get("q", "").strip()
    f_ini = parse_date(request.GET.get("f_ini")) if request.GET.get("f_ini") else None
    f_fin = parse_date(request.GET.get("f_fin")) if request.GET.get("f_fin") else None

    if q:
        qs = qs.filter(
            Q(usuario_responsable__nombre_completo__icontains=q)
            | Q(usuario_responsable__matricula__icontains=q)
            | Q(usuario_responsable__email__icontains=q)
        )

    if f_ini:
        qs = qs.filter(fecha_programada__date__gte=f_ini)
    if f_fin:
        qs = qs.filter(fecha_programada__date__lte=f_fin)

    # =========================
    # 3) Estadísticas globales
    # =========================
    total_tareas = qs.count()
    realizadas = qs.filter(estado=TareaMantenimiento.ESTADO_REALIZADA).count()
    pendientes = qs.filter(estado=TareaMantenimiento.ESTADO_PENDIENTE).count()
    cumplimiento_global = (
        round(realizadas * 100 / total_tareas, 2) if total_tareas > 0 else 0.0
    )

    # =========================
    # 4) Agregados por usuario de mantenimiento
    # =========================
    agregados = (
        qs.values(
            "usuario_responsable__id_usuario",
            "usuario_responsable__nombre_completo",
            "usuario_responsable__matricula",
            "usuario_responsable__email",
        )
        .annotate(
            total=Count("id"),
            realizadas=Count(
                "id",
                filter=Q(estado=TareaMantenimiento.ESTADO_REALIZADA),
            ),
        )
        .order_by("-realizadas")  # ranking: más activas primero
    )

    filas = []
    for r in agregados:
        total_u = r["total"] or 0
        realizadas_u = r["realizadas"] or 0
        pendientes_u = total_u - realizadas_u
        pct = round(realizadas_u * 100 / total_u, 2) if total_u > 0 else 0.0

        nombre = (
            r["usuario_responsable__nombre_completo"]
            or r["usuario_responsable__matricula"]
            or r["usuario_responsable__email"]
            or "Sin nombre"
        )

        filas.append(
            {
                "id": r["usuario_responsable__id_usuario"],
                "nombre": nombre,
                "matricula": r["usuario_responsable__matricula"],
                "email": r["usuario_responsable__email"],
                "total": total_u,
                "realizadas": realizadas_u,
                "pendientes": pendientes_u,
                "porcentaje": pct,
            }
        )

    # =========================
    # 5) Datos para gráficas
    # =========================
    # Gráfica 1: % cumplimiento por usuario
    chart1_labels = [f["nombre"] for f in filas]
    chart1_data = [f["porcentaje"] for f in filas]

    # Gráfica 2: tareas realizadas vs pendientes (global)
    chart2_labels = ["Realizadas", "Pendientes"]
    chart2_data = [realizadas, pendientes]

    # =========================
    # 6) Exportar a Excel
    # =========================
    if "excel" in request.GET:
        from openpyxl.drawing.image import Image as XLImage
        from openpyxl.chart import BarChart, PieChart, Reference

        df = pd.DataFrame(filas)
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Hoja 1: Resumen por usuario
            df.to_excel(
                writer, sheet_name="Cumplimiento", index=False, startrow=6
            )
            workbook = writer.book
            sheet = writer.sheets["Cumplimiento"]

            # Logo
            logo_path = finders.find("img/upemor-logo.png")
            if logo_path:
                logo = XLImage(logo_path)
                logo.width = 180
                logo.height = 90
                sheet.add_image(logo, "A1")

            # Encabezado
            sheet["A5"] = "Reporte de cumplimiento de tareas por usuarios"
            sheet["A5"].font = sheet["A5"].font.copy(bold=True, size=14)

            sheet[
                "A6"
            ] = f"Total tareas: {total_tareas} | Realizadas: {realizadas} | Pendientes: {pendientes} | Cumplimiento global: {cumplimiento_global}%"
            sheet["A6"].font = sheet["A6"].font.copy(bold=True)

            # Hoja 2: Gráficas
            sheet2 = workbook.create_sheet(title="Gráficas")

            # Datos para gráfica 1 (por usuario)
            sheet2["A1"] = "Usuario"
            sheet2["B1"] = "% Cumplimiento"
            for i, (lbl, val) in enumerate(
                zip(chart1_labels, chart1_data), start=2
            ):
                sheet2[f"A{i}"] = lbl
                sheet2[f"B{i}"] = float(val)

            # Datos para gráfica 2 (global)
            sheet2["D1"] = "Estado"
            sheet2["E1"] = "Cantidad"
            for i, (lbl, val) in enumerate(
                zip(chart2_labels, chart2_data), start=2
            ):
                sheet2[f"D{i}"] = lbl
                sheet2[f"E{i}"] = int(val)

            # Gráfica 1: BarChart cumplimiento por usuario
            if chart1_labels:
                bar1 = BarChart()
                bar1.title = "Cumplimiento por usuario (%)"
                bar1.y_axis.title = "% Cumplimiento"
                bar1.x_axis.title = "Usuario"

                data_ref1 = Reference(
                    sheet2,
                    min_col=2,
                    min_row=1,
                    max_row=1 + len(chart1_data),
                )
                cats_ref1 = Reference(
                    sheet2,
                    min_col=1,
                    min_row=2,
                    max_row=1 + len(chart1_data),
                )
                bar1.add_data(data_ref1, titles_from_data=True)
                bar1.set_categories(cats_ref1)
                bar1.width = 20
                bar1.height = 12
                sheet2.add_chart(bar1, "A10")

            # Gráfica 2: PieChart realizadas vs pendientes
            if sum(chart2_data) > 0:
                pie = PieChart()
                pie.title = "Tareas realizadas vs pendientes"
                data_ref2 = Reference(
                    sheet2,
                    min_col=5,
                    min_row=1,
                    max_row=1 + len(chart2_data),
                )
                cats_ref2 = Reference(
                    sheet2,
                    min_col=4,
                    min_row=2,
                    max_row=1 + len(chart2_data),
                )
                pie.add_data(data_ref2, titles_from_data=True)
                pie.set_categories(cats_ref2)
                pie.width = 15
                pie.height = 10
                sheet2.add_chart(pie, "J10")

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_cumplimiento_usuarios.xlsx"'
        )
        return response

    # =========================
    # 7) Exportar a PDF
    # =========================
    if "pdf" in request.GET:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=36,
            leftMargin=36,
            rightMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        story = []

        # Logo
        logo_path = finders.find("img/upemor-logo.png")
        if logo_path:
            img = Image(logo_path, width=120, height=60)
            story.append(img)
            story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                "Reporte de cumplimiento de tareas por usuarios",
                styles["Title"],
            )
        )
        story.append(
            Paragraph(
                f"Total tareas: {total_tareas} | Realizadas: {realizadas} | Pendientes: {pendientes} | Cumplimiento global: {cumplimiento_global}%",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 10))

        # Gráfica 1: cumplimiento por usuario
        if chart1_labels:
            drawing1 = Drawing(400, 200)
            bc1 = VerticalBarChart()
            bc1.x = 50
            bc1.y = 30
            bc1.height = 150
            bc1.width = 300
            bc1.data = [chart1_data]
            bc1.categoryAxis.categoryNames = chart1_labels
            bc1.valueAxis.valueMin = 0
            drawing1.add(bc1)

            story.append(
                Paragraph("Cumplimiento por usuario (%)", styles["Heading3"])
            )
            story.append(drawing1)
            story.append(Spacer(1, 12))

        # Gráfica 2: realizadas vs pendientes
        if sum(chart2_data) > 0:
            drawing2 = Drawing(400, 200)
            pie2 = Pie()
            pie2.x = 100
            pie2.y = 15
            pie2.width = 200
            pie2.height = 200
            pie2.data = chart2_data
            pie2.labels = chart2_labels
            drawing2.add(pie2)

            story.append(
                Paragraph(
                    "Tareas realizadas vs pendientes",
                    styles["Heading3"],
                )
            )
            story.append(drawing2)
            story.append(Spacer(1, 12))

        # Tabla de resumen por usuario
        headers = [
            "Usuario",
            "Matrícula",
            "Email",
            "Tareas programadas",
            "Realizadas",
            "Pendientes",
            "% Cumplimiento",
        ]
        data = [headers]
        for f in filas[:300]:
            data.append(
                [
                    f["nombre"],
                    f["matricula"],
                    f["email"],
                    f["total"],
                    f["realizadas"],
                    f["pendientes"],
                    f["porcentaje"],
                ]
            )

        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d0f0d0")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.whitesmoke, colors.lightgrey],
                    ),
                ]
            )
        )

        story.append(table)
        doc.build(story)

        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(
            pdf_value, content_type="application/pdf"
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_cumplimiento_usuarios.pdf"'
        )
        return response

    # =========================
    # 8) Render HTML (filtros + tabla)
    # =========================
    context = {
        "total_tareas": total_tareas,
        "realizadas": realizadas,
        "pendientes": pendientes,
        "cumplimiento_global": cumplimiento_global,
        "usuarios": filas,          # listado de mantenimiento con métricas
        "q": q,
        "f_ini": request.GET.get("f_ini", ""),
        "f_fin": request.GET.get("f_fin", ""),
        "chart1_labels": chart1_labels,
        "chart1_data": chart1_data,
        "chart2_labels": chart2_labels,
        "chart2_data": chart2_data,
    }
    return render(
        request,
        "reportes/reportes_tareas.html",
        context,
    )

# --------- 6) REPORTE DE ACTIVIDADES POR USUARIO ---------

@login_required
def reporte_actividades_usuario(request):
    usuario = request.user
    rol = _rol(usuario)

    # Solo Administrador y Gestor pueden consultar este reporte
    if rol not in ("administrador", "gestor"):
        return HttpResponseForbidden("No tiene permiso para ver este reporte.")

    User = get_user_model()

    # =========================
    # 1) Usuarios de mantenimiento disponibles para filtrar
    # =========================
    usuarios_mantenimiento = User.objects.filter(
        rol="mantenimiento", is_active=True
    ).order_by("nombre_completo")

    usuario_id = request.GET.get("usuario")  # id_usuario seleccionado
    tipo_accion = request.GET.get("tipo", "todas")  # todas / realizada / pendiente
    f_ini = parse_date(request.GET.get("f_ini")) if request.GET.get("f_ini") else None
    f_fin = parse_date(request.GET.get("f_fin")) if request.GET.get("f_fin") else None

    # =========================
    # 2) Query base: tareas con usuario_responsable de rol mantenimiento
    # =========================
    qs = TareaMantenimiento.objects.select_related("usuario_responsable").filter(
        usuario_responsable__rol="mantenimiento"
    )

    # Filtro por usuario específico (reporte por usuario)
    if usuario_id:
        qs = qs.filter(usuario_responsable__id_usuario=usuario_id)

    # Filtro por tipo de acción (estado)
    if tipo_accion == "realizada":
        qs = qs.filter(estado=TareaMantenimiento.ESTADO_REALIZADA)
    elif tipo_accion == "pendiente":
        qs = qs.filter(estado=TareaMantenimiento.ESTADO_PENDIENTE)

    # Filtro por rango de fechas (usamos fecha_programada como referencia)
    if f_ini:
        qs = qs.filter(fecha_programada__date__gte=f_ini)
    if f_fin:
        qs = qs.filter(fecha_programada__date__lte=f_fin)

    # =========================
    # 3) Armar las "actividades" (filas del reporte)
    # =========================
    filas = []
    for t in qs:
        u = t.usuario_responsable
        if not u:
            nombre_usuario = "Sin usuario"
            rol_usuario = "-"
            matricula = ""
            email = ""
        else:
            nombre_usuario = u.nombre_completo or u.matricula or u.email
            rol_usuario = u.get_rol_display() if hasattr(u, "get_rol_display") else u.rol
            matricula = u.matricula
            email = u.email

        # Tipo de acción según estado
        if t.estado == TareaMantenimiento.ESTADO_REALIZADA:
            tipo = "Tarea de mantenimiento - Realizada"
            fecha_hora = t.fecha_realizacion or t.fecha_programada
        else:
            tipo = "Tarea de mantenimiento - Pendiente"
            fecha_hora = t.fecha_programada

        detalle = f"{t.get_tipo_display()} en {t.planta.nombre_comun if t.planta else 'Sin especie'}"

        filas.append({
            "usuario": nombre_usuario,
            "rol": rol_usuario,
            "matricula": matricula,
            "email": email,
            "tipo_accion": tipo,
            "fecha_hora": fecha_hora,
            "detalle": detalle,
        })

    # =========================
    # 4) Estadísticas básicas
    # =========================
    total_acciones = len(filas)
    realizadas = qs.filter(estado=TareaMantenimiento.ESTADO_REALIZADA).count()
    pendientes = qs.filter(estado=TareaMantenimiento.ESTADO_PENDIENTE).count()
    cumplimiento = round(realizadas * 100 / total_acciones, 2) if total_acciones > 0 else 0.0

    # =========================
    # 5) Exportar a Excel
    # =========================
    if "excel" in request.GET:
        from openpyxl.drawing.image import Image as XLImage

        df = pd.DataFrame(filas)
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Actividades", index=False, startrow=6)
            workbook = writer.book
            sheet = writer.sheets["Actividades"]

            # Logo
            logo_path = finders.find("img/upemor-logo.png")
            if logo_path:
                logo = XLImage(logo_path)
                logo.width = 180
                logo.height = 90
                sheet.add_image(logo, "A1")

            # Encabezado
            sheet["A5"] = "Reporte de actividades de usuario"
            sheet["A5"].font = sheet["A5"].font.copy(bold=True, size=14)

            sheet["A6"] = (
                f"Total acciones: {total_acciones} | "
                f"Realizadas: {realizadas} | Pendientes: {pendientes} | "
                f"% cumplimiento (tareas realizadas): {cumplimiento}%"
            )
            sheet["A6"].font = sheet["A6"].font.copy(bold=True)

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_actividades_usuario.xlsx"'
        )
        return response

    # =========================
    # 6) Exportar a PDF
    # =========================
    if "pdf" in request.GET:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=36,
            leftMargin=36,
            rightMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        story = []

        # Logo
        logo_path = finders.find("img/upemor-logo.png")
        if logo_path:
            img = Image(logo_path, width=120, height=60)
            story.append(img)
            story.append(Spacer(1, 8))

        story.append(Paragraph("Reporte de actividades de usuario", styles["Title"]))
        story.append(
            Paragraph(
                f"Total acciones: {total_acciones} | "
                f"Realizadas: {realizadas} | Pendientes: {pendientes} | "
                f"% cumplimiento (tareas realizadas): {cumplimiento}%",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 10))

        # Tabla de actividades
        headers = [
            "Usuario",
            "Rol",
            "Tipo de acción",
            "Fecha y hora",
            "Detalle",
        ]
        data = [headers]
        for f in filas[:500]:
            data.append([
                f["usuario"],
                f["rol"],
                f["tipo_accion"],
                f["fecha_hora"].strftime("%Y-%m-%d %H:%M") if f["fecha_hora"] else "",
                f["detalle"],
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d0f0d0")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.whitesmoke, colors.lightgrey],
                    ),
                ]
            )
        )

        story.append(table)
        doc.build(story)

        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_value, content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="reporte_actividades_usuario.pdf"'
        )
        return response

    # =========================
    # 7) Render HTML (filtros + tabla)
    # =========================
    context = {
        "usuarios_mantenimiento": usuarios_mantenimiento,
        "usuario_id": usuario_id or "",
        "tipo_accion": tipo_accion,
        "f_ini": request.GET.get("f_ini", ""),
        "f_fin": request.GET.get("f_fin", ""),
        "total_acciones": total_acciones,
        "realizadas": realizadas,
        "pendientes": pendientes,
        "cumplimiento": cumplimiento,
        "actividades": filas,
    }
    return render(request, "reportes/reportes_actividades_usuario.html", context)
