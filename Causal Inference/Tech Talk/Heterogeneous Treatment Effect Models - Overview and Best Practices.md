Cross-sectional Data vs Panel Data

Causal Tree and Generalized Random Forest 

Double Robust 

# MLU Tech Talk

## Heterogeneous Treatment Effect Models

Description:While we are often interested in aggregated impacts from experiments, estimates of the average impact can mask customer or unit-level variation. This variation can drive targeted policies and programs. Understanding variation in impacts such as how different customers respond to improved delivery options, product selection, or marketing materials can point to how Amazon leaders to better serve and delight customers. Heterogeneous Treatment Effect (HTE) models allow scientists to identify and estimate segment or individualized treatment effects from randomized experiment or observational datasets. Various applications of HTE across Amazon will be mentioned, and audience members will leave with an overview of popular HTE models such as generalized random forests and heterogeneous DML, and guidance on how to use HTE models with causal models.



### Mini-exeriments in your non-experimental data

* unconfoundedness assumption - we can not validate because we do not have ground truth. There could be an unobserved feature that explains differences between treatment and control units. 
* Overlap/common support: for every control unit, there is a sufficiently similar treatment. 

#### HTE Modeling and Notation

![Screen Shot 2023-07-19 at 10.12.54 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-07-19 at 10.12.54 AM.png)