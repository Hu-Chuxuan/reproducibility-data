label_specs_prompt = """
You are given two pictures. The first picture shows reproduced results, while the second picture presents the original results. 

Your first task is to decide the type of replication specifications in the reproduced results. Your decision should be based on the footnotes and the names in the reproduced results. In this step, you should focus on the reproduced results. 

    1. You should determine the level of replication specifications in the reproduced results based on your summry above and the namings. 
        (1) List the possible levels of replication specifications in the reproduction results. 
            (i) If the pictures contain tables, it might be columns, rows, panels, or the entire table. 
            (ii) If the pictures contain plots, it might be the curves, or the entire plot. When a plot has multiple figures and these figures can form a "matrix" of figures, we can also consider the rows and columns of the matrix as levels. 
            (iii) A special case is that the levels may be distinguished by the fonts if there are multiple fonts, e.g., the reproduced results are in italic or bold.
        (2) We consider all experiments in the original results as sub-experiments of the replication specifications instead of replication specifications. 
            (i) Read the original results, list the the sub-experiments, and determine at which level they are presented in the reproduced results. 
            (ii) Elimitate the levels that only present sub-experiments from the list of replication specifications and list the rest of the possible levels. 
        (3) We only focus on the replication specifications, which could include reproductions, original results, and robustness tests. Find the level of replication specifications from the rest of the possible list based on the footnotes and the namings in the reproduced results.
            (i) If there are footnotes in the reproduced results, carefully read them and summarize the information in the footnotes to find the corresponding level in the rest of the possible list and the description of each specification. 
            (ii) If there is no information of the level, e.g. there are no footnotes and the namings are not about replication specifications, you should consider the entire table or plot as a replication specification. 
        (4) Then, you should list the replication specifications identified in the picture. The replication specifications you listed MUST be able to cover ALL the data points in the picture.

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

The, you need to extract data points from the picture. 
    1. If this is a table:
        (1) For each reproduction data point, first find its corresponding data point in the original results.
        (2) You ONLY need to re-draw the data point labeled as "#reproduced" in the reproduced results and their corresponding data points using markdown syntax. 
        (3) In your extracted table, each cell MUST only contain one data point. This means that if there are multiple data points in a cell, e.g. a cell contains a mean and a standard error, you should split them into two cells. 
        (4) Each data point might have different statistics in the brackets and parantheses. You MUST read the footnotes in each picture carefully, explicitly copy sentences describing their meanings, determine their meanings individually. Then, you should choose one of the statistics and convert it into the other one if it is possible. You should elaborate the reasoning for each data point, and label them in the tables. 
            For example, when the original results present the standard error and the reproduced results present the p-values, you should calculate the p-values of the original results when they also provided the coefficient and the samples size. However, if the original results does not have the sample size, while the reproduced results have the sample size, you should calculate the standard error of the reproduced results.

    2. If they are discrete plots:
        (1) If the plot includes error bars, estimate its diameter comparing with the increments of the axis ticks.
        (2) To estimate a data point, 
            (i) You should first identify the pixel positions of the ticks on the axis. 
            (ii) For each data point, you should estimate the pixel position of the mean and the diameter of the error bars in pixel. 
            (iii) Calculate the mean and the diameter of the error bars to convert them in the same unit as the axis based on the pixel positions.
        (3) Extract the data points from the original results following the same rules. But you MUST NOT referernce to the reproduced results in the original results since they are independent. When extracting the original results, you MUST IGNORE the reproduced ones. 
        (4) You should re-draw the data points of both figures with the reasoning in two tables of markdown syntax.

    3. If they are continuous plots, for each picture, identify the increments on the x-axis, and divide the range of x-axis into intervals with a length of 1/5 of a single step increment. In this case, you only need to output the sliced intervals for each picture. 

    Note:
        A. the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL picture AND IGNORE THE OTHER ONE** when extracting data points from them. You MUST reason for each picture INDIVIDUALLY. 
        B. For the tables, you MUST elaborate the reasoning for the statistics in the format of "{original footnotes}" + "{reproduced footnotes}" + "{reasoning for their statistics}" + "{reasoning for their conversion}" + "#" + "{values for the original and reproduced statistics}".
        C. For the plots, you MUST elaborate the reasoning for all data points in the format of "{data point}" + "{pixel position for mean and pixel distance of diameter}" + "{calculation for convert unit}" + "#" + "{values for mean and diameter}". 
            For example: "In the plot, in y-axis, 0 is about 450 pixel, 0.05 is about 350 pixel. 
            Control: 
                The pixel posititon of its mean is about (100, 420), the diameter of its error bar is about 40 pixels. 
                Consider that the 0 in y-axis is in about 450 pixel and 0.05 is in about 350 pixel, the mean should be around 0 + (450 - 420) * (0.05 - 0) / (450 - 350) = 0.015 and the diameter should be 0.05 * 40 / (450 - 350) = 0.02
                # mean: 0.015, error bar: 0.02".

Let's think step-by-step. 
"""

