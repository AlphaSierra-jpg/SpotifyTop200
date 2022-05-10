import Script.getMusic

if __name__ == "__main__":
    print("Get All CSV")
    Script.getMusic.getAllCSV(Script.getMusic.getAllDay())
    print("CSV in mongo")
    Script.getMusic.allCSVtoMongo()
    print("Finished")
