# Getting started with dataset analysis
Welcome to the dataset catalog, where you can find various datasets, including quality reports.

## Structure of dataset
Datasets are organized in a two-level structure. The first level contains only the Dataset Name, and the Dataset Version is empty. This level represents original and publicly available datasets, and the analysis is mainly based on public data (Google Scholar and related papers). The second level dataset shares the same Dataset Name and contains the Dataset Version name (it is mandatory to have a unique combination of Dataset Name and Dataset Version to avoid collisions). This level represents a subset or modified subset of the original dataset, which is usually used as a feature dataset for direct ML applications. Usually, the analysis is based on evaluation using dataset analysis tools (metric and drifts).

## How to submit dataset analysis request
Use the Submit Dataset button and provide as many details as possible. Our data analysts will process the dataset and generate the final report with support metadata. You can track the progress with the Analysis Status field. 

## How to run dataset analysis
In dataset-catalog.liberouter.org we have data analysts who run the dataset evaluation and validate results. If needed you can download all necessary files and run your own evaluation. Documentation of used workflow and tools can be found [here](https://gitlab.liberouter.org/monitoring/katoda-tools)

## How to provide feedback
If you have any questions or feedback, you can reach out to soukudom@fit.cvut.cz. If you have comments for a specific dataset, you can use the Discussion section inside the dataset report. 
