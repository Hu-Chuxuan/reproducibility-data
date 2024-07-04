label_specs_prompt = """
You are given two pictures. The first picture shows reproduced results, while the second picture presents the original results. 

Your first task is to decide the type of replication specifications in the reproduced results. Your decision should be based on the footnotes and the names in the reproduced results. In this step, you should focus on the reproduced results. By "reproduced results", we mean that the results of sub-experiments in the original paper with the same specification or only correcting errors in the original paper.

    1. You should determine the level of replication specifications in the reproduced results based on your summry above and the namings. 
        (1) You MUST know that the naming of something is only about itself instead of some sub-parts of it. For example, the title of a table describes the entire table instead of a column or a row. 
        (2) List the possible levels of replication specifications and their contents in the reproduction results. 
            (i) If the pictures contain tables, it might be columns, rows, panels, or the entire table. 
            (ii) If the pictures contain plots, it might be the curves, or the entire plot. When a plot has multiple figures, the smallest unit is not panels, but the figures. These figures can form a "matrix" of figures, and we can also consider the rows and columns of the matrix as levels. In addition, each subfigure may also be a specification. 
            (iii) For the tables, there are two special cases for the possible levels of replication specifications. The first case is that the levels may be distinguished by the fonts if there are multiple fonts, e.g., the reproduced results are in italic or bold. Another case is that there might have sub-tables, which can be identified that multiple tables with different titles in one picture, and you should consider the sub-tables as levels.
        (3) We only focus on the replication specifications, which could include reproductions, original results, and robustness tests. Find the level of replication specifications from the rest of the possible list based on the footnotes and the namings in the reproduced results.
            (i) If there are footnotes in the reproduced results, carefully read them and summarize the information in the footnotes to find the corresponding level in the rest of the possible list and the description of each specification. 
        (4) If the footnotes and namings do not provide useful information about replication specifications, e.g. meaningless indices, the entire table or plot should be considered as a replication specification. 
        (5) Then, you should list the replication specifications identified in the picture. The replication specifications you listed MUST be able to cover ALL the data points in the picture.

    2. Label each replication specification in the reproduced results identified in (1) based on the descriptions in the footnotes and namings following these rules:
        (1) If it is from the original paper, label it as "original". 
            Examples for descriptions: main results, baseline results, main findings, or the authors' names.
        (2) If it is a robustness test, label it as "robust". 
            Types of robustness tests include removal/additional control variables, changing the sample, removal/additional the independent or dependent variable, changing the estimation method/model, changing the method of inference, changing the weighting scheme, replication using new data, or placebo tests.
        (3) If it reproduces the original results or there is not obvious proof of being robustness tests or original paper, label it as "reproduced." 
        (4) If a replication specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced replication specifications that did not correct errors.

    Note: 
    A. You ONLY need to label the identified replication specifications in 1. and focus ONLY on the description of these replication specifications in the footnotes and namings. You should ignore all other levels at this stage. 
        For example, if the replication specifications are reported in columns, you should only focus on the description of each column and ignore the descriptions and namings of rows, panels, or the entire table.
    B. If there is not obvious proof of being robustness tests or original paper, you should label it as "reproduced" by default.
    C. The full-specification of the results from the original paper is a reproduced result instead of an original result. But a full-specification of the robustness tests, e.g. the types mentioned before, should still be seen as a robustness test.
        For example, a specification of "full specification of the panel regression of the original paper" should be labeled as "reproduced" instead of "original", while a specification of "full specification of the panel regression of the original paper removing of one of the control variables" should be labeled as "robust".

    You should first elaborate on the reasoning of your decision for the level. 
    For each replication specification, you should elaborate on the reasoning for each step behind your decision for its type.
    Your output format can ONLY be "{replication specification names}" + "{reasoning for replication specification type}" + "#" + "original"/"robust"/"reproduced".

Then, you need to extract data points from both pictures. 
    1. If they are tables:
        (1) You ONLY need to re-draw the data point labeled as "#reproduced" in the reproduced results and their corresponding data points using markdown syntax. Your tables MUST include ALL the rest of the data points in the pictured. For each reproduction data point, first find its corresponding data point in the original results. 
        (2) You MUST INCLUDE ALL data points in the pictures. You MUST NOT REPEAT OR MISS any data point in the pictures. Notably, some cell might be empty and some statistics might do not exist in all cells. You MUST pay attention to whether the statistics exist in the cells or not. 
        (3) Before any extraction, you should have a global view of the distribution of the data points in the pictures. You should notice which cells have data points and which cells are empty.
        (4) You need to extract different types of statistics in each picture. More specifically,
            (i) You should first find all the sample sizes in a picture, and put them in the first table. 
            (ii) Then, you should find all the errors/std errors/processed numbers in a picture, and put them in the second table.
            (iii) Next, you should find all the coefficients in a picture, and put them in the third table.
            (iv) Finally, you should find the rest of the numbers in a picture, and put them in the fourth table.
            (v) Each table MUST INCLUDE ALL the targe statistics in the picture. But you also MUST NOT REPEAT any statistics in the tables. 
            (vi) Your should output for each reproduction specification in the reproduced results and their corresponding data points in the original results. But the it is not required to be able to distinguish the where the statistics come from. Identifying a statistic from the reproduced results and its corresponding statistic from the original results is NECESSARY.
        (5) Each data point might have different statistics in the brackets and parantheses. You MUST read the footnotes in each picture carefully, explicitly copy sentences describing their meanings, determine their meanings individually. Then, you should choose one of the statistics and convert it into the other one if it is possible. You should elaborate on the reasoning for each data point, and label them in the tables. When multiple directions are possible, p-values should be preferred over the standard errors.
            For example, when the original results present the standard error and the reproduced results present the p-values, you should calculate the p-values of the original results when they also provided the coefficient and the samples size. However, if the original results does not have the sample size, while the reproduced results have the sample size, you should calculate the standard error of the reproduced results. 
        (6) For brevity, you may output the statistics without their row and column names. But you MUST ENSURE that all of the statistics in the pictures are matched and MUST explicitly output ALL the statistics in the pictures. Only output part of the statistics is NOT allowed.
    
    2. If they are discrete plots:
        (1) If the plot includes error bars, estimate its diameter comparing with the increments of the axis ticks.
        (2) To estimate a data point, 
            (i) You should first identify the pixel positions of the ticks on the axis. 
            (ii) For each data point, you should estimate the pixel position of the mean and the diameter of the error bars in pixel. 
            (iii) Calculate the mean and the diameter of the error bars to convert them in the same unit as the axis based on the pixel positions.
        (3) Extract the data points from the original results following the same rules. But you MUST NOT referernce to the reproduced results in the original results since they are independent. When extracting the original results, you MUST IGNORE the reproduced ones. 
        (4) You should re-draw the data points of both figures with the reasoning in two tables of markdown syntax.
        (5) You MUST elaborate on the reasoning for all data points in the format of "{data point}" + "{pixel position for mean and pixel distance of diameter}" + "{calculation for convert unit}" + "#" + "{values for mean and diameter}". 
            For example: "In the plot, in y-axis, 0 is about 450 pixel, 0.05 is about 350 pixel. 
            Control: 
                The pixel posititon of its mean is about (100, 420), the diameter of its error bar is about 40 pixels. 
                Consider that the 0 in y-axis is in about 450 pixel and 0.05 is in about 350 pixel, the mean should be around 0 + (450 - 420) * (0.05 - 0) / (450 - 350) = 0.015 and the diameter should be 0.05 * 40 / (450 - 350) = 0.02
                # mean: 0.015, error bar: 0.02".

    3. If they are continuous plots, for each picture, identify the increments on the x-axis, and divide the range of x-axis into intervals with a length of 1/5 of a single step increment. In this case, you only need to output the sliced intervals for each picture. 

    Note:
        A. the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL picture AND IGNORE THE OTHER ONE** when extracting data points from one of them. You MUST reason for each picture INDIVIDUALLY. 

Let's think step-by-step. 
"""

