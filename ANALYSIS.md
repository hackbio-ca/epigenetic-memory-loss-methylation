# Epigenetic Markers of Memory Loss
===================================

### Introduction
DNA methylation is an epigenetic modification involving the addition of methyl groups to the CG dinucleotide in the DNA sequnce, which can affect gene expression. These can be influenced by genetic and environmental factors, such as aging. Specific DNA methylation sites have beenlinked to various diseases, such as Alzheimer’s disease and cancer, making them promising epigenetic biomarkers for disease prediction.

### UMAP

UMAP is a method that can infer manifolds from hyperdimensional matrices. This allows the compression of the features while protecting their information relative to one another. Through UMAP, we can get cluster visuals based on the reduced features of the data examples. Color-coding the data based on the label allows researchers to assess if there's any meaningful relation between the input features (X) and the output label (y).

<img width="989" height="790" alt="output2" src="https://github.com/user-attachments/assets/48ac6c16-f14c-4435-9b4d-2e89c04dec31" />


As shown by our UMAP analysis, even though the noise can be seen by overlapping of data examples of different labels (shown by distinct colors), there's noticeable separation between two main clusters, where one of them visually appears to be "purer" than the smaller cluster, which has more data examples of Alzheimer's and Mild Cognitive Impairment. This indicates that the separation shows that the underlying methylation data has a distinguishable relation between a normal individual and that of any form of cognitive impairment.


### PCC

PCC is a method that visualizes the correlation between the data features. This is done by computing the correlation matrix of the dataset transposed. By clustering/shuffling/grouping the feature columns of high correlation, we can get a PCC plot that shows us the association between the feature groups and the output labels.

<img width="1288" height="990" alt="output3" src="https://github.com/user-attachments/assets/8765396a-0840-4463-9ed8-c1f322cfaa48" />


As seen in the plot above, there is 3 definite grids representing these feature clusters, we see that the color-coded labels (blue = control | alzheimers = red | mci = yellow) show separation and grouping based on feature clusters. This provides an evidence for a relation between the blood methylation data and cognitive diseases.

### Evaluation

You can find the classification network evaluation metrics below for reference. There's definitely room for improvement through researching model architectures, fine-tuning, and better analysis & pre-processing of the dataaset.

<img width="1920" height="1440" alt="roc_curve" src="https://github.com/user-attachments/assets/cf884476-21b0-4e82-9953-a08772454034" />

<img width="1920" height="1440" alt="confusion_matrix" src="https://github.com/user-attachments/assets/4e9e3d08-748c-42bf-ac4c-c79233c3d2e3" />


### Implications
Our findings suggest that blood-derived DNA methylation profiles could serve as a viable biomarker for Alzheimer's disease, offering a minimally invasive alternative to brain tissue based DNA methylation profiles. This has potential to advance biomarker discovery, and complement existing diagnostic pipelines such as neuroimaging. With larger datasets and refined feature selection, this framework could also extend to identifying intermediate states like mild cognitive impairment, contributing to a deeper understanding of disease progression and facilitating translational applications in clinical research.
