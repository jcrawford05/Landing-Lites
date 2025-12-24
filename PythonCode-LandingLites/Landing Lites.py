import sqlite3 #Database
import tkinter as tk #GUI
import sqlite3 as sq #Database
from sqlite3 import Error
from tkinter import messagebox
from PIL import Image, ImageTk # Allows for image on the front page
import winsound #Supress chimes when opening pages, it was really annoying

"""
Landing Lite
By James Crawford
Written for the Final Project of HUM 1600 taught by John Gordon

Please refer to the Terms of Service and Credits

Disclaimer: 
AI was used in the writing of this code as a tool for debugging and proper function use.
AI used was OpenAI's ChatGPT 3.5

"""

class LandingLite:
    def __init__(this, master):
        """This function creates the Landing Lite GUI"""
        this.master = master
        this.master.title("Landing Lite")
        this.master.geometry("1100x750")

        # Creating the Widgets
        this.homePage = tk.Frame(master)
        this.homePage.pack()

        image = Image.open("C:\\Users\\jrc05\\Desktop\\Schoolwork\\HUM 1600\\Final Project\\"
                           "Runway-lights-precision-approach.jpg") # Change this line to match your file path
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        this.logoLabel = tk.Label(this.homePage, image=photo)
        this.logoLabel.image = photo  # Keep a reference to avoid garbage collection
        this.logoLabel.grid(row=0, column=0, columnspan=2, pady=10)  # Added columnspan to span two columns
        this.logoLabel.config(anchor="center")  # Center the image horizontally

        this.appNameLabel = tk.Label(this.homePage, text="Landing Lite")
        this.appNameLabel.grid(row=1, column=0, columnspan=2, pady=10)  # Added columnspan to span two columns
        this.appNameLabel.config(anchor="center")  # Center the label horizontally

        # Creating space between logo and labels
        this.emptyLabel = tk.Label(this.homePage, text="")
        this.emptyLabel.grid(row=2, column=0)

        # Creating the Search fields
        labels = ["Airport Name:", "Airport ICAO:", "City:", "Country:"]
        for i, labelText in enumerate(labels):
            label = tk.Label(this.homePage, text=labelText)
            label.grid(row=i + 3, column=0, sticky="e")

        this.nameField = tk.Entry(this.homePage)
        this.nameField.grid(row=3, column=1)

        this.icaoField = tk.Entry(this.homePage)
        this.icaoField.grid(row=4, column=1)

        this.cityField = tk.Entry(this.homePage)
        this.cityField.grid(row=5, column=1)

        this.countryField = tk.Entry(this.homePage)
        this.countryField.grid(row=6, column=1)

        this.searchButton = tk.Button(this.homePage, text="Search", command=this.search)
        this.searchButton.grid(row=7, column=0, columnspan=2, pady=10)
        this.searchButton.config(anchor="center")

        # Creating space between fields and buttons
        this.emptyLabel2 = tk.Label(this.homePage, text="")
        this.emptyLabel2.grid(row=8, column=0, columnspan=2)

        # Creating the TOS and credits buttons
        this.tosButton = tk.Button(this.homePage, text="TOS", command=this.openTOS)
        this.tosButton.grid(row=9, column=0, padx=10, pady=10)

        this.creditsButton = tk.Button(this.homePage, text="Credits", command=this.openCredits)
        this.creditsButton.grid(row=9, column=1, padx=10, pady=10)

        this.conn = sqlite3.connect('Airports.db')
        this.cursor = this.conn.cursor()

    def search(this):
        """Function enabling users to search Airport Database"""

        name = this.nameField.get()
        icao = this.icaoField.get()
        city = this.cityField.get()
        country = this.countryField.get()

        # Constructing the query based on the provided input
        query = "SELECT * FROM Airports WHERE 1=1"

        # Adding conditions based on the provided input
        if name:
            query += " AND [Airport Name] = '{}'".format(name)
        if icao:
            query += " AND Identifier = '{}'".format(icao)
        if city:
            query += " AND Municipality = '{}'".format(city)
        if country:
            query += " AND Country = '{}'".format(country)

        this.cursor.execute(query)
        results = this.cursor.fetchall()

        if results:
            this.homePage.pack_forget()
            this.loadSearchResults(results)
        else:
            messagebox.showinfo("No Results", "No matching results found")

    def loadSearchResults(this, results):
        """Defines the search results of a user search"""
        this.listPage = tk.Frame(this.master)
        this.listPage.pack()

        this.resultsListBox = tk.Listbox(this.listPage, selectmode=tk.SINGLE, width=75)
        for result in results:
            name, icao, city, country, airportID = result[3], result[1], result[8], result[7], result[0]
            displayText = f"{name},   {icao},   {city},   {country},   {airportID}"
            this.resultsListBox.insert(tk.END, displayText)
        this.resultsListBox.pack()

        this.submitButton = tk.Button(this.listPage, text="Submit", command=this.loadAirportPage)
        this.submitButton.pack()

        this.backButton = tk.Button(this.listPage, text="Return to Home Page", command=this.goToHomePage)
        this.backButton.pack(side=tk.RIGHT)

    def loadAirportPage(this):
        """Creates an interfacec for the results of a user selected airport"""
        selectedIndex = this.resultsListBox.curselection()
        if selectedIndex:
            selectedText = this.resultsListBox.get(selectedIndex)
            selectedID = selectedText.split(',')[4].strip()
            airportInfo = this.getAirportInfo(selectedID)
            this.listPage.pack_forget()
            this.loadAirportInfoPage(airportInfo)
        else:
            messagebox.showinfo("No Selection", "Please select an airport from the list.")

    def getAirportInfo(this, selectedID):
        """Gathers Data from the SQLite Database for the given airport"""
        
        this.cursor.execute("SELECT * FROM Airports WHERE ID = ?", (selectedID,))
        airportInfo = this.cursor.fetchone()

        return airportInfo

    def loadAirportInfoPage(this, airportInfo):
        """This function gatheres the information about a chosen airport to a new page in the Landing Lite GUI"""
        this.airportPage = tk.Frame(this.master)
        this.airportPage.pack()
        airport_labels = ["Airport ID:", "ICAO:", "Airport Size:", "Airport Name:", "Latitude:", "Longitude:",
                          "Elevation (ft):",
                          "Country:", "City:"]
        for i, label_text in enumerate(airport_labels):
            label = tk.Label(this.airportPage, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=10, pady=5)

            info = tk.Label(this.airportPage, text=airportInfo[i])
            info.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        this.airportInfo = airportInfo
        this.displayRunwayInfo(this.airportInfo)

        runwayRows = len(airport_labels) + 2
        this.backButton = tk.Button(this.airportPage, text="Back to Search Results", command=this.goBack)
        this.backButton.grid(row = runwayRows, columnspan=2, pady=10)

    def displayRunwayInfo(this, airportInfo):
        """This function gathers and displays information about the runways at a user-defined airport"""
        airportID = airportInfo[0]
        this.cursor.execute("SELECT * FROM Runways WHERE [Airport Ref.] = ?", (airportID,))
        runwayInfo = this.cursor.fetchall()

        # Create a frame for the runway table
        this.runwayFrame = tk.Frame(this.airportPage)
        this.runwayFrame.grid(row=len(airportInfo) + 1, columnspan=2, padx=10, pady=10)

        columns = {
            "Primary RWY Name": 6,
            "Secondary RWY Name": 9,
            "RWY Length (ft.)": 3,
            "RWY Width (ft.)": 4,
            "Surface": 5,
            "Primary Elevation (ft.)": 7,
            "Primary Heading": 8,
            "Secondary Elevation (ft.)": 10,
            "Secondary Heading": 11
        }

        # Create header labels
        for i, header in enumerate(columns.keys()):
            tk.Label(this.runwayFrame, text=header).grid(row=0, column=i, padx=5, pady=5)

        # Populate the table with runway information
        for rowIndex, runway in enumerate(runwayInfo):
            for header, colIndex in columns.items():
                # Displaying only the values corresponding to the desired columns and headers
                value = runway[colIndex]
                tk.Label(this.runwayFrame, text=value).grid(row=rowIndex + 1,
                                                            column=list(columns.keys()).index(header), padx=5,
                                                            pady=5)

    def goBack(this):
        """Creates functionality for the back button used in the Airport Page"""
        this.airportPage.destroy()
        this.listPage.pack()

    def goToHomePage(this):
        """Creates functionality for the Return home button on the results page"""
        this.listPage.destroy()
        this.homePage.pack()

    def openTOS(this):
        """Assigns action to the TOS button"""
        with open("C:\\Users\\jrc05\\Desktop\\Schoolwork\\HUM 1600\\Final Project\\"
                  "Landing Lite - TOS.txt", "r") as file: # Change this line to match your file path
            tosText = file.read()
        messagebox.showinfo("Terms of Service", tosText)

    def openCredits(this):
        """Assigns action to the Credits button"""
        with open("C:\\Users\\jrc05\\Desktop\\Schoolwork\\HUM 1600\\Final Project\\"
                  "Landing Lite -Credits.txt", "r") as file: # Change this line to match your file path
            creditsText = file.read()
        messagebox.showinfo("Credits", creditsText)

if __name__ == "__main__":
    root = tk.Tk()
    app = LandingLite(root)
    root.mainloop()

