"""
example 1: W2 form data extraction
"""
import base64
from pathlib import Path
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utility import client, is_file_or_url, load_file_as_base64

document_dir = Path('./documents')
w2_dir = document_dir / 'w2'
file_path = w2_dir / 'W2_Clean_DataSet_01' / 'W2_XL_input_clean_1000.jpg'

if not file_path.exists():
    raise FileNotFoundError(f'File {file_path} not found')

model_id = "prebuilt-tax.us.w2"

document_ai_client = client()

# doc_source = '<doc url>'
doc_source = file_path

if is_file_or_url(str(doc_source)) == 'url':
    print('Doc is a url')
    poller = document_ai_client.begin_analyze_document(
        model_id, AnalyzeDocumentRequest(url_source=doc_source)
    )
elif is_file_or_url(str(doc_source)) == 'file':
    print('Doc is a file')
    poller = document_ai_client.begin_analyze_document(
        model_id, {"base64Source": load_file_as_base64(doc_source)}
    )

result = poller.result()

# dict_keys(['apiVersion', 'modelId', 'stringIndexType', 'content', 'pages', 'styles', 'documents', 'contentFormat'])
print(result.keys())
print('Document Page Total:', len(result['pages']))
print(result['modelId'])
print(result['pages'][0].keys())
print(result['pages'][0]['pageNumber']) # document page number
print(result['pages'][0]['words']) # words in the document page
# A line is an ordered sequence of consecutive content elements separated by a visual space
for line_indx, line in enumerate(result['pages'][0]['lines']):
    print(f'Line {line_indx+1}:', line['content'])
print(result['content'])
print(result['contentFormat'])

print('Document count :', len(result.documents))

