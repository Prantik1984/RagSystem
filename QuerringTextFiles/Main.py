from TextOperator import TextOperator
import os
from pathlib import Path

# main function
# displays to the users the list of available files
# accepts input from the user
def main():
    current_dir = Path(__file__).parent
    data_folder = current_dir / "data"
    docs=get_docs_list(data_folder)

    print("Available Documents:")

    for index, filename in docs.items():
        print(f"{index}. {filename}")

    print("Enter number like 1/2/3 to select documents to query")

    while True:
        try:
          user_choice = int(input("Enter File Number:"))
          if user_choice in docs:
            break
        except ValueError:
            print("Invalid Input")

    text_operator = TextOperator(os.path.join(data_folder, docs[user_choice]))
    text_operator.load_document()

def get_docs_list(folder_path:str) -> list:
    return {
        i: file.name
        for i, file in enumerate(Path(folder_path).iterdir(), start=1)
        if file.is_file()}


if __name__ == "__main__":
    main()