compare_dps_prompt = """
You are previously given two pictures depicting the reproduced results and the original results. Now, your job is to decide if the reproduced results match with the original results.

To do so, you need to decide the replication specification to compare according the previous step following these rules:

1. The types of replication specifications are given in the previous step marked by "#original", "#robustness", or "#reproduced". 
2. Focus solely on the reproduced results shared by both pictures, ignoring the original paper's data and robustness tests. 
3. Ignore the data points that only exist in one of the pictures. 
    (1) You should compare the naming of the data points in the reproduced results with the original results. 
    (2) The data points that only exist in the reproduced results could be labeled as "#reproduced" in the previous step. 
    (3) Compare only the shared data points if only a subset of the original results is reproduced. 
    (4) If a replication specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced replication specifications that did not correct errors.
4. For each selected replication specification, find the corresponding data points in the original results.

For each selected or discarded replication specification, you should elaborate on the reasoning behind your decision.
Your output format can ONLY be "{replication specification names}" + "{reasoning for replication specification selection}" + "#" + "selected" + " {corresponding original results}" or "discarded".

After determined the replication specifications, You can start comparison.

If the reproduced result is a table:
1. The previous prompt extracted reproduced results, reference them instead of recognizing data points from the pictures again. You do not need to repeat the statistics extracted from the previous prompt. But you MUST read them carefully before you start the comparison.
2. You need to calculate the following four matching rates one by one in order. The matching rates of the types of statistics MUST be calculated in the entire table level instead of particular columns or rows. 
    (1) The matching rate of sample sizes/observation numbers. 
    (2) The matching rate of errors/std errors/processed numbers. 
    (3) The matching rate of coefficients. 
    (4) The matching rate of all numbers. Besides the above three types of statistics, you should also compare the rest of the statistics. 
3. For the sample size/observation number types, you can claim a pair of numbers is a "Match" if it is exactly the original value. For all other types of statistics, you can claim a pair of numbers from the original and reproduced results is a "Match" if one of the following conditions is true:
    (1) They have different decimal places and the one with more decimal places can be rounded to the other number. 
        For example, 0.44 and 0.4 are considered as a "Match" since 0.44 can be rounded to 0.4 even though they are not within the range of 0.95 and 1.05 times of the original value, while 0.44 and 0.40 are not considered as a "Match" since 0.44 cannot be rounded to 0.40 since they have the same decimal places and 0.44 is not within the range of 0.95 and 1.05 times of the original value.
    (2) The difference is less than 5 percent of the original value, i.e. it is within the range of 0.95 and 1.05 times of the original value. You only need to check this condition when the (1) is not satisfied. 
    (3) Let's stress again that you should compare the statistics by the percentage of their differences instead of the absolute differences.
3. You MUST calculate the matching rates with all data points in that reproduced results that belong to one of the reproduction specifications and shared by both pictures.
4. Pay attention what statistics you are used to calculate the matching rates since a data point often contains more than one statistics. 
5. For brevity, you do not need to elaborate on the data points that are reproduced exactly either when they are already exactly the same or they match the condition of rouding in the 3.(1). You MUST elaborate on the comparison process of the second condition in the format of "{a statistic from one of the data points in the original results}" + "{a corresponding statistic from the corresponding data points in the reproduced results}" + "{calculation for their differences}" + "#" + "{Matched/Unmatched}". For example: 
    0.09 v.s. 0.10, |0.09 - 0.10| / 0.09 = 0.11 > 0.05, same decimal places, cannot be rounded, # Unmatched
    0.14 v.s. 0.1, |0.14 - 0.1| / 0.14 = 0.29 > 0.05, they are standard errors, 0.14 has two decimal places, 0.1 has one decimal place, 0.14 rounded to 0.1, # Matched
    1.0 v.s. 1.01, |1.0 - 1.01| / 1.0 = 0.01 < 0.05, # Matched
6. For each calculation of the matching rate, you MUST elaborate on in the format of "{total number of data points}" + "{comparison reason}" + "{counting the number of matched data points}" + "{calculation for the matching rate}" + "#" + "{matching rate}".
7. A table is claimed as a "Match" if and only if all the following conditions are met:
    (1) The matching rate of sample sizes/observation numbers is at least 80 percent.
    (2) The matching rate of errors/std errors/processed numbers is at least 80 percent.
    (3) The matching rate of coefficients is at least 80 percent.
    (4) The matching rate of overall numbers is at least 90 percent.

If the reproduced result is a plot, you should first decide the plot type:
1. If it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
    (1) The previous step should have extracted the data points from the pictures. You should reference them instead of recognizing data points from the pictures again. You need to compare the data points, including the error bars, extracted from the reproduced results with the original results.
    (2) ONLY IF the values are clearly labeled: less than 10 percent of errors
    (3) ELSE: the difference is less than half of the granularity of the axis ticks;
2. Else, if it's of continuous values: 
    (1) You MUST examine both the coarse-grained global trends and the fine-grained localities of the data points.
    (2) In the coarse-grained global trends, you should compare the overall trends of the data points in the reproduced results with the original results and their stationary points. 
    (3) In the fine-grained localities, 
        i. The previous step have sliced the x-axis into intervals with a length of 1/5 of a single step increment. You should compare the data points in each interval.
        ii. Compare the data points in each interval. For each interval, you can claim it as matched if the data points in it exhibit the same trend between it and its neighboring points (if any) are the same (increase, decrease, or almost identical. 
        iii. For this step, you should elaborate on your sliced intervals first and then your comparisons the data points in each interval.
3. You claim the plot is a "Match" if and only if 
    (1) more than 50 percent of the diameter described by the error bars are considered "Match"
    and
    (2) more than 70 percent of the remaining data points are considered "Match"

Notes: 
1. The original and reproduced results may present different statistics in the same experiment, you should only compare the statstics shared by both pictures. For example, if the original results present the mean and the standard error, while the reproduced results present the mean and the p-values, you should only compare the mean.
2. You should look carefully at the ticks of numbers on the axis.
3. You MUST compare ALL data point except the ones that is not reproduced results or not shared by both pictures.
4. Your final decision should be the general impression of the table or plot based on the rules above instead of the individual data points.
5. For ALL of your calculations, you MUST elaborate on your calculation process instead of only the final results. For ALL comparisons, you MUST elaborate on your reasoning path including the original data points, the reproduced data points, and the calculation for their differences.

You should first elaborate on the reasoning of the chosen replication specifications.
When you output your decision, if it's unmatched you should clearly label all unmatched points according to aforementioned rules; if matched, you should also give detailed examples to elaborate on the comparisons.
Your output format can ONLY be "{reasoning for matched/unmatched}" + "#"+ "Matched"/"Unmatched"

Let's think step-by-step. 
"""

