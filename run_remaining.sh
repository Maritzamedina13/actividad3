#!/bin/bash
set -e
cd /home/mmedinag/Documentos/actividad_3/archivos

source /home/mmedinag/yes/etc/profile.d/conda.sh
conda activate qiime2-amplicon-2023.9

echo "=== PASO 8 CONT.: Alpha diversity group significance ==="

mkdir -p core-metrics-results/Alfa-diversity

qiime diversity alpha-group-significance \
  --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization core-metrics-results/Alfa-diversity/faith-pd-group-significance.qzv

qiime diversity alpha-group-significance \
  --i-alpha-diversity core-metrics-results/shannon_vector.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization core-metrics-results/Alfa-diversity/shannon-group-significance.qzv

qiime diversity alpha-group-significance \
  --i-alpha-diversity core-metrics-results/observed_features_vector.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization core-metrics-results/Alfa-diversity/observed_features-group-significance.qzv

qiime diversity alpha-group-significance \
  --i-alpha-diversity core-metrics-results/evenness_vector.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization core-metrics-results/Alfa-diversity/evenness-group-significance.qzv

echo "=== PASO 8 CONT.: Beta diversity PERMANOVA ==="

mkdir -p core-metrics-results/Beta-diversity

for col in transect-name vegetation extract-group-no; do
  qiime diversity beta-group-significance \
    --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization core-metrics-results/Beta-diversity/unweighted-unifrac-${col}-significance.qzv \
    --p-pairwise
done

for col in transect-name vegetation extract-group-no; do
  qiime diversity beta-group-significance \
    --i-distance-matrix core-metrics-results/weighted_unifrac_distance_matrix.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization core-metrics-results/Beta-diversity/weighted-unifrac-${col}-significance.qzv \
    --p-pairwise
done

for col in transect-name vegetation extract-group-no; do
  qiime diversity beta-group-significance \
    --i-distance-matrix core-metrics-results/bray_curtis_distance_matrix.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization core-metrics-results/Beta-diversity/bray_curtis-${col}-significance.qzv \
    --p-pairwise
done

for col in transect-name vegetation extract-group-no; do
  qiime diversity beta-group-significance \
    --i-distance-matrix core-metrics-results/jaccard_distance_matrix.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization core-metrics-results/Beta-diversity/jaccard-${col}-significance.qzv \
    --p-pairwise
done

echo "=== PASO 8 CONT.: Emperor PCoA plots ==="

for col in depth elevation ph; do
  qiime emperor plot \
    --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza \
    --m-metadata-file sample-metadata.tsv \
    --p-custom-axes $col \
    --o-visualization core-metrics-results/Beta-diversity/unweighted-unifrac-emperor-${col}.qzv
done

qiime emperor plot \
  --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza \
  --m-metadata-file sample-metadata.tsv \
  --p-custom-axes depth \
  --o-visualization core-metrics-results/unweighted-unifrac-emperor-depth.qzv

echo "=== PASO 9: Taxonomía ==="

qiime feature-classifier classify-sklearn \
  --i-classifier /home/mmedinag/Documentos/actividad_3/Actividad3_ficheros/Actividad2/gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza

qiime metadata tabulate \
  --m-input-file taxonomy.qza \
  --o-visualization taxonomy.qzv

qiime taxa barplot \
  --i-table table.qza \
  --i-taxonomy taxonomy.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization taxa-bar-plots.qzv

echo "=== PASO 10: ANCOM ==="

mkdir -p AMCO

qiime composition add-pseudocount \
  --i-table table.qza \
  --o-composition-table comp-table.qza

for col in transect-name vegetation extract-group-no; do
  qiime composition ancom \
    --i-table comp-table.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization AMCO/ancom-${col}.qzv
done

qiime taxa collapse \
  --i-table table.qza \
  --i-taxonomy taxonomy.qza \
  --p-level 6 \
  --o-collapsed-table table-l6.qza

qiime composition add-pseudocount \
  --i-table table-l6.qza \
  --o-composition-table comp-table-l6.qza

for col in transect-name vegetation extract-group-no; do
  qiime composition ancom \
    --i-table comp-table-l6.qza \
    --m-metadata-file sample-metadata.tsv \
    --m-metadata-column $col \
    --o-visualization AMCO/l6-ancom-${col}.qzv
done

echo "=== TODOS LOS PASOS COMPLETADOS ==="
