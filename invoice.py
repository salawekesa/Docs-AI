"""
Example 2. Extract invoice detail
"""
from pathlib import Path
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utility import client, load_file_as_base64

document_dir = Path('./documents')
invoice_dir = document_dir / 'invoice'
file_path = invoice_dir / 'TC-0964-21.pdf'

if not file_path.exists():
    raise FileNotFoundError(f'File {file_path} not found')

model_id = 'prebuilt-invoice'

doc_source = file_path

document_ai_client = client()

file_base64 = load_file_as_base64(doc_source)
poller = document_ai_client.begin_analyze_document(
    model_id, 
    {"base64Source": file_base64},
    locale="en-US",
)

result = poller.result()

print('Document count :', len(result.documents))

for document in result.documents:
    # print('Doc type:', document['docType'])
    # print('Bounding Area:', document['boundingRegions'])
    # print('Confidence:', document['confidence'] * 100.0, '%')
    
    document_fields = document['fields']
    fields = document_fields.keys()
    print(fields)

    for field in fields:
        if field == 'Items':
            items_list = []
            items = document_fields[field]

            for item in items['valueArray']:
                item_fields = item['valueObject']
                item_dict = {}
                for item_field in item_fields.keys():
                    value = item_fields[item_field].get('content', '')
                    item_dict[item_field] = value
                items_list.append(item_dict)
            print(items_list)
            print('---')
            continue
        value = document_fields[field].get('content', '')
        print(f'{field} : {value}')
        print('---')