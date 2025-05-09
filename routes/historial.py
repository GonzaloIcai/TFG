from flask import Blueprint, render_template, request, send_file, make_response
from flask_login import login_required, current_user
from models.database import db, Informe
import io
import pdfkit

historial = Blueprint('historial', __name__)

@historial.route('/historial')
@login_required
def ver_historial():
    informes = Informe.query.filter_by(user_id=current_user.id).order_by(Informe.fecha.desc()).all()
    return render_template('historial.html', informes=informes)

@historial.route('/descargar_informe/<int:informe_id>')
@login_required
def descargar_informe(informe_id):
    informe = Informe.query.get_or_404(informe_id)

    # Renderiza el HTML del informe usando tu plantilla existente
    rendered = render_template(
        'informe.html',
        informe=informe.contenido,
        desde=informe.fecha,
        hasta=informe.fecha
    )

    # Configura wkhtmltopdf con ruta absoluta (ajusta si la tuya es distinta)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Genera PDF en memoria
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    # Devuelve el PDF como descarga al navegador
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        download_name=f'informe_{informe.fecha.strftime("%Y-%m-%d")}.pdf'
    )
