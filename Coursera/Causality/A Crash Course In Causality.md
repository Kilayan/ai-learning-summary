1. Propensity Score Matching in R 

* Background: 
  * right heart catheterization data, publicly available at https://biostat.mc.vanderbilt.edu/Main/DataSets, ICU patients in 5 hospitals
  * Treatment: right heart catheterization (rhc) vs. not
  * Outcome: death (yes/no)
  * Confounders: demographics, insurance, disease diagnoses, etc. 
  * 2184 treated and 3551 controls

![Screen Shot 2023-05-06 at 11.13.48 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.13.48 AM.png)

![Screen Shot 2023-05-06 at 11.14.44 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.14.44 AM.png)

![Screen Shot 2023-05-06 at 11.15.08 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.15.08 AM.png)

![Screen Shot 2023-05-06 at 11.15.24 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.15.24 AM.png)

![Screen Shot 2023-05-06 at 11.16.56 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.16.56 AM.png)

![Screen Shot 2023-05-06 at 11.17.11 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.17.11 AM.png)

![Screen Shot 2023-05-06 at 11.17.37 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.17.37 AM.png)

you can also put method = "optimal" -> which takes longer time to calculate. 

![Screen Shot 2023-05-06 at 11.18.42 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.18.42 AM.png)

![Screen Shot 2023-05-06 at 11.20.13 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.20.13 AM.png)

![Screen Shot 2023-05-06 at 11.20.59 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.20.59 AM.png)

![Screen Shot 2023-05-06 at 11.21.51 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.21.51 AM.png)

![Screen Shot 2023-05-06 at 11.23.18 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.23.18 AM.png)

![Screen Shot 2023-05-06 at 11.24.18 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.24.18 AM.png)

![Screen Shot 2023-05-06 at 11.24.59 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.24.59 AM.png)

![Screen Shot 2023-05-06 at 11.25.53 AM](/Users/fqinyan/Library/Application Support/typora-user-images/Screen Shot 2023-05-06 at 11.25.53 AM.png)

--------

2. 