compare_dps_prompt = """
You are previously given two pictures depicting the reproduced results and the original results. Now, your job is to decide if the reproduced results match with the original results.

To do so, you need to decide the replication specification to compare according the previous step following these rules:

(1) The types of replication specifications are given in the previous step marked by "#original", "#robustness", or "#reproduced". 
(2) Focus solely on the reproduced results shared by both pictures, ignoring the original paper's data and robustness tests. 
(3) Ignore the data points that only exist in one of the pictures. 
    (i) You should compare the naming of the data points in the reproduced results with the original results. 
    (ii) The data points that only exist in the reproduced results could be labeled as "#reproduced" in the previous step. 
    (iii) Compare only the shared data points if only a subset of the original results is reproduced. 
    (iv) If a replication specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced replication specifications that did not correct errors.
(4) For each selected replication specification, find the corresponding data points in the original results.

For each selected or discarded replication specification, you should elaborate on the reasoning behind your decision.
Your output format can ONLY be "{replication specification names}" + "{reasoning for replication specification selection}" + "#" + "selected" + " {corresponding original results}" or "discarded".

After determined the replication specifications, You can start comparison.

If the reproduced result is a table:
(1) If the previous prompt extracted reproduced results, reference them instead of recognizing data points from the pictures again. 
    (i) You should pay attention that some cells may be empty. 
        For example, when the first column has three data points and the second column has six data points, you should only compare nine data points since the last three data points in the first column do not exist.
    (ii) Also, you should extract the data points from the original results following the same rules as the previous prompt. 
(2) You can only claim a data point is a "Match" if the values are less than 10 percents of errors. The exception is the sample size/observation number types, where you can claim a data point is a "Match" if it is exactly the original value.
(3) You claim the table is a "Match" if and only if 
    (i) more than 80 percents of the data points of sample size/observation number types are considered "Match"
    and
    (ii) more than 50 percents of the data points of errors/std errors/processed number types are considered "Match"
    and
    (iii) more than 70 percents of the data points of other number types are considered "Match"

If the reproduced result is a plot, you should first decide the plot type:
(1) If it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
    (i) The previous step should have extracted the data points from the pictures. You should reference them instead of recognizing data points from the pictures again. You need to compare the data points, including the error bars, extracted from the reproduced results with the original results.
    (ii) ONLY IF the values are clearly labelled: less than 10 percents of errors
    (iii) ELSE: the difference is less than half of the granularity of the axis ticks;
(2) Else, if it's of continuous values: 
    (i) You MUST examine both the coarse-grained global trends and the fine-grained localities of the data points.
    (ii) In the coarse-grained global trends, you should compare the overall trends of the data points in the reproduced results with the original results and their stationary points. 
    (iii) In the fine-grained localities, 
        A. The previous step have sliced the x-axis into intervals with a length of 1/5 of a single step increment. You should compare the data points in each interval.
        B. Compare the data points in each interval. For each interval, you can claim it as matched if the data points in it exhibit the same trend between it and its neighboring points (if any) are the same (increase, decrease, or almost identical. 
        C. For this step, you should elaborate your sliced intervals first and then your comparisons the data points in each interval.
(3) You claim the plot is a "Match" if and only if 
    (i) more than 50 percents of the diameter described by the error bars are considered "Match"
    and
    (ii) more than 70 percents of the remaining data points are considered "Match"

Notes: 
(1) The original and reproduced results may present different statistics in the same experiment, you should only compare the statstics shared by both pictures. For example, if the original results present the mean and the standard error, while the reproduced results present the mean and the p-values, you should only compare the mean.
(2) You should look carefully at the ticks of numbers on the axis.
(3) You MUST compare ALL data point except the ones that is not reproduced results or not shared by both pictures.
(4) Your final decision should be the general impression of the table or plot based on the rules above instead of the individual data points.

You should first elaborate on the reasoning of the chosen replication specifications.
When you output your decision, if it's unmatched you should clearly label all unmatched points according to aforementioned rules; if matched, you should also give detailed examples to elaborate the comparisons.
Your output format can ONLY be "{reasoning for matched/unmatched}" + "#"+ "Matched"/"Unmatched"

Let's think step-by-step. 
"""

