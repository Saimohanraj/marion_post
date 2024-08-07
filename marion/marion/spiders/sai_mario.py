import scrapy
import json
import re
from parsel import Selector

class ExampleSpider(scrapy.Spider):
    name = 'test'
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

        }
    def start_requests(self):
        url="https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll"
        yield scrapy.Request(url=url,callback=self.parse,headers=self.headers)
    
    def parse(self,response):
        link=response.xpath('//form/@action').get('').strip()
        track_id=response.xpath('//input[@name="IW_TrackID_"]/@value').get('').strip()
        SessionID=response.xpath('//input[@name="IW_SessionID_"]/@value').get('').strip()
        WindowID=response.xpath('//input[@name="IW_WindowID_"]/@value').get('').strip()
        payload={
        "IW_width": "1920",
        "IW_height": "443",
        "IW_dpr": "1",
        "IW_SessionID_":SessionID ,
        "IW_TrackID_": track_id,
        "IW_WindowID_":WindowID 
        }
        url=f"https://cdplusmobile.marioncountyfl.org{link}"
        yield scrapy.FormRequest(url,callback=self.parse_detail,formdata=payload,headers=self.headers)
    
    def parse_detail(self,response):
        
        link=response.xpath('//form/@action').get('').strip()
        id_seesion = link.split('/')[-2]
        url = f'https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=BTNPERMITS.DoOnAsyncClick&x=127&y=35&which=0&modifiers='
        payload={
                "BTNPERMITS": "TIMERLOAD.DoOnAsyncTimer",
                "IW_FormName": "FrmStart",
                "IW_FormClass": "TFrmStart",
                "IW_width": "1903",
                "IW_height":"620",
                "IW_Action": "BTNPERMITS",
                "IW_ActionParam":"" ,
                "IW_Offset": "1",
                "IW_SessionID_":id_seesion,
                "IW_TrackID_":"2",
                "IW_WindowID_":"",
                "IW_AjaxID":"17147417591421"
        }
        yield scrapy.FormRequest(url,callback=self.parse_details,formdata=payload,headers=self.headers)

    def parse_details(self,response):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        # breakpoint()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_callback_one,formdata=payload,headers=self.headers)
    def parse_callback_one(self,response):
        link=response.xpath('//form/@action').get('').strip()
        id=link.split('/')[-2]
        url = f'https://cdplusmobile.marioncountyfl.org{link}$/callback?callback=EDTPERMITNBR.DoOnAsyncChange'
        
        payload={
            "EDTPERMITNBR":"2022012100",
            "IW_FormName":"FrmMain",
            "IW_FormClass":"TFrmMain",
            "IW_width":"1920",
            "IW_height":"904",
            "IW_Action":"EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_":id,
            "IW_TrackID_":"5",
            "IW_WindowID_":"",
            "IW_AjaxID":"17147313511098",
        }
        yield scrapy.FormRequest(url,callback=self.parse_callback_two,formdata=payload,headers=self.headers)
    def parse_callback_two(self,response):
            # breakpoint()
            data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
            value=Selector(data)
            submit=value.xpath('//submit/text()').get('').strip()
            id=submit.split('/')[-2]
            track_id=value.xpath('//trackid/text()').get('').strip()

            url=f"https://cdplusmobile.marioncountyfl.org{id}$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
            payload={
                "EDTPERMITNBR":"2022012100",
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
            yield scrapy.FormRequest(url,callback=self.parse_callback_three,formdata=payload,headers=self.headers)
    def parse_callback_three(self,response):
        breakpoint()
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=86&char=V&modifiers=CTRL_MASK,"
        payload={
            "EDTPERMITNBR":"2022012100",
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
        yield scrapy.FormRequest(url,callback=self.parse_callback_four,formdata=payload,headers=self.headers)
    def parse_callback_four(self,response):
        breakpoint()
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}$/callback?callback=EDTPERMITNBR.DoOnAsyncKeyUp&which=17&char=%11&modifiers=CTRL_MASK,"
        payload={
            "EDTPERMITNBR":"2022012100",
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
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_three,formdata=payload,headers=self.headers)
    def parse_details_callback_three(self,response):
        data=re.findall(r'\<response\>[\w\W]+\<\/response\>',response.text)[0]
        value=Selector(data)
        submit=value.xpath('//submit/text()').get('').strip()
        id=submit.split('/')[-2]
        track_id=value.xpath('//trackid/text()').get('').strip()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        payload={
            "EDTPERMITNBR":"2022012100",
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
        yield scrapy.FormRequest(url,callback=self.parse_details_callback_four,formdata=payload,headers=self.headers)
    def parse_details_callback_four(self,response):
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
        yield scrapy.FormRequest(url,callback=self.parse_details_product,formdata=payload,headers=self.headers)
    def parse_details_product(self,response):
        id = re.findall(r'\{\"IW_SessionID_\"\:\s*\"([^>]*?)\"\,',response.text)[0]
        track_id=re.findall(r'\"IW_TrackID_\"\:\s*([^>]*?)\}',response.text)[0]
        submit = re.findall(r'post\(\"([^>]*?)\"\,',response.text)[0]
        # breakpoint()
        url=f"https://cdplusmobile.marioncountyfl.org{submit}"
        payload={
            "IW_SessionID_":id,
            "IW_TrackID_":track_id,
            
        }
        yield scrapy.FormRequest(url,callback=self.parse_details_check,formdata=payload,headers=self.headers)
    def parse_details_check(self,response):
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
        yield item