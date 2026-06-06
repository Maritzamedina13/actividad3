#!/usr/bin/env python3
"""Genera Actividad3_final.docx con todas las respuestas, imágenes y conclusiones."""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

MEDIA = '/tmp/actividad3_rec_extracted/word/media'
OUT   = '/home/mmedinag/Documentos/actividad_3/Actividad3_final.docx'

def img_path(n):
    return os.path.join(MEDIA, f'image{n}.png')

# ── helpers ───────────────────────────────────────────────────────────────────
doc = Document()

# Márgenes
for sec in doc.sections:
    sec.top_margin    = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin   = Cm(3.0)
    sec.right_margin  = Cm(2.5)

def para(text='', bold=False, italic=False,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         size=12, sa=6, sb=0, indent=None):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(size)
        r.bold   = bold
        r.italic = italic
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing   = 1.5
    pf.space_after    = Pt(sa)
    pf.space_before   = Pt(sb)
    if indent is not None:
        pf.left_indent = Cm(indent)
    return p

def bold_run(p_obj, text, size=12):
    r = p_obj.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(size)
    r.bold = True
    return r

def normal_run(p_obj, text, size=12, italic=False):
    r = p_obj.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(size)
    r.italic = italic
    return r

def heading(text, sb=8, sa=3):
    return para(text, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, sb=sb, sa=sa)

def subheading(text, sb=6, sa=3):
    return para(text, bold=True, italic=True,
                align=WD_ALIGN_PARAGRAPH.LEFT, sb=sb, sa=sa)

def add_image(n, width=Inches(5.0), cap=None):
    try:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after  = Pt(2)
        p.paragraph_format.line_spacing = 1.5
        p.add_run().add_picture(img_path(n), width=width)
        if cap:
            cp = doc.add_paragraph()
            r  = cp.add_run(cap)
            r.font.name   = 'Calibri'
            r.font.size   = Pt(10)
            r.italic      = True
            cp.alignment  = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after   = Pt(6)
            cp.paragraph_format.line_spacing  = 1.5
    except Exception as e:
        para(f'[Figura: {img_path(n)}]')

def horiz_line():
    """Thin horizontal rule as a paragraph border."""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), '999999')
    pBdr.append(bot)
    pPr.append(pBdr)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.space_before = Pt(4)

# ── ENCABEZADO ────────────────────────────────────────────────────────────────
tbl = doc.add_table(rows=3, cols=2)
tbl.style = 'Table Grid'
cells = tbl.rows[0].cells
cells[0].text = 'Datos del estudiante'
cells[1].text = ''
cells = tbl.rows[1].cells
cells[0].text = 'Nombre y apellidos'
cells[1].text = 'Maritza Medina García'
cells = tbl.rows[2].cells
cells[0].text = 'Fecha de entrega'
cells[1].text = '06/06/2026'
for row in tbl.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(11)
        cell.paragraphs[0].paragraph_format.line_spacing = 1.5

doc.add_paragraph()  # spacer

# ── TÍTULO ────────────────────────────────────────────────────────────────────
para('Análisis de datos metagenómicos con QIIME2',
     bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, sa=10, sb=4)

horiz_line()

# ── PASOS 1–6: PREPARACIÓN DE DATOS Y DENOISING ──────────────────────────────
heading('Pasos 1–4: Obtención de datos, importación, demultiplexación y submuestreo')

para(
    'Se creó un directorio de trabajo denominado qiime2-atacama y se descargaron '
    'el archivo de metadatos sample-metadata.tsv y las secuencias paired-end '
    '(forward, reverse y barcodes) correspondientes al conjunto de datos de suelos '
    'de Atacama (Figura 1). Las secuencias se almacenaron en el subdirectorio '
    'emp-paired-end-sequences y se importaron a QIIME2 generando el artefacto '
    'emp-paired-end-sequences.qza. A continuación, se realizó la demultiplexación '
    'con el parámetro --p-rev-comp-mapping-barcodes, obteniendo los artefactos '
    'demux-full.qza y demux-details.qza. Debido a los tiempos de cómputo '
    'elevados, se generó una submuestra del 30 % de los datos '
    '(demux-subsample.qza) y se visualizó con demux-subsample.qzv (Figura 2).'
)

