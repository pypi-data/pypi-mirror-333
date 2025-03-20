import time
import requests
import os
import argparse
from dotenv import load_dotenv


def download_image(image_url, output_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved to {output_path}")
    else:
        print("Failed to download the image.")


def generate_image(url, api_key):
    if not api_key:
        raise Exception(
            "API key is required. Provide it as a parameter or set it in the environment variable."
        )

    api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"
    headers = {
        "X-DashScope-Async": "enable",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "wanx-style-repaint-v1",
        "input": {"image_url": url, "style_index": 3},
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response_data = response.json()

    if "output" in response_data and "task_id" in response_data["output"]:
        task_id = response_data["output"]["task_id"]
    else:
        raise Exception("Failed to retrieve task_id")

    task_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

    while True:
        time.sleep(3)
        result_response = requests.get(
            task_url, headers={"Authorization": f"Bearer {api_key}"}
        )
        result_data = result_response.json()

        if "output" in result_data:
            task_status = result_data["output"].get("task_status", "")

            if task_status == "SUCCEEDED":
                if (
                    "results" in result_data["output"]
                    and len(result_data["output"]["results"]) > 0
                ):
                    return result_data["output"]["results"][0]["url"]
                else:
                    raise Exception("Failed to retrieve processed image URL")

            elif task_status == "FAILED":
                error_message = result_data["output"].get("message", "Unknown error")
                raise Exception(f"Task failed: {error_message}")

            elif task_status == "RUNNING":
                print("Task is still running, waiting...")
                continue

        raise Exception("Unexpected API response format")


def load_env_file():
    current_directory = os.getcwd()

    env_file_path = os.path.join(current_directory, ".env")

    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
        print(".env file found and environment variables loaded.")
    else:
        print(".env file not found.")


def main():
    load_env_file()
    parser = argparse.ArgumentParser(
        description="Generate styled image using DashScope API"
    )
    parser.add_argument("url", type=str, help="Image URL to process")
    parser.add_argument(
        "--api_token",
        type=str,
        help="DashScope API Token",
        default=os.getenv("DASHSCOPE_API_KEY"),
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path to save the image"
    )
    args = parser.parse_args()

    if not args.api_token:
        print(
            "Error: API token is required. Provide --api_token or set DASHSCOPE_API_KEY in environment variables."
        )
        exit(1)

    try:
        result_url = generate_image(args.url, args.api_token)
        print("Processed Image URL:", result_url)

        if args.output:
            download_image(result_url, args.output)
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()