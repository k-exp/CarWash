from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty
from ServiceModification import ServiceModification
import re


#Window.fullscreen = True

class ImgButton(Button):
    img = StringProperty("car.png")


class PasswordPopup( Popup ):

    def open(self, *largs):
        super(PasswordPopup,self).open()
        self.ids.message.text = largs[0]
    def closeThis(self):
        self.dismiss()




class CarUI( TabbedPanel ):
    # This is run once.
    Window.size = (1024, 600)

    # Admin password for saving service changes.
    adminPassword = "carKEXP882"

    # Service name dictionary. Key: service id
    services = {}
    # Service costs dictionary. Key: service id.
    serviceCosts = {}
    # The list of services actively selected.
    activeServices = []

    # List of cars in the queue as ServiceModification objects.
    carQueue = []

    def loadFiles(self):
        numREGX = re.compile('\d+(\.\d+)?')

        # First service Selector
        buttonLabels1 = open("services1", "r")
        buttonCounter = 1
        for label in buttonLabels1:
            label = label.replace('\n', '')
            if (not numREGX.match(label)):
                # If we are reading in service name.
                self.ids["s1_b" + str(buttonCounter)].text = label
                self.services[buttonCounter] = label
            else:
                # We are reading in service cost.
                self.serviceCosts[buttonCounter] = float(label)
                buttonCounter += 1
        buttonLabels1.close()

        # Second service selector.
        buttonLabels2 = open("services2", "r")
        buttonCounter = 13
        for label in buttonLabels2:
            # Remove the newline character at the end of the line.
            label = label.replace('\n', '')
            if (not numREGX.match(label)):
                # If we are reading in service name.
                self.ids["s2_b" + str(buttonCounter)].text = label
                self.services[buttonCounter] = label
            else:
                # We are reading in service cost.
                self.serviceCosts[buttonCounter] = float(label)
                buttonCounter += 1
        buttonLabels2.close()

    # Init. Load service names from the services files and map them to the UI button text.
    def __init__(self, **kwargs):
        #super(ContainerBox, self).__init__(**kwargs)
        super(CarUI, self).__init__(**kwargs)

        self.loadFiles()

        # Fill out settings page.

        settingsChildren = self.ids.serviceSettings.children

        # The children are listen in reverse, where the column headers are the last
        # elements. We want to start before the headers with the first row, then decrement.
        curIndex = len(settingsChildren) - 4


        while curIndex >= 0:
            # Cur Index - 0 = ID label
            # Cur Index - 1 = Input Name
            # Cur Index - 2 = Input Cost

            # If we a processing the settings row, not the last row that has the id "Admin Password"
            if( settingsChildren[curIndex].text.isdigit() ):
                settingsChildren[ curIndex - 1 ].text = self.services[ int(settingsChildren[curIndex].text)  ]
                settingsChildren[ curIndex - 2 ].text = str(self.serviceCosts[ int(settingsChildren[curIndex].text) ])
            curIndex -= 3

    def buttonPressHandler(self, id):
        #100 = enter button on first pane pressed
        #200 = enter button on second pane pressed.

        if(id != 100 and id != 200):
            serviceSelection = "s1_b"

            if( id > 12 ):
                serviceSelection = "s2_b"


            # Toggle service logic.
            # If service is not selected, turn it green. If it is selected, turn it back to the default color.
            if( self.ids[serviceSelection+str(id)].background_color[0] != 0):
                # Select service.
                self.ids[serviceSelection+str(id)].background_color = (0,1,0,1)
                self.activeServices.append(id)
            else:
                # Unselect service.
                self.ids[serviceSelection+ str(id)].background_color = (1, 1, 1, 1)
                self.activeServices.remove( id )

            self.ids.servicesOut1.text = ""
            self.ids.servicesOut2.text = ""

            for serviceID in self.activeServices:
                self.ids.servicesOut1.text += self.services[serviceID] + " | "
                self.ids.servicesOut2.text += self.services[serviceID] + " | "

        else:
            # Enter button pressed.
            if( len(self.activeServices) >= 1):
                bttn = Button()
                bttn.size_hint = "None", "None"

                for serviceID in self.activeServices:
                    bttn.text += " | "+ self.services[serviceID]

                bttn.text += " |"


                bttn.height = 80
                bttn.width = len(bttn.text) * 7

                # Adjust the size of large buttons.
                if( bttn.width > self.width ):
                    bttn.text_size = (self.width/2.5, bttn.height )
                    bttn.width = bttn.width / 2.5

                bttn.valign = "middle"

                svsMod = ServiceModification(ref=self,index=len(self.carQueue), buttonRef=bttn)
                self.carQueue.append(svsMod)
                bttn.on_press = lambda : svsMod.open()

                self.ids.carQueue.add_widget(bttn)

            self.clearServices()


    def clearServices(self):
        # When we press the enter button and enqueue the car, we need to clear.

        for id in range(1,25):

            serviceSelection = "s1_b"

            if (id > 12):
                serviceSelection = "s2_b"

            # Unselect service.
            self.ids[serviceSelection + str(id)].background_color = (1, 1, 1, 1)

        self.ids.servicesOut1.text = ""
        self.ids.servicesOut2.text = ""
        self.activeServices = []


    def saveSettings(self):
        #TODO: Only save if the proper password is added.
        settingsChildren = self.ids.serviceSettings.children
        passwordInput = self.ids.savePass.text

        p = PasswordPopup()

        if(passwordInput.strip() == self.adminPassword):

            ############## Write changes to file #########################
            # The children are listen in reverse, where the column headers are the last
            # elements. We want to start before the headers with the first row, then decrement.
            curIndex = len(settingsChildren) - 4

            servicesFile1 = open("services1", "w")
            servicesFile2 = open("services2", "w")

            while curIndex >= 0:
                # Cur Index - 0 = ID label
                # Cur Index - 1 = Input Name
                # Cur Index - 2 = Input Cost
                if( settingsChildren[curIndex].text.isdigit() ):
                    if( int(settingsChildren[curIndex].text) <  13 ):
                        servicesFile1.write(settingsChildren[curIndex - 1].text + "\n" )
                        servicesFile1.write(settingsChildren[curIndex - 2].text + "\n")
                    else:
                        servicesFile2.write(settingsChildren[curIndex - 1].text + "\n")
                        servicesFile2.write(settingsChildren[curIndex - 2].text + "\n")
                curIndex -= 3

            servicesFile1.close()
            servicesFile2.close()
            ############################################################

            ########## LOAD CHANGES TO UI ##############################
            self.loadFiles()
            #################################################

            #Popup to confirm change in settings.
            p.open("Settings Changed")
        else:
            p.open("Incorrect Password!\nSettings not changed.")


    def removeCar(self, car):
        self.carQueue.remove(car)




class CarUIApp( App ):
    def build(self):
        return CarUI()

if __name__ == '__main__':
    CarUIApp().run()