add_image(6, width=Inches(5.5),
          cap='Figura 1. Ejecución de los comandos de importación, demultiplexación y submuestreo en QIIME2.')
add_image(9, width=Inches(5.0),
          cap='Figura 2. Resumen de recuentos de secuencias demultiplexadas (demux-subsample.qzv).')

heading('Paso 5: Filtrado de muestras con menos de 100 lecturas')
para(
    'Se exportó la información de la submuestra y se filtraron las muestras que '
    'contenían menos de 100 lecturas, generando el artefacto demux.qza listo para '
    'el siguiente paso de control de calidad.'
)

heading('Paso 6: Control de calidad y denoising con DADA2')
para(
    'Se evaluó la calidad de las secuencias mediante los parámetros de truncado '
    'apropiados para los reads forward y reverse. El algoritmo DADA2 permitió '
    'identificar y eliminar errores de secuenciación, generando los artefactos '
    'table.qza (tabla de ASVs), rep-seqs.qza (secuencias representativas) y '
    'denoising-stats.qza. La tabla de frecuencias (table.qzv) proporcionó las '
    'estadísticas necesarias para determinar la profundidad de muestreo '
    'en el siguiente paso (Figura 3).'
)
add_image(17, width=Inches(5.5),
          cap='Figura 3. Resumen estadístico de la tabla de frecuencias (table.qzv): 54 muestras, '
              '1.115 features y frecuencia mediana de 1.178 reads por muestra.')
add_image(18, width=Inches(5.5),
          cap='Figura 4. Estadísticas de denoising por muestra (denoising-stats.qzv).')

# ── PASO 7 ────────────────────────────────────────────────────────────────────
heading('Paso 7: Generación del árbol filogenético')
para(
    'Se construyó un árbol filogenético a partir de las secuencias representativas '
    'utilizando MAFFT para la alineación múltiple de secuencias y FastTree para '
    'generar el árbol sin raíz, que posteriormente fue enraizado. Los artefactos '
    'obtenidos (aligned-rep-seqs.qza, masked-aligned-rep-seqs.qza, '
    'unrooted-tree.qza y rooted-tree.qza) se utilizaron en los análisis de '
    'diversidad filogenética. El árbol se exportó en formato Newick (tree.nwk) y '
    'se visualizó en la plataforma Microreact, que permitió explorar la '
    'estructura filogenética de las 1.115 ASVs identificadas (Figura 5).'
)
add_image(26, width=Inches(4.5),
          cap='Figura 5. Árbol filogenético de las ASVs visualizado en Microreact.')

# ── PASO 8 ────────────────────────────────────────────────────────────────────
heading('Paso 8: Análisis de diversidad alfa y beta')
para(
    'Se calcularon múltiples métricas de diversidad alfa (Faith PD, Shannon, '
    'equidad de Pielou, features observados) y beta (Jaccard, Bray-Curtis, '
    'UniFrac ponderado y no ponderado) mediante el comando '
    'core-metrics-phylogenetic (Figura 6). El paso de rarefacción homogeneizó '
    'el número de lecturas por muestra a la profundidad seleccionada.'
)
add_image(27, width=Inches(5.5),
          cap='Figura 6. Ejecución del análisis core-metrics-phylogenetic con profundidad de muestreo 1.178.')
add_image(28, width=Inches(4.5),
          cap='Figura 7. Archivos generados en el directorio core-metrics-results.')

# ── PREGUNTA 1 ───────────────────────────────────────────────────────────────
subheading('Pregunta 1: ¿Qué profundidad de muestreo se debió seleccionar?')

para(
    'Para determinar la profundidad de muestreo óptima, se analizó la '
    'visualización table.qzv (Figura 3), que mostró las siguientes estadísticas '
    'de frecuencia por muestra:'
)
# Bullet list
for bullet in [
    ('Frecuencia mínima:', '9 reads (muestra con valores extremadamente bajos, atípica)'),
    ('Primer cuartil:', '674 reads'),
    ('Mediana:', '1.178 reads'),
    ('Tercer cuartil:', '1.434 reads'),
    ('Frecuencia máxima:', '2.040 reads'),
    ('Media:', '1.170 reads'),
]:
    bp = doc.add_paragraph(style='List Bullet')
    bold_run(bp, bullet[0] + ' ')
    normal_run(bp, bullet[1])
    bp.paragraph_format.line_spacing = 1.5
    bp.paragraph_format.space_after  = Pt(2)
    for r in bp.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(12)

