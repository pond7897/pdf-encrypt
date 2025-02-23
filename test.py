import os
import re
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

pdf_trans = './pdf'
pdf_trans_encrypted = './pdf/Encrypted'

for filename in os.listdir(pdf_trans):
    if filename.endswith('.pdf'):
        input_path = os.path.join(pdf_trans, filename)
        output_path = os.path.join(pdf_trans_encrypted, filename.replace('.pdf', '_encrypted.pdf'))

        with pdfplumber.open(input_path) as reader:
            for page in reader.pages:
                text = page.extract_text()

                # find start with 640
                match = re.search(r'640.*', text)
                if match:
                    std_id = match.group(0)
                    print(f'Found: {std_id}')
                    break

        if std_id:
            print(f'Student ID: {std_id}')

            reader = PdfReader(input_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(user_password=std_id)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

print('Done')