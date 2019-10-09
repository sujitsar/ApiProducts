#!/usr/local/bin/python3
#Importing the required the modules
import sys
import requests
import json
import configparser

############################################################################
#Author: Sujit Sar
#Title:  Python utility to make API call to Kogan's Products API Endpoint and
#        calculate the average weight of Air conditioners.
#Date:    10/10/2019
#Version: 1.0
############################################################################

# To read values from the configuration file
config = configparser.RawConfigParser()
config.read('config.properties')
config_dist=dict(config.items('API_PROPERTIES'))


# Function to calculate the  weight of a product
def calculateProductWeight(height,  width,  breadth):
    # To convert cubic cms to cubic meters, divide by 1000000
    cubicCmsToCubicMts=1000000 

    # a conversion factor which is the density of the material  
    conversionFactor=250 

    #Calculating volume in cc
    volumeinCubicCms=height*width*breadth

    #calculating volume in cubic meters
    volumeinCubicMeters = volumeinCubicCms/cubicCmsToCubicMts

    #calculating weight by multiplying volumeinCubicMeters with conversion factor 250
    weight = volumeinCubicMeters*conversionFactor
    return weight



# Function to calculate the average weight
def calculateAverageWeight( TotalWeight, numberOfItems):
    try: 
        #Average weight = total weight divided by number of items 
        averageWeight=TotalWeight/numberOfItems

        #Exception handling for divide by zero error in case the response doesn't have Air Conditioners
    except ZeroDivisionError as err:
        print("No Products found having category : Air Conditioners")
        print("Exiting because of the exception ...... " +str(err))
        sys.exit(1)            
    return averageWeight



#Function to do the rest API call.
def getApiResponse():
    #url='http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com/api/products/1'
    url=config_dist['url']
    try:
        # Sending request to the url to get response
        rApi=requests.get(url)

        #Status code of the response
        status=rApi.status_code
        print ("The Status of the API call is ...." +str(status)+"\n")

        #Execption handling in case of error
    except Exception as e:
        print("Exiting because of the exception ...... "+str(e))
        sys.exit(0)

        #Formatting the JSON response for iteration
    try:          
        jsonResponse = json.loads(json.dumps(rApi.json()))

        # Handling Value error in case response is not present
    except ValueError as e:
        print("exiting as no value found for response ...." +str(e)+"\n")
        sys.exit(0)              
    return jsonResponse



# Function to parse JSON data from API call response
def executeApiResponse():

    # variable to store total weight of all iterations        
    totalWeight=0 

    # number of items to find average
    numberOfItems=0 

    # Air conditioners is the category for which we find the total weight
    #category='Air Conditioners' 
    category=config_dist['category']

    # API call function's response
    loaded_json=getApiResponse()  

    # looping over the response 
    for i in loaded_json['objects']: 

        # getting  the width for every  iteration    
        width=i['size']['width']  

        # getting  the length for every  iteration
        length=i['size']['length'] 

        # getting  the height for every  iteration
        height=i['size']['height']

        title=i['title']

        # Filtering the  category for Air Conditioners fom JSON response
        if i['category'] == str(category):

            # Function call calculateProductWeight to calculate the weight of each item
            # totalWeight variable adds the weight of items during every iteration 

            totalWeight= totalWeight + calculateProductWeight(width, length, height)

            #Counting the number of Items
            numberOfItems=numberOfItems+1

            print("The weight of "+str(title)+ " is "+str(calculateProductWeight(width, length, height))+"\n")

    # Calling calculateAverageWeight function passing totalWeight and numberOfItems parameters  
    Average= calculateAverageWeight(totalWeight,numberOfItems) 

    print("The Total weight of the "+str(numberOfItems)+" Air Conditioners is " +str(totalWeight)+ "\n")   
    print("The Average weight of the "+str(numberOfItems)+" Air Conditioners is "  +str(Average)+"\n")  

# Calling the executeApiResponse() function for final execution

executeApiResponse()


       

