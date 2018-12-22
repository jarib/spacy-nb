from spacy.strings import StringStore

stringstore = StringStore()
stringstore.add(u'rigga')
apple_hash = stringstore[u'rigga']
assert apple_hash == 17293262079951405058
assert stringstore[apple_hash] == u'rigga'