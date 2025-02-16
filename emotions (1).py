"""
******************************
Code by: Muniver Kaur Kharod
******************************
This file contains functions for text processing and emotion analysis.
"""

# Define the list of emotions globally
# This is the reference list used for emotion analysis throughout the program
EMOTIONS = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']


def clean_text(comment):
    """
    Cleans the comment by replacing non-alphabetic characters with spaces
    and converting all text to lowercase.
    Args:
        comment (str): The comment text to clean.
    Returns:
        str: The cleaned comment.
    """
    cleaned_comment = ""
    for char in comment:
        # Retain only alphabetic characters and spaces
        if char.isalpha() or char.isspace():
            cleaned_comment += char
        else:
            # Replace non-alphabetic characters with spaces
            cleaned_comment += " "
    # Convert the entire text to lowercase for uniformity
    return cleaned_comment.lower()


def make_keyword_dict(keyword_file_name):
    """
    Reads a TSV file of keywords and their associated emotions and creates a nested dictionary.
    Args:
        keyword_file_name (str): The name of the TSV file.
    Returns:
        dict: A dictionary where each keyword maps to a dictionary of emotions and their scores.
    """
    keyword_dict = {}
    try:
        with open(keyword_file_name, 'r') as file:
            for line in file:
                # Split each line into a word and its associated emotion scores
                parts = line.strip().split('\t')
                word = parts[0]
                # Map each emotion to its corresponding score
                emotions = {EMOTIONS[i]: int(parts[i + 1]) for i in range(len(EMOTIONS))}
                keyword_dict[word] = emotions
    except FileNotFoundError:
        raise IOError(f"File '{keyword_file_name}' not found!")  # Handle missing file error
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading '{keyword_file_name}': {e}")  # Handle other errors
    return keyword_dict


def make_comments_list(filter_country, comments_file_name):
    """
    Reads a CSV file of comments and filters them by country.
    Args:
        filter_country (str): The country to filter by ("all" for all countries).
        comments_file_name (str): The name of the CSV file.
    Returns:
        list: A list of dictionaries containing the filtered comments.
    """
    import csv
    comments_list = []
    try:
        with open(comments_file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Ensure the row has exactly 4 fields
                if len(row) != 4:
                    raise ValueError("Each row in the CSV must have exactly 4 values.")
                comment_id, username, country, text = row
                # Filter by country if applicable
                if filter_country == "all" or country.strip().lower() == filter_country.lower():
                    comments_list.append({
                        'comment_id': int(comment_id),
                        'username': username.strip(),
                        'country': country.strip().lower(),
                        'text': text.strip(),
                    })
    except FileNotFoundError:
        raise IOError(f"File '{comments_file_name}' not found!")  # Handle missing file error
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading '{comments_file_name}': {e}")  # Handle other errors
    return comments_list


def classify_comment_emotion(comment, keywords):
    """
    Classifies the emotion of a comment based on the keywords dictionary.
    Args:
        comment (str): The comment text to classify.
        keywords (dict): The keywords dictionary.
    Returns:
        str: The most dominant emotion in the comment.
    """
    # Clean the comment text for uniform processing
    cleaned_comment = clean_text(comment)
    # Initialize scores for each emotion
    emotion_scores = {emotion: 0 for emotion in EMOTIONS}
    for word in cleaned_comment.split():
        # Check if the word exists in the keywords dictionary
        if word in keywords:
            # Update emotion scores based on the keyword's values
            for emotion, value in keywords[word].items():
                emotion_scores[emotion] += value
    # Determine the most dominant emotion by sorting
    sorted_emotions = sorted(
        emotion_scores.items(),
        key=lambda x: (-x[1], EMOTIONS.index(x[0]))  # Sort by descending score, then emotion order
    )
    return sorted_emotions[0][0]  # Return the emotion with the highest score


def make_report(comment_list, keywords, report_filename):
    """
    Generates a report summarizing the most common emotion and the counts of all emotions.
    Args:
        comment_list (list): A list of filtered comments.
        keywords (dict): The keywords dictionary.
        report_filename (str): The name of the report file to create.
    Returns:
        str: The most common emotion in the dataset.
    Raises:
        RuntimeError: If the comment list is empty.
    """
    # Check if the comment list is empty
    if not comment_list:
        raise RuntimeError("No comments in dataset!")

    # Initialize a dictionary to store totals for each emotion
    emotion_totals = {emotion: 0 for emotion in EMOTIONS}
    for comment in comment_list:
        # Classify the emotion of each comment
        emotion = classify_comment_emotion(comment['text'], keywords)
        # Increment the count for the identified emotion
        emotion_totals[emotion] += 1

    # Sort emotions by total count to determine the most common
    sorted_emotions = sorted(
        emotion_totals.items(),
        key=lambda x: (-x[1], EMOTIONS.index(x[0]))
    )
    most_common_emotion = sorted_emotions[0][0]

    # Write the report to a file
    total_comments = sum(emotion_totals.values())
    try:
        with open(report_filename, 'w') as report_file:
            report_file.write(f"Most common emotion: {most_common_emotion}\n\n")
            report_file.write("Emotion Totals\n")
            # Write counts and percentages for each emotion
            for emotion in EMOTIONS:
                count = emotion_totals[emotion]
                percentage = (count / total_comments) * 100
                report_file.write(f"{emotion}: {count} ({percentage:.2f}%)\n")
    except Exception as e:
        raise IOError(f"An error occurred while writing the report: {e}")  # Handle file writing errors

    return most_common_emotion  # Return the most common emotion
