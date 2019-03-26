import gspread
from oauth2client.service_account import ServiceAccountCredentials
from amazon_bot import AmazonBot
from email_c import EmailSender

class PriceUpdator:
	#Building the Constroctor
	def __init__(self,sheet_name):
		#Class Variables corres to the Column ID(Tuple)
		self.items_colm,self.price_colm,self.freq_colm,self.prod_url,self.prod_name, self.total_cost = (1,2,3,4,5,6)
		
		#Scope Variable For API 
		scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('budget-amazon-sec.json', scope)
		#Authentication of API
		client = gspread.authorize(creds)
		#Accessing the Google Sheets
		self.sheet = client.open(sheet_name).sheet1
	def  update_items_sheet(self):
		self.items = self.sheet.col_values(self.items_colm)[1:]
		amazon_bot = AmazonBot(self.items)
		urls, prices, name_of_items = amazon_bot.search_items()

		print("\nUpdating the Spreadsheet.....\n")
		for x in range(len(urls)):
			self.sheet.update_cell(x+2, self.price_colm, prices[x])
			self.sheet.update_cell(x+2, self.prod_url, urls[x])
			self.sheet.update_cell(x+2, self.prod_name, name_of_items[x])

#Loading the Class
bot_price_updator = PriceUpdator("ProductPrice")
bot_price_updator.update_items_sheet()
#Sending Email once the Updating is Completed.
email_sender = EmailSender()
sub = "Google Spreadsheet Updated Successfully"
msg = "The Product, URL and Total Price is Updated Successfully in Your Google Spreadsheet."
email_sender.send_email(sub,msg)




