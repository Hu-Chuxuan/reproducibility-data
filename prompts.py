label_specs_prompt = """
You are given a figure shows reproduced results. 

Your first task is to decide the type of specifications in the first figure. Your decision should be based on the footnotes and the names in the first figure. 

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

    (3) If they are discrete plots:
        (i) If the plot includes error bars, estimate the upper and lower bounds of the error bars instead of just their length. You MUST BEAR IN MIND that the mean should be the middle of the error bars, i.e. upper bound - mean should be the same as mean - lower bound.
        (ii) To estimate a data point, you should first carefully estimate the relative position of its mean, upper bound, and lower bound with respect to the axis ticks, precisely describe the distance of these values to boundaries of the ticks. Then preliminarily estimate the value of each data point by observing its distances ratio with respect to the axis tick boundaries. Finally, adjust the value of each data point based on the mean being the midpoint rule.
        (iii) For all data points, you MUST first state your reasoning with the relative position of each data point with the ticks of numbers on the axis. You MUST first output your reasoning process for all data points following this example: 
            "Control: The mean of a data point is between 0 and 0.05, positioned such that its distance to 0.05 is roughly four times its distance to 0. Its upper bound is equidistant to 0 and 0.05, while its lower bound is slightly below and very close to 0. Given these relative positions, the mean should be around 0 + (0.05 - 0) / (1 + 4) * 1 = 0.01, upper bound should be around 0 + (0.05 - 0) / (1 + 1) * 1 = 0.025, lower bound should be around 0. Further considering that the mean should be the midpoint of the error bars, the value of mean should be 0.01, the uppoer bound should be 0.025, and the lower bound should be -0.005, where 0.01 * 2 = 0.025 + (-0.005)".
        (iv) You MUST first elaborate the reasoning for all data points in the format of "{data point}" + "{reasoning for mean, upper bound, and lower bound}" + "{final decisions}". Then, you should re-draw the data points of both figures with the reasoning in two tables of markdown syntax. 
    
    Notably, the reproduced results may be significantly different from the original results. You **MUST ONLY FOCUS ON EACH INDIVIDUAL FIGURE AND IGNORE THE OTHER ONE** when extracting data points from them. You MUST reason for each figure INDIVIDUALLY. 

Let's think step-by-step. 
"""

compare_dps_prompt = """
You are given a figure depicting the reproduced results in the previous query. Now, there is a new figure presenting the original results. Your job is to decide if the reproduced results match with the original results.

To do so, you need to check if the original figure contains a table or a plot

If it is a discrete plot, you should first extract the data points from the original results. 
    (1) If the plot includes error bars, estimate the radium of the error bars instead of just their length. You MUST BEAR IN MIND that the mean should be the middle of the error bars, i.e. upper bound - mean should be the same as mean - lower bound.
    (2) To estimate a data point, you should first carefully estimate the relative position of its mean, upper bound, and lower bound with respect to the axis ticks, precisely describe the distance of these values to boundaries of the ticks. Then preliminarily estimate the value of each data point by observing its distances ratio with respect to the axis tick boundaries. Finally, adjust the value of each data point based on the mean being the midpoint rule.
    (3) For all data points, you MUST first state your reasoning with the relative position of each data point with the ticks of numbers on the axis. You MUST first output your reasoning process for all data points following this example: 
        "Control: The mean of a data point is between 0 and 0.05, positioned such that its distance to 0.05 is roughly four times its distance to 0. Its upper bound is equidistant to 0 and 0.05, while its lower bound is slightly below and very close to 0. Given these relative positions, the mean should be around 0 + (0.05 - 0) / (1 + 4) * 1 = 0.01, upper bound should be around 0 + (0.05 - 0) / (1 + 1) * 1 = 0.025, lower bound should be around 0. Further considering that the mean should be the midpoint of the error bars, the value of mean should be 0.01, the uppoer bound should be 0.025, and the lower bound should be -0.005, where 0.01 * 2 = 0.025 + (-0.005)".
    (4) You MUST first elaborate your reasoning for all data points in the format of "{data point}" + "{reasoning for mean, upper bound, and lower bound}" + "{final decisions}". Then, you should re-draw the data points of both figures with the reasoning in two tables of markdown syntax. 
    (5) You MUST ONLY focus on the original results in this step and IGNORE the reproduced results.

Then, decide the specification to compare according the previous step following these rules:

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
    (i) ONLY IF the values are clearly labelled: less than 10 percents of errors
    (ii) ELSE: the difference is less than half of the granularity of the axis ticks;
(2) else if it's of continuous values, you can only claim a data point is a "Match" if the trends between it and its neighboring points (if any) are the same (increase, decrease, or almost identical with less than 5 percents of difference).
You claim the plot is a "Match" if and only if 
    (i) more than 50 percents of the upper and lower bound described by the error bars are considered "Match"
    and
    (ii) more than 70 percents of the remaining data points are considered "Match"

Notes: 
(1) You should look carefully at the ticks of numbers on the axis.
(2) You MUST compare ALL data point except the ones that is not reproduced results or not shared by both figures.
(3) Your final decision should be the general impression of the table or plot based on the rules above instead of the individual data points.

You should first elaborate on the reasoning of the chosen specifications.
When you output your decision, if it's unmatched you should clearly label unmatched points according to either (1) or (2); if matched, you should also give detailed examples to elaborate the comparisons.
Your output format can ONLY be "{reasoning for matched/unmatched}" + "#"+ "Matched"/"Unmatched"

Let's think step-by-step. 
"""