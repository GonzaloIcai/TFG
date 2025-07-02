from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime

analysis_simulados = Blueprint('analysis_simulados', __name__)

@analysis_simulados.route('/informe_simulado/<caso>')
@login_required
def informe_simulado(caso):
    informes = {
        "mejora": """
<h4>Informe de Evolución Cognitiva – Del 2025-05-01 al 2025-05-31</h4>
<p>Durante el mes de mayo, el usuario ha participado regularmente en ejercicios de memoria, atención y razonamiento. A continuación se detalla el análisis de los resultados obtenidos en cada área, junto con una valoración general y una serie de recomendaciones para continuar con el desarrollo cognitivo de forma efectiva y personalizada.</p>

<p class="titulo-seccion">Memoria:</p>
<p>Se observa una mejora progresiva en la capacidad de retención y en la agilidad mental asociada a tareas de memoria. A medida que avanzan los días del mes, los errores disminuyen y los tiempos de ejecución se vuelven más eficientes. Esta tendencia sugiere una consolidación del aprendizaje y una mayor familiarización con los estímulos presentados. La constancia en la práctica ha sido un factor clave en este progreso.</p>

<p class="titulo-seccion">Atención:</p>
<p>El rendimiento en los ejercicios de atención muestra una evolución muy positiva. El número de errores ha disminuido de forma sostenida, lo que indica una mejora en la capacidad de concentración, el enfoque sostenido y la reducción de distracciones. También se aprecia una estabilización en los tiempos de respuesta, lo que refleja un mejor control cognitivo durante la ejecución de tareas que exigen vigilancia activa y discriminación visual.</p>

<p class="titulo-seccion">Razonamiento:</p>
<p>La capacidad de razonamiento ha experimentado también un desarrollo notable. A lo largo del mes, el usuario ha ido cometiendo menos errores en las pruebas lógicas y ha mantenido un ritmo constante en la resolución de problemas. Esto sugiere una mejora tanto en la toma de decisiones como en el procesamiento lógico, elementos clave en el mantenimiento de funciones ejecutivas eficientes.</p>

<p class="titulo-seccion">Conclusión General:</p>
<p>El desempeño global del usuario durante el mes de mayo ha sido muy positivo. Se evidencia una mejora clara y sostenida en las tres áreas evaluadas, lo que refleja tanto un compromiso con la práctica como una buena respuesta al tipo de estimulación cognitiva aplicada. El progreso observado confirma que la plataforma está cumpliendo su objetivo de reforzar y mantener las capacidades mentales activas de forma eficaz.</p>

<p class="titulo-seccion">Recomendaciones Personalizadas:</p>
<ul>
<li>Mantener la práctica diaria con los ejercicios actuales, idealmente completando las tres categorías en la rutina diaria.</li>
<li>Considerar aumentar ligeramente la dificultad o la variedad de los ejercicios en el siguiente mes para seguir promoviendo la plasticidad cognitiva.</li>
<li>Combinar el entrenamiento digital con actividades cotidianas que fomenten el pensamiento activo, como juegos de mesa, lectura, escritura o conversación.</li>
<li>Asegurar una correcta higiene del sueño, una alimentación equilibrada y pausas adecuadas durante las sesiones para potenciar el rendimiento.</li>
<li>En caso de detectar una pérdida de motivación o estancamiento, se recomienda consultar con un profesional para valorar ajustes personalizados.</li>
</ul>
""",

        "empeora": """
<h4>Informe de Evolución Cognitiva – Del 2025-05-01 al 2025-05-31</h4>
<p>Durante el mes de mayo, el usuario ha estado realizando ejercicios cognitivos de forma constante, abarcando las áreas de memoria, atención y razonamiento. Sin embargo, en este periodo se ha observado una tendencia general negativa en el rendimiento, especialmente a partir de la segunda semana. A continuación, se detallan los resultados por área y se incluyen recomendaciones específicas.</p>

<p class="titulo-seccion">Memoria:</p>
<p>Se observa un aumento progresivo en la cantidad de intentos necesarios y en el tiempo empleado para completar los ejercicios. A medida que avanza el mes, los errores son más frecuentes y los tiempos más prolongados, lo que puede indicar dificultades para retener y recordar la información. La tendencia es clara y persistente, y sugiere la necesidad de reforzar esta área con ejercicios de menor dificultad y mayor frecuencia.</p>

<p class="titulo-seccion">Atención:</p>
<p>En los ejercicios de atención también se percibe un empeoramiento gradual. El número de errores aumenta semana tras semana, y los tiempos de respuesta se vuelven más variables y prolongados. Hay días donde el rendimiento se ve especialmente afectado, lo cual podría deberse a fatiga, falta de concentración o falta de motivación. Se recomienda reducir la carga cognitiva y favorecer descansos breves entre rondas de atención.</p>

<p class="titulo-seccion">Razonamiento:</p>
<p>El área de razonamiento muestra una tendencia descendente, aunque algo más estable. Aumentan las respuestas incorrectas y se detecta cierta pérdida de consistencia en la ejecución. Aunque el número de errores es menor que en las otras áreas, el patrón sugiere una leve pérdida de agilidad mental y de capacidad lógica que convendría trabajar con ejercicios más guiados o apoyos visuales.</p>

<p class="titulo-seccion">Conclusión General:</p>
<p>El usuario presenta un descenso significativo en las tres áreas cognitivas analizadas. Aunque ha mantenido la constancia en la realización de los ejercicios, los resultados indican que el nivel de dificultad actual podría no ser el adecuado, o que existen factores externos (estrés, fatiga, falta de sueño) que afectan negativamente su desempeño. Es importante tomar medidas para evitar una desmotivación futura y reconducir esta tendencia.</p>

<p class="titulo-seccion">Recomendaciones Personalizadas:</p>
<ul>
<li>Disminuir la dificultad de los ejercicios actuales y centrarse en reforzar los básicos.</li>
<li>Realizar sesiones más cortas pero más frecuentes para mantener el hábito sin generar frustración.</li>
<li>Incluir ejercicios complementarios de relajación y atención plena (mindfulness) antes de iniciar la rutina.</li>
<li>Consultar a un especialista si se mantiene esta tendencia negativa en los próximos meses.</li>
</ul>
""",

        "empeora_atencion": """
<h4>Informe de Evolución Cognitiva – Del 2025-05-01 al 2025-05-31</h4>
<p>Durante el mes de mayo, el usuario ha mantenido su rutina cognitiva habitual, realizando ejercicios en las áreas de memoria, atención y razonamiento. Si bien dos de estas áreas presentan resultados estables, se ha detectado un deterioro progresivo en la atención.</p>

<p class="titulo-seccion">Memoria:</p>
<p>El rendimiento en memoria ha sido constante y aceptable. La cantidad de intentos y los tiempos de respuesta se mantienen dentro de un rango regular. No se aprecian signos de deterioro, lo que sugiere una buena consolidación de esta capacidad.</p>

<p class="titulo-seccion">Atención:</p>
<p>Esta es el área con mayor deterioro durante el mes. El número de errores ha aumentado de forma constante, y los tiempos de respuesta muestran una creciente variabilidad. Esto puede deberse a fatiga acumulada, distracciones frecuentes o una sobreexposición a tareas exigentes sin pausas adecuadas. El patrón observado requiere atención inmediata para evitar que esta disminución afecte a otras capacidades cognitivas.</p>

<p class="titulo-seccion">Razonamiento:</p>
<p>El área de razonamiento se mantiene estable, con un número reducido de errores y tiempos de respuesta adecuados. El usuario ha demostrado conservar su capacidad lógica y de resolución de problemas a lo largo del mes sin fluctuaciones significativas.</p>

<p class="titulo-seccion">Conclusión General:</p>
<p>El usuario presenta un rendimiento desigual entre las distintas áreas cognitivas. La memoria y el razonamiento se mantienen estables, pero la atención ha sufrido un claro empeoramiento durante el mes. Este desequilibrio sugiere la necesidad de adaptar la rutina para proteger el desempeño global y prevenir un impacto mayor en el resto de funciones.</p>

<p class="titulo-seccion">Recomendaciones Personalizadas:</p>
<ul>
<li>Incluir ejercicios más breves y dinámicos de atención para evitar la fatiga.</li>
<li>Establecer un entorno libre de distracciones al realizar las sesiones.</li>
<li>Probar diferentes horarios del día para identificar cuándo existe mayor claridad mental.</li>
<li>Combinar las sesiones con pausas activas o ejercicios físicos suaves para facilitar la recuperación cognitiva.</li>
</ul>
"""
    }

    informe_html = informes.get(caso, "<p>No se encontró el caso solicitado.</p>")
    desde = datetime(2025, 5, 1, 0, 0)
    hasta = datetime(2025, 5, 31, 23, 59)

    return render_template("informe.html", informe=informe_html, desde=desde, hasta=hasta)
