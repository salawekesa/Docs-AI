from pathlib import Path
import pandas as pd
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utility import client, load_file_as_base64

document_dir = Path('./documents')

file_path = document_dir / 'citi_bank_statement.pdf'

if not file_path.exists():
    raise FileNotFoundError(f'File {file_path} not found')

model_id = 'prebuilt-layout'

doc_source = file_path

document_ai_client = client()

file_base64 = load_file_as_base64(doc_source)
poller = document_ai_client.begin_analyze_document(
    model_id, 
    {"base64Source": file_base64},
    locale="en-US",
)

result = poller.result()
# result.keys()
# dict_keys(['apiVersion', 'modelId', 'stringIndexType', 'content', 'pages', 'tables', 'paragraphs', 'styles', 'contentFormat', 'sections', 'figures'])

print('Number of tables:', len(result.tables))
tables = []
if result.tables:
    for table in result.tables:
        data = []
        for row_idx in range(table.row_count):
            row_data = []
            for column_idx in range(table.column_count):
                cell = [cell for cell in table.cells if cell.row_index == row_idx and cell.column_index == column_idx]
                if cell:
                    row_data.append(cell[0].content)
                else:
                    row_data.append(None)
            data.append(row_data)
        df = pd.DataFrame(data[1:], columns=data[0])
        tables.append(df)

for indx, talbe in enumerate(tables):
    print(f'Table {indx+1}')
    print(talbe)
    print('\n\n')        