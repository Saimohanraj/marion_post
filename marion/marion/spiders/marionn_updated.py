import scrapy
import json
import re
from parsel import Selector

class ExampleSpider(scrapy.Spider):
    name = 'marion_updated'
    # allowed_domains = ['example.com']
    headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://cdplusmobile.marioncountyfl.org',
            'pragma': 'no-cache',
            # 'referer': 'https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/1G5VmezPCZ~XSgnbUlqVbmV3Ota/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            # 'Cookie': 'ak_bmsc=8CE1CB1DEC634307D3D7DFBA5898B13E~000000000000000000000000000000~YAAQ5C/JF3a9B+aOAQAAm2x9PRc/zBl/YckK/qYUK8cWkM/xRIN04wR5C/PeLkpCvDNW+hmcnSqGoMfymETkj0JV6gqnkOh5CQopJMcwXQ2qZBLIB4r3L5SjO3xmwltA6pHOY+PAZaWq64wi6ai2veaIHJr+KzcQ/znkwfTZAyLKLz5elDgx7ifOhY+s4EZ2wCTJk0mCWzmaC2XBBx8H7bV0WoIhgF4e0EaE9Z5XQxEPjLC8XO+bJ0ZCuPvSePwd42Ow9mUvKe0mx945QsfRWJaadOyK4muWBJRI4E/4kUIlSelUVlkfQROIL6ZJkgPlT4IcCr2XzRQxfYcoUEckkiUrMfay9PjleTvZMoAgeIy/iqiX6iKk8BDR/Dx/rLnWAWKtr83Z'
        }
    # start_urls = ['https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections']
    def start_requests(self):
        # file_path = "generated_numbers.txt"
        # with open(file_path, 'r') as file:
        #     lines = file.readlines()
        lines = ['2022010019']    
        for ids in lines:
            print(ids.strip())  
            url="https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll"
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,cb_kwargs={'ids':ids},dont_filter=True)
    
    def parse(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        WindowID=response.xpath('//input[@name="IW_WindowID_"]/@value').get('').strip()
        payload={
        "IW_width": "507",
        "IW_height": "798",
        "IW_dpr": "1.25",
        "IW_SessionID_":SessionID ,
        "IW_TrackID_": track_id,
        "IW_WindowID_":WindowID 
        }
        url=f"https://cdplusmobile.marioncountyfl.org{link}"
        yield scrapy.FormRequest(url,callback=self.parse_detail,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    
    def parse_detail(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNPERMITS.DoOnAsyncClick&x=126&y=38&which=0&modifiers="
        payload={
                "IW_FormName": "FrmStart",
                "IW_FormClass": "TFrmStart",
                "IW_width": "652",
                "IW_height": "783",
                "IW_Action": "BTNPERMITS",
                "IW_ActionParam": "",
                "IW_Offset": "",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})

    def parse_details(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        IW_SessionID_=value.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        IW_TrackID_=value.xpath("//input[@name='IW_TrackID_']/@value").get('').strip()
        link=re.findall(r'\<\!\[CDATA\[IW\.post\(\"(.*?)\"\,',response.text)[0]
        payload={
            'IW_SessionID_':IW_SessionID_,
            'IW_TrackID_': IW_TrackID_
        }
        url=f"https://cdplusmobile.marioncountyfl.org{link}"
        yield scrapy.FormRequest(url,callback=self.parse_details_1,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})

    def parse_details_1(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org/{link}$/callback?callback=BTNGUESTLOGIN.DoOnAsyncClick&x=107&y=23&which=0&modifiers="
        id=link.split('/')[-2]
        # breakpoint()
        payload={
            "EDTPERMITNBR": ids,
            "BTNGUESTLOGIN": "",
            "IW_FormName": "FrmMain",
            "IW_FormClass": "TFrmMain",
            "IW_width": "652",
            "IW_height": "783",
            "IW_Action": "BTNGUESTLOGIN",
            "IW_ActionParam": "",
            "IW_Offset": "",
            "IW_SessionID_": id,
            "IW_TrackID_": "10",
            "IW_WindowID_": "I1",
            "IW_AjaxID": "17147302644146",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_2,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    
    def parse_details_2(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        payload={
            'IW_SessionID_':id,
            'IW_TrackID_':track_id
        }
        url=f'https://cdplusmobile.marioncountyfl.org{submit}'
        yield scrapy.FormRequest(url,callback=self.parse_details_3,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})

    def parse_details_3(self,response,ids):
        link=response.xpath('//form/@action').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        id=link.split('/')[-2]
        payload={
            "EDTPERMITNBR":ids,
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1903",
            "IW_height":"620",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":"12",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_callback,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_callback(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        payload={
            "EDTPERMITNBR":ids,
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1903",
            "IW_height":"620",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_one,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_callback_one(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}/$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=86&char=V&modifiers=CTRL_MASK"
        payload={
            "EDTPERMITNBR":ids,
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1903",
            "IW_height":"620",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_two,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_callback_two(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}/$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=17&char=%11&modifiers="
        payload={
            "EDTPERMITNBR":ids,
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1903",
            "IW_height":"620",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_three,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_callback_three(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        payload={
            "EDTPERMITNBR":ids,
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1903",
            "IW_height":"620",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_four,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_callback_four(self,response,ids):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}$/callback?callback=BTNGUESTLOGIN.DoOnAsyncClick&x=104&y=34&which=0&modifiers="
        payload={
            "BTNGUESTLOGIN":"",
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1386",
            "IW_height":"904",
            "IW_Action":"BTNGUESTLOGIN",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_product,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_product(self,response,ids):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        # breakpoint()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_check,formdata=payload,headers=self.headers,cb_kwargs={'ids':ids})
    def parse_details_check(self,response,ids):
        item = {}
        item['Permit #'] = response.xpath('//*[contains(@class,"IWDBEDIT1CSS")]/@value').get()
        item['Permit Status'] = response.xpath('//*[contains(@class,"IWDBEDIT2CSS")]/@value').get()
        item['Type'] = response.xpath('//*[contains(@class,"IWDBEDIT12CSS")]/@value').get()
        item['Type_1'] = response.xpath('//*[contains(@class,"IWDBEDIT3CSS")]/@value').get()
        item['Address'] = response.xpath('//*[contains(@class,"IWDBEDIT5CSS")]/@value').get()
        item['Parcel'] = response.xpath('//*[contains(@class,"IWDBEDIT14CSS")]/@value').get()
        item['DBA'] = response.xpath('//*[contains(@class,"IWDBEDIT6CSS")]/@value').get()
        item['Job Desc'] = response.xpath('//*[contains(@class,"IWDBMEMO1CSS")]/text()').get()
        item['Apply Date'] = response.xpath('//*[contains(@class,"IWDBEDIT13CSS")]/@value').get()
        item['Issued Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT8CSS")]/@value').get()
        item['CO Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT7CSS")]/@value').get()
        item['Expiration Date'] = response.xpath('//*[contains(@class,"IWDBEDIT9CSS")]/@value').get()
        item['Last Inspection Request'] = response.xpath('//*[contains(@class,"IWDBEDIT10CSS")]/@value').get()
        item['CO Desc'] = response.xpath('//*[contains(@class,"IWDBEDIT7CSS")]/@value').get()
        item['Last Inspection Result'] = response.xpath('//*[contains(@class,"IWDBEDIT11CSS")]/@value').get()
        # yield item
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWCERT.DoOnAsyncClick&x=24&y=21&which=0&modifiers="
        payload={
            "BTNVIEWCERT":"",
            "IW_FormName":"FrmPermitDetail",
            "IW_FormClass":"TFrmPermitDetail",
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"BTNVIEWCERT",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":link.split('/')[-2],
            "IW_TrackID_":track_id,
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_view_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_details_view_navigation(self,response,item):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        # breakpoint()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_inside_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_details_inside_navigation(self,response,item):
        # item ={}
        item['DBA_Address'] = response.xpath('//span[contains(text(),"Address:")]/following-sibling::span[1]/text()').get()
        item['DBA_Qualifier'] = response.xpath('//span[contains(text(),"Qualifier")]/following-sibling::span[1]/text()').get()
        item['DBA_Status'] = response.xpath('//span[contains(text(),"Status:")]/following-sibling::span[1]/text()').get()
        item['DBA_Class'] = ' '.join(response.xpath('//span[@class="IWDBLABEL4CSS"]/text()|//span[@class="IWDBLABEL12CSS"]/text()').getall())
        item['DBA_State'] = response.xpath('//span[contains(text(),"State #")]/following-sibling::span[1]/text()').get()
        item['DBA_Country'] = response.xpath('//span[contains(text(),"County #")]/following-sibling::span[1]/text()').get()
        item['DBA_Email'] = response.xpath('//span[contains(text(),"Email:")]/following-sibling::span[1]/text()').get()
        item['DBA_Phone'] = response.xpath('//span[contains(text(),"Phone:")]/following-sibling::span[1]/text()').get()
        item['DBA_Fax'] = response.xpath('//span[contains(text(),"Fax:")]/following-sibling::span[1]/text()').get()
        item['DBA_Expire_Date'] = response.xpath('//span[contains(text(),"Expire Date")]/following-sibling::span[1]/text()').get()
        item['DBA_Expire_Date_2'] = response.xpath('//span[@class="IWLABEL14CSS"]/following-sibling::span[1]/text()').get()
        item['DBA_Record_Count'] =response.xpath('//span[contains(text(),"Record Count:")]/following-sibling::span[1]/text()').get()
        empty_list = []
        for i in  response.xpath('//table[@id="ASGRID_"]/tr')[1:-1]:
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
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=IMGBACK.DoOnAsyncClick&x=48&y=25&which=0&modifiers="
        payload={
            "IW_FormName":"FrmCertDetail",
            "IW_FormClass":"TFrmCertDetail",
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"IMGBACK",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":link.split('/')[-2],
            "IW_TrackID_":"22",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_details_back_navigation(self,response,item):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_outside_option,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_outside_option(self,response,item):
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWINSPECTIONS.DoOnAsyncClick&x=57&y=18&which=0&modifiers="
        payload={
            "BTNVIEWINSPECTIONS":"",
            "IW_FormName":"FrmPermitDetail",
            "IW_FormClass":"TFrmPermitDetail",
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"BTNVIEWINSPECTIONS",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":link.split('/')[-2],
            "IW_TrackID_":"25",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_inspection_option,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_inspection_option(self,response,item):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_inspection_collection,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    def parse_inspection_collection(self,response,item):
        empty_list = []
        for i in  response.xpath('//table[@id="INSPGRID_"]/tr')[1:-1]:
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
        
        item['inspection'] = data
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=IMGBACK.DoOnAsyncClick&x=25&y=25&which=0&modifiers="
        payload={
            "IW_FormName":"FrmPermitInspections",
            "IW_FormClass":"TFrmPermitInspections",
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"IMGBACK",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":link.split('/')[-2],
            "IW_TrackID_":"16",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_next_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
    def parse_details_next_back_navigation(self,response,item):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_review_option,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
        
    def parse_review_option(self,response,item):
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWPLANREVIEWS.DoOnAsyncClick&x=37&y=20&which=0&modifiers="
        payload={
            "BTNVIEWPLANREVIEWS":"",
            "IW_FormName":"FrmPermitDetail",
            "IW_FormClass":"TFrmPermitDetail",
            "IW_width":"1920",
            "IW_height":"654",
            "IW_Action":"BTNVIEWPLANREVIEWS",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":link.split('/')[-2],
            "IW_TrackID_":"25",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_review_option_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
    def parse_review_option_navigation(self,response,item):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_review_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
    def parse_review_datapoints(self,response,item):
        empty_list = []
        for i in  response.xpath('//table[@id="PRGRID_"]/tr')[1:-1]:
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
        item['review_released_by'] = response.xpath('//*[contains(text(),"Released By:")]/text()').get('').replace('\r\n',' ').strip()
        yield item
    #     link=response.xpath('//form/@action').get('').strip()
    #     track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
    #     SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
    #     url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=IMGBACK.DoOnAsyncClick&x=25&y=32&which=0&modifiers="
    #     payload={
    #         "IW_FormName":"FrmPlanReviews",
    #         "IW_FormClass":"TFrmPlanReviews",
    #         "IW_width":"1920",
    #         "IW_height":"654",
    #         "IW_Action":"IMGBACK",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"22",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_third_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_third_back_navigation(self,response,item):
    #     id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
    #     track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
    #     submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
    #     url=f"https://cdplusmobile.marioncountyfl.org{submit}"
    #     payload={
    #         "IW_SessionID_":id,
    #         "IW_TrackID_":track_id,
            
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_third_navigation_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
    # def parse_third_navigation_datapoints(self,response,item):
    #     link=response.xpath('//form/@action').get('').strip()
    #     track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
    #     SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
    #     url = f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWCOS.DoOnAsyncClick&x=27&y=18&which=0&modifiers="
    #     payload={
    #         "BTNVIEWCOS":"",
    #         "IW_FormName":"FrmPermitDetail",
    #         "IW_FormClass":"TFrmPermitDetail",
    #         "IW_width":"1920",
    #         "IW_height":"654",
    #         "IW_Action":"BTNVIEWCOS",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"25",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_cos_option,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_cos_option(self,response,item):
    #     id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
    #     track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
    #     submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
    #     url=f"https://cdplusmobile.marioncountyfl.org{submit}"
    #     payload={
    #         "IW_SessionID_":id,
    #         "IW_TrackID_":track_id,
            
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_cos_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item})

    # def parse_cos_datapoints(self,response,item):
    #     empty_list = []
    #     for i in  response.xpath('//table[@id="COGRID_"]/tr')[1:-1]:
    #         dic_inspec={}
    #         code  = i.xpath('./td[1]/font/div/text()').get('')
    #         if '\xa0' not in code:
    #             dic_inspec['co #'] = code
    #         status  = i.xpath('./td[2]/font/div/text()').get('')
    #         if '\xa0' not in code:
    #             dic_inspec['co type'] = status
    #         out_date  = i.xpath('./td[3]/font/div/text()').get('')
    #         if '\xa0' not in code:
    #             dic_inspec['status'] = out_date
    #         released = i.xpath('./td[4]/font/div/text()').get('')
    #         if '\xa0' not in code:
    #             dic_inspec['issued_date'] = released
    #         empty_list.append(dic_inspec)
    #         data = [item for item in empty_list if item]
    #     item['COS'] = data
    #     link=response.xpath('//form/@action').get('').strip()
    #     track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
    #     SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
    #     url=f"https://cdplusmobile.marioncountyfl.org{link}"
    #     payload={
    #         "BTNPRINTCOS":"FrmPlanReviews",
    #         "MSGDLGOK":"^isvisible:false",
    #         "COGRID":"100000000000000000|R0|0^0|x||||",
    #         "IW_FormName":"FrmCertOcc",
    #         "IW_FormClass":"TFrmCertOcc",
    #         "IW_width":"1920",
    #         "IW_height":"904",
    #         "IW_Action":"IMGBACK",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"16",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_cos_from_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_cos_from_back_navigation(self,response,item):
    #     link=response.xpath('//form/@action').get('').strip()
    #     url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNVIEWFEES.DoOnAsyncClick&x=69&y=20&which=0&modifiers="
    #     payload={
    #         "BTNVIEWFEES":"",
    #         "IW_FormName":"FrmPermitDetail",
    #         "IW_FormClass":"TFrmPermitDetail",
    #         "IW_width":"1920",
    #         "IW_height":"904",
    #         "IW_Action":"BTNVIEWFEES",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"18",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_impact_fees_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    #     # print(item)
    # def parse_impact_fees_navigation(self,response,item):
    #     id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
    #     track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
    #     submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
    #     url=f"https://cdplusmobile.marioncountyfl.org{submit}"
    #     payload={
    #         "IW_SessionID_":id,
    #         "IW_TrackID_":track_id,
            
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_impact_fees_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_impact_fees_datapoints(self,response,item):
    #     empty_list = []
    #     for i in  response.xpath('//table[@id="FEESGRID_"]/tr')[1:-1]:
    #         dic_inspec={}
    #         Fee  = i.xpath('./td[1]/font/div/text()').get('')
    #         if '\xa0' not in Fee:
    #             dic_inspec['Fee'] = Fee
    #         description  = i.xpath('./td[2]/font/div/text()').get('')
    #         if '\xa0' not in description:
    #             dic_inspec['description'] = description
    #         amt_due  = i.xpath('./td[3]/font/div/text()').get('')
    #         if '\xa0' not in amt_due:
    #             dic_inspec['AMT_DUE'] = amt_due
    #         amt_paid = i.xpath('./td[4]/font/div/text()').get('')
    #         if '\xa0' not in amt_paid:
    #             dic_inspec['AMT_PAID'] = amt_paid
    #         status = i.xpath('./td[5]/font/div/text()').get('')
    #         if '\xa0' not in status:
    #             dic_inspec['STATUS'] = status
    #         empty_list.append(dic_inspec)
    #         data = [item for item in empty_list if item]
    #     item['Impact_fees'] = data
    #     item['Impact_total_pending'] = response.xpath('//span[contains(text(),"TOTAL PENDING")]/following-sibling::span[1]/text()').get('').strip()
    #     item['Impact_total_paid'] = response.xpath('//span[contains(text(),"TOTAL PAID")]/following-sibling::span[1]/text()').get('').strip()
    #     # breakpoint()
    #     link=response.xpath('//form/@action').get('').strip()
    #     track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
    #     SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
    #     url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=IMGBACK.DoOnAsyncClick&x=46&y=16&which=0&modifiers="
    #     payload={
    #         "IW_FormName":"FrmFees",
    #         "IW_FormClass":"TFrmFees",
    #         "IW_width":"1920",
    #         "IW_height":"654",
    #         "IW_Action":"IMGBACK",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"22",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_impact_from_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    #     # yield item
    # def parse_impact_from_back_navigation(self,response,item):
    #     id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
    #     track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
    #     submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
    #     url=f"https://cdplusmobile.marioncountyfl.org{submit}"
    #     payload={
    #         "IW_SessionID_":id,
    #         "IW_TrackID_":track_id,
            
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_impact_to_main_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item},dont_filter=True)
    # def parse_impact_to_main_datapoints(self,response,item):
    #     link=response.xpath('//form/@action').get('').strip()
    #     url=f"https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNSUBS.DoOnAsyncClick&x=69&y=20&which=0&modifiers="
    #     payload={
    #         "BTNSUBS":"",
    #         "IW_FormName":"FrmPermitDetail",
    #         "IW_FormClass":"TFrmPermitDetail",
    #         "IW_width":"1920",
    #         "IW_height":"904",
    #         "IW_Action":"BTNSUBS",
    #         "IW_ActionParam":"",
    #         "IW_Offset":"",
    #         "IW_SessionID_":link.split('/')[-2],
    #         "IW_TrackID_":"18",
    #         "IW_WindowID_":"",
    #         "IW_AjaxID":"17147313511098",
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_main_to_sub_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    #     # print(item)
    # def parse_main_to_sub_datapoints(self,response,item):
    #     id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
    #     track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
    #     submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
    #     url=f"https://cdplusmobile.marioncountyfl.org{submit}"
    #     payload={
    #         "IW_SessionID_":id,
    #         "IW_TrackID_":track_id,
            
    #     }
    #     yield scrapy.FormRequest(url,callback=self.parse_sub_datapoints,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_sub_datapoints(self,response,item):
    #     empty_list = []
    #     for i in  response.xpath('//table[@id="SUBSGRID_"]/tr')[1:-1]:
    #         dic_inspec={}
    #         dba  = i.xpath('./td[1]/font/div/text()').get('')
    #         if '\xa0' not in dba:
    #             dic_inspec['DBA'] = dba
    #         type_dba  = i.xpath('./td[2]/font/div/text()').get('')
    #         if '\xa0' not in type_dba:
    #             dic_inspec['TYPE'] = type_dba
    #         status = i.xpath('./td[3]/font/div/text()').get('')
    #         if '\xa0' not in status:
    #             dic_inspec['STATUS'] = status
    #         start_date = i.xpath('./td[4]/font/div/text()').get('')
    #         if '\xa0' not in start_date:
    #             dic_inspec['START_DATE'] = start_date
    #         end_date = i.xpath('./td[5]/font/div/text()').get('')
    #         if '\xa0' not in end_date:
    #             dic_inspec['END_DATE'] = end_date
    #         empty_list.append(dic_inspec)
    #         data = [item for item in empty_list if item]
    #     item['SUBS'] = data
    #     breakpoint()
    #     yield item
        # breakpoint()
        # link=response.xpath('//form/@action').get('').strip()
        # url=f"https://cdplusmobile.marioncountyfl.org{link}"
        # payload={
        #     "BTNSETINACTIVE":"",
        #     "BTNSETACTIVE":"",
        #     "BTNADDSUB":"",
        #     "CBINSPCLASS":"-1",
        #     "EDTDBA":"",
        #     "EDTLIC":"",
        #     "BTNSEARCH":"",
        #     "CERTSEARCHGRID":"000000|R0|0^0|x|||",
        #     "BTNSEARCHCLOSE":"",
        #     "BTNSELECTCERT":"",
        #     "SUBSGRID":"10000000000000000000|R0|0^0|x|||||",
        #     "MSGDLGOK":"^isvisible:false",
        #     "IW_FormName":"FrmSubContractors",
        #     "IW_FormClass":"TFrmSubContractors",
        #     "IW_width":"1920",
        #     "IW_height":"654",
        #     "IW_Action":"IMGBACK",
        #     "IW_ActionParam":"",
        #     "IW_Offset":"",
        #     "IW_SessionID_":link.split('/')[-2],
        #     "IW_TrackID_":"22",
        #     "IW_WindowID_":"",
        #     "IW_AjaxID":"17147313511098",
        # }
        # yield scrapy.FormRequest(url,callback=self.parse_subs_from_back_navigation,formdata=payload,headers=self.headers,cb_kwargs={'item':item})
    # def parse_subs_from_back_navigation(self,response,item):
    #     breakpoint()