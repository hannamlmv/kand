# Q-linea Test Panel Selection

Q-linea is a company that develops innovative solutions for improved infection diagnostics, focusing on developing instruments and consumables that can have positive effects for patients, healthcare providers, and society. Their leading product, ASTar®, is a fully automated instrument for testing antibiotic resistance, providing a sensitivity profile within six hours directly from a positive blood culture. This is significantly faster than current diagnostics, with new antibiotics and pathogens continuously being added to the platform.

Q-linea has lists of bacterial strains with information on their MIC values generated using a reference method. Some strains have many reference MIC values, while others only have a few. There is a script that creates a panel of strains from a list of strains, attempting to include as many on-scale (i.e., with an MIC value within the range ASTar measures) and as many resistant MIC values as possible. The purpose of this project is to facilitate the process of creating test panels by developing indicators that can be used to select strains to be included from each species, indicating the quality of the strain selection and enabling the user to make an informed choice of panel.

## Overview of repository

The scripts that have been developed for this project can be divided in to two main parts, isolate selection and visualisation

### Visualisation

The primary goal of the project was to develope indicators that represent spred, coverage and redundancy of a test panel. master_vis.py calls upon scripts in the Visualisation folder. 


### Isolate Selection

In order to test the indicators and see if they work in practice, a script was developed that uses the indicators to select isolates. 
