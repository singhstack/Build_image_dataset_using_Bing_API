#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import exceptions
import argparse
import requests
import cv2
import os


# In[2]:


'''# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
    help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
    help="path to output directory of images")
args = vars(ap.parse_args())'''


# In[8]:


args={}
args["query"]="Footballers"
args["output"]=r"C:\Users\tarandeepsingh1\Downloads\Vision\Building Image Dataset using Bing API\Footballer Dataset"


# In[13]:


API_KEY="77fa602924364837802538708d19fb1a"
MAX_RESULTS=250
GROUP_SIZE=50


# Enter the API Key obtained from Bing Cognitive Services.
# I am limiting max number of results to 250 here and returning the max number of images per request by the Bing API to 50 total images.

# Group size can be thought of as total number of results 'per page'

# In[10]:


URL="https://api.cognitive.microsoft.com/bing/v7.0/images/search"


# In[11]:


# when attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = set([IOError, FileNotFoundError,
    exceptions.RequestException, exceptions.HTTPError,
    exceptions.ConnectionError, exceptions.Timeout])


# In[16]:


# store the search term in a convenience variable then set the
# headers and search parameters
term=args["query"]
headers={"Ocp-Apim-Subscription-Key" : API_KEY}
params={"q": term, "offset": 0, "count": GROUP_SIZE}

#make the search
print()
search=requests.get(URL,headers=headers,params=params)
search.raise_for_status()

# grab the results from the search, including the total number of
# estimated results returned by the Bing API
results=search.json()
estNumResults=min(results["totalEstimatedMatches"],MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults,term))

# initialize the total number of images downloaded thus far
total=0


# In[19]:


# loop over the estimated number of results in `GROUP_SIZE` groups
for offset in range(0, estNumResults, GROUP_SIZE):
    # update the search parameters using the current offset, then
    # make the request to fetch the results
    print("[INFO] making request for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    print("[INFO] saving images for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))
    #loop over the results
    for v in results["value"]:
        
        try:
            print("[INFO] fetching: {}".format(v["contentUrl"]))
            r=requests.get(v["contentUrl"],timeout=30)
            
            #build the path to the output image
            ext=v["contentUrl"][v["contentUrl"].rfind("."):]
            p=os.path.sep.join([args["output"],"{}{}".format
                                (str(total).zfill(8),ext)])
            total+=1
            print("Image Path: {}".format(p))
            # write the image to disk
            f = open(p, "wb")
            f.write(r.content)
            f.close()
        except Exception as e:
            # check to see if our exception is in our list of
            # exceptions to check for
            if type(e) in EXCEPTIONS:
                print("[INFO] skipping: {}".format(v["contentUrl"]))
                continue


# In[ ]:




