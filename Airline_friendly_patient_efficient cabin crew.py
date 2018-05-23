from textblob.classifiers import NaiveBayesClassifier

train = [('This flight from Bodhgaya to Delhi was the latest of about 20 domestic flights sectors completed with Air India over the last 3 - 4 years.', 'pos'),('The level of service has remained consistent in all areas, with some aspects of service stronger than others.', 'pos'),('This flight was originally due to depart Bodhgaya at 14.35h arriving in Delhi at 16.25h.', 'pos'),('An initial delay to a revised 16.00h departure was notified by e-mail several hours in advance.',  'pos'),('We had no idea how long the delay would be until we saw our aircraft land.', 'neg'),('Except for an expensive coffee kiosk there were no customer facilities while waiting.', 'neg')]

cl = NaiveBayesClassifier(train)
print(cl.classify('Check-in queue management at Bodhgaya airport was poor but agent service was good once you eventually got to the check-in desk.'))