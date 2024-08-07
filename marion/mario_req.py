import re

content = 'GASetCell(INSPGRIDObj, "0|0|201~1|0|201 FINAL ELECTRIC WITH POWER RELEASE~2|0|11/18/2022~3|0|11/15/2022~4|0|(81) DISAPPROVED - NO FEES~0|1|208~1|1|208 ROUGH ELECTRIC~2|1|7/1/2022~3|1|7/1/2022~4|1|(90) APPROVED~0|2|210~1|2|210 ELE UNDERGROUND~2|2|10/14/2022~3|2|10/14/2022~4|2|(90) APPROVED~0|3|213~1|3|213 PRELIMINARY POWER RELEASE~2|3|10/14/2022~3|3|10/14/2022~4|3|(90) APPROVED~0|4|241~1|4|241 FINAL PLUMBING~2|4|11/21/2022~3|4|11/18/2022~4|4|(90) APPROVED~0|5|241~1|5|241 FINAL PLUMBING~2|5|11/15/2022~3|5|11/15/2022~4|5|(81) DISAPPROVED - NO FEES~0|6|241~1|6|241 FINAL PLUMBING~2|6|11/2/2022~3|6|11/2/2022~4|6|(81) DISAPPROVED - NO FEES~0|7|243~1|7|243 ROUGH PLUMBING~2|7|5/5/2022~3|7|5/3/2022~4|7|(75) CANCEL~0|8|243~1|8|243 ROUGH PLUMBING~2|8|5/3/2022~3|8|5/3/2022~4|8|(90) APPROVED~0|9|243~1|9|243 ROUGH PLUMBING~2|9|3/10/2022~3|9|3/9/2022~4|9|(75) CANCEL~0|10|243~1|10|243 ROUGH PLUMBING~2|10|3/9/2022~3|10|3/9/2022~4|10|(81) DISAPPROVED - NO FEES~0|11|244~1|11|244 SECOND ROUGH PLUMBING~2|11|6/27/2022~3|11|6/27/2022~4|11|(90) APPROVED~0|12|245~1|12|245 SEWER/SEPTIC HOOK-UP~2|12|11/2/2022~3|12|11/2/2022~4|12|(90) APPROVED~0|13|245~1|13|245 SEWER/SEPTIC HOOK-UP~2|13|10/26/2022~3|13|10/22/2022~4|13|(75) CANCEL~");'

# Extracting data using regular expressions
pattern = r"\d\|\d\|([\w\s]+) ~\d\|\d\|([\w\s]+)~\d\|\d\|([\d/]+)"
matches = re.findall(pattern, content)
pattern = r"(\d+)\|(\d+)\|([\w\s/]+)~(\d+)\|(\d+)\|([\w\s/-]+)~(\d+)\|(\d+)\|([\w\s/-]+)~(\d+)\|(\d+)\|\((\d+)\) ([\w\s/-]+)"
matches = re.findall(pattern, content)

# Printing extracted data
for match in matches:
    print("Inspection Number:", match[0])
    print("Description:", match[1])
    print("Start Date:", match[2])
    print("End Date:", match[5])
    print("Status:", match[10])
    print()


# Printing extracted data
for match in matches:
    print("Name:", match[0])
    print("Title:", match[1])
    print("Expiration Date:", match[2])
    print()
