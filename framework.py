from openai import OpenAI
import json
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "/workdir/m3cot/images/physics-825.png"
question = "Which property do these four objects have in common? choices: hard, soft, opaque"

client = OpenAI(
    api_key="***",  # 请替换为你的API KEY
    base_url="***"
)

prompt_path = "./prompt.json"
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = json.load(f)

# observation_stage
base64_image = encode_image(image_path)
observation_task = prompt["observation_stage"] + f"Question: {question}"
observation_response = client.chat.completions.create(
    model="***",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
                {"type": "text", "text": observation_task},
            ],
        }
    ]
)
observation_result = observation_response.choices[0].message.content
print(observation_result)

# reflection_stage
reflection_task = prompt["reflection_stage"] + f"Question: {question}" + f"Image Description: {observation_result}"
reflection_response = client.chat.completions.create(
    model="***",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": reflection_task},
            ],
        }
    ]
)
reflection_result = reflection_response.choices[0].message.content[-1]
print(reflection_result)

# reasoning_stage
if reflection_result != "1":
    reasoning_task = prompt["reasoning_stage"] + f"Question: {question}" + f"Image Description: {observation_result}"
    reasoning_response = client.chat.completions.create(
        model="***",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": reasoning_task},
                ],
            }
        ]
    )
    reasoning_result = reasoning_response.choices[0].message.content
else:
    reasoning_result = None
print(reasoning_result)

# decision_stage
if reasoning_result:
    decision_task = prompt["decision_stage"] + f"Question: {question}" + f"Chain of Thought: {reasoning_result}"
    decision_response = client.chat.completions.create(
        model="***",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": decision_task},
                ],
            }
        ]
    )
    decision_result = decision_response.choices[0].message.content
else:
    decision_task = prompt["decision_stage"] + f"Question: {question}" + f"Chain of Thought: {observation_result}"
    decision_response = client.chat.completions.create(
        model="***",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": decision_task},
                ],
            }
        ]
    )
    decision_result = decision_response.choices[0].message.content
print(decision_result)