for document in result.documents:
    # >>> document.keys()
    # dict_keys(['docType', 'boundingRegions', 'fields', 'confidence', 'spans'])
    print('Doc type:', document['docType'])
    print('Bounding Area:', document['boundingRegions'])
    print('Confidence:', document['confidence'] * 100.0, '%')
    # a span refers to a specific segment of text within a document,
    print('Spans:', document['spans'])

    document_fields = document['fields']
    
    if document_fields.get('W2FormVariant'):
        print('W2-Form:', document_fields['W2FormVariant']['content'])

    if document_fields.get('TaxYear'):
        print('Tax Year:', document_fields['TaxYear']['content'])
    
    if document_fields.get('W2Copy'):
        print('W2 Copy:', document_fields['W2Copy']['content'])

    if document_fields.get('Employer'):
        print('Full Address:', document_fields['Employer']['valueObject']['Address']['content'])
        print('Employer ID:', document_fields['Employer']['valueObject']['IdNumber'].get('valueString', ''))
        print('Employer:', document_fields['Employer']['valueObject']['Name'].get('valueString', ''))
        print('Address:', document_fields['Employer']['valueObject']['Address']['valueAddress'].get('streetAddress', ''))
        print('City:', document_fields['Employer']['valueObject']['Address']['valueAddress'].get('city', ''))
        print('State:', document_fields['Employer']['valueObject']['Address']['valueAddress'].get('state', ''))
        print('Postal Code:', document_fields['Employer']['valueObject']['Address']['valueAddress'].get('postalCode', ''))
        
    if document_fields.get('ControlNumber'):
        print('Control Number:', document_fields['ControlNumber']['content'])
        print('Confidence:', document_fields['ControlNumber']['confidence'] * 100.0, '%')

    if document_fields.get('Employee'):
        print('Employee:', document_fields['Employee']['valueObject']['Name']['content'])
        print('Address:', document_fields['Employee']['valueObject']['Address']['valueAddress'].get('streetAddress', ''))
        print('Confidence:', document_fields['Employee']['valueObject']['Address']['confidence'] * 100.0, '%')

    if document_fields.get('WagesTipsAndOtherCompensation'):
        print('Box1:', document_fields['WagesTipsAndOtherCompensation']['content'])
        print('Confidence:', document_fields['WagesTipsAndOtherCompensation']['confidence'] * 100.0, '%')

    if document_fields.get('FederalIncomeTaxWithheld'):
        print('Box2:', document_fields['FederalIncomeTaxWithheld']['content'])
        print('Confidence:', document_fields['FederalIncomeTaxWithheld']['confidence'] * 100.0, '%')

    if document_fields.get('SocialSecurityWages'):
        print('Box3:', document_fields['SocialSecurityWages']['content'])
        print('Confidence:', document_fields['SocialSecurityWages']['confidence'] * 100.0, '%')

    if document_fields.get('SocialSecurityTaxWithheld'):
        print('Box4:', document_fields['SocialSecurityTaxWithheld']['content'])
        print('Confidence:', document_fields['SocialSecurityTaxWithheld']['confidence'] * 100.0, '%')
    
    if document_fields.get('MedicareWagesAndTips'):
        print('Box5:', document_fields['MedicareWagesAndTips']['content'])
        print('Confidence:', document_fields['MedicareWagesAndTips']['confidence'] * 100.0, '%')

    if document_fields.get('MedicareTaxWithheld'):
        print('Box6:', document_fields['MedicareTaxWithheld']['content'])
        print('Confidence:', document_fields['MedicareTaxWithheld']['confidence'] * 100.0, '%')

    if document_fields.get('SocialSecurityTips'):
        print('Box7:', document_fields['SocialSecurityTips']['content'])
        print('Confidence:', document_fields['SocialSecurityTips']['confidence'] * 100.0, '%')
    
    if document_fields.get('AllocatedTips'):
        print('Box8:', document_fields['AllocatedTips']['content'])
        print('Confidence:', document_fields['AllocatedTips']['confidence'] * 100.0, '%')
    
    if document_fields.get('DependentCareBenefits'):
        print('Box10:', document_fields['DependentCareBenefits']['content'])
        print('Confidence:', document_fields['DependentCareBenefits']['confidence'] * 100.0, '%')
    
    if document_fields.get('NonQualifiedPlans'):
        print('Box11:', document_fields['NonQualifiedPlans']['content'])
        print('Confidence:', document_fields['NonQualifiedPlans']['confidence'] * 100.0, '%')

    # box 12a - 12d
    abcd = ['12a', '12b', '12c', '12d']
    if document_fields.get('AdditionalInfo'):
        for indx, value_field in enumerate(document_fields['AdditionalInfo']['valueArray']):
            if 'LetterCode' in value_field['valueObject']:
                print(f'Box{abcd[indx]}', 'Letter:', value_field['valueObject']['LetterCode']['valueString'])
            else:
                print(f'Box{abcd[indx]}', None)

            if 'Amount' in value_field['valueObject']:
                print(f'Box{abcd[indx]}', 'Amount:', value_field['valueObject']['Amount']['content'])

    if document_fields.get('IsStatutoryEmployee'):
        print('Box13 Statutory Employee:', document_fields['IsStatutoryEmployee']['valueString'])
      
    if document_fields.get('IsRetirementPlan'):
        print('Box13 Retire Plan:', document_fields['IsRetirementPlan']['valueString'])
      
    if document_fields.get('IsThirdPartySickPay'):
        print('Box13 Third-Party Sick Pay:', document_fields['IsThirdPartySickPay']['valueString'])

    if document_fields.get('StateTaxInfos'):
        for indx, value_field in enumerate(document_fields['StateTaxInfos']['valueArray']):
            print(f'state_{indx+1}_Box15a:', value_field['valueObject']['State']['content'])
            print(f'state_{indx+1}_Box15b:', value_field['valueObject']['EmployerStateIdNumber']['content'])
            print(f'state_{indx+1}_Box16:', value_field['valueObject']['StateWagesTipsEtc']['content'])
            print(f'state_{indx+1}_Box17:', value_field['valueObject']['StateIncomeTax']['content'])

    if document_fields.get('LocalTaxInfos'):
        for indx, value_field in enumerate(document_fields['LocalTaxInfos']['valueArray']):
            print(f'local_{indx+1}_Box18:', value_field['valueObject']['LocalWagesTipsEtc']['content'])
            print(f'local_{indx+1}_Box19:', value_field['valueObject']['LocalIncomeTax']['content'])
            print(f'local_{indx+1}_Box20:', value_field['valueObject']['LocalityName']['content'])

    if document_fields.get('Other'):
        print('Box14:', document_fields['Other']['content'])
        print('Confidence:', document_fields['Other']['confidence'] * 100.0, '%')

    print('-----------------------------------')