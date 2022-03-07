from . import get_pdf_details 
from io import BytesIO
from urllib.request import urlopen
from deta import Deta

# Initialize with a Project Key
deta = Deta("a0zd0kwp_zP8cFJdLzpuSB3YR7N9TyAjbR2LYaeQp")

def gettradingdataframes(df, id_df, pdf_file_url):
    people = deta.Base("People")
    trading_dataframes = {}
    for i, entry in id_df.iterrows():
        key = entry["key"]
        last_name = entry["last_name"]
        first_name = entry["first_name"]
        last_doc_id = entry["last_doc_id"]
        try:
            df_name = df[(df["Last"] == last_name) & (df["First"] == first_name)]
            doc_id = str(df_name.iloc[-1]["DocID"]) #most recent
            
            if doc_id != last_doc_id:
                r = urlopen(f"{pdf_file_url}{doc_id}.pdf")
                fileReader = BytesIO(r.read())

                df_details = get_pdf_details.getpdfdetails(fileReader)
                trading_dataframes[key] = df_details
                
                #update doc_id
                person = people.get(key)
                person['last_doc_id'] = doc_id
                people.put(person, key)
            else:
                pass
        except IndexError as err:
            pass
    return trading_dataframes