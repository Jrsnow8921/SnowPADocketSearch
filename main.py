from SnowDocketScrMJ import *
from SnowDocketScrCP import *



class SnowDocketSearch():

  def search(self):
    x = str(raw_input('Please input a 0 for MJ Cases or a 1 for CP Cases: '))
    if x == '0':
      SnowDocketScrMJ().run()
      SnowDocketScrMJ().driverClose()
    elif x == '1':
      SnowDocketScrCP().run()
      SnowDocketScrCP().driverClose()


SnowDocketSearch().search()
