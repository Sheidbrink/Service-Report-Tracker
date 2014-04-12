from flask import request

if(request.method == "GET") # Search
	print "Searching..."
elif(request.method == "POST") # Submit
	print "Submitting..."
