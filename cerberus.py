import sys
import fire
from llama import Llama
import json
import os
from typing import Any
from typing import Optional


def write_as_json(data: Any, output_file_path: str) -> None:
    content = json.dumps(data)
    with open(output_file_path, "w") as out_file:
        out_file.writelines(content)


def read_json(file_path: str) -> Optional[Any]:
    json_data = None
    if os.path.isfile(file_path):
        with open(file_path, "r") as in_file:
            content = in_file.readlines()
            if len(content) > 1:
                content_str = " ".join([l.strip().replace("\n", "") for l in content])
            else:
                content_str = content[0]
            json_data = json.loads(content_str)
    return json_data


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    prompt_json_path: str,
    result_json_path: str,
    prog_language: str,
    num_responses:int = 5,
    temperature: float = 0.2,
    top_p: float = 0.95,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    result_list = []
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    prompt_list = read_json(prompt_json_path)
    for prompt in prompt_list:
        instructions = [
            [
                {
                    "role": "system",
                    "content": f"You are a software developer, please provide"
                               f" {num_responses} answers "
                               f"as code in {prog_language} "
                               f"language without explanation",
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],
        ]
        results = generator.chat_completion(
            instructions,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )

        for instruction, result in zip(instructions, results):
            result_list.append((prompt, result['generation']['content']))
    write_as_json(result_list, result_json_path)


if __name__ == "__main__":
    fire.Fire(main)
