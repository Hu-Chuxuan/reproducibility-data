from openai import OpenAI
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--api", type=str, required=True)
parser.add_argument("--org", type=str, required=True)
parser.add_argument("--paper", type=int, required=True)
parser.add_argument("--sample", type=int, required=True)

args = parser.parse_args()

client = OpenAI(api_key=args.api, organization=args.org)

def create_comparsion_set(original_img, reproduced_img):
    msgs = [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''
            You are given a figure that shows reproduced results. Your task is to decide the type of specifications.
            Your decision should be based on the footnotes and the names.
            
            (1) You should first read the footnotes and the namings of the figure to determine the level of specifications. 
                (i) If there is no information of the level, e.g. there are no footnotes and the namings are not about specifications, you should consider the entire table or plot as a specification.
                (ii) Examples for the level of specifications are columns, rows, curves, panels, or the entire table or plot.
                (iii) Then, you should list the specifications identified in the figure. The specifications you listed MUST be able to cover ALL the data points in the figure.

            (2) Label each specification identified in (1) following these rules:
                (i) If it is from the original paper, label it as "original". 
                    Examples for descriptions: main results, baseline results, main findings, or the authors' names.
                (ii) If it is a robustness test, label it as "robust". 
                    Types of robustness tests: removal/additional control variables, changing the sample, changing the dependent variable, changing the main independent variable, changing the estimation method/model, changing the method of inference, changing the weighting scheme, replication using new data, or placebo tests.
                (iii) If it reproduces the original results or there is not obvious proof of being robustness tests or original paper, label it as "reproduced." 
            
            Note: 
            (1) You ONLY need to label the identified specifications in (1) and focus ONLY on the description of these specifications in the footnotes and namings. You should ignore all other levels at this stage. 
                For example, if the specifications are reported in columns, you should only focus on the description of each column and ignore the descriptions and namings of rows, panels, or the entire table.
            (2) If there is not obvious proof of being robustness tests or original paper, you should label it as "reproduced" by default.
            
            You should first elaborate on the reasoning of your decision for the level. 
            For each specification, you should elaborate on the reasoning behind your decision for its type.
            Your output format can ONLY be "{specification names}" + "{reasoning for specification type}" + "#" + "original"/"robust"/"reproduced".

            Finally, you may need to extract data from the figure depending of whether it contains a table or a figure: 
                (1) If this figure contains a table, you should re-draw the contents in table that is labeled as "#reproduced" in the figure in markdown grammar. 
                (2) You MUST ENSURE the data points are in the same order as the original results.
            
            Let's think step-by-step. 
            '''
            },
            {
            "type": "image_url",
            "image_url": {
                "url": reproduced_img,
            },
            },
        ]
        }
    ]
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=msgs,
    temperature=0.7,
    max_tokens=2048,
    top_p=1
    )
    print(response.choices[0].message.content)

    with open(f"Results/{args.paper}.txt", "+a") as f:
        f.write("Types Prompt:\n" + msgs[0]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

def compare_images(original_img, reproduced_img, types):
    msgs = [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''
            You are given a figure that shows reproduced results. Your task is to decide the type of specifications.
            Your decision should be based on the footnotes and the names.
            
            You should first decide if the figure contains a table or a plot

            If it is a table:
            The specification may be reported in columns, rows, panels, or the entire table. 

            If it is a plot:
            The specifications may be at different curves, panels, or the entire plot.
            
            Follow these rules:
            (1) Label specifications from the original paper or robustness tests as "original or robust."
                (i) Examples of the original paper's data descriptions: main results, baseline results, main findings, or the authors' names.
                (ii) Examples of robustness test descriptions: alternative specifications, placebo tests, or removal/additional controls.
            (2) Label specifications from the reproduced results as "reproduced." 

            For each specification, you should elaborate on the reasoning behind your decision.
            Your output format can ONLY be "{specification names}" + "{reasoning for specification type}" + "#" + "original or robust" or "reproduced".
            '''
            },
        ]
        },
        {
        "role": "assistant",
        "content": [
            {
            "type": "text",
            "text": types
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''
            You are given a figure depicting the experiment results from the original paper of the reproduced results of previous prompt. Your job is to decide if the reproduced results match with the original results.

            To do so, you should first decide the specification to compare according the previous step following these rules:

            (1) The types of specifications are given in the previous step marked by "#original", "#robustness", or "#reproduced". 
            (2) Focus solely on the reproduced results shared by both figures, ignoring the original paper's data and robustness tests. 
            (3) Ignore the data points that only exist in one of the figures. 
                (i) You should compare the naming of the data points in the reproduced results with the original results. 
                (ii) The data points that only exist in the reproduced results could be labeled as "#reproduced" in the previous step. 
                (iii) Compare only the shared data points if only a subset of the original results is reproduced. 
            (4) For each selected specification, find the corresponding data points in the original results.
            
            For each selected or discarded specification, you should elaborate on the reasoning behind your decision.
            Your output format can ONLY be "{specification names}" + "{reasoning for specification selection}" + "#" + "selected" + " {corresponding original results}" or "discarded".

            After determined the specifications, you need to check if the figure contains a table or a plot.

            If it is a table:
            (1) If the previous prompt extracted reproduced results, reference it instead of recognizing data points from the figure again. 
                (i) Since the table drawn by the last prompt could be inaccurate, you should double check it with the figure. 
                (ii) You should pay attention that some cells may be empty. 
                For example, when the first column has three data points and the second column has six data points, you should only compare nine data points since the last three data points in the first column do not exist.
            (2) You can only claim a data point is a "Match" if the values are less than 10 percents of errors. The exception is the sample size/observation number types, where you can claim a data point is a "Match" if it is exactly the original value.
            (3) You claim the table is a "Match" if and only if 
                (i) more than 80 percents of the data points of sample size/observation number types are considered "Match"
                and
                (ii) more than 50 percents of the data points of errors/std errors/processed number types are considered "Match"
                and
                (iii) more than 70 percents of the data points of other number types are considered "Match"

            If it is a plot, you should first decide the plot type:
            (1) if it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
                (i) You should identify the data points from the figure before making comparisons. You MUST ensure that the data you identify from the figure have at least four significant digits
                (ii) ONLY IF the values are clearly labelled: less than 10 percents of errors
                (iii) ELSE: the difference is less than half of the granularity of the axis ticks;
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
            ''',
            },
            {
            "type": "image_url",
            "image_url": {
                "url": original_img,
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": reproduced_img,
            },
            },
        ],
        }
    ]
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=msgs,
    temperature=0.7,
    max_tokens=4096,
    top_p=1
    )
    
    print(response.choices[0].message.content)
    
    with open(f"Results/{args.paper}.txt", "+a") as f:
        f.write("Prompt:\n" + msgs[2]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

original_img = f"https://github.com/Hu-Chuxuan/reproducibility-data/raw/main/Samples/{args.paper}/O{args.sample}.png"
reproduced_img = f"https://github.com/Hu-Chuxuan/reproducibility-data/raw/main/Samples/{args.paper}/R{args.sample}.png"

with open(f"Results/{args.paper}.txt", "+a") as f:
    f.write("-"*25 +  f" {args.sample} (2 steps) " + "-"*25 + "\n")

types, input_token_type, output_token_type = create_comparsion_set(original_img, reproduced_img)
print("="*50)
time.sleep(5)
response, input_token_cmp, output_token_cmp = compare_images(original_img, reproduced_img, types)
print("# of input tokens: ", input_token_type, "+", input_token_cmp, "=", input_token_type + input_token_cmp)
print("# of output tokens: ", output_token_type, "+", output_token_cmp, "=", output_token_type + output_token_cmp)