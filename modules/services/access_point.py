import util, config
import os
from threading import Thread
from service import Service

#
# Implements a fake wireless access point for harvesting credentials/keys/etc
# Requires airbase-ng
#

class APService(Service):
	def __init__(self):
		self.ap_essid = 'zoopzop'
		self.mon_adapt = None
		super(APService,self).__init__('Access Point')
	
	# init bg
	def initialize_bg(self):
		if not util.check_program('airbase-ng'):
			util.Error('\'airbase-ng\' not found in local path.')
			return False

		while True:
			try:
				tmp = raw_input('[!] Enter ESSID [%s]: '%self.ap_essid)
				if len(tmp) > 2:
					self.ap_essid = tmp
				break
			except KeyboardInterrupt:
				break
			except:
			 	continue

		util.Msg('Initializing access point..')
		thread = Thread(target=self.initialize)
		thread.start()
		return True

	# init
	def initialize(self):
		if not util.check_program('airbase-ng'):
			util.Error('\'airbase-ng\' not found in local path.')
			return False
	
		self.running = True
		ap_proc = None
			
		try:
			self.mon_adapt = util.get_monitor_adapter()
			if self.mon_adapt is None:
				self.mon_adapt = util.enable_monitor()
					
			airbase_cmd = [
						'airbase-ng',
						'--essid', self.ap_essid,
						self.mon_adapt
						  ]
			ap_proc = util.init_app(airbase_cmd, False)
			while self.running: pass
		except KeyboardInterrupt:
			self.running = False
		except Exception, er:
			util.Error('Error with wireless AP: %s'%er)
		finally:
			util.disable_monitor()
			util.kill_app(ap_proc)