label_specs_prompt_no_extract = """
Your first task is to decide the type of replication specifications in the reproduced results. Your decision should be based on the footnotes and the names in the reproduced results. In this step, you should focus on the reproduced results. 

    1. You should determine the level of replication specifications in the reproduced results based on your summry above and the namings. 
        (1) You MUST know that the naming of something is only about itself instead of some sub-parts of it. For example, the title of a table describes the entire table instead of a column or a row. 
        (2) List the possible levels of replication specifications and their contents in the reproduction results. 
            (i) If the pictures contain tables, it might be columns, rows, panels, or the entire table. 
            (ii) If the pictures contain plots, it might be the curves, or the entire plot. When a plot has multiple figures, the smallest unit is not panels, but the figures. These figures can form a "matrix" of figures, and we can also consider the rows and columns of the matrix as levels. In addition, each subfigure may also be a specification. 
            (iii) For the tables, there are two special cases for the possible levels of replication specifications. The first case is that the levels may be distinguished by the fonts if there are multiple fonts, e.g., the reproduced results are in italic or bold. Another case is that there might have sub-tables, which can be identified that multiple tables with different titles in one picture, and you should consider the sub-tables as levels.
        (3) We only focus on the replication specifications, which could include reproductions, original results, and robustness tests. Find the level of replication specifications from the rest of the possible list based on the footnotes and the namings in the reproduced results.
            (i) If there are footnotes in the reproduced results, carefully read them and summarize the information in the footnotes to find the corresponding level in the rest of the possible list and the description of each specification. 
        (4) If the footnotes and namings do not provide useful information about replication specifications, e.g. meaningless indices, the entire table or plot should be considered as a replication specification. 
        (5) Then, you should list the replication specifications identified in the picture. The replication specifications you listed MUST be able to cover ALL the data points in the picture.

    2. Label each replication specification in the reproduced results identified in (1) based on the descriptions in the footnotes and namings following these rules:
        (1) If it is from the original paper, label it as "original". 
            Examples for descriptions: main results, baseline results, main findings, or the authors' names.
        (2) If it is a robustness test, label it as "robust". 
            Types of robustness tests include removal/additional control variables, changing the sample, removal/additional the independent or dependent variable, changing the estimation method/model, changing the method of inference, changing the weighting scheme, replication using new data, or placebo tests.
        (3) If it reproduces the original results or there is not obvious proof of being robustness tests or original paper, label it as "reproduced." 
        (4) If a replication specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced replication specifications that did not correct errors.

    Note: 
    A. You ONLY need to label the identified replication specifications in 1. and focus ONLY on the description of these replication specifications in the footnotes and namings. You should ignore all other levels at this stage. 
        For example, if the replication specifications are reported in columns, you should only focus on the description of each column and ignore the descriptions and namings of rows, panels, or the entire table.
    B. If there is not obvious proof of being robustness tests or original paper, you should label it as "reproduced" by default.
    C. The full-specification of the results from the original paper is a reproduced result instead of an original result. But a full-specification of the robustness tests, e.g. the types mentioned before, should still be seen as a robustness test.
        For example, a specification of "full specification of the panel regression of the original paper" should be labeled as "reproduced" instead of "original", while a specification of "full specification of the panel regression of the original paper removing of one of the control variables" should be labeled as "robust".

    You should first elaborate on the reasoning of your decision for the level. 
    For each replication specification, you should elaborate on the reasoning for each step behind your decision for its type.
    Your output format can ONLY be "{replication specification names}" + "{reasoning for replication specification type}" + "#" + "original"/"robust"/"reproduced".

Let's think step-by-step. 
"""

