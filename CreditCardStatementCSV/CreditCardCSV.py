import sys
from pypdf import PdfReader
import csv
import re

valid_credit_cards = ['bilt']

def processBilt(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        text += "\n"
    raw_statement = text.split("\n")
    statement_rows = []
    statement_line = ""
    num_words = 0
    for word in raw_statement:
        statement_line += word + ' '
        num_words += 1
        if (num_words >= 5):
            if word.startswith("$"):
                statement_line = statement_line.strip()
                statement_line_arr = statement_line.split(" ", 4)
                descr = statement_line_arr[len(statement_line_arr) - 1]
                statement_line_arr.pop(len(statement_line_arr) - 1)
                split_descr = descr.split(" $")
                for string in split_descr:
                    statement_line_arr.append(string)
                statement_rows.append(statement_line_arr)
                statement_line = ""
                num_words = 0

    with open('cc_statement.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        headers = ["Trans Date", "Post Date", "Reference Number", "", "Description of Transaction or Credit", "Amount"]

        writer.writerow(headers)
        for row in statement_rows:
            writer.writerow(row)

    

def main():
    # command format: CreditCardCSV.py [credit card name] [filename]
    if len(sys.argv) != 3:
        print("Please provide the following command line arguments in this order: credit_card_type file_name")
        return
    elif not sys.argv[1] in valid_credit_cards:
        print("Please provide a valid credit card from the following supported cards: ")
        print(valid_credit_cards)
        return
    elif not sys.argv[2].endswith('.pdf'):
        print("Please provide a credit card statement in PDF format as a command line argument")
        return

    creditCardType = sys.argv[1]
    file_path = sys.argv[2]

    if creditCardType == 'bilt':
        processBilt(file_path)

if __name__ == "__main__":
    main()