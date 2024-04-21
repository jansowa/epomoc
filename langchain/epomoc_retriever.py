counter = 0

def retrieve_documents(query):
    global counter
    counter += 1
    return "there will be retrieved html document number: " + str(counter) + " https://www.google.com"