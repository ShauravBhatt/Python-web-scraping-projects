import fitz 

def read_pdf(filepath):
    doc = fitz.open(filepath)
    all_txt = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        all_txt += page.get_text() 

    doc.close()
    return all_txt

if __name__ == "__main__":
    file_path = "test.pdf"
    try:
        content = read_pdf(file_path)
        print('-'*30)
        print(f"\n{content}")
        print('-'*30)

    except Exception as e:
        print("Error: " , e)
