"""
# Please install pandas like below before running this script
# pip install pandas
# Run: python3 tx_anoymizer.py <File Name>
"""
import argparse

import pandas as pd

parser = argparse.ArgumentParser(description='csv to anonymise')
parser.add_argument('file', help='csv file to import', action='store')
args = parser.parse_args()
csv_file = args.file

names = ['branch_number','account_code','account_number','cycle_number','transaction_details_number','cleared_transaction_category','transaction_type','registration_category','transaction_type_breakdown','not_applicable_for_bookkeeping','correction_indication','correction_reason_code','input_type_code','terminal_transaction_mode','processing_date','processing_time','processing_store_number','terminal_installation_store_number','terminal_machine_number','slip_binding_serial_number','operator_id','seat_id','account_date','start_date','overtime_cd_display','external_account_display','priority_deposit_display','corrected_original_transaction_details_number','parent_transaction_details_number','external_input_category','input_output_category','transaction_amount','abstract_code','other_hand_code','cheque_bill_category','cheque_bill_number','convenience_store_atm_number','convenience_store_atm_serial_number','convenience_store_atm_date','linkage_category','linkage_store_number','linkage_cif_number','linkage_account_code','linked_account_number','linked_transaction_statement_number','authentication_method','atm_palm_authentication','basic_transaction_type','setting_change_type','additional_transaction_category','additional_transaction_details','kana_remarks','invalid1','invalid2','invalid3','invalid4','invalid5','invalid6','invalid7','invalid8','invalid9','invalid10']
dataset = pd.read_csv(csv_file, header=None, encoding='shift-jis', names=names, dtype=str)

branch_number = dataset['branch_number'].astype(str) 
account_code = dataset['account_code'].astype(str) 
account_number = dataset['account_number'].astype(str)  
cycle_number = dataset['cycle_number'].astype(str)  
transaction_details_number = dataset['transaction_details_number'].astype(str)  
cleared_transaction_category = dataset['cleared_transaction_category'].astype(str) 
transaction_type = dataset['transaction_type'].astype(str)  
registration_category = dataset['registration_category'].astype(str)  
transaction_type_breakdown = dataset['transaction_type_breakdown'].astype(str)  
not_applicable_for_bookkeeping = dataset['not_applicable_for_bookkeeping'].astype(str)  
correction_indication = dataset['correction_indication'].astype(str)  
correction_reason_code = dataset['correction_reason_code'].astype(str) 
input_type_code = dataset['input_type_code'].astype(str) 
terminal_transaction_mode = dataset['terminal_transaction_mode'].astype(str) 
processing_date = dataset['processing_date'].astype(str) 
processing_time = dataset['processing_time'].astype(str) 
processing_store_number = dataset['processing_store_number'].astype(str) 
terminal_installation_store_number = dataset['terminal_installation_store_number'].astype(str) 
terminal_machine_number = dataset['terminal_machine_number'].astype(str) 
slip_binding_serial_number = dataset['slip_binding_serial_number'].astype(str) 
operator_id = dataset['operator_id'].astype(str) 
seat_id = dataset['seat_id'].astype(str) 
account_date = dataset['account_date'].astype(str) 
start_date = dataset['start_date'].astype(str) 
overtime_cd_display = dataset['overtime_cd_display'].astype(str) 
external_account_display = dataset['external_account_display'].astype(str) 
priority_deposit_display = dataset['priority_deposit_display'].astype(str) 
corrected_original_transaction_details_number = dataset['corrected_original_transaction_details_number'].astype(str) 
parent_transaction_details_number = dataset['parent_transaction_details_number'].astype(str) 
external_input_category = dataset['external_input_category'].astype(str) 
input_output_category = dataset['input_output_category'].astype(str) 
transaction_amount = dataset['transaction_amount'].astype(str) 
abstract_code = dataset['abstract_code'].astype(str) 
other_hand_code = dataset['other_hand_code'].astype(str) 
cheque_bill_category = dataset['cheque_bill_category'].astype(str) 
cheque_bill_number = dataset['cheque_bill_number'].astype(str) 
convenience_store_atm_number = dataset['convenience_store_atm_number'].astype(str) 
convenience_store_atm_serial_number = dataset['convenience_store_atm_serial_number'].astype(str) 
convenience_store_atm_date = dataset['convenience_store_atm_date'].astype(str) 
linkage_category = dataset['linkage_category'].astype(str) 
linkage_store_number = dataset['linkage_store_number'].astype(str) 
linkage_cif_number = dataset['linkage_cif_number'].astype(str) 
linkage_account_code = dataset['linkage_account_code'].astype(str) 
linked_account_number = dataset['linked_account_number'].astype(str) 
linked_transaction_statement_number = dataset['linked_transaction_statement_number'].astype(str) 
authentication_method = dataset['authentication_method'].astype(str) 
atm_palm_authentication = dataset['atm_palm_authentication'].astype(str) 
basic_transaction_type = dataset['basic_transaction_type'].astype(str) 
setting_change_type = dataset['setting_change_type'].astype(str) 
additional_transaction_category = dataset['additional_transaction_category'].astype(str) 
additional_transaction_details = dataset['additional_transaction_details'].astype(str) 
kana_remarks = dataset['kana_remarks'].astype(str).replace('nan', '')

