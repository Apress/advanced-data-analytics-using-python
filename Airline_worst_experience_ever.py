from textblob.classifiers import NaiveBayesClassifier

train = [("It's a very long and exhausting flight!", 'pos'),('I traveled alone with my 9 month old son from Frankfurt to Delhi and onto Sydney!', 'pos'),('At the end they wrote a manual boarding pass.', 'pos'),("I think everybody knows with a baby it's even harder!", 'pos'),('After this 2 hours they gave me just the boarding pass until Delhi and I had to run carrying my son and all the luggage to the boarding as this had started already.', 'pos'),("The first problems started when they weren't be able to print the boarding pass for my son.", 'neg'),("They kept me 2 hours in front of the check-in that I couldn't care properly for my son.", 'neg'),('No toilets, no food again - just hard chairs to wait on.', 'neg'),("They didn't care.", 'neg'),('I got more and more stressed.', 'pos')]

cl = NaiveBayesClassifier(train)
print(cl.classify("Worst experience ever with Air India!"))