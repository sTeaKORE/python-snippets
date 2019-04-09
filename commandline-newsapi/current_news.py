import sys
import requests
import os
from enum import Enum

class SupportedCountries:
	def __init__(self, name, code):
		self.name = name
		self.code = code

def get_supported_countries():
	supported_countries = []
	supported_country_file = open("newsapi_supported_countries.txt","r")
	for line in supported_country_file:
		temp = line.split(",")
		supported_country = SupportedCountries(temp[0], temp[1][:-1])
		supported_countries.append(supported_country)
	return supported_countries
		
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

def checkIfSupportedCountry(supported_countries, toCheck):
	for country in supported_countries:
		if country.code == toCheck:
			return True
	return False

def get_news_url(supported_countries, countrycode, apiKey):
	if checkIfSupportedCountry(supported_countries, countrycode):
		return ('https://newsapi.org/v2/top-headlines?pageSize=100&country=' + countrycode + '&apiKey=' + apiKey)
	else:
		return None

def checkNone(toCheck):
	if toCheck is None:
		return False
	return True

def fancy_print(json):
	article_count = json["totalResults"]
	count = 1
	articles = json["articles"]
	for article in articles:
		clear()
		print("PageCount: " + str(count) + "/" + str(article_count))
		print()
		if(checkNone(article["source"]["name"]) and checkNone(article["author"])):
			print("Source: " + article["source"]["name"])
			print("Author: " + article["author"])
			print()
		if(checkNone(article["title"])):
			print("Title: " + article["title"])
		if(checkNone(article["description"])):
			print("Description: " + article["description"])
			print()
		if(checkNone(article["content"])):
			print("Preview: " + article["content"])
			print()
		if(checkNone(article["url"])):
			print("Url: " + article["url"])
			print()
		count = count + 1
		cont = input('Press Enter For Next or q then Enter To Quit\n')
		if cont == 'q':
			break;
def pad_string(toPad):
	if len(toPad) is 25:
		return toPad
	return toPad.ljust(25)
			
def get_supported_countries_string(supported_countries):
	breakcount = 0
	result = ""
	for country in supported_countries:
		temp = country.code + "(" + country.name + "),"
		result += pad_string(temp)
		breakcount += 1
		if breakcount is 4:
			result += "\n"
			breakcount = 0
	return result[:-2]
	
			
def main():
	supported_countries = get_supported_countries()
	supported_countries_string = get_supported_countries_string(supported_countries)
	apiKey = sys.argv[1]
	loop = True
	while loop:
		clear()
		print("Enter one of the supported country codes above for specific headlines or q to quit")
		print(supported_countries_string)
		option = input('> ')
		if option == 'q':
			loop = False
		else:
			url = get_news_url(supported_countries, option, apiKey)
			if url is not None:
				response = requests.get(url)
				fancy_print(response.json())
			else:
				print("Invalid Country Code, Try again!")
		
main()
	