label_specs_prompt_no_extract = """
Your first task is to decide the type of replication specifications in the reproduced results. Your decision should be based on the footnotes and the names in the reproduced results. In this step, you should focus on the reproduced results. 

    1. You should determine the level of replication specifications in the reproduced results based on your summry above and the namings. 
        (1) List the possible levels of replication specifications in the reproduction results. 
            (i) If the pictures contain tables, it might be columns, rows, panels, or the entire table. 
            (ii) If the pictures contain plots, it might be the curves, or the entire plot. When a plot has multiple figures and these figures can form a "matrix" of figures, we can also consider the rows and columns of the matrix as levels. 
            (iii) A special case is that the levels may be distinguished by the fonts if there are multiple fonts, e.g., the reproduced results are in italic or bold.
        (2) We consider all experiments in the original results as sub-experiments of the replication specifications instead of replication specifications. 
            (i) Read the original results, list the the sub-experiments, and determine at which level they are presented in the reproduced results. 
            (ii) Elimitate the levels that only present sub-experiments from the list of replication specifications and list the rest of the possible levels. 
        (3) We only focus on the replication specifications, which could include reproductions, original results, and robustness tests. Find the level of replication specifications from the rest of the possible list based on the footnotes and the namings in the reproduced results.
            (i) If there are footnotes in the reproduced results, carefully read them and summarize the information in the footnotes to find the corresponding level in the rest of the possible list and the description of each specification. 
            (ii) If there is no information of the level, e.g. there are no footnotes and the namings are not about replication specifications, you should consider the entire table or plot as a replication specification. 
        (4) Then, you should list the replication specifications identified in the picture. The replication specifications you listed MUST be able to cover ALL the data points in the picture.

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
In the previous query, you have determined the type of replication specifications in the reproduced results. Now, you need to extract data points from the picture. 

1. If this is a table:
    (1) For each reproduction data point, first find its corresponding data point in the original results.
    (2) You ONLY need to re-draw the data point labeled as "#reproduced" in the reproduced results and their corresponding data points using markdown syntax. 
    (3) In your extracted table, each cell MUST only contain one data point. This means that if there are multiple data points in a cell, e.g. a cell contains a mean and a standard error, you should split them into two cells. 

2. If they are discrete plots:
    (1) If the plot includes error bars, estimate its diameter comparing with the increments of the axis ticks.
    (2) To estimate a data point, 
        (i) You should first identify the pixel positions of the ticks on the axis. 
        (ii) For each data point, you should estimate the pixel position of the mean and the diameter of the error bars in pixel. 
        (iii) Calculate the mean and the diameter of the error bars to convert them in the same unit as the axis based on the pixel positions.
    (3) Extract the data points from the original results following the same rules. But you MUST NOT referernce to the reproduced results in the original results since they are independent. When extracting the original results, you MUST IGNORE the reproduced ones. 
    (4) You should re-draw the data points of both figures with the reasoning in two tables of markdown syntax.

3. If they are continuous plots, for each picture, identify the increments on the x-axis, and divide the range of x-axis into intervals with a length of 1/5 of a single step increment. In this case, you only need to output the sliced intervals for each picture. 

Note:
    A. the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL picture AND IGNORE THE OTHER ONE** when extracting data points from them. You MUST reason for each picture INDIVIDUALLY. 
    B. For the plots, you MUST elaborate the reasoning for all data points in the format of "{data point}" + "{pixel position for mean and pixel distance of diameter}" + "{calculation for convert unit}" + "#" + "{values for mean and diameter}". 
        For example: "In the plot, in y-axis, 0 is about 450 pixel, 0.05 is about 350 pixel. 
        Control: 
            The pixel posititon of its mean is about (100, 420), the diameter of its error bar is about 40 pixels. 
            Consider that the 0 in y-axis is in about 450 pixel and 0.05 is in about 350 pixel, the mean should be around 0 + (450 - 420) * (0.05 - 0) / (450 - 350) = 0.015 and the diameter should be 0.05 * 40 / (450 - 350) = 0.02
            # mean: 0.015, error bar: 0.02".

Let's think step-by-step. 
"""