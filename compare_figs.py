from openai import OpenAI
client = OpenAI(api_key="your-api-key", organization="your-org-id")

def compare_images(original_img, reproduced_img):
    msgs = [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''
            You are given the following figures, the first one depicts the experiment results from the original paper, and the second one depicts the reproduced results. Your job is to decide if the reproduced results match with the original results.

            First, you should determine the level at which specifications in the second figure are reported (e.g. columns, rows, curves, panels) and the types of specifications.
                (1) You should first read the footnotes and the namings of the second figure to determine the level and types of specifications. Sometimes the entire table or plot may be considered as a specification.
                (2) Label each specification following these rules:
                    (i) If it reproduces the original results, label it as "reproduced." 
                    (ii) If it is from the original paper, label it as "original". Examples: main results, baseline results, main findings, or the authors' names.
                    (iii) If it is a robustness test, label it as "robust". Examples: alternative specifications, placebo tests, or removal/additional controls.
                You should first elaborate on the reasoning of your decision for the level. 
                For each specification, you should elaborate on the reasoning behind your decision for its type.
                Your output format can ONLY be "{specification names}" + "{reasoning for specification type}" + "#" + "original"/"robust"/"reproduced".

            Next, select the specifications in the second figure to compare according the previous step following these rules:
                (1) The types of specifications are given in the previous step marked by "#original", "#robust", or "#reproduced". 
                (2) Focus solely on the reproduced results ("#reproduced" in the previous step), ignoring the original paper's data and robustness tests ("#orignal" or "#robust"). 
                (3) Compare only the shared data points if only a subset of the original results is reproduced.
                (4) For each selected specification, find the corresponding data points in the original results.
                For each selected or discarded specification, you should elaborate on the reasoning behind your decision.
                Your output format can ONLY be "{specification names}" + "{reasoning for specification selection}" + "#" + "selected {corresponding original results}" or "discarded".

            Finally, you need to check if the figure contains a table or a plot and compare the seleted specifications.
                If it is a table:
                    You can only claim a data point is a "Match" if the values are less than 10 percents of errors. The exception is the sample size/observation number types, where you can claim a data point is a "Match" if it is exactly the original value.
                    You claim the table is a "Match" if and only if 
                        (i) more than 80 percents of the data points of sample size/observation number types are considered "Match"
                        and
                        (ii) more than 50 percents of the data points of errors/std errors/processed number types are considered "Match"
                        and
                        (iii) more than 70 percents of the data points of other number types are considered "Match"

                If it is a plot, you should first decide the plot type:
                    (1) You should identify the data points from the figure before making comparisons. You MUST ensure that the data you identify from the figure have at least four significant digits
                    (2) if it is bar plots, scattered plots, line charts connecting dots, or other types of discrete values, you can only claim a data point is a "Match":
                        (ii) ONLY IF the values are clearly labelled: less than 10 percents of errors
                        (iii) ELSE: the difference is less than half of the granularity of the axis ticks;
                    (3) else if it's of continuous values, you can only claim a data point is a "Match" if the trends between it and its neighboring points (if any) are the same (increase, decrease, or almost identical with less than 5 percents of difference).
                        You claim the plot is a "Match" if and only if 
                        (i) more than 50 percents of the upper and lower bound described by the error bars are considered "Match"
                        and
                        (ii) more than 70 percents of the remaining data points are considered "Match"
                    (4) You should look carefully at the ticks of numbers on the axis.
                
                When you output your decision, if it's unmatched you should clearly label unmatched points according to either (1) or (2); if matched, you should also give detailed examples to elaborate both the selection of comparison set and the comparisons.
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
    print("# of input tokens: ", response.usage.prompt_tokens)
    print("# of output tokens: ", response.usage.completion_tokens)

    with open(f"Results/{i}.txt", "+a") as f:
        f.write("Prompt:\n" + msgs[0]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")
        f.write("# of input tokens: " + str(response.usage.prompt_tokens) + "\n")
        f.write("# of output tokens: " + str(response.usage.completion_tokens) + "\n")
        f.write("\n")

i = 13

with open(f"Results/{i}.txt", "+a") as f:
    f.write("-"*25 +  " 1 (zero-shot cot, output format each step) " + "-"*25 + "\n")

original_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/O1.png"
reproduced_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/R1.png"
compare_images(original_img, reproduced_img)