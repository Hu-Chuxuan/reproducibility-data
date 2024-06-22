from openai import OpenAI
import time
import argparse
from prompts import label_specs_prompt_no_extract, extract_dps_prompt, compare_dps_prompt

parser = argparse.ArgumentParser()
parser.add_argument("--api", type=str, required=True)
parser.add_argument("--org", type=str, required=True)
parser.add_argument("--paper", type=int, required=True)
parser.add_argument("--sample", type=int, required=True)

args = parser.parse_args()

client = OpenAI(api_key=args.api, organization=args.org)

def chat(msgs):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=msgs,
    temperature=0.7,
    max_tokens=4096,
    top_p=1
    )

    return response

def label_specs(original_img, reproduced_img):
    msgs = [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": label_specs_prompt_no_extract
            },
            {
            "type": "image_url",
            "image_url": {
                "url": reproduced_img,
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": original_img,
            },
            }
        ]
        }
    ]
    response = chat(msgs)
    print(response.choices[0].message.content)

    with open(f"Results/{args.paper}.txt", "+a") as f:
        f.write("Types Prompt:\n" + msgs[0]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

def extract_dps(original_img, reproduced_img, types):
    msgs = [
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": label_specs_prompt_no_extract
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": reproduced_img,
                },
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": original_img,
                },
                }
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
                "text": extract_dps_prompt,
                },
            ],
        }
    ]

    response = chat(msgs)
    print(response.choices[0].message.content)
    with open(f"Results/{args.paper}.txt", "+a") as f:
        f.write("Extract Prompt:\n" + msgs[2]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")
    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

def compare_dps(original_img, reproduced_img, types, dps):
    msgs = [
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": label_specs_prompt_no_extract
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": reproduced_img,
                },
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": original_img,
                },
                }
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
                "text": extract_dps_prompt,
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": dps
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": compare_dps_prompt
                },
            ],
        }
    ]
    response = chat(msgs)
    
    print(response.choices[0].message.content)
    
    with open(f"Results/{args.paper}.txt", "+a") as f:
        f.write("Prompt:\n" + msgs[2]["content"][0]["text"] + "\n")
        f.write(response.choices[0].message.content + "\n")

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens

original_img = f"https://github.com/Hu-Chuxuan/reproducibility-data/raw/main/Samples/{args.paper}/O{args.sample}.png"
reproduced_img = f"https://github.com/Hu-Chuxuan/reproducibility-data/raw/main/Samples/{args.paper}/R{args.sample}.png"

with open(f"Results/{args.paper}.txt", "+a") as f:
    f.write("-"*25 +  f" {args.sample} (2 steps) " + "-"*25 + "\n")

types, input_token_type, output_token_type = label_specs(original_img, reproduced_img)
print("="*50)
time.sleep(10)
extract, input_token_extract, output_token_extract = extract_dps(original_img, reproduced_img, types)
print("="*50)
time.sleep(10)
compare, input_token_cmp, output_token_cmp = compare_dps(original_img, reproduced_img, types, extract)
print("# of input tokens: ", input_token_type, "+", input_token_extract, "+", input_token_cmp, "=", input_token_type + input_token_extract + input_token_cmp)
print("# of output tokens: ", output_token_type, "+", output_token_extract, "+", output_token_cmp, "=", output_token_type + output_token_extract + output_token_cmp)