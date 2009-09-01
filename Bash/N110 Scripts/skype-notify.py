#!/usr/bin/env python
#	Python script to make Skype use notify-osd

# Copyright (c) 2009, Lightbreeze

# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# to use this script: Open Skype -> Open the menu and press 'Options' or press Ctrl-O
# -> hit the 'Advanced' button and check 'Execute the following script on _any_ event'
# -> paste: python /path/to/skype-notify.py -e"%type" -n"%sname" -f"%fname" -p"%fpath" -m"%smessage" -s%fsize -u%sskype
# -> disable or enable the notifications you want to receive.

# TODO: add sound if it is not synchronising; add indicator-applet presence; add buddy photo in IM
import pynotify
import sys
from optparse import OptionParser

# for indicator-applet: import indicate
# for sound: import gst

class NotifyForSkype:
	def __init__(self):
		# Initiate pynotify
		if not pynotify.init("Skype Notifier"):
		    sys.exit(-1)

		# Add argument parser options
		parser = OptionParser()
		parser.add_option("-e", "--event", dest="type", help="type of SKYPE_EVENT")
		parser.add_option("-n", "--sname", dest="sname", help="display-name of contact")
		parser.add_option("-u", "--skype", dest="sskype", help="skype-username of contact")
		parser.add_option("-m", "--smessage", dest="smessage", help="message body", metavar="FILE")
		parser.add_option("-p", "--path", dest="fpath", help="path to file")
		parser.add_option("-s", "--size", dest="fsize", help="incoming file size")
		parser.add_option("-f", "--filename", dest="fname", help="file name", metavar="FILE")
		(o, args) = parser.parse_args()

		print(args)
		print(sys.argv)
		print(o.type)
		
		# If event type x show notification (summary, body, icon)
		# Summary should not be None
		if o.type == 'SkypeLogin': self.showNotification("Skype","You have logged into Skype with {contact}".format(contact=o.sname),"skype")
		elif o.type == 'SkypeLogout': self.showNotification("You have logged out of Skype",None,"user-offline")
		elif o.type == 'SkypeLoginFailed': self.showNotification("Skype login failed",None,"user-offline")
		elif o.type == 'CallConnecting': self.showNotification("Dailing... {contact}".format(contact=o.sname),None,"skype") #some of these should be merged and update to the same bubble: Call Connecting -> CallRingingOut -> Call Asnwered
		elif o.type == 'CallRingingIn': self.showNotification("Brring..","{contact} is calling you".format(contact=o.sname),"skype")
		elif o.type == 'CallRingingOut': self.showNotification("Dididi.. dididi...","You are calling {contact}".format(contact=o.sname),"skype") #merge ^^ see above
		elif o.type == 'CallAnswered': self.showNotification("Call Answered",None,"skype")
		elif o.type == 'VoicemailReceived': self.showNotification(o.sname,"Voicemail Received","skype")
		elif o.type == 'VoicemailSent': self.showNotification("Voicemail Sent",None,"skype")
		elif o.type == 'ContactOnline': self.showNotification("{contact} is now online".format(contact=o.sname),None,"skype")
		elif o.type == 'ContactOffline': self.showNotification("{contact} is now offline".format(contact=o.sname),None,"user-offline")
		elif o.type == 'ContactDeleted': self.showNotification("Contact Deleted", "{contact} has been deleted from your contact list".format(contact=o.sname),"skype")
		elif o.type == 'ChatIncomingInitial': self.showNotification("{contact}".format(contact=o.sname),o.smessage,"notification-message-IM")
		elif o.type == 'ChatIncoming': self.showNotification("{contact}".format(contact=o.sname),o.smessage,"notification-message-IM")
		elif o.type == 'ChatOutgoing': self.showNotification("{contact}".format(contact=o.sname),o.smessage,"notification-message-IM")
		elif o.type == 'ChatJoined': self.showNotification("{contact} joined chat".format(contact=o.sname),o.smessage,"emblem-people")
		elif o.type == 'ChatParted': self.showNotification("{contact} left chat".format(contact=o.sname),o.smessage,None)
		elif o.type == 'TransferComplete': self.showNotification("Transfer Complete","{filename} saved to {path}{filename}".format(filename=o.fname,path=o.fpath),"gtk-save")
		elif o.type == 'TransferFailed': self.showNotification("Transfer Failed","{filename}".format(filename=o.fname),"gtk-close")
		elif o.type == 'Birthday': self.showNotification("{contact} has a birthday Tomorrow".format(contact=o.sname),None,"appointment-soon")

	def showNotification(self, summary, message, ikon):
		'''takes a title sumamry and a message to display the email notification. Returns the created notification object'''
		if summary == None: summary = " "		
		n = pynotify.Notification(summary, message, ikon)
		n.show()
		print("showNotification..")
		return n

cm = NotifyForSkype()