"""
1.摘要コードが、「5：振込」「51：振込」「119：振込」「518：振込」の場合に、
　「カナ摘要」の項目を削除する。
　（行削除ではなく、項目のクリア）
　ただし、「カナ摘要」に「(ｶ」「ｶ)」を含む場合は削除の対象外
"""
new_kana_remark = []
target_codes = [5,51,119,518]
for i, code in enumerate(abstract_code):
    if int(code) in target_codes:
      if len(kana_remarks[i]) != 0 and "ｶ)" not in kana_remarks[i] and "(ｶ" not in kana_remarks[i]:
        new_kana_remark.append("deleted")
      else:
        new_kana_remark.append(kana_remarks[i])
    else:
      new_kana_remark.append(kana_remarks[i])

"""
2.追加取明区分に個人名が入るパターン
　摘要コード＝ZERO＆基本取明区分＝82＆設定変更区分＝1　と
　摘要コード＝ZERO＆基本取明区分＝82＆設定変更区分＝2　
　の場合に、「追加取明区分」の項目を削除する。
　（行削除ではなく、項目のクリア）
"""
new_additional_transaction_category = []
for i,code in enumerate(abstract_code):
    if int(code) == 0 and int(basic_transaction_type[i]) == 82 and int(setting_change_type[i]) in [1, 2]:
      new_additional_transaction_category.append("deleted")
    else:
      new_additional_transaction_category.append(additional_transaction_category[i])

df = pd.DataFrame({
  'branch_number' : branch_number,
  'account_code' : account_code,
  'account_number' : account_number,
  'cycle_number' : cycle_number,
  'transaction_details_number' : transaction_details_number,
  'cleared_transaction_category' : cleared_transaction_category,
  'transaction_type' : transaction_type,
  'registration_category' : registration_category,
  'transaction_type_breakdown' : transaction_type_breakdown,
  'not_applicable_for_bookkeeping' : not_applicable_for_bookkeeping,
  'correction_indication' : correction_indication,
  'correction_reason_code' : correction_reason_code,
  'input_type_code' : input_type_code,
  'terminal_transaction_mode' : terminal_transaction_mode,
  'processing_date' : processing_date,
  'processing_time' : processing_time,
  'processing_store_number' : processing_store_number,
  'terminal_installation_store_number' : terminal_installation_store_number,
  'terminal_machine_number' : terminal_machine_number,
  'slip_binding_serial_number' : slip_binding_serial_number,
  'operator_id' : operator_id,
  'seat_id' : seat_id,
  'account_date' : account_date,
  'start_date' : start_date,
  'overtime_cd_display' : overtime_cd_display,
  'external_account_display' : external_account_display,
  'priority_deposit_display' : priority_deposit_display,
  'corrected_original_transaction_details_number' : corrected_original_transaction_details_number,
  'parent_transaction_details_number' : parent_transaction_details_number,
  'external_input_category' : external_input_category,
  'input_output_category' : input_output_category,
  'transaction_amount' : transaction_amount,
  'abstract_code' : abstract_code,
  'other_hand_code' : other_hand_code,
  'cheque_bill_category' : cheque_bill_category,
  'cheque_bill_number' : cheque_bill_number,
  'convenience_store_atm_number' : convenience_store_atm_number,
  'convenience_store_atm_serial_number' : convenience_store_atm_serial_number,
  'convenience_store_atm_date' : convenience_store_atm_date,
  'linkage_category' : linkage_category,
  'linkage_store_number' : linkage_store_number,
  'linkage_cif_number' : linkage_cif_number,
  'linkage_account_code' : linkage_account_code,
  'linked_account_number' : linked_account_number,
  'linked_transaction_statement_number' : linked_transaction_statement_number,
  'authentication_method' : authentication_method,
  'atm_palm_authentication' : atm_palm_authentication,
  'basic_transaction_type' : basic_transaction_type,
  'setting_change_type' : setting_change_type,
  'new_additional_transaction_category' : new_additional_transaction_category,
  'additional_transaction_details' : additional_transaction_details,
  'new_kana_remark' : new_kana_remark
})

df.to_csv('tx_anonymized.csv', index=False, header=None)
