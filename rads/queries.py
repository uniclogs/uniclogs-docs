#in progress to be converted to sqlalchemy

''' findrequests()
Query to find the requests that need to be approved
SELECT * FROM public.requests
WHERE is_approved IS NULL
ORDER BY last_modified ASC
'''

'''currentschedule()
Query to find Scheduled requests approved slightly wrong needs to get public.pass start time > NOW () and match pass id with user token
Can fix by using a join between the tables to get the data needed
SELECT * FROM public.requests
WHERE is_approved IS true AND  pass.start_time > NOW()
ORDER BY created_date ASC
'''

'''archives()
Query to find Archived requests either approved or denied
SELECT * FROM public.requests
WHERE is_approved IS not null
ORDER BY created_date ASC
'''

'''accept(user_token, date) 
Query to Accept requests using a user token
UPDATE requests
SET is_approved = true,
	last_modified = NOW()
WHERE user_token = 'user token' AND created_date = 'date'
'''

'''deny(user_token, date)
Query to Deny requests using a user token
UPDATE requests
SET is_approved = true,
	last_modified = NOW()
WHERE user_token = 'user token' AND created_date = 'date'
'''
