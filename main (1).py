"""
******************************
Code by: Muniver Kaur Kharod
******************************
This file contains the main program logic for YouTube Emotion analysis.
"""
import os.path
from emotions import make_keyword_dict, make_comments_list, make_report

VALID_COUNTRIES = [
    'bangladesh', 'brazil', 'canada', 'china', 'egypt',
    'france', 'germany', 'india', 'iran', 'japan', 'mexico',
    'nigeria', 'pakistan', 'russia', 'south korea', 'turkey',
    'united kingdom', 'united states'
]

def ask_user_for_input():
    """
    Asks the user for input file names and country filter, checks for valid input,
    and raises exceptions if invalid.
    """
    keyword_filename = input("Input keyword file (ending in .tsv): ")
    if not keyword_filename.endswith('.tsv'):
        raise ValueError("Keyword file does not end in .tsv!")
    if not os.path.exists(keyword_filename):
        raise IOError(f"{keyword_filename} does not exist!")

    comment_filename = input("Input comment file (ending in .csv): ")
    if not comment_filename.endswith('.csv'):
        raise ValueError("Comment file does not end in .csv!")
    if not os.path.exists(comment_filename):
        raise IOError(f"{comment_filename} does not exist!")

    country = input("Input a country to analyze (or 'all' for all countries): ").lower()
    if country != 'all' and country not in VALID_COUNTRIES:
        raise ValueError(f"{country} is not a valid country to filter by!")

    report_filename = input("Input the name of the report file (ending in .txt): ")
    if not report_filename.endswith('.txt'):
        raise ValueError("Report file does not end in .txt!")
    if os.path.exists(report_filename):
        raise IOError(f"{report_filename} already exists!")

    return keyword_filename, comment_filename, country, report_filename

def main():
    """
    Main function to handle the workflow.
    """
    try:
        keyword_file, comment_file, country, report_file = ask_user_for_input()
        keywords = make_keyword_dict(keyword_file)
        comments = make_comments_list(country, comment_file)
        if not comments:
            raise RuntimeError("No comments in dataset!")

        most_common_emotion = make_report(comments, keywords, report_file)
        print(f"Most common emotion is: {most_common_emotion}")
    except Exception as e:
        print(e)
        # Optionally, you can allow the user to retry by not returning here and adding a loop in main.
        return

if __name__ == "__main__":
    main()
