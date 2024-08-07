import scrapy
import json
import requests
import re
from parsel import Selector

def extract(response):
    item={}
    if response.xpath('//form/@action').get('').strip():
        item['link']=response.xpath('//form/@action').get('').strip()
        item['track_id']=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        item['SessionID']=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        item['WindowID']=response.xpath('//input[@name="IW_WindowID_"]/@value').get('').strip()
    else:
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        item['IW_SessionID_']=value.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        item['IW_TrackID_']=value.xpath("//input[@name='IW_TrackID_']/@value").get('').strip()
        try:
            item['link']=re.findall(r'\<\!\[CDATA\[IW\.post\(\"(.*?)\"\,',response.text)[0]
        except:
            item['link']=''
        item['submit']=value.xpath('//submit/text()').get('').strip()
        if item['submit']:
            item['id']=item['submit'].split('/')[-2]
            item['track_id']=value.xpath('//trackid/text()').get('').strip()
    return item

class ExampleSpider(scrapy.Spider):
    name = 'test_mario'
    json_string =''' {
    "parse_payload": {
        "IW_width": "507",
        "IW_height": "798",
        "IW_dpr": "1.25",
        "IW_SessionID_": "",
        "IW_TrackID_": "",
        "IW_WindowID_": ""
    }, "parse_detail_payload": {
        "IW_FormName": "FrmStart",
        "IW_FormClass": "TFrmStart",
        "IW_width": "652",
        "IW_height": "783",
        "IW_Action": "BTNPERMITS",
        "IW_ActionParam": "",
        "IW_Offset": ""
    }, "parse_details_payload_1": {
        "EDTPERMITNBR": "",
        "BTNGUESTLOGIN": "",
        "IW_FormName": "FrmMain",
        "IW_FormClass": "TFrmMain",
        "IW_width": "652",
        "IW_height": "783",
        "IW_Action": "BTNGUESTLOGIN",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "10",
        "IW_WindowID_": "I1"
    },
    "parse_details_payload_3": {
        "EDTPERMITNBR": "",
        "IW_FormName": "FrmMain",
        "IW_FormClass": "TFrmMain",
        "IW_width": "1903",
        "IW_height": "620",
        "IW_Action": "EDTPERMITNBR",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "12",
        "IW_WindowID_": ""
    }, "parse_details_callback_payload": {
        "EDTPERMITNBR": "",
        "IW_FormName": "FrmMain",
        "IW_FormClass": "TFrmMain",
        "IW_width": "1903",
        "IW_height": "620",
        "IW_Action": "EDTPERMITNBR",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "",
        "IW_WindowID_": ""
    }, "BTNGUESTLOGIN_payload": {
        "BTNGUESTLOGIN": "",
        "IW_FormName": "FrmMain",
        "IW_FormClass": "TFrmMain",
        "IW_width": "1386",
        "IW_height": "904",
        "IW_Action": "BTNGUESTLOGIN",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "",
        "IW_WindowID_": ""
    }, "parse_view_option_payload": {
        "BTNVIEWCERT": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWCERT",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    }, "parse_details_inside_navigation_payload": {
        "IW_FormName": "FrmCertDetail",
        "IW_FormClass": "TFrmCertDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "IMGBACK",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "22",
        "IW_WindowID_": ""
    }, "parse_inspection_option_payload": {
        "BTNVIEWINSPECTIONS": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWINSPECTIONS",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    }, "parse_review_option_paylaod": {
        "BTNVIEWPLANREVIEWS": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWPLANREVIEWS",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    },"parse_subs_option_paylaod": {
        "BTNSUBS": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNSUBS",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    },"parse_impact_option_paylaod": {
        "BTNVIEWFEES": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWFEES",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    },"parse_cos_option_paylaod": {
        "BTNVIEWCOS": "",
        "IW_FormName": "FrmPermitDetail",
        "IW_FormClass": "TFrmPermitDetail",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWCOS",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    }
}'''
    
    headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://cdplusmobile.marioncountyfl.org',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
   
    payloads=json.loads(json_string)

    
    
    def start_requests(self):
        with open("generated_numbers.txt", 'r') as file:
            lines = file.readlines()
        for iddd in lines:
            ids = iddd.strip()
            self.log(f'===============>{ids}')
            url="https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll"
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)
    
    def parse(self,response,ids):
        item=extract(response)
        payload={
        "IW_width": "507",
        "IW_height": "798",
        "IW_dpr": "1.25",
        "IW_SessionID_":item['SessionID'] ,
        "IW_TrackID_": item['track_id'],
        "IW_WindowID_":item['WindowID'] 
        }
        url=f"https://cdplusmobile.marioncountyfl.org{item['link']}"
        yield scrapy.FormRequest(url,callback=self.parse_detail,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)
    
    def parse_detail(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNPERMITS.DoOnAsyncClick&x=126&y=38&which=0&modifiers="
        self.payloads['parse_detail_payload']
        yield scrapy.FormRequest(url,callback=self.parse_details,formdata=self.payloads['parse_detail_payload'],headers=self.headers,cb_kwargs={'ids':ids})

    def parse_details(self,response,ids):
        item=extract(response)
        payload={
            'IW_SessionID_':item['IW_SessionID_'],
            'IW_TrackID_': item['IW_TrackID_']
        }
        url=f"https://cdplusmobile.marioncountyfl.org{item['link']}"
        yield scrapy.FormRequest(url,callback=self.parse_details_1,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_1(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org/{link}$/callback?callback=BTNGUESTLOGIN.DoOnAsyncClick&x=107&y=23&which=0&modifiers="
        id=link.split('/')[-2]
        payload=self.payloads["parse_details_payload_1"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=id
        yield scrapy.FormRequest(url,callback=self.parse_details_2,formdata=self.payloads["parse_details_payload_1"],headers=self.headers,cb_kwargs={'ids':ids})
    
    def parse_details_2(self,response,ids):
        item=extract(response)
        payload={
            'IW_SessionID_':item['id'],
            'IW_TrackID_':item['track_id']
        }
        url=f'https://cdplusmobile.marioncountyfl.org{item["submit"]}'
        yield scrapy.FormRequest(url,callback=self.parse_details_3,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_3(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        id=link.split('/')[-2]
        payload=self.payloads["parse_details_payload_3"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=id
        yield scrapy.FormRequest(url,callback=self.parse_details_callback,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_callback(self,response,ids):
        item=extract(response)
        url=f"https://cdplusmobile.marioncountyfl.org{item['submit']}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        payload=self.payloads["parse_details_payload_3"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=item['id']
        payload['IW_TrackID_']=item['track_id']
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_one,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_callback_one(self,response,ids):
        item=extract(response)
        url=f"https://cdplusmobile.marioncountyfl.org{item['submit']}/$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=86&char=V&modifiers=CTRL_MASK"
        payload=self.payloads["parse_details_payload_3"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=item['id']
        payload['IW_TrackID_']=item['track_id']
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_two,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_callback_two(self,response,ids):
        item=extract(response)
        url=f"https://cdplusmobile.marioncountyfl.org{item['submit']}/$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=17&char=%11&modifiers="
        payload=self.payloads["parse_details_payload_3"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=item['id']
        payload['IW_TrackID_']=item['track_id']
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_three,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_callback_three(self,response,ids):
        item=extract(response)
        url=f"https://cdplusmobile.marioncountyfl.org{item['submit']}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        payload=self.payloads["parse_details_payload_3"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=item['id']
        payload['IW_TrackID_']=item['track_id']
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_four,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_callback_four(self,response,ids):
        item=extract(response)
        url=f"https://cdplusmobile.marioncountyfl.org{item['submit']}$/callback?callback=BTNGUESTLOGIN.DoOnAsyncClick&x=104&y=34&which=0&modifiers="
        payload=self.payloads["BTNGUESTLOGIN_payload"]
        payload["EDTPERMITNBR"]=ids
        payload["IW_SessionID_"]=item['id']
        payload['IW_TrackID_']=item['track_id']
        yield scrapy.FormRequest(url,callback=self.parse_details_product,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)

    def parse_details_product(self,response,ids):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id, 
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_check,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids,"session_id":id},dont_filter=True)

    async def parse_details_check(self,response,ids,session_id):
        item = {}
        item['Permit #'] = response.xpath('//*[contains(@class,"IWDBEDIT1CSS")]/@value').get('').strip()
        item['Permit Status'] = response.xpath('//*[contains(@class,"IWDBEDIT2CSS")]/@value').get('').strip()
        item['Permit #'] = response.xpath('//*[contains(@class,"IWDBEDIT1CSS")]/@value').get('').strip()
        item['Permit Status'] = response.xpath('//*[contains(@class,"IWDBEDIT2CSS")]/@value').get('').strip()
        item['Type'] = response.xpath('//*[contains(@class,"IWDBEDIT12CSS")]/@value').get('').strip()
        item['Type_1'] = response.xpath('//*[contains(@class,"IWDBEDIT3CSS")]/@value').get('').strip()
        item['Address'] = response.xpath('//*[contains(@class,"IWDBEDIT5CSS")]/@value').get('').strip()
        item['Parcel'] = response.xpath('//*[contains(@class,"IWDBEDIT14CSS")]/@value').get('').strip()
        item['Owner'] = response.xpath('//*[contains(@class,"IWDBEDIT4CSS")]/@value').get('').strip()
        item['DBA'] = response.xpath('//*[contains(@class,"IWDBEDIT6CSS")]/@value').get('').strip()
        item['Job Desc'] = response.xpath('//*[contains(@class,"IWDBMEMO1CSS")]/text()').get('').strip()
        item['Apply Date'] = response.xpath('//*[contains(@class,"IWDBEDIT13CSS")]/@value').get('').strip()
        item['Issued Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT8CSS")]/@value').get('').strip()
        item['CO Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT7CSS")]/@value').get('').strip()
        item['Expiration Date'] = response.xpath('//*[contains(@class,"IWDBEDIT9CSS")]/@value').get('').strip()
        item['Last Inspection Request'] = response.xpath('//*[contains(@class,"IWDBEDIT10CSS")]/@value').get('').strip()
        item['CO Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT7CSS")]/@value').get('').strip()
        item['Last Inspection Result'] = response.xpath('//*[contains(@class,"IWDBEDIT11CSS")]/@value').get('').strip()
        
        reviews_count=int(re.findall(r'RGNBTNVIEWPLANREVIEWS.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        impact_fees_count=int(re.findall(r'RGNBTNVIEWFEES.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        inspection_count=int(re.findall(r'RGNBTNVIEWINSPECTIONS.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        subs_count=int(re.findall(r'RGNBTNSUBS.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        cos_count=int(re.findall(r'RGNBTNVIEWCOS.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        premit_holds_count=int(re.findall(r'RGNBTNPERMITHOLDS.*(?:\'|\")data\-badge(?:\'|\")\,(?:\'|\")(\d+)(?:\'|\")\)\;',response.text)[0])
        headers = response.request.headers
        decoded_headers = {key.decode('utf-8'): [value_item.decode('utf-8') for value_item in value] if isinstance(value, list) else value.decode('utf-8') for key, value in headers.items()}
        item['inspection'] = []
        item['review'] = []
        item['review_released_by'] = ''
        item['COS'] = []
        item['impact_fee'] = []
        item['impact_total_pending'] = ''
        item['impact_total_paid'] = ''
        item['subs'] = []
        item['Permit Holds'] = []

        link=response.xpath('//form/@action').get('').strip()
        try:
            view_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWCERT.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            view_response = self.view_ping(view_tab_url,session_id,item)
        except:
            pass
        if inspection_count>0:
            inspection_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWINSPECTIONS.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            inspection_response = self.id_ping(inspection_tab_url,session_id,item) 
            item['inspection'] = inspection_response
        if reviews_count >0:
            review_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWPLANREVIEWS.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            review_response = self.review_ping(review_tab_url,session_id,item)
        if subs_count>0 :
            subs_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNSUBS.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            subs_response = self.subs_ping(subs_tab_url,session_id,item)
        if impact_fees_count>0:
            impact_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWFEES.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            impact_response = self.impact_ping(impact_tab_url,session_id,item)
        if cos_count>0:
            cos_tab_url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWCOS.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
            cos_response = self.cos_ping(cos_tab_url,session_id,item)

        yield item


    def view_ping(self,view_tab_url,session_id,item):
        data = ''
        payload=self.payloads['parse_view_option_payload']
        payload['IW_SessionID_'] = session_id
        view_response = requests.request("POST", view_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',view_response.text)[0]
        view_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_view={"IW_SessionID_":session_id,"IW_TrackID_":"33"}
        view_detail = requests.request("POST", view_url, headers=self.headers, data=payload_view)
        view_detail_response = Selector(text=view_detail.text)
        item['DBA_Address'] = view_detail_response.xpath('//span[contains(text(),"Address:")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Qualifier'] = view_detail_response.xpath('//span[contains(text(),"Qualifier")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Status'] = view_detail_response.xpath('//span[contains(text(),"Status:")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Class'] = ' '.join(view_detail_response.xpath('//span[@class="IWDBLABEL4CSS"]/text()|//span[@class="IWDBLABEL12CSS"]/text()').getall())
        item['DBA_State'] = view_detail_response.xpath('//span[contains(text(),"State #")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Country'] = view_detail_response.xpath('//span[contains(text(),"County #")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Email'] = view_detail_response.xpath('//span[contains(text(),"Email:")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Phone'] = view_detail_response.xpath('//span[contains(text(),"Phone:")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Fax'] = view_detail_response.xpath('//span[contains(text(),"Fax:")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Expire_Date'] = view_detail_response.xpath('//span[contains(text(),"Expire Date")]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Expire_Date_2'] = view_detail_response.xpath('//span[@class="IWLABEL14CSS"]/following-sibling::span[1]/text()').get('').strip()
        item['DBA_Record_Count'] =view_detail_response.xpath('//span[contains(text(),"Record Count:")]/following-sibling::span[1]/text()').get('').strip()
        empty_list = []
        for i in  view_detail_response.xpath('//table[@id="ASGRID_"]/tr')[1:-1]:
            dic_inspec={}
            code  = i.xpath('./td[1]/font/div/text()').get('').replace('\xa0','')
            if code:
                dic_inspec['Name'] = code
            description  = i.xpath('./td[2]/font/div/text()').get('').replace('\xa0','')
            if code:
                dic_inspec['Title'] = description
            request_date  = i.xpath('./td[3]/font/div/text()').get('').replace('\xa0','')
            if code:
                dic_inspec['Expire_date'] = request_date
            
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]

        item['Authorized signers'] = data
        self.back_button(IW_FormName='FrmCertDetail',IW_FormClass='TFrmCertDetail',submit=submit,session_id=session_id)
        return item

    def cos_ping(self,cos_tab_url,session_id,item): 
        data = ''   
        payload=self.payloads['parse_cos_option_paylaod']
        payload['IW_SessionID_'] = session_id
        cos_response = requests.request("POST", cos_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',cos_response.text)[0]
        cos_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_cos={"IW_SessionID_":session_id,"IW_TrackID_":"39"}
        cos_detail = requests.request("POST", cos_url, headers=self.headers, data=payload_cos)
        cos_response = Selector(text=cos_detail.text)
        empty_list = []
        for i in  cos_response.xpath('//table[@id="COGRID_"]/tr')[1:-1]:
            dic_inspec={}
            code  = i.xpath('./td[1]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['co #'] = code
            status  = i.xpath('./td[2]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['co type'] = status
            out_date  = i.xpath('./td[3]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['status'] = out_date
            released = i.xpath('./td[4]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['issued_date'] = released
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]
        item['COS'] = data
        self.back_button(IW_FormName='FrmFees',IW_FormClass='TFrmFees',submit=submit,session_id=session_id)
        return item
    def impact_ping(self,impact_tab_url,session_id,item): 
        data = ''   
        payload=self.payloads['parse_impact_option_paylaod']
        payload['IW_SessionID_'] = session_id
        impact_response = requests.request("POST", impact_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',impact_response.text)[0]
        impact_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_impact={"IW_SessionID_":session_id,"IW_TrackID_":"39"}
        impact_detail = requests.request("POST", impact_url, headers=self.headers, data=payload_impact)
        impact_response = Selector(text=impact_detail.text)
        empty_list = []
        for i in  impact_response.xpath('//table[@id="FEESGRID_"]/tr')[1:-1]:
            import time
            time.sleep(1)
            dic_inspec={}
            fee  = i.xpath('./td[1]/font/div/text()').get('')
            if '\xa0' not in fee:
                dic_inspec['fee'] = fee
            description  = i.xpath('./td[2]/font/div/text()').get('')
            if '\xa0' not in description:
                dic_inspec['description'] = description
            amt_due  = i.xpath('./td[3]/font/div/text()').get('')
            if '\xa0' not in amt_due:
                dic_inspec['amt_due'] = amt_due
            amt_paid = i.xpath('./td[4]/font/div/text()').get('')
            if '\xa0' not in amt_paid:
                dic_inspec['amt_paid'] = amt_paid
            status = i.xpath('./td[5]/font/div/text()').get('')
            if '\xa0' not in status:
                dic_inspec['status'] = status
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]
        item['impact_fee'] = data
        item['impact_total_pending'] = impact_response.xpath('//span[contains(text(),"TOTAL PENDING")]/following-sibling::span[1]/text()').get('').strip()
        item['impact_total_paid'] = impact_response.xpath('//span[contains(text(),"TOTAL PAID")]/following-sibling::span[1]/text()').get('').strip()
        self.back_button(IW_FormName='FrmFees',IW_FormClass='TFrmFees',submit=submit,session_id=session_id)
        return item
    def subs_ping(self,subs_tab_url,session_id,item): 
        data = ''   
        payload=self.payloads['parse_subs_option_paylaod']
        payload['IW_SessionID_'] = session_id
        subs_response = requests.request("POST", subs_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',subs_response.text)[0]
        subs_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_subs={"IW_SessionID_":session_id,"IW_TrackID_":"39"}
        subs_detail = requests.request("POST", subs_url, headers=self.headers, data=payload_subs)
        subs_response = Selector(text=subs_detail.text)
        empty_list = []
        for i in  subs_response.xpath('//table[@id="SUBSGRID_"]/tr')[1:-1]:
            dic_inspec={}
            dba  = i.xpath('./td[1]/font/div/text()').get('')
            if '\xa0' not in dba:
                dic_inspec['DBA'] = dba
            type_dba  = i.xpath('./td[2]/font/div/text()').get('')
            if '\xa0' not in type_dba:
                dic_inspec['TYPE'] = type_dba
            status  = i.xpath('./td[3]/font/div/text()').get('')
            if '\xa0' not in status:
                dic_inspec['STATUS'] = status
            start_date = i.xpath('./td[4]/font/div/text()').get('')
            if '\xa0' not in start_date:
                dic_inspec['START_DATE'] = start_date
            end_date = i.xpath('./td[5]/font/div/text()').get('')
            if '\xa0' not in end_date:
                dic_inspec['END_DATE'] = end_date
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]
        item['subs'] = data
        self.subs_back_button(IW_FormName='FrmSubContractors',IW_FormClass='TFrmSubContractors',submit=submit,session_id=session_id)
        return item        
    def review_ping(self,review_tab_url,session_id,item): 
        data = ''   
        payload=self.payloads['parse_review_option_paylaod']
        payload['IW_SessionID_'] = session_id
        inspc_response = requests.request("POST", review_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',inspc_response.text)[0]
        review_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_ins={"IW_SessionID_":session_id,"IW_TrackID_":"39"}
        review_detail = requests.request("POST", review_url, headers=self.headers, data=payload_ins)
        review_response = Selector(text=review_detail.text)
        empty_list = []
        for i in  review_response.xpath('//table[@id="PRGRID_"]/tr')[1:-1]:
            dic_inspec={}
            code  = i.xpath('./td[1]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['review_department'] = code
            status  = i.xpath('./td[2]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['status'] = status
            out_date  = i.xpath('./td[3]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['out_date'] = out_date
            released = i.xpath('./td[4]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['released'] = released
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]
        item['review'] = data
        item['review_released_by'] = review_response.xpath('//*[contains(text(),"Released By:")]/text()').get('').replace('\r\n',' ').strip()
        self.back_button(IW_FormName='FrmPlanReviews',IW_FormClass='TFrmPlanReviews',submit=submit,session_id=session_id)
        return item
            
    def id_ping(self,inspection_tab_url,session_id,item):     
        payload=self.payloads['parse_inspection_option_payload']
        payload['IW_SessionID_'] = session_id
        inspc_response = requests.request("POST", inspection_tab_url, headers=self.headers, data=payload)
        submit = re.findall(r'post\(\"([^>]*?)\"\,',inspc_response.text)[0]
        ins_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_ins={"IW_SessionID_":session_id,"IW_TrackID_":"19"}
        inspc_detail = requests.request("POST", ins_url, headers=self.headers, data=payload_ins)
        inspec_response = Selector(text=inspc_detail.text)
        empty_list = []
        for i in  inspec_response.xpath('//table[@id="INSPGRID_"]/tr')[1:-1]:
            dic_inspec={}
            code  = i.xpath('./td[1]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['code'] = code
            description  = i.xpath('./td[2]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['description'] = description
            request_date  = i.xpath('./td[3]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['request_date'] = request_date
            result_date = i.xpath('./td[4]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['result_date'] = result_date
            result  = i.xpath('./td[5]/font/div/text()').get('')
            if '\xa0' not in code:
                dic_inspec['result'] = result
            empty_list.append(dic_inspec)
            data = [item for item in empty_list if item]

        detail_inspec_url = inspec_response.xpath('//form/@action').get('').strip()
        inspect_list = []
        for payload_itration in range(len(data)):
            inspec_dict = {}
            hit_one_inspec = self.multiple_inspection_ping(payload_itration,detail_inspec_url)
            hit_two_inspec = self.multiple_inspection_ping(payload_itration,detail_inspec_url)
            ins_1_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
            payload_ins={"IW_SessionID_":session_id,"IW_TrackID_":"29"}
            ins_1_urres = requests.request("POST", ins_1_url, headers=self.headers, data=payload_ins)
            ins_res = Selector(text=ins_1_urres.text)
            inspec_dict['priority'] = ins_res.xpath('//input[@class="IWDBEDIT1CSS"]/@value').get('')
            inspec_dict['inspection_code'] = ins_res.xpath('//input[@class="IWDBEDIT2CSS"]/@value').get('')
            inspec_dict['description'] = ins_res.xpath('//input[@class="IWDBEDIT4CSS"]/@value').get('')
            inspec_dict['request_date'] = ins_res.xpath('//input[@class="IWDBEDIT5CSS"]/@value').get('')
            inspec_dict['scheduled_inspector'] = ins_res.xpath('//input[@class="IWDBEDIT6CSS"]/@value').get('')
            inspec_dict['result_date'] = ins_res.xpath('//input[@class="IWDBEDIT7CSS"]/@value').get('')
            inspec_dict['inspection_results'] = ins_res.xpath('//input[@class="IWDBEDIT9CSS"]/@value').get('')            
            inspec_dict['result_inspector'] = ins_res.xpath('//input[@class="IWDBEDIT8CSS"]/@value').get('')
            inspec_dict['notes'] = ins_res.xpath('//textarea[@class="IWDBMEMO1CSS"]/text()').get('')
            inspect_list.append(inspec_dict)
            IW_FormName = "FrmInspDetail"
            IW_FormClass = "TFrmInspDetail"
            self.back_button(IW_FormName,IW_FormClass,submit,session_id)
            
        self.back_button(IW_FormName='FrmPermitInspections',IW_FormClass='TFrmPermitInspections',submit=submit,session_id=session_id)
         
        return inspect_list

    def multiple_inspection_ping(self,payload_itration,detail_inspec_url):
        inspec_url = f"https://cdplusmobile.marioncountyfl.org{detail_inspec_url}$/callback?callback=INSPGRID.DoAsyncGotoRow"
        parse_review_options_paylaod= {
        "INSPGRID": f"10000000000000|R0|0^0|x||||||gotor{payload_itration}",
        "IW_FormName": "FrmPermitInspections",
        "IW_FormClass": "TFrmPermitInspections",
        "IW_width": "1920",
        "IW_height": "654",
        "IW_Action": "BTNVIEWPLANREVIEWS",
        "IW_ActionParam": "",
        "IW_Offset": "",
        "IW_SessionID_": "",
        "IW_TrackID_": "25",
        "IW_WindowID_": ""
    }
        inspec_hit_response = requests.request("POST", inspec_url, headers=self.headers, data=parse_review_options_paylaod)
        return inspec_hit_response
    
    def back_button(self,IW_FormName,IW_FormClass,submit,session_id):
        url_back=f"https://cdplusmobile.marioncountyfl.org{submit}$/callback?callback=IMGBACK.DoOnAsyncClick&x=25&y=25&which=0&modifiers="
        back_payload={
            "IW_FormName":IW_FormName,
            "IW_FormClass":IW_FormClass,
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"IMGBACK",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":session_id,
            "IW_TrackID_":"16",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        back_hit_response = requests.request("POST", url_back, headers=self.headers, data=back_payload)
        back_form_url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload_click_back={"IW_SessionID_":session_id,"IW_TrackID_":"29"}
        back_response = requests.request("POST", back_form_url, headers=self.headers, data=payload_click_back)
        return back_response
    
    def subs_back_button(self,IW_FormName,IW_FormClass,submit,session_id):
        url_back=f"https://cdplusmobile.marioncountyfl.org{submit}"
        back_payload={
            "BTNSETINACTIVE":"",
            "BTNSETACTIVE":"",
            "BTNADDSUB":"",
            "CBINSPCLASS":"-1",
            "EDTDBA":'',
            "EDTLIC":"",
            "BTNSEARCH":"",
            "CERTSEARCHGRID":"000000|R0|0^0|x|||",
            "BTNSEARCHCLOSE":"",
            "BTNSELECTCERT":"",
            "SUBSGRID":"10000000000000000000|R0|0^0|x|||||",
            "MSGDLGOK":"^isvisible:false",
            "IW_FormName":IW_FormName,
            "IW_FormClass":IW_FormClass,
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"IMGBACK",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":session_id,
            "IW_TrackID_":"16",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        back_hit_response = requests.request("POST", url_back, headers=self.headers, data=back_payload)
        return back_hit_response
        
