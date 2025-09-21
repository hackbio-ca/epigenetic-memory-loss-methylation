# epigenetic-memory-loss-methylation

Epigenetic Markers of Memory Loss: Using DNA Methylation Profiles to Predict Cognitive Impairment and Dementia

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

Epigenetics involves the changes in gene expression without altering the DNA sequence and can be passed down through generations. It is regulated by chemical modifications which alter the DNA molecule to inhibit or express a gene. One such mechanism is called DNA methylation which adds a methyl group to the CpG dinucleotide of the DNA molecule. Both environmental factors and genetics can shape DNA methylation patterns and whether or not a gene is expressed. Alzheimer’s disease, a neurodegenerative condition affected by both genetic factors and environment, may therefore be studied through these epigenetic signatures. By analyzing DNA methylation profiles, we aim to monitor cognitive decline, identify disease-associated genes and CpG sites, and predict Alzheimer’s risk using machine learning. In this project, DNA methylation profiles extracted from blood samples of individuals with Alzheimer’s disease, those experiencing cognitive impairment, and healthy controls will be used to create a dataset for training the machine learning model. This model will predict the likelihood of Alzheimer’s as well as monitor cognitive decline based on methylation patterns. Furthermore, by analyzing feature importance scores from the trained model, we can identify the specific methylation sites and genes most strongly associated with Alzheimer’s, offering valuable insights into disease mechanisms, potential biomarkers, and cognitive impairment.

## Installation

Provide instructions on how to install and set up the project, such as installing dependencies and preparing the environment.

```bash
# Example command to install dependencies (Python)
pip install project-dependencies

# Example command to install dependencies (R)
install.packages("project-dependencies")
```

## Quick Start

Provide a basic usage example or minimal code snippet that demonstrates how to use the project.

```python
# Example usage (Python)
import my_project

demo = my_project.example_function()
print(demo)
```
```r
# Example usage (R)
library(my_project)

demo <- example_function()
print(demo)
```

## Usage

Add detailed information and examples on how to use the project, covering its major features and functions.

```python
# More usage examples (Python)
import my_project

demo = my_project.advanced_function(parameter1='value1')
print(demo)
```
```r
# More usage examples (R)
library(demoProject)

demo <- advanced_function(parameter1 = "value1")
print(demo)
```

## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/demo-project/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).

==========

## Setup

From the project directory, first set up the virtual environment by running:

```
python -m venv venv
pip3 install -r requirements.txt
```

After, make sure that your front-end is set up. To do so simply run,

```
cd frontend
npm install
```

You can simply run the front-end via `npm run dev`. Make sure to user port 3000 as CORS middleware in backend is allowed only for that port in dev mode.

As for the model training, you can call the files in the fashion of `python -m model.data.loaders.loader_xgboost`, or `python -m model._dir1_._dir2_.target_file` in a more general format.