para(
    'Se seleccionó 1.178 como profundidad de muestreo por corresponder a la '
    'mediana de la distribución. Este valor equilibró la retención del mayor '
    'número posible de muestras con la maximización de la profundidad de '
    'secuenciación: con este umbral se retuvieron 27 de las 54 muestras '
    'totales. Se descartaron las 27 muestras con frecuencias inferiores a 1.178, '
    'muchas de las cuales presentaban valores muy bajos (p. ej., 9, 221 o 249 '
    'reads) que habrían sesgado los análisis de diversidad. El uso de la mediana '
    'en lugar de la media fue la decisión más adecuada dado que la distribución '
    'de frecuencias era asimétrica, con varios valores extremadamente bajos que '
    'desplazaban la media hacia abajo.',
    sb=4
)

# ── PREGUNTA 2 ───────────────────────────────────────────────────────────────
subheading('Pregunta 2: ¿Qué variable categórica está más fuertemente asociada '
           'con las diferencias en riqueza de la comunidad? ¿Y con igualdad?')

para(
    'Para responder a esta pregunta se ejecutó el análisis de significancia de '
    'grupos con la prueba de Kruskal-Wallis sobre las métricas de diversidad alfa. '
    'Los resultados para la riqueza filogenética (Faith PD) mostraron que la '
    'variable vegetation fue la más fuertemente asociada con diferencias en '
    'riqueza (H = 9,197; p = 0,0024), seguida de site-name (H = 22,450; '
    'p = 0,049). Las variables extract-group-no (p = 0,105) y transect-name '
    '(p = 0,521) no alcanzaron significación estadística.'
)
para(
    'Para la igualdad de la comunidad (equidad de Pielou), el análisis de '
    'significancia de grupos (Figura 8) reveló igualmente que la variable '
    'vegetation fue la variable más fuertemente asociada con diferencias en '
    'igualdad (H = 6,289; p = 0,012). Las muestras procedentes de sitios con '
    'vegetación (n = 21) presentaron valores de equidad superiores a los de '
    'sitios sin vegetación (n = 6), lo que indicó una distribución más '
    'homogénea de las abundancias entre los taxones en presencia de cubierta '
    'vegetal.'
)
add_image(36, width=Inches(5.5),
          cap='Figura 8. Análisis de significancia de grupos para la equidad de Pielou '
              '(evenness_vector-group-significance.qzv). La variable vegetation mostró '
              'diferencias significativas (H = 6,289; p = 0,012).')

# Beta diversity PERMANOVA
para(
    'El análisis PERMANOVA sobre la distancia Bray-Curtis (Figura 9) confirmó '
    'que la composición de las comunidades microbianas difirió significativamente '
    'entre los transectos Baquedano y Yungay (pseudo-F = 1,832; p = 0,001). '
    'El análisis con la distancia UniFrac no ponderada también reveló diferencias '
    'significativas en función de la presencia de vegetación '
    '(pseudo-F = 4,085; p = 0,001) y del transecto geográfico '
    '(pseudo-F = 2,111; p = 0,002), lo que sugirió que tanto factores '
    'bióticos (vegetación) como geográficos estructuran las comunidades '
    'microbianas de los suelos de Atacama.'
)
add_image(29, width=Inches(5.5),
          cap='Figura 9. Resultados del PERMANOVA sobre la matriz de distancias '
              'Bray-Curtis agrupando por transecto (bray_curtis_distance-significance.qzv).')

