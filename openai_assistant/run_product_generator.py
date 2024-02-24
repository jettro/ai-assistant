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
            {"role": "system", "content": "You are the manager of a coffee shop."},
            {"role": "user", "content": "Create a list "
                                        "of products that the shop should sell. You need to create a list of twenty "
                                        "products with the following attributes: name, price, description, "
                                        "ingredients and the ratio of ingredients. The "
                                        "output should be ready to be written to a text file. Only output the "
                                        "asked data no additional comments or information."},
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
