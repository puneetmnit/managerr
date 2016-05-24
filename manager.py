#! /usr/bin/python
"""
 TODO:
1. argument parsing
	1.1 min upload date
	1.2 no. of days, hours, min, secs
	1.3 optional default posted dated to be set, in case of errors

2. exception handling

3. upload to GIT

4. more arguments

5. GUI

"""

import datetime
import time
import flickrapi
import webbrowser
import xml.etree.ElementTree as ET

api_key = u'507db6aa91972622e8a393c5845adddf'
api_secret = u'baba6283e06da35d'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms=u'write'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=u'write')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = unicode(raw_input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

print('Step 2: use Flickr')

"""
change it to first find and store photo ids and then update all
"""
# find pics to be updated
photos = []
page_size = 500
num_photos = 0
for photo in flickr.walk(user_id='me',min_upload_date='2013-11-04',per_page=page_size):
	#get the photo id
	photo_id = photo.get('id')
	#print photo_id
	photo_info = flickr.photos.getInfo(photo_id=photo_id)
	
	#get dates
	if (photo_info.get('stat') == "ok"): 
		dates = photo_info.find('photo').find('dates')

		posted_date = int(dates.get('posted'))
		taken_date = int(datetime.datetime.strptime(dates.get('taken'),"%Y-%m-%d %H:%M:%S").strftime("%s"))
		"""
		try:
			ET.dump(flickr.photos.setdates(photo_id=photo_id,date_posted=1322677800))
			ET.dump(flickr.photos.setdates(photo_id=photo_id,date_posted=posted_date))
		except flickrapi.exceptions.FlickrError as e:
			print "FlickrError: {}".format(e.message)
			print 'resetting'
			ET.dump(flickr.photos.setdates(photo_id=photo_id,date_posted=posted_date))
			break
		"""

		if posted_date>taken_date:
			num_photos = num_photos + 1
			photos.append((photo_id, posted_date, taken_date))
			flickr.photos.setdates(photo_id=photo_id,date_posted=taken_date)
			#ET.dump(photo_info)

print "will update {0} pics".format(num_photos)

"""
for photo in photos:
	print "id: {} posted: {} taken: {}".format(photo[0],photo[1],photo[2])
"""