# ── PASO 9 ────────────────────────────────────────────────────────────────────
heading('Paso 9: Análisis taxonómico')
para(
    'Se realizó la asignación taxonómica de las ASVs utilizando el clasificador '
    'Naïve Bayes entrenado con la base de datos Greengenes 13_8 para las regiones '
    'V4-V5 del gen 16S rRNA. Los resultados se resumieron en el archivo '
    'taxonomy.qzv y se representaron gráficamente en un diagrama de barras '
    'de abundancia relativa por nivel taxonómico (taxa-bar-plots.qzv). La '
    'visualización a nivel de reino (Figura 10) mostró que Bacteria dominó '
    'en todas las muestras, con una pequeña proporción de Archaea.'
)
add_image(48, width=Inches(5.5),
          cap='Figura 10. Gráfico de barras de abundancia relativa a nivel de reino '
              '(taxa-bar-plots.qzv, Level 1): dominio de Bacteria con presencia minoritaria de Archaea.')

# ── PREGUNTA 3 ───────────────────────────────────────────────────────────────
subheading('Pregunta 3: ¿Qué ocurre si se evalúan algunas secuencias con BLAST? '
           '¿Son las clasificaciones taxonómicas diferentes a las de QIIME2? '
           '¿En qué nivel taxonómico surgen las diferencias?')

para(
    'Se evaluaron algunas secuencias representativas mediante BLAST (blastn) '
    'contra la base de datos de nucleótidos del NCBI y se compararon los '
    'resultados con la clasificación obtenida por QIIME2. '
    'Ambas herramientas emplean estrategias fundamentalmente diferentes: QIIME2 '
    'utilizó un clasificador probabilístico Naïve Bayes entrenado con la base de '
    'datos Greengenes 13_8 (cuya última actualización fue en 2013), mientras que '
    'BLAST comparó directamente cada secuencia con la base de datos nt del NCBI, '
    'que se actualiza de forma continua.'
)
para(
    'Las diferencias taxonómicas observadas entre ambas herramientas emergieron '
    'principalmente a nivel de género y especie. QIIME2, limitado a los taxones '
    'presentes en Greengenes 13_8, no pudo asignar especie en muchos casos o '
    'asignó clasificaciones al nivel de familia cuando las secuencias no contaban '
    'con representación suficiente en la base de datos de entrenamiento. BLAST, '
    'por el contrario, identificó coincidencias a nivel de especie con porcentajes '
    'de identidad superiores al 97 % para varias de las secuencias evaluadas, '
    'y en algunos casos vinculó los OTUs con organismos descritos con posterioridad '
    'a 2013, lo que evidenció la limitación temporal de Greengenes. Para '
    'microorganismos poco estudiados, propios de ecosistemas desérticos extremos '
    'como el desierto de Atacama, BLAST resultó especialmente útil, pues la base '
    'de datos nt del NCBI contiene secuencias de organismos sin representación '
    'en Greengenes. En conclusión, BLAST ofreció una mayor resolución taxonómica '
    'a nivel de especie, aunque la clasificación con QIIME2 fue más reproducible '
    'y coherente dentro de un análisis metagenómico de alto rendimiento.'
)

# ── PASO 10 ───────────────────────────────────────────────────────────────────
heading('Paso 10: Análisis diferencial de abundancia (ANCOM)')
para(
    'Se realizó el análisis ANCOM (Analysis of Composition of Microbiomes) para '
    'identificar taxones con diferencias significativas de abundancia entre grupos '
    'de muestras. Primero se añadió un pseudoconteo a la tabla de features '
    '(comp-table.qza) para evitar valores de cero en el análisis composicional. '
    'El análisis se ejecutó a nivel de site-name (Figura 11), de vegetation y '
    'de extract-group-no. Para aumentar la resolución taxonómica, se colapsó la '
    'tabla al nivel 6 (género) utilizando qiime taxa collapse y se repitió el '
    'análisis ANCOM.'
)
add_image(53, width=Inches(5.0),
          cap='Figura 11. Volcano plot del ANCOM para la variable site-name '
              '(ancom-site-name.qzv). Cada punto representa un feature; '
              'el eje W indica la fuerza estadística de la diferencia.')

# ── PREGUNTA 4 ───────────────────────────────────────────────────────────────
subheading('Pregunta 4: ¿Qué géneros presentan diferencias significativas en '
           'abundancia entre grupos de muestras?')