extract_dps_prompt = """
In the previous query, you have determined the type of replication specifications in the reproduced results. Now, you need to extract data points from both pictures. 

1. If they are tables:
    (1) You ONLY need to re-draw the data point labeled as "#reproduced" in the reproduced results and their corresponding data points using markdown syntax. Your tables MUST include ALL the rest of the data points in the pictured. For each reproduction data point, first find its corresponding data point in the original results. 
    (2) You MUST INCLUDE ALL data points in the pictures. You MUST NOT REPEAT OR MISS any data point in the pictures. Notably, some cell might be empty and some statistics might do not exist in all cells. You MUST pay attention to whether the statistics exist in the cells or not. 
    (3) Before any extraction, you should have a global view of the distribution of the data points in the pictures. You should notice which cells have data points and which cells are empty.
    (4) You need to extract different types of statistics in each picture. More specifically,
        (i) You should first find all the sample sizes in a picture, and put them in the first table. 
        (ii) Then, you should find all the errors/std errors/processed numbers in a picture, and put them in the second table.
        (iii) Next, you should find all the coefficients in a picture, and put them in the third table.
        (iv) Finally, you should find the rest of the numbers in a picture, and put them in the fourth table.
        (v) Each table MUST INCLUDE ALL the targe statistics in the picture. But you also MUST NOT REPEAT any statistics in the tables. 
        (vi) Your output is not required to be able to distinguish the where the statistics come from. Only need to identify a statistic from the reproduced results and its corresponding statistic from the original results.
    (5) Each data point might have different statistics in the brackets and parantheses. You MUST read the footnotes in each picture carefully, explicitly copy sentences describing their meanings, determine their meanings individually. Then, you should choose one of the statistics and convert it into the other one if it is possible. You should elaborate on the reasoning for each data point, and label them in the tables. When multiple directions are possible, p-values should be preferred over the standard errors.
        For example, when the original results present the standard error and the reproduced results present the p-values, you should calculate the p-values of the original results when they also provided the coefficient and the samples size. However, if the original results does not have the sample size, while the reproduced results have the sample size, you should calculate the standard error of the reproduced results. 
    (6) For brevity, you may output the statistics without their row and column names. But you MUST ENSURE that all of the statistics in the pictures are matched and MUST explicitly output ALL the statistics in the pictures. Only output part of the statistics is NOT allowed.

2. If they are discrete plots:
    (1) If the plot includes error bars, estimate its diameter comparing with the increments of the axis ticks.
    (2) To estimate a data point, 
        (i) You should first identify the pixel positions of the ticks on the axis. 
        (ii) For each data point, you should estimate the pixel position of the mean and the diameter of the error bars in pixel. 
        (iii) Calculate the mean and the diameter of the error bars to convert them in the same unit as the axis based on the pixel positions.
    (3) Extract the data points from the original results following the same rules. But you MUST NOT referernce to the reproduced results in the original results since they are independent. When extracting the original results, you MUST IGNORE the reproduced ones. 
    (4) You should re-draw the data points of both figures with the reasoning in two tables of markdown syntax.
    (5) You MUST elaborate on the reasoning for all data points in the format of "{data point}" + "{pixel position for mean and pixel distance of diameter}" + "{calculation for convert unit}" + "#" + "{values for mean and diameter}". 
        For example: "In the plot, in y-axis, 0 is about 450 pixel, 0.05 is about 350 pixel. 
        Control: 
            The pixel posititon of its mean is about (100, 420), the diameter of its error bar is about 40 pixels. 
            Consider that the 0 in y-axis is in about 450 pixel and 0.05 is in about 350 pixel, the mean should be around 0 + (450 - 420) * (0.05 - 0) / (450 - 350) = 0.015 and the diameter should be 0.05 * 40 / (450 - 350) = 0.02
            # mean: 0.015, error bar: 0.02".

3. If they are continuous plots, for each picture, identify the increments on the x-axis, and divide the range of x-axis into intervals with a length of 1/5 of a single step increment. In this case, you only need to output the sliced intervals for each picture. 

Note:
    A. the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL picture AND IGNORE THE OTHER ONE** when extracting data points from one of them. You MUST reason for each picture INDIVIDUALLY. 

Let's think step-by-step. 
"""