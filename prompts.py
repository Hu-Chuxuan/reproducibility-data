label_specs_prompt = """
You are given two figures. The first figure shows reproduced results, while the second figure presents the original results. 

Your first task is to decide the type of specifications in the first figure. Your decision should be based on the footnotes and the names in the first figure. In this step, you should focus on the first figure. 

(1) If there are footnotes in the first figure, you should summarize the information in the footnotes.

(2) You should determine the level of specifications in the first figure based on its footnotes and the namings. 
    (i) If there is no information of the level, e.g. there are no footnotes and the namings are not about specifications, you should consider the entire table or plot as a specification.
    (ii) Examples for the level of specifications are columns, rows, curves, panels, or the entire table or plot.
    (iii) A special case is that the levels may be distinguished by the fonts, e.g., the reproduced results are in italic or bold.
    (iv) Then, you should list the specifications identified in the figure. The specifications you listed MUST be able to cover ALL the data points in the figure.

(3) Label each specification in the first figure identified in (1) following these rules:
    (i) If it is from the original paper, label it as "original". 
        Examples for descriptions: main results, baseline results, main findings, or the authors' names.
    (ii) If it is a robustness test, label it as "robust". 
        Types of robustness tests: removal/additional control variables, changing the sample, changing the dependent variable, changing the main independent variable, changing the estimation method/model, changing the method of inference, changing the weighting scheme, replication using new data, or placebo tests.
    (iii) If it reproduces the original results or there is not obvious proof of being robustness tests or original paper, label it as "reproduced." 
    (iv) If a specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced specifications that did not correct errors.

Note: 
A. You ONLY need to label the identified specifications in (1) and focus ONLY on the description of these specifications in the footnotes and namings. You should ignore all other levels at this stage. 
    For example, if the specifications are reported in columns, you should only focus on the description of each column and ignore the descriptions and namings of rows, panels, or the entire table.
B. If there is not obvious proof of being robustness tests or original paper, you should label it as "reproduced" by default.

You should first elaborate on the reasoning of your decision for the level. 
For each specification, you should elaborate on the reasoning behind your decision for its type.
Your output format can ONLY be "{specification names}" + "{reasoning for specification type}" + "#" + "original"/"robust"/"reproduced".

Finally, you may need to extract data points from the figure.
    (1) If this is a table, you ONLY need to re-draw the data point labeled as "#reproduced" in the reproduced results using markdown syntax. 
        (i) In your extracted table, each cell MUST only contain one data point. This means that if there are multiple data points in a cell, e.g. a cell contains a mean and a standard error, you should split them into two cells. 
        (ii) For each reproduction results, extract their corresponding data points in the original results.

    (3) If they are discrete plots:
        (i) If the plot includes error bars, estimate its diameter comparing with the increments of the axis ticks.
        (ii) To estimate a data point, you should first identify the pixel positions of the ticks on the axis. Then, for each data point, you should estimate the pixel position of the mean and the diameter of the error bars in pixel. Finally, you should calculate the mean and the diameter of the error bars to convert them in the same unit as the axis based on the pixel positions.
        (iii) For all data points, you MUST first state your reasoning with the relative position of each data point with the ticks of numbers on the axis. You MUST first output your reasoning process for all data points following this example: 
            "In the plot, in y-axis, 0 is about 450 pixel, 0.05 is about 350 pixel. 
            Control: The pixel posititon of its mean is about (100, 420), the diameter of its error bar is about 40 pixels. Consider that the 0 in y-axis is in about 450 pixel and 0.05 is in about 350 pixel, the mean should be around 0 + (450 - 420) * (0.05 - 0) / (450 - 350) = 0.015 and the diameter should be 0.05 * 40 / (450 - 350) = 0.02".
        (iv) You MUST first elaborate the reasoning for all data points in the format of "{data point}" + "{pixel position for mean and pixel distance of diameter}" + "{calculation for convert unit}" + "#" + "{values for mean and diameter}". Then, you should re-draw the data points of both figures with the reasoning in two tables of markdown syntax. 
        (v) Extract the data points from the original results following the same rules. But you MUST referernce to the reproduced results in the original results since they are independent. When extracting the original results, you MUST IGNORE the reproduced ones. 
    
    Notably, the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL FIGURE AND IGNORE THE OTHER ONE** when extracting data points from them. You MUST reason for each figure INDIVIDUALLY. 

Let's think step-by-step. 
"""

compare_dps_prompt = """
You are given two figures depicting the reproduced results and the original results in the previous query. Now, your job is to decide if the reproduced results match with the original results.

To do so, you need to decide the specification to compare according the previous step following these rules:

(1) The types of specifications are given in the previous step marked by "#original", "#robustness", or "#reproduced". 
(2) Focus solely on the reproduced results shared by both figures, ignoring the original paper's data and robustness tests. 
(3) Ignore the data points that only exist in one of the figures. 
    (i) You should compare the naming of the data points in the reproduced results with the original results. 
    (ii) The data points that only exist in the reproduced results could be labeled as "#reproduced" in the previous step. 
    (iii) Compare only the shared data points if only a subset of the original results is reproduced. 
    (iv) If a specification corrected some errors in the original paper without including robustness tests, you should label it as "reproduced" as well and ignore other reproduced specifications that did not correct errors.
(4) For each selected specification, find the corresponding data points in the original results.

For each selected or discarded specification, you should elaborate on the reasoning behind your decision.
Your output format can ONLY be "{specification names}" + "{reasoning for specification selection}" + "#" + "selected" + " {corresponding original results}" or "discarded".

After determined the specifications, You can start comparison.

If the reproduced result is a table:
(1) If the previous prompt extracted reproduced results, reference them instead of recognizing data points from the figures again. 
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
(1) if it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
    (i) The previous step should have extracted the data points from the figures. You should reference them instead of recognizing data points from the figures again. You need to compare the data points, including the error bars, extracted from the reproduced results with the original results.
    (i) ONLY IF the values are clearly labelled: less than 10 percents of errors
    (ii) ELSE: the difference is less than half of the granularity of the axis ticks;
(2) else if it's of continuous values, you can only claim a data point is a "Match" if the trends between it and its neighboring points (if any) are the same (increase, decrease, or almost identical with less than 5 percents of difference).
(3) You claim the plot is a "Match" if and only if 
    (i) more than 50 percents of the diameter described by the error bars are considered "Match"
    and
    (ii) more than 70 percents of the remaining data points are considered "Match"

Notes: 
(1) You should look carefully at the ticks of numbers on the axis.
(2) You MUST compare ALL data point except the ones that is not reproduced results or not shared by both figures.
(3) Your final decision should be the general impression of the table or plot based on the rules above instead of the individual data points.

You should first elaborate on the reasoning of the chosen specifications.
When you output your decision, if it's unmatched you should clearly label all unmatched points according to aforementioned rules; if matched, you should also give detailed examples to elaborate the comparisons.
Your output format can ONLY be "{reasoning for matched/unmatched}" + "#"+ "Matched"/"Unmatched"

Let's think step-by-step. 
"""