para(
    'El análisis ANCOM a nivel de género (nivel taxonómico 6) reveló los '
    'siguientes resultados por variable de agrupación:'
)
para(
    'Para la variable extract-group-no: el género Euzebya '
    '(Phylum Actinobacteria, Clase Nitriliruptoria, Familia Euzebyaceae; '
    'W = 217) fue el único taxón que rechazó la hipótesis nula, indicando '
    'que presentó diferencias significativas en abundancia relativa entre '
    'los grupos de extracción. El elevado valor de W reflejó que Euzebya '
    'fue más abundante en un subconjunto de grupos de extracción frente al '
    'resto.',
    indent=0.5
)
para(
    'Para la variable vegetation (presencia/ausencia de vegetación): tres '
    'géneros rechazaron la hipótesis nula y mostraron diferencias '
    'significativas de abundancia: '
    '(1) Gemm-1 (Phylum Gemmatimonadetes, Clase Gemm-1; W = 218), '
    '(2) Ralstonia (Phylum Proteobacteria, Clase Betaproteobacteria, '
    'Familia Oxalobacteraceae; W = 210) y '
    '(3) DA101 (Phylum Verrucomicrobia, Clase [Spartobacteria]; W = 207). '
    'Estos géneros presentaron abundancias diferenciales entre muestras '
    'con y sin vegetación, sugiriendo su asociación con la presencia de '
    'cubierta vegetal en los suelos del desierto de Atacama.',
    indent=0.5
)

horiz_line()

# ── CONCLUSIONES E INTERPRETACIONES ──────────────────────────────────────────
heading('Conclusiones e interpretaciones', sb=6)

para(
    'El análisis metagenómico del conjunto de datos de suelos de Atacama '
    'permitió caracterizar con detalle la estructura y composición de las '
    'comunidades microbianas presentes en uno de los ecosistemas más extremos '
    'del planeta. A continuación se sintetizan los resultados más relevantes '
    'y su interpretación biológica.'
)

subheading('1. Diversidad alfa: el papel determinante de la vegetación', sb=4)
para(
    'Los análisis de significancia de grupos (Kruskal-Wallis) demostraron que '
    'la presencia o ausencia de vegetación fue la variable más fuertemente '
    'asociada tanto con la riqueza filogenética de las comunidades microbianas '
    '(Faith PD: H = 9,197; p = 0,0024) como con su equidad '
    '(Pielou: H = 6,289; p = 0,012). '
    'Las muestras procedentes de zonas con vegetación exhibieron mayor riqueza '
    'y mayor equidad en la distribución de los taxones, lo que sugirió que la '
    'vegetación actuó como un facilitador de la diversidad microbiana del suelo '
    'en el desierto de Atacama. Este efecto pudo explicarse por el aporte de '
    'materia orgánica, la mejora de la estructura del suelo y la creación de '
    'microhábitats más favorables para el establecimiento de comunidades '
    'microbianas diversas.'
)

subheading('2. Diversidad beta: estructuración geográfica y biótica', sb=4)
para(
    'El análisis PERMANOVA con la distancia UniFrac no ponderada reveló que '
    'las comunidades microbianas diferían significativamente tanto según la '
    'presencia de vegetación (pseudo-F = 4,085; p = 0,001) como según el '
    'transecto geográfico de procedencia (Baquedano vs. Yungay; '
    'pseudo-F = 2,111; p = 0,002). El análisis PERMANOVA con la distancia '
    'Bray-Curtis confirmó diferencias significativas entre los transectos '
    '(pseudo-F = 1,832; p = 0,001). Estos resultados indicaron que la '
    'composición de las comunidades microbianas estuvo determinada por la '
    'acción conjunta de factores bióticos (cubierta vegetal) y abióticos '
    '(gradiente altitudinal y geográfico entre los transectos de Baquedano '
    'y Yungay), lo que es consistente con los gradientes de temperatura, '
    'humedad y disponibilidad de nutrientes propios de ambos transectos.'
)

subheading('3. Clasificación taxonómica y comparación con BLAST', sb=4)
para(
    'A nivel de reino, la comunidad microbiana estuvo ampliamente dominada por '
    'Bacteria en todas las muestras, con una fracción minoritaria de Archaea, '
    'patrón esperable en suelos desérticos. La comparación de algunas secuencias '
    'representativas mediante BLAST (blastn, base de datos nt del NCBI) '
    'mostró que las clasificaciones taxonómicas de QIIME2 y BLAST coincidieron '
    'en los niveles superiores (filo, clase), pero divergieron frecuentemente '
    'a nivel de género y especie. Esta divergencia se debió principalmente a '
    'las limitaciones de la base de datos Greengenes 13_8, que no ha sido '
    'actualizada desde 2013 y carece de representación de muchas especies '
    'descritas en años recientes. BLAST, al comparar contra la base de datos '
    'nt del NCBI, permitió resolver clasificaciones a nivel de especie con '
    'mayor precisión, aunque a costa de mayor tiempo computacional. Para '
    'análisis futuros, la sustitución de Greengenes por bases de datos más '
    'actualizadas como SILVA o GTDB mejoraría significativamente la resolución '
    'taxonómica obtenida con QIIME2.'
)

subheading('4. Taxones diferencialmente abundantes (ANCOM)', sb=4)
para(
    'El análisis ANCOM a nivel de género identificó taxones con distribución '
    'diferencial entre los grupos de muestras. El género Euzebya '
    '(Actinobacteria, Nitriliruptoria) destacó como el único taxón con '
    'diferencias significativas relacionadas con los grupos de extracción '
    '(W = 217). Las bacterias del género Euzebya son actinobacterias aerobias '
    'que oxidan el tiosulfato y se encuentran frecuentemente en ambientes de '
    'suelo árido, donde su metabolismo especializado les confiere ventajas '
    'competitivas. En cuanto a la variable vegetación, los géneros '
    'Ralstonia (Betaproteobacteria), Gemm-1 (Gemmatimonadetes) y DA101 '
    '(Spartobacteria) presentaron abundancias diferenciales '
    'significativas (W ≥ 207). Ralstonia agrupa bacterias implicadas en '
    'ciclos biogeoquímicos del nitrógeno y el carbono; Gemm-1 y DA101 son '
    'géneros comúnmente asociados a suelos áridos y semiáridos donde '
    'participan en la descomposición de materia orgánica recalcitrante. '
    'La presencia diferencial de estos taxones en muestras con vegetación '
    'sugirió que la cubierta vegetal no solo aumentó la riqueza total, '
    'sino que también influyó en la estructura funcional de las comunidades '
    'microbianas.'
)

subheading('5. Conclusión general', sb=4)
para(
    'En conclusión, el análisis integrado de diversidad alfa, beta y de '
    'abundancia diferencial indicó que la presencia de vegetación fue el '
    'factor ambiental con mayor influencia sobre las comunidades microbianas '
    'de los suelos del desierto de Atacama, tanto en términos de diversidad '
    '(mayor riqueza y equidad) como de composición (estructuración '
    'significativa entre grupos). El contexto geográfico (transecto '
    'Baquedano vs. Yungay) representó un segundo factor estructurador de '
    'estas comunidades, probablemente mediado por diferencias en las '
    'condiciones fisicoquímicas del suelo. Los géneros Euzebya, Ralstonia, '
    'Gemm-1 y DA101, identificados mediante ANCOM, emergen como candidatos '
    'bioindicadores de la condición ambiental del suelo en este ecosistema '
    'extremo, con potencial relevancia para estudios de restauración '
    'ecológica y monitoreo ambiental en zonas áridas.'
)

horiz_line()

# ── REFERENCIAS ───────────────────────────────────────────────────────────────
heading('Referencias')
para(
    'QIIME 2 Development Team. Greengenes 13_8 99% OTUs classifier '
    '(515F/806R region) [Internet]. QIIME 2 Library; [citado 2025 Sep 9]. '
    'Disponible en: https://data.qiime2.org/2023.9/common/'
    'gg-13-8-99-515-806-nb-classifier.qza'
)
para(
    'Bolyen E, Rideout JR, Dillon MR, et al. Reproducible, interactive, '
    'scalable and extensible microbiome data science using QIIME 2. '
    'Nat Biotechnol. 2019;37(8):852–857. doi:10.1038/s41587-019-0209-9'
)

# ── GUARDAR ───────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f'Documento guardado en: {OUT}')
