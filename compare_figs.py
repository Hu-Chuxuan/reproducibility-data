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

            To do so, you should first create the comparison set of data: 
            (1) Identify the data set for comparison using footnotes and column/row names from the reproduced results.
            (2) Focus solely on the reproduced results, ignoring the original paper's data and robustness tests.
            (3) Compare only the shared data points if only a subset of the original results is reproduced.
            (4) If uncertain about certain data points, ignore them and explain the reason in your output.

            Next, you should decide if the figure contains a table or a plot.

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
            (2) In cases where some data points in the original figures are not included in the reproduced figures, you should IGNORE those data points.

            When you output your decision, if it's unmatched you should clearly label unmatched points according to either (1) or (2); if matched, you should also give detailed examples to elaborate both the selection of comparison set and the comparisons.
            Your output format can ONLY be "{reasoning for comparison set} + {reasoning for matched/unmatched}" + "#"+ "Matched"/"Unmatched"
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

i = 13
original_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/O1.png"
reproduced_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/R1.png"
compare_images(original_img, reproduced_img)