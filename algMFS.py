from re import split

from utils import *

try:
	if argv[1] == "-v":
		setLogVerbosity(int(argv[2]))
except (IndexError, ValueError):
	pass


# algMFS: Most Frequent Sense (Baseline)
def algMFS(context, word):
	context = getDistinct(context)
	
	log('Starting "%s".' %(word), 2)
	
	# Get word senses
	senseURIs = querySenses(word)
	log('Got senses of word: %s.' %(str(senseURIs)), 4)
	
	wsenses = []
	
	# Check each sense
	for senseURI in senseURIs:
		senseName = senseURI.rsplit("/", 1)[-1]
		
		log('Checking sense "%s".' %(senseName), 3)
		
		# Get weight
		try:
			weight = int(queryInLinkCount(senseURI))
		except KeyError:
			weight = 0
		
		log('Got incoming links.', 4)
		
		# Catalogue the sense:weight
		wsenses.append( (senseName, weight, senseURI) )
		
		log('Done checking sense at weight %d.' %(weight), 3)
	
	return wsenses


# Enter interactive session if run directly
if __name__ == "__main__":
	startLogging()
	
	# Get inputs
	text = raw_input("Enter a text: ")
	word = raw_input("Enter a word in that text: ")
	
	print

	# Format input text
	textWords = split("\W+", text.lower())
	
	wsenses = algMFS(textWords, word)
	
	print
	
	if wsenses:
		best = (None, -1, None)
		# Output sense and weight while finding best sense
		for wsense in wsenses:
			sense, weight = wsense[0], wsense[1]
			if logVerbosity >= 3:
				print sense, ":", weight
			if weight >= best[1]:
				best = wsense
		
		# Output best sense
		print
		log("Best sense: %s at %d" %(best[0], best[1]), 2)
		print "\n---\n"
		
		raw_input("Press Enter for additional information...")
		
		print "\nAbstract:"
		try:
			print queryAbstract(best[2])
		except UnicodeEncodeError:
			print "Your console does not support Unicode."
		
		print "\nFetching image..."
		
		imgURL = queryImage(best[2])
		
		try:
			from webbrowser import open
			open(imgURL)
		except TypeError:
			print "Image not available."
		
	else:
		print "Word not found."
else:
	startLogging("algMFS.log")