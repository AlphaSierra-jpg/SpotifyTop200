import getMusic

if __name__ == "__main__":
    print("Get All CSV")
    getMusic.getAllCSV(getMusic.getAllDay())
    print("CSV in mongo")
    getMusic.allCSVtoMongo()
    print("Finished")
