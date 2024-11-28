import os

def count_words_in_files(directory, words):
    # Initialize total counts for each word
    total_counts = {word: 0 for word in words}

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Only process .txt files
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().lower()
                    # Count each word in the file
                    for word in words:
                        count = content.count(word)
                        total_counts[word] += count
                        print(f"{filename}: {word} -> {count}")
            except Exception as e:
                print(f"Could not process {file_path}: {e}")

    # Display total counts
    print("\nTotal counts across all files:")
    for word, count in total_counts.items():
        print(f"{word}: {count}")

# Specify the directory to search and words to count
directory = "./Deep-Learning-Cpe-Project/dataset_part_2/valid/labelTxt"  # Change this to your target directory
words_to_count = ["cars", "truck"]

count_words_in_files(directory, words_to_count)
