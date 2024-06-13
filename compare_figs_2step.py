from openai import OpenAI
import time
client = OpenAI(api_key="your-api-key", organization="your-org-id")

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
            
            You should first read the footnotes and the namings of the second figure to determine the level and types of specifications. Sometimes the entire table or plot may be considered as a specification.
            
            Label each specification following these rules:
                (1) If it reproduces the original results, label it as "reproduced." 
                (2) If it is from the original paper, label it as "original". 
                    Examples: main results, baseline results, main findings, or the authors' names.
                (3) If it is a robustness test, label it as "robust". 
                    Examples: alternative specifications, placebo tests, or removal/additional controls.
            
            You should first elaborate on the reasoning of your decision for the level. 
            For each specification, you should elaborate on the reasoning behind your decision for its type.
            Your output format can ONLY be "{specification names}" + "{reasoning for specification type}" + "#" + "original"/"robust"/"reproduced".
            
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
    max_tokens=1024,
    top_p=1
    )
    print(response.choices[0].message.content)

    with open(f"Results/{i}.txt", "+a") as f:
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
            (2) Focus solely on the reproduced results, ignoring the original paper's data and robustness tests. 
            (3) Compare only the shared data points if only a subset of the original results is reproduced.
            
            After determined the specifications, you need to check if the figure contains a table or a plot.

            If it is a table:
            You can only claim a data point is a "Match" if the values are less than 10 percents of errors. The exception is the sample size/observation number types, where you can claim a data point is a "Match" if it is exactly the original value.
            You claim the table is a "Match" if and only if 
            (i) more than 80 percents of the data points of sample size/observation number types are considered "Match"
            and
            (ii) more than 50 percents of the data points of errors/std errors/processed number types are considered "Match"
            and
            (iii) more than 70 percents of the data points of other number types are considered "Match"

            If it is a plot, you should first decide the plot type:
            (1) if it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
            (i) You should identify the data points from the figure before making comparisons. You MUST ensure that the data you identify from the figure have at least four significant digits
            (i) ONLY IF the values are clearly labelled: less than 10 percents of errors
            (ii) ELSE: the difference is less than half of the granularity of the axis ticks;
            (2) else if it's of continuous values, you can only claim a data point is a "Match" if the trends between it and its neighboring points (if any) are the same (increase, decrease, or almost identical with less than 5 percents of difference).
            You claim the plot is a "Match" if and only if 
            (i) more than 50 percents of the upper and lower bound described by the error bars are considered "Match"
            and
            (ii) more than 70 percents of the remaining data points are considered "Match"

            Notes: 
            (1) You should look carefully at the ticks of numbers on the axis.

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
    
    with open(f"Results/{i}.txt", "+a") as f:
        f.write("Prompt:\n" + msgs[2]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")
        f.write("# of input tokens: " + str(response.usage.prompt_tokens) + "\n")
        f.write("# of output tokens: " + str(response.usage.completion_tokens) + "\n")
        f.write("\n")

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

i = 13
original_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/O1.png"
reproduced_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/R1.png"

with open(f"Results/{i}.txt", "+a") as f:
    f.write("-"*25 +  " 1 (2 steps) " + "-"*25 + "\n")

types, input_token_type, output_token_type = create_comparsion_set(original_img, reproduced_img)
command = input("Whether continue (y/n): ")
if command == "y":
    response, input_token_cmp, output_token_cmp = compare_images(original_img, reproduced_img, types)
    print("# of input tokens: ", input_token_type, "+", input_token_cmp, "=", input_token_type + input_token_cmp)
    print("# of output tokens: ", output_token_type, "+", output_token_cmp, "=", output_token_type + output_token_cmp)
else:
    print("# of input tokens: ", input_token_type)
    print("# of output tokens: ", output_token_type)