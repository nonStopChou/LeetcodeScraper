from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from pymongo.mongo_client import MongoClient
import os

USER = os.getenv("MONGO_RESUME_USER")
PASSWORD = os.getenv("MONGO_RESUME_PASS")
CLUSTER_ADDRESS = "resume.xg22b.mongodb.net"
MONGO_URL = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER_ADDRESS}/?retryWrites=true&w=majority&appName=Resume"

LEETCODE_USERNAME = "pingruchou1125tw"

problem_status_element = {
    "easy_status": '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div[2]',
    "medium_status": '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[3]/div[1]/div/div/div[2]/div[2]/div[2]',
    "hard_status": '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[3]/div[1]/div/div/div[2]/div[3]/div[2]',
    "total_solved": '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/span[1]',
    "total_problem": '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/span[2]',
}

language_status_element = {
	"languages_info" : '//*[@id="__next"]/div[1]/div[4]/div/div[1]/div/div[6]'
}

click_button_element = {
	"show_more_language" : '//*[@id="__next"]/div[1]/div[4]/div/div[1]/div/div[6]/div[4]/span'
}

if __name__ == "__main__":
		
	# Set up Chrome options to run it headless (without opening the browser window)
	options = Options()
	options.add_argument("--headless")  # Run in headless mode
	options.add_argument(
		"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
	)

	# Set up the WebDriver (with automatic ChromeDriver installation via webdriver_manager)
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	# Open the webpage
	url = f'https://leetcode.com/u/{LEETCODE_USERNAME}/'  # Replace with the URL of the dynamic page
	driver.get(url)


	# Now you can extract the data after JS execution
	try:
		
		# action perform before collecting
		for name, xpath in click_button_element.items():
			try:
				click_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
				click_btn.click()
			except Exception as e:
				print(f"Action {name} perform fail...")
				print("Error : e")

		# start to collect data
		leetcode_status = {}

		leetcode_status['username'] = f"{LEETCODE_USERNAME}"
		
		# collect problem related data
		for name, xpath in problem_status_element.items():
			try:
				element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
				leetcode_status[name] = element.text.lstrip("/")
			except Exception as e:
				leetcode_status[name] = f"Error : {str(e)}"
				print("Error : ", e)
		

		languages_block = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, language_status_element['languages_info'])))
		span_elements = languages_block.find_elements(By.XPATH, './/span')

		# collect language related data
		try:
			languages_data = {}
			# Iterate through each language and its corresponding problem count
			languages_list = [language for language in span_elements[::3]]
			languages_problem_solved = [problem_solved for problem_solved in span_elements[1::3]]
			
			for lang, count in zip(languages_list, languages_problem_solved):
				language = lang.text.strip()  # Extract language name
				problems_solved = count.text.strip()  # Extract number of problems solved
				languages_data[language] = int(problems_solved)
				print(f"Language: {language}, Problems Solved: {problems_solved}")

		except Exception as e:
			print("Error : ", e)
		finally:
			leetcode_status['languages_info'] = languages_data
			

		# insert data to mongoDB
		# Create a new client and connect to the server
		client = MongoClient(MONGO_URL)
		try:
			client.admin.command('ping')
			print("Pinged your deployment. You successfully connected to MongoDB!")
			db = client['resume']
			db_collection = db['leetcode_information']
			db_collection.update_one(
				{"username": leetcode_status['username']},  # Filter condition (search by username)
				{"$set": leetcode_status},  # Update data
				upsert=True  # If document doesn't exist, it will be inserted
			)

		except Exception as e:
			print(e)


	finally:

		json_data = json.dumps(leetcode_status, indent=4)
		with open("./leetcode_status.json", "w") as file:
			json.dump(leetcode_status, file, indent=4)
		
		driver.quit()


