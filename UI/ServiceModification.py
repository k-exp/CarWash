from kivy.uix.popup import Popup

class ServiceModification( Popup ):

    selectedServices = []
    carUIRef = None
    index = None
    buttonRef = None

    def __init__(self, **kwargs):
        super(ServiceModification, self).__init__(**kwargs)

        self.index     = kwargs["index"]
        self.carUIRef  = kwargs["ref"]
        self.buttonRef = kwargs["buttonRef"]

        self.selectedServices = self.carUIRef.activeServices

        # Populate the buttons.
        for serviceID in range(1, 25):
            self.ids["b" + str(serviceID)].text = self.carUIRef.services[serviceID]
            if(serviceID in self.selectedServices ):
                self.ids["b" + str(serviceID)].background_color = (0, 1, 0, 1)


    def open(self, *largs):
        super(ServiceModification,self).open()


    def closeThis(self):
        self.dismiss()

    def removeCar(self):
        self.carUIRef.removeCar(self)
        self.buttonRef.parent.remove_widget(self.buttonRef)
        self.closeThis()

    def buttonPressHandler(self,bttnID):

        # Toggle service logic.
        # If service is not selected, turn it green. If it is selected, turn it back to the default color.
        if (self.ids["b" + str(bttnID)].background_color[0] != 0):
            # Select service.
            self.ids["b"+ str(bttnID)].background_color = (0, 1, 0, 1)
            self.addService(bttnID)
        else:
            # Unselect service.
            self.ids["b"+ str(bttnID)].background_color = (1, 1, 1, 1)
            self.removeService(bttnID)


        self.buttonRef.text = ""

        for serviceID in self.selectedServices:
            self.buttonRef.text += " | "+self.carUIRef.services[serviceID]

        self.buttonRef.text += " |"

        self.buttonRef.height = 80
        self.buttonRef.width = len(self.buttonRef.text) * 7

        # Adjust the size of large buttons.
        if (self.buttonRef.width > self.width):
            self.buttonRef.text_size = (self.width / 2.5, self.buttonRef.height)
            self.buttonRef.width = self.buttonRef.width / 2.5

    def removeService(self,index):
        self.selectedServices.remove(index)


    def addService(self, servID):
        self.selectedServices.append(servID)
