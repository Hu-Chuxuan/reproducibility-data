from openai import OpenAI
client = OpenAI(api_key="your-openai-key", organization="your-org-id")

def compare_images(original_img, reproduced_img):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": '''
            You are given the following figures, the first one depicts the experiment results from the original paper, and the second one depicts the reproduced results. Your job is to decide if the reproduced results match with the original results.

            To do so, you should first decide if the figure contains a table or a plot.

            If it is a table:
            You can only claim a data point is a "Match" if the values are less than 10 percents of errors.
            You claim the table is a "Match" if and only if 
            (i) more than 80 percents of the data points of sample size/observation number types are considered "Match"
            and
            (ii) more than 50 percents of the data points of errors/std errors/processed number types are considered "Match"
            and
            (iii) more than 70 percents of the data points of other number types are considered "Match"

            If it is a plot, you should first decide the plot type:
            (1) if it's of continuous values or represents trends, you can only claim a data point is a "Match" if the trends between it and its neighboring points (if any) are the same (increase, decrease, or almost identical with less than 5 percents of difference).
            (2) else (e.g., bar plots, scattered plots), you can only claim a data point is a "Match":
            (i) ONLY IF the values are clearly labelled: less than 10 percents of errors
            (ii) ELSE: the difference is less than half of the granularity of the axis ticks;
            You claim the plot is a "Match" if and only if 
            (i) more than 50 percents of the error bars are considered "Match"
            and
            (ii) more than 70 percents of the remaining data points are considered "Match"

            Notes: 
            (1) sometimes the reproduced results can contain data from original paper, in this cases you should ignore those data and focus on reproduced results.
            (2) You should look carefully at the ticks of numbers on the axis.

            When you output your decision, if it's unmatched you should clearly label unmatched points according to either (1) or (2); if matched, you should also give detailed examples to elaborate.
            Your output format can ONLY be "Matched"/"Unmatched" + "#" + "{reasoning for matched/unmatched}"
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
    ],
    temperature=0.7,
    max_tokens=1024,
    top_p=1
    )

    print(response.choices[0].message.content)
    print("# of input tokens: ", response.usage.prompt_tokens)
    print("# of output tokens: ", response.usage.completion_tokens)

i = 62
original_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/O6.png"
reproduced_img = f"https://github.com/liyun-zhang/reproducibility-data/raw/main/{i}/R6.png"
compare_images(original_img, reproduced_img)