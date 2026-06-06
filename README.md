# Actividad 3 — Análisis de datos metagenómicos con QIIME2

Análisis metagenómico del conjunto de datos de suelos del desierto de Atacama
usando QIIME2 (versión amplicon-2023.9).

## Estructura del repositorio

```
actividad_3_github/
├── README.md
├── sample-metadata.tsv          # Metadatos de las 75 muestras originales
├── Actividad3_final.docx        # Informe final con respuestas y conclusiones
├── build_actividad3.py          # Script que genera el informe .docx
├── run_remaining.sh             # Script de análisis QIIME2 (pasos 8–10)
└── resultados/
    ├── table.qza / table.qzv           # Tabla de ASVs post-DADA2
    ├── rep-seqs.qza / rep-seqs.qzv     # Secuencias representativas
    ├── denoising-stats.qza / .qzv      # Estadísticas DADA2
    ├── aligned-rep-seqs.qza            # Alineamiento MAFFT
    ├── masked-aligned-rep-seqs.qza     # Alineamiento enmascarado
    ├── unrooted-tree.qza               # Árbol sin raíz (FastTree)
    ├── rooted-tree.qza                 # Árbol enraizado
    ├── Visualizacion/tree.nwk          # Árbol en formato Newick
    ├── taxonomy.qza / taxonomy.qzv     # Clasificación taxonómica (Greengenes 13_8)
    ├── taxa-bar-plots.qzv              # Gráfico de abundancia taxonómica
    ├── comp-table.qza                  # Tabla con pseudoconteo (ANCOM)
    ├── table-l3.qza / comp-table-l3.qza / l3-ancom-site-name.qzv   # ANCOM nivel 3 (clase)
    ├── table-l6.qza / comp-table-l6.qza                            # ANCOM nivel 6 (género)
    ├── ancom-site-name.qzv             # ANCOM por site-name
    ├── ancom-extract-group-no.qzv      # ANCOM por grupo de extracción
    ├── ancom-extract-group-no-l6-example.qzv  # ANCOM L6 ejemplo
    ├── demux-subsample.qzv             # Resumen de submuestreo (30%)
    ├── core-metrics-results/
    │   ├── Alfa-diversity/             # faith-pd, evenness, shannon, observed_features (significancia)
    │   ├── Beta-diversity/             # PERMANOVA y Emperor PCoA por variable
    │   ├── evenness_vector-group-significance.qzv
    │   ├── bray_curtis_distance-significance.qzv
    │   ├── *_emperor.qzv               # Gráficos PCoA interactivos
    │   ├── rarefied_table.qza
    │   └── evenness_vector.qza / faith_pd_vector.qza / ...
    └── AMCO/
        ├── ancom-extract-group-no.qzv  # ANCOM nivel feature
        ├── ancom-vegetation.qzv
        ├── ancom-transect-name.qzv
        ├── l6-ancom-extract-group-no.qzv  # ANCOM nivel 6 (género)
        ├── l6-ancom-vegetation.qzv
        └── l6-ancom-transect-name.qzv
```

## Archivos excluidos (demasiado grandes para GitHub)

| Archivo | Tamaño | Motivo |
|---|---|---|
| emp-paired-end-sequences.qza | 310 MB | Secuencias crudas (descargables desde QIIME2 tutorials) |
| emp-paired-end-sequences/ | 310 MB | FASTQ crudos |
| demux-full.qza | 92 MB | Demultiplexado completo (75 muestras) |
| demux-subsample.qza | 28 MB | Submuestra 30% |
| demux.qza | 28 MB | Submuestra filtrada (>100 reads) |
| gg-13-8-99-515-806-nb-classifier.qza | ~900 MB | Clasificador descargable desde QIIME2 |

## Resultados clave

| Métrica | Resultado |
|---|---|
| Profundidad de muestreo | 1.178 reads (mediana; 27/54 muestras retenidas) |
| Variable más asociada a riqueza (Faith PD) | vegetation (H=9,197; p=0,0024) |
| Variable más asociada a igualdad (Pielou) | vegetation (H=6,289; p=0,012) |
| PERMANOVA vegetation (UniFrac no pond.) | pseudo-F=4,085; p=0,001 |
| PERMANOVA transecto (UniFrac no pond.) | pseudo-F=2,111; p=0,002 |
| Género significativo ANCOM (extract-group-no, L6) | *Euzebya* (Actinobacteria; W=217) |
| Géneros significativos ANCOM (vegetation, L6) | *Gemm-1* (W=218), *Ralstonia* (W=210), *DA101* (W=207) |

## Requisitos

```bash
conda activate qiime2-amplicon-2023.9
pip install python-docx   # para regenerar el informe
```

## Referencia de datos

Metcalf JL et al. (2016). Microbial community assembly and metabolic function
during mammalian corpse decomposition. *Science*, 351(6269), 158–162.

Tutorial oficial: https://docs.qiime2.org/2023.9/tutorials/atacama-soil-microbiome/
