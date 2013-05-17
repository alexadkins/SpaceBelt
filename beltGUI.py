from Tkinter import *
import serial
import struct
from googlemaps import GoogleMaps, GoogleMapsError
from spaceserial import BeltMessages
API_KEY = 'AIzaSyAUJUxQr9qWzH80aTbc9oBc5ShmpHORHXU'
gmaps = GoogleMaps(API_KEY)
class app:
        def __init__(self, parent): #INCOMPLETE DUE TO SERIAL
                #Begin the serial.
                self.ser=serial.Serial('/dev/ttyACM1', 9600)
                #self.ser=0
                #self.CurrentLocation=ser.readline()
                
                #Needed Values
                #Reset color:
                self.Basecolor = '#%02x%02x%02x' % (217, 217, 217)
                #Button padding (which is zero and thus irrevelant)
                self.button_pad = 0
                
                #Parent (initial) window that holds frames
                self.myParent = parent
                        #Button Frame on the left
                self.button_frame = Frame(parent)
                self.button_frame.pack(
                        padx = self.button_pad,
                        pady = self.button_pad,
                        side=LEFT
                )
                
                #Creates frame on right for start and menus
                self.right_frame = Frame(parent)
                self.right_frame.pack(side=RIGHT)
                
                #Creates blank frame where various menus will go
                self.BlankFrame()
                
                #Frame for start button; does not change
                self.activate_frame = Frame(self.right_frame, width = 500, height = 100)
                self.activate_frame.pack(
                        side=BOTTOM
                        )
                self.activate_frame.pack_propagate(0)
                
                #Start Button
                self.ActButton = Button(self.activate_frame, text="Start", background="red")
                self.ActButton.configure(
                        height=3,
                        width=50)
                self.ActButton.place(
                        anchor=CENTER,
                        relx = .5,
                        rely = .5)
                self.ActButton.bind("<Button-1>", self.StartClick)
                
                self.MakeButtons()
                
                self.msg = struct.Struct("ii")
                
        def BlankFrame(self):
                self.Bstate = True
                self.menu_frame = Frame(self.right_frame, width = 500, height=225)
                self.menu_frame.pack(
                        side=TOP
                        )
                self.menu_frame.pack_propagate(0)
                label = Label(self.menu_frame, text="Please select a mode to the left.")
                label.pack(side=TOP, pady = 30)
                
        def MakeButtons(self):
                button_width = 20
                button_height = 7
                
                self.Cbutton = Button(self.button_frame, text="COMPASS")
                self.Cbutton.configure(
                        width = button_width,
                        height = button_height,
                        padx = self.button_pad,
                        pady = self.button_pad
                        )
                self.Cbutton.pack()
                self.Cstate = False
                self.Cbutton.bind("<Button-1>", self.CompassClick)
                self.Cbutton.bind("<Return>", self.CompassClick)
                
                self.Dbutton = Button(self.button_frame, text="DIRECTIONAL")
                self.Dbutton.configure(
                        width = button_width,
                        height = button_height,
                        padx = self.button_pad,
                        pady = self.button_pad
                        )
                self.Dbutton.pack()
                self.Dstate = False
                self.Dbutton.bind("<Button-1>", self.DirectionalClick)
                self.Dbutton.bind("<Return>", self.DirectionalClick)
                
                self.Nbutton = Button(self.button_frame, text="NAVIGATION")
                self.Nbutton.configure(
                        width = button_width,
                        height = button_height,
                        padx = self.button_pad,
                        pady = self.button_pad
                        )
                self.Nbutton.pack()
                self.Nstate = False
                self.Nbutton.bind("<Button-1>", self.NavigationClick)
                self.Nbutton.bind("<Return>", self.NavigationClick)                
                
        def CompassClick(self, event):
                if self.Cstate == False:
                        #Compass Menu's Initial Button State Values
                        self.Comp_on_button_state = False
                        
                        self.DeadClick()
                        self.C_frame = Frame(self.right_frame, width = 500, height=225)
                        self.C_frame.pack(
                                side=TOP
                                )
                        self.C_frame.pack_propagate(0)        
                        
                        self.Comp_On_Button = Button(self.C_frame, text="OFF")
                        self.Comp_On_Button.configure(
                                width = 2,
                                height = 1
                                )
                        self.Comp_On_Button.place(
                                anchor=CENTER,
                                relx = .5,
                                rely = .5)
                        self.Comp_On_Button.bind("<Button-1>", self.OnClick)
                        
                        title = Label(self.C_frame, text = "Compass Mode")
                        title.pack(side=TOP, pady = 10)
                        
                        self.Clabel = Label(self.C_frame, text = "")
                        self.Clabel.pack(side=BOTTOM)
                        
                        self.Cstate = True
                        self.Cbutton["background"] = "gray"
                        self.Dstate = False
                        self.Dbutton["background"] = self.Basecolor
                        self.Nstate = False
                        self.Nbutton["background"] = self.Basecolor
                else:
                        self.DeadClick()
                        self.Cstate = False
                        self.Cbutton["background"] = self.Basecolor
                        self.BlankFrame()
                        
        def DirectionalClick(self, event):
                if self.Dstate == False:                
                        self.Direct_on_button_state = False
                        self.DeadClick()
                        self.D_frame = Frame(self.right_frame, width = 500, height=225)
                        self.D_frame.pack(
                                side=TOP
                                )
                        self.D_frame.pack_propagate(0)        
                        
                        title = Label(self.D_frame, text = "Directional Mode")
                        title.pack(side=TOP, pady = 10)
                        
                        self.Dlabel = Label(self.D_frame, text = "")
                        self.Dlabel.pack(side=BOTTOM)
                        
                        #Directional On Button
                        self.Direct_On_Button = Button(self.D_frame, text="OFF")
                        self.Direct_On_Button.configure(
                                width = 2,
                                height = 1
                                )
                        self.Direct_On_Button.pack(side=BOTTOM)
                        self.Direct_On_Button.bind("<Button-1>", self.OnClick)
                        
                        #Frame for Lat & Long inputs
                        topD_frame = Frame(self.D_frame)
                        topD_frame.pack(side=TOP)
                        
                        #Latitude frame, label, and entry box of Directional Mode
                        leftD_frame = Frame(topD_frame)
                        leftD_frame.pack(side=LEFT, padx = 30)
                        
                        latLabel = Label(leftD_frame, text = "Latitude Chosen Destination")
                        latLabel.pack(side=TOP)
                        
                        self.DLatEntry = Entry(leftD_frame)
                        self.DLatEntry.pack(side=TOP)
                        
                        formatLabel1 = Label(leftD_frame, text = "Format: 000.0000")
                        formatLabel1.pack(side=TOP)
                        
                        #Longitude frame, label, and entry box of Directional Mode
                        rightD_frame = Frame(topD_frame)
                        rightD_frame.pack(side=RIGHT, padx = 30)
                        
                        longLabel = Label(rightD_frame, text = "Longitude Chosen Destination")
                        longLabel.pack(side=TOP)
                        
                        self.DLongEntry = Entry(rightD_frame)
                        self.DLongEntry.pack(side=TOP)
                        
                        formatLabel2 = Label(rightD_frame, text = "Format: 000.0000")
                        formatLabel2.pack(side=TOP)
                        
                        #Address label & entry box of Direct Mode        
                        blankLabel = Label(self.D_frame, text = "")
                        blankLabel.pack(side=BOTTOM)
                        
                        self.DAddressEntry = Entry(self.D_frame)
                        self.DAddressEntry.pack(side=BOTTOM)
                        
                        addressLabel = Label(self.D_frame, text = "Address of Chosen Destination")
                        addressLabel.pack(side=BOTTOM)
                        self.Dstate = True
                        self.Dbutton["background"] = "gray"
                        self.Cstate = False
                        self.Cbutton["background"] = self.Basecolor
                        self.Nstate = False
                        self.Nbutton["background"] = self.Basecolor
                else:
                        self.DeadClick()
                        self.Dstate = False
                        self.Dbutton["background"] = self.Basecolor
                        self.BlankFrame()
        def NavigationClick(self, event):
                if self.Nstate == False:
                        self.Nav_on_button_state = False
                        self.NavCoordState = False
                        self.NavAddressState = False
                        
                        #Create Nav Frame                        
                        self.DeadClick()
                        self.N_frame = Frame(self.right_frame, width = 500, height=225)
                        self.N_frame.pack(
                                side=TOP
                                )
                        self.N_frame.pack_propagate(0)
                        
                        #Nav Mode Title
                        title = Label(self.N_frame, text = "Navigational Mode")
                        title.pack(side=TOP, pady = 10)
                        
                        #Nav Mode Status Message
                        self.Nlabel = Label(self.N_frame, text = "")
                        self.Nlabel.pack(side=BOTTOM)
                        
                        #Nav Mode On Button
                        self.Nav_On_Button = Button(self.N_frame, text="OFF")
                        self.Nav_On_Button.configure(
                                width = 2,
                                height = 1
                                )
                        self.Nav_On_Button.pack(side=BOTTOM)
                        self.Nav_On_Button.bind("<Button-1>", self.OnClick)
                        
                        self.coordButtonFrame = Frame(self.N_frame)
                        self.coordButtonFrame.pack(side=LEFT)
                        
                        coordButton = Button(self.coordButtonFrame, text="Via Lat. & Long. Coordinates")
                        coordButton.configure(
                                width = 25,
                                height = 2
                                )
                        coordButton.pack(padx = 10, side = RIGHT)
                        coordButton.bind("<Button-1>", self.NavCoord)
                                                
                        self.addressButtonFrame = Frame(self.N_frame)
                        self.addressButtonFrame.pack(side=RIGHT)
                        
                        addressButton = Button(self.addressButtonFrame, text="Via Written Address")
                        addressButton.configure(
                                width = 25,
                                height = 2
                                )
                        addressButton.pack(padx = 10, side = LEFT)
                        addressButton.bind("<Button-1>", self.NavAddress)
                                        
                        self.Nstate = True
                        self.Nbutton["background"] = "gray"
                        self.Cstate = False
                        self.Cbutton["background"] = self.Basecolor
                        self.Dstate = False
                        self.Dbutton["background"] = self.Basecolor
                else:
                        self.DeadClick()
                        self.Nstate = False
                        self.Nbutton["background"] = self.Basecolor
                        self.BlankFrame()
                
        def DeadClick(self):
                if self.Bstate == True:
                        self.menu_frame.destroy()
                        self.Bstate = False
                elif self.Cstate == True:
                        self.C_frame.destroy()
                        self.Cstate = False
                elif self.Dstate == True:
                        self.D_frame.destroy()
                        self.Dstate = False
                elif self.Nstate == True:
                        self.N_frame.destroy()
                        self.Nstate = False
        def OnClick(self, event):        #INCOMPLETE DUE TO SERIAL
                if self.Cstate == True:
                        if self.Comp_on_button_state == False:
                                self.ser.write(BeltMessages.mode('1'))
                                self.Comp_On_Button["background"] = "green"
                                self.Comp_On_Button["text"] = "ON"
                                self.Comp_on_button_state = True
                                self.Clabel["text"] =  "Please press 'Start' to begin."                                
                        elif self.Comp_on_button_state == True:
                                self.Comp_On_Button["background"] = self.Basecolor
                                self.Comp_On_Button["text"] = "OFF"
                                self.Comp_on_button_state = False
                                self.Clabel["text"] =  ""
                
                elif self.Dstate == True:
                        if self.Direct_on_button_state == False:
                                self.ser.write(BeltMessages.mode('2'))
                                self.Direct_On_Button["background"] = "green"
                                self.Direct_On_Button["text"] = "ON"
                                self.Direct_on_button_state = True
                                self.Dlabel["text"] =  "Please press 'Start' to begin."                                
                        elif self.Direct_on_button_state == True:
                                self.Direct_On_Button["background"] = self.Basecolor
                                self.Direct_On_Button["text"] = "OFF"
                                self.Direct_on_button_state = False
                                self.Dlabel["text"] =  ""
                        
                elif self.Nstate == True:        
                        if self.Nav_on_button_state == False:
                                self.ser.write(BeltMessages.mode('3'))
                                self.Nav_On_Button["background"] = "green"
                                self.Nav_On_Button["text"] = "ON"
                                self.Nav_on_button_state = True
                                self.Nlabel["text"] =  "Please press 'Start' to begin."                                
                        elif self.Nav_on_button_state == True:
                                self.Nav_On_Button["background"] = self.Basecolor
                                self.Nav_On_Button["text"] = "OFF"
                                self.Nav_on_button_state = False
                                self.Nlabel["text"] =  ""
        def NavCoord(self,event):
                self.NavCoordState = True
                
                self.addressButtonFrame.destroy()
                self.coordButtonFrame.destroy()
                
                #Latitude frame, label, and entry box of Navigational Mode
                leftN_frame = Frame(self.N_frame)
                leftN_frame.pack(side=LEFT, padx = 30)
                
                latLabel1 = Label(leftN_frame, text = "Latitude of Current Location")
                latLabel1.pack(side=TOP)
                
                self.NLatStartEntry = Entry(leftN_frame)
                self.NLatStartEntry.pack(side=TOP)
                
                formatLabel1 = Label(leftN_frame, text = "Format: 000.0000")
                formatLabel1.pack(side=TOP)
        
                blankLabel = Label(leftN_frame, text = "")
                blankLabel.pack()
                                
                formatLabel2 = Label(leftN_frame, text = "Format: 000.0000")
                formatLabel2.pack(side=BOTTOM)
                self.NLatFinalEntry = Entry(leftN_frame)
                self.NLatFinalEntry.pack(side=BOTTOM)
                
                latLabel2 = Label(leftN_frame, text = "Latitude of Final Destination")
                latLabel2.pack(side=BOTTOM)
                #Longitude frame, label, and entry box of Nav Mode
                rightN_frame = Frame(self.N_frame)
                rightN_frame.pack(side=RIGHT, padx = 30)
                
                longLabel = Label(rightN_frame, text = "Longitude of Current Location")
                longLabel.pack(side=TOP)
                
                self.NLongStartEntry = Entry(rightN_frame)
                self.NLongStartEntry.pack(side=TOP)
                        
                formatLabel2 = Label(rightN_frame, text = "Format: 000.0000")
                formatLabel2.pack(side=TOP)
                
                blankLabel = Label(rightN_frame, text = "")
                blankLabel.pack()
                                
                formatLabel2 = Label(rightN_frame, text = "Format: 000.0000")
                formatLabel2.pack(side=BOTTOM)
                self.NLongFinalEntry = Entry(rightN_frame)
                self.NLongFinalEntry.pack(side=BOTTOM)
                
                latLabel2 = Label(rightN_frame, text = "Longitude of Final Destination")
                latLabel2.pack(side=BOTTOM)
        def NavAddress(self, event):
                self.NavAddressState = True
                
                self.addressButtonFrame.destroy()
                self.coordButtonFrame.destroy()
                
                addressLabel1 = Label(self.N_frame, text = "Address of Current Location")
                addressLabel1.pack(side=TOP)
                
                self.NAddressStartEntry = Entry(self.N_frame)
                self.NAddressStartEntry.pack(side=TOP)
                
                blankLabel = Label(self.N_frame, text = "")
                blankLabel.pack(side=BOTTOM)
                self.NAddressFinalEntry = Entry(self.N_frame)
                self.NAddressFinalEntry.pack(side=BOTTOM)
                
                addressLabel2 = Label(self.N_frame, text = "Address of Final Destination")
                addressLabel2.pack(side=BOTTOM)
        def StartClick(self, event):
                if self.Bstate == True:
                        self.BlankGo()
                elif self.Cstate == True:
                        self.CompGo()
                elif self.Dstate == True:
                        self.DirectGo()
                elif self.Nstate == True:
                        self.NavGo()
                
        def BlankGo(self):
                pass
                        
        def CompGo(self):        #INCOMPLETE DUE TO SERIAL
                if self.Comp_on_button_state == False:
                        self.Clabel["text"]= "Please turn Compass on before pressing Start."
                else:
                        #self.ser.write('Compass')        #(1)
                        #print "Compass"
                        self.myParent.destroy()
                
        def DirectGo(self):        #INCOMPLETE DUE TO SERIAL
                if self.Direct_on_button_state == False:
                        self.Dlabel["text"]= "Please turn Directional Mode on before pressing Start."
                else:
                        LatText = self.DLatEntry.get()
                        LongText = self.DLongEntry.get()
                        AddressText = self.DAddressEntry.get()
                        if len(LatText) > 0 and len(LongText) > 0:
                                try:
                                        LatFloat = float(LatText)
                                        LongFloat = float(LongText)
                                        if abs(LatFloat) > 90 or abs(LongFloat) > 180:
                                                raise ValueError("herp a derp derp")
                                        self.ser.write(BeltMessages.begin(1))
                                        self.ser.write(BeltMessages.point(0, LatFloat, LongFloat))
                                        self.ser.write(BeltMessages.end())
                                        self.myParent.destroy()
                                except ValueError:
                                        self.Dlabel["text"] = "Please insert lat. and long. in correct format. You troll."
                        elif len(AddressText) > 0:
                                try:
                                        Lat, Lng = gmaps.address_to_latlng(AddressText)
                                        print Lat, Lng
                                        self.ser.write(BeltMessages.begin(1))
                                        self.ser.write(BeltMessages.point(0, Lat, Lng))
                                        self.ser.write(BeltMessages.end())
                                        self.myParent.destroy()
                                except GoogleMapsError:
                                        self.Dlabel["text"] = "Invalid Address"
                        else:
                                self.Dlabel["text"] = "Please insert a destination in one category"
                
        def NavGo(self):
                if self.Nav_on_button_state == False:
                        self.Nlabel["text"]= "Please turn Navigational Mode on before pressing Start."
                else:
                        if self.NavCoordState == True:
                                LatStartText = self.NLatStartEntry.get()
                                LongStartText = self.NLongStartEntry.get()
                                LatFinalText = self.NLatFinalEntry.get()
                                LongFinalText = self.NLongFinalEntry.get()
                                AddressStartText = ''
                                AddressFinalText = ''
                        elif self.NavAddressState == True:
                                LatStartText = ''
                                LongStartText = ''
                                LatFinalText = ''
                                LongFinalText = ''
                                AddressStartText = self.NAddressStartEntry.get()
                                AddressFinalText = self.NAddressFinalEntry.get()
                        else:
                                LatStartText = ''
                                LongStartText = ''
                                LatFinalText = ''
                                LongFinalText = ''
                                AddressStartText = ''
                                AddressFinalText = ''
                        
                        if len(LatStartText) > 0 and len(LongStartText) > 0 and len(LatFinalText) > 0 and len(LongFinalText) > 0:
                                try:
                                        LatStartFloat = float(LatStartText)
                                        LongStartFloat = float(LongStartText)
                                        
                                        LatFinalFloat = float(LatFinalText)
                                        LongFinalFloat = float(LongFinalText)
                                except ValueError:
                                        self.Nlabel["text"] = "Please insert lat. and long. in correct format. You troll."
                                try:
                                        reverseGeoStart = gmaps.reverse_geocode(LatStartFloat, LongStartFloat)
                                        startAddress = reverseGeoStart['Placemark'][0]['address']
        
                                        reverseGeoFinal = gmaps.reverse_geocode(LatFinalFloat, LongFinalFloat)
                                        finalAddress = reverseGeoFinal['Placemark'][0]['address']
                                        
                                        self.NavData(startAddress, finalAddress)
                                except GoogleMapsError:
                                        self.Nlabel["text"] = "Unknown coordinates. Try other coordinates or via address instead."
                        elif len(AddressStartText) > 0 and len(AddressFinalText) > 0:
                                try:
                                        self.NavData(AddressStartText, AddressFinalText)
                                except GoogleMapsError:
                                        self.Nlabel["text"] = "Unknown address. Try another address or via coordinates instead."
                        else:
                                self.Nlabel["text"] = "Choose Coordinates or Address"
                
        #Function that takes a start and end address, and prints/sends the nav. coordinates        
        def NavData(self, start, finish):        #INCOMPLETE DUE TO SERIAL
                dirs = gmaps.directions(start, finish)
                route = dirs['Directions']['Routes'][0]
                print "Navigational"
                self.ser.write(BeltMessages.begin(len(route['Steps'])))
                for idx, step in enumerate(route['Steps']):
                        print step['Point']['coordinates'][1], step['Point']['coordinates'][0]
                        latitude = step['Point']['coordinates'][1]
                        longitude = step['Point']['coordinates'][0]
                        self.ser.write(BeltMessages.point(idx, latitude, longitude))        
                self.ser.write(BeltMessages.end())
                self.myParent.destroy()        
                
        def build_message(self, latitude, longitude):
                return self.msg.pack(latitude*100000, longitude*100000)
                
root = Tk()
myapp = app(root)
root.mainloop()