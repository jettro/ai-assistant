import os

from openai import OpenAI

if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a maintainer of product data. You assist users in generating product data."},
            {"role": "user", "content": "I want ten products with the following attributes: name, price, and description. They should be groceries that people need on a regular basis. The output should be ready to be written to a text file. Only output the products no additional comments or information."},
        ]
    )

    print(completion.choices[0].message.content)

    # Generate a filename
    filename = "products.txt"

    # Write the content to the file
    with open(filename, "w") as f:
        f.write(completion.choices[0].message.content)

    # Upload the file to OpenAI
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="assistants",
    )

    print(file)