import pandas 

def convert_excel_to_array(file_path):
    names = [
        "Candidate Name", 
        "Candidate Email", 
        "Qualified Score", 
        "Saberr Score", 
        "High on Qualified> 80%", 
        "High Saberr Score >50", 
        "Criteria Met", 
        "Should Be Invited?"
    ]
    df = pandas.read_excel(file_path, header=None, names=names)
    values = df["Candidate Email"].values
    user_emails = list(values[3:])

    return user_emails

