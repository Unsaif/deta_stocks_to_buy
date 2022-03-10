import pandas as pd
import fitz
import re

def getpdfdetails(f, name):
    columns = ["Ticker", "Type", "Description"] 
    df = pd.DataFrame(columns = columns)
    rows = []
    try:
        doc = fitz.open(stream=f, filetype="pdf")
        row = []
        for page in doc:  # iterate the document pages
            text = page.get_text('text')  # get plain text (is in UTF-8)
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if "(" in line and line != "S (partial)":
                    if len(row) == 2: #ticker and type present
                        try:
                            ticker = re.search(r"\(([^)]+)\)", line).group(1)
                            if any(x.isupper() for x in ticker): #helps ensure the likelihood that a ticker is present by checking is there is uppercase characters
                                row.append("")
                                zipped = zip(columns, row)
                                rows.append(dict(zipped))
                                row = []
                                row.append(ticker.upper())
                            else:
                                pass
                        except:
                            pass #pass and not continue and we still want other conditions checked
                    elif len(row) != 0:
                        pass
                    else:
                        try:
                            ticker = re.search(r"\(([^)]+)\)", line).group(1)
                            if any(x.isupper() for x in ticker):
                                row.append(ticker.upper())
                            else:
                                pass
                        except:
                            pass
                elif line == "S" or line == "P" or line == "S (partial)":
                    if len(row) != 1:
                        pass
                    else:
                        row.append(line)
                elif re.match("DESCRIPTION", line):
                    description = line.split(": ",1)[1]
                    if len(row) != 2:
                        pass
                    else:
                        row.append(description.lower())
                        zipped = zip(columns, row)
                        rows.append(dict(zipped))
                        row = []
        df = pd.DataFrame(rows, columns=columns)
        return df
    except RuntimeError as err:
        print(err)
        print(name)
        return df
