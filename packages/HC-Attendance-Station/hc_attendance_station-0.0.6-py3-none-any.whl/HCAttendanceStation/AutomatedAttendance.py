import requests
import json
import sys
import usb.core
import usb.util
import msvcrt
import os
import zoneinfo
import time
import keyring
import winsound
from datetime import datetime
from datetime import date
from datetime import timezone
from datetime import timedelta
import keyboard
keyboard.press('f11')

# DEPENDENCIES:
# pip install requests
# pip install keyring
# pip install pyusb
# pip install tzdata
# pip install keyboard
# pip install hc-attendance-station
# install the libusb-1.0.dll windows dll from the MinGW64 directory in c:\windows\system32
# download zadig-2.8.exe and select "list all devices" and install the WinUSB driver for the magstrip reader (MAGTEK 21040110 USB ID: 0801 0001)
# download goodswipe.wav from project folder and place in C:\Windows\Media\

printDebug = False  # Set to False when finished testing

testDate = None 
testTime = None 
testEnvironment = False  
testFacultyID = False
testStudentID = False

webAPICredential = keyring.get_credential('ethos', '')	
webAPIBody = {"UserId":webAPICredential.username, "Password":webAPICredential.password}

ethosProdAPIKey = keyring.get_credential('ProdKey', '')
ethosTestAPIKey = keyring.get_credential('TestKey', '')

ethosURL = 'https://integrate.elluciancloud.com'
ethosToken = ''

webAPIURL = 'https://webapi.hocking.edu/Colleagueapi' # PROD
webQAPIURL = 'https://webapi.hocking.edu/Colleagueapi/qapi' # PROD
ethosAPIKey = {'Authorization': 'Bearer ' + ethosProdAPIKey.password} # PROD

ethosAcceptV16 = 'application/vnd.hedtech.integration.v16+json'
colleagueAPIAcceptV1 = 'application/vnd.ellucian.v1+json'
colleagueAPIAcceptV2 = 'application/vnd.ellucian.v2+json'
colleagueAPIAcceptV5 = 'application/vnd.ellucian.v5+json'
authAccept = {'Accept': colleagueAPIAcceptV2}

ethosAuthURL = ethosURL + '/auth'
academic_periodsAPI = ethosURL + '/api/academic-periods'
sectionsAPI = ethosURL + '/api/sections'


attendanceStart = timedelta(minutes=15)
attendanceEnd = timedelta(minutes=5)


# Begin Initialize USB Card Reader -------->
#
# for dev in usb.core.find(find_all=True):
#     print(dev)

VENDOR_ID = 0x0801
PRODUCT_ID = 0x0001
DATA_SIZE = 192

# find the MagTek reader

device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if device is None:
	sys.exit("Could not find MagTek USB HID Swipe Reader.")

# make sure the hiddev kernel driver is not active

# if device.is_kernel_driver_active(0):
#     try:
#         device.detach_kernel_driver(0)
#     except usb.core.USBError as e:
#         sys.exit("Could not detatch kernel driver: %s" % str(e))

# set configuration

try:
	# device.reset()  # Does not seem to be needed
	device.set_configuration()
except usb.core.USBError as e:
	sys.exit("Could not set configuration: %s" % str(e))

endpoint = device[0][(0,0)][0]
#
# <-------- End Initialize USB Card Reader

def add_one(number):
    return number + 1

def clear(): # Clear the console screen
	os.system('cls')

def kbfunc(): # Detect a keybaord interrupt
	return ord(msvcrt.getch()) if msvcrt.kbhit() else 0

def swipeCard(cardType):
	data = []
	swiped = False

	if cardType == 'Faculty':
		print('Please swipe your Faculty ID Card to search for sections.')
	else:
		print ("Please swipe your Student ID Card to record your attendance.")
	
	print('\n')
	print ('Press any key to return to the Main Menu.')
	print('\n')

	while 1:
		try:
			data += device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
			if not swiped: 
				print ("Reading...")
				# print (data)
			swiped = True
		except usb.core.USBError as e:
			# print (e.args, swiped)
			if kbfunc() != 0:
				break
			if e.args == (10060, 'Operation timed out') and swiped:
				if len(data) < DATA_SIZE or len(data) > DATA_SIZE:
					print ("Bad swipe, try again. (%d bytes)" % len(data))
					print ("Data: %s" % ''.join(map(chr, data)))
					winsound.PlaySound(r"C:\Windows\Media\Windows Critical Stop.wav", winsound.SND_FILENAME)
					data = []
					swiped = False
					continue
				else:
					break   # we got it!
		except KeyboardInterrupt:
			if printDebug == True:
				print ('Ctrl + C')
			break

	# device.reset()  # Does not seem to be needed

	# the following dictionary converts keybaord values to their assocaited ASCII equivalent
	convertValue = {'0':'Reserved', '1':'ErrorRollOver', '2':'POSTFail', '3':'ErrorUndefined', '4':'a', '5':'b', '6':'c', '7':'d', '8':'e', '9':'f', '10':'g', '11':'h', '12':'i', '13':'j', '14':'k', '15':'l', '16':'m', '17':'n', '18':'o', '19':'p', '20':'q', '21':'r', '22':'s', '23':'t', '24':'u', '25':'v', '26':'w', '27':'x', '28':'y', '29':'z', '30':'1', '31':'2', '32':'3', '33':'4', '34':'5', '35':'6', '36':'7', '37':'8', '38':'9', '39':'0', '40':'Return', '41':'ESCAPE', '42':'DELETE', '43':'Tab', '44':'Spacebar', '45':'-', '46':'=', '47':'[', '48':']', '49':'\\', '50':'#', '51':';', '52':'`', '53':'`', '54':',', '55':'.', '56':'/'}

	word = []
	j = 2    

	for i in range(len(data)):
		if i == j:
			value = str(data[i])
			word.append(convertValue[value])
			j = j + 16

	delimeter = ''
	
	if printDebug == True:
		print(delimeter.join(word)[1:8])
	
	if delimeter.join(word)[:1] == ';' and delimeter.join(word)[10:11] == '/':
		return delimeter.join(word)[1:8]
	else:
		return None

def ZNow():
	if testDate != None:
		return datetime.strptime(testDate + testTime, '%Y-%m-%dT%H:%M:%S%z')
	else:
		return datetime.fromisoformat(datetime.now(timezone.utc).isoformat(timespec='seconds'))

def convertZDate(thisDate):
	return datetime.strptime(thisDate, '%Y-%m-%dT%H:%M:%S%z')

def convertZNow(meetingTime):
	if testDate != None:
		return datetime.strptime(testDate + meetingTime[10:], '%Y-%m-%dT%H:%M:%S%z')
	else:
		return datetime.strptime(str(date.today()) + meetingTime[10:], '%Y-%m-%dT%H:%M:%S%z')

def convertDate(thisDate):
	return datetime.strptime(thisDate, '%Y-%m-%dT%H:%M:%S') # 2021-01-19T00:00:00

def dateNow():
	if testDate != None:
		return datetime.strptime(testDate + 'T00:00:00', '%Y-%m-%dT%H:%M:%S') # 2021-01-19T00:00:00 date.today())
	else:
		return datetime.strptime(str(date.today()) + 'T00:00:00', '%Y-%m-%dT%H:%M:%S') # 2021-01-19T00:00:00 date.today())

def faculty_sectionsAPI(facultyID):
	faculty_sectionsAPI = webAPIURL + '/faculty/' + facultyID + '/sections'
	return faculty_sectionsAPI

def section_meeting_instancesAPI(sectionID):
	section_meeting_instancesAPI = webAPIURL + '/sections/' + sectionID + '/section-meeting-instances'
	return section_meeting_instancesAPI

def ethosRequestPut(ethosURL, ethosHeaders, ethosBody):
	ethosPut = requests.put(ethosURL, headers=ethosHeaders, json=ethosBody)
	# print(ethosPost.headers)
	if printDebug == True:
		print('ethosRequestPut ', ethosPut.status_code, '\n')
	return ethosPut

def ethosRequestPost(ethosURL, ethosHeaders, ethosBody):
	ethosPost = requests.post(ethosURL, headers=ethosHeaders, json=ethosBody)
	# print(ethosPost.headers)
	if printDebug == True:
		print('ethosRequestPost ', ethosPost.status_code, '\n')
	return ethosPost

def ethosRequestGet(ethosURL, ethosHeaders, ethosParams):
	ethosGet = requests.get(ethosURL, headers=ethosHeaders, params=ethosParams)
	if printDebug == True:
		print('ethosRequestGet ', ethosGet.status_code, '\n')
	return ethosGet

# def query_student_ids():
# 	global webAPIToken
# 	accept = {'Accept': colleagueAPIAcceptV1}
# 	apiBody = {'termId': '2022SP'}
# 	apiHeader = dict()
# 	apiHeader.update(accept)
# 	apiHeader.update(webAPIToken)
# 	studentIDS = ethosRequestPost(query_student_idsAPI, apiHeader, apiBody)
# 	if studentIDS.status_code == 401:
# 		print("renew webapi token")
# 		time.sleep(5)
# 		authAccept = {'Accept': colleagueAPIAcceptV2}
# 		webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
# 		accept = {'Accept': colleagueAPIAcceptV1}
# 		apiBody = {'termId': '2022SP'}
# 		apiHeader = dict()
# 		apiHeader.update(accept)
# 		apiHeader.update(webAPIToken)
# 		studentIDS = ethosRequestPost(query_student_idsAPI, apiHeader, apiBody)
# 	if studentIDS.status_code == 200:
# 		return json.loads(studentIDS.text)
# 	else:
# 		return None

def student_attendances(sectionID, attendanceDate):
	global webAPIToken
	accept = {'Accept': colleagueAPIAcceptV1}
	apiBody = {'SectionId': sectionID, 'IncludeCrossListedAttendances': False, 'AttendanceDate': attendanceDate}
	apiHeader = dict()
	apiHeader.update(accept)
	apiHeader.update(webAPIToken)
	studentAttendances = ethosRequestPost(student_attendancesAPI, apiHeader, apiBody)
	if studentAttendances.status_code == 401:
		authAccept = {'Accept': colleagueAPIAcceptV2}
		webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
		accept = {'Accept': colleagueAPIAcceptV1}
		apiBody = {'SectionId': sectionID, 'IncludeCrossListedAttendances': False, 'AttendanceDate': attendanceDate}
		apiHeader = dict()
		apiHeader.update(accept)
		apiHeader.update(webAPIToken)
		studentAttendances = ethosRequestPost(student_attendancesAPI, apiHeader, apiBody)
	if studentAttendances.status_code == 200:
		return json.loads(studentAttendances.text)
	else:
		return None

def student_attendancesPUT(attendance):
	global webAPIToken
	accept = {'Accept': colleagueAPIAcceptV1}
	apiBody = attendance
	apiHeader = dict()
	apiHeader.update(accept)
	apiHeader.update(webAPIToken)
	studentAttendances = ethosRequestPut(student_attendancesPUTAPI, apiHeader, apiBody)
	if studentAttendances.status_code == 401:
		authAccept = {'Accept': colleagueAPIAcceptV2}
		webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
		accept = {'Accept': colleagueAPIAcceptV1}
		apiBody = attendance
		apiHeader = dict()
		apiHeader.update(accept)
		apiHeader.update(webAPIToken)
		studentAttendances = ethosRequestPut(student_attendancesPUTAPI, apiHeader, apiBody)
	if studentAttendances.status_code == 200:
		return True
	else:
		return False

def faculty_sections(facultyID):
	global webAPIToken
	accept = {'Accept': colleagueAPIAcceptV5}
	apiHeader = dict()
	apiHeader.update(accept)
	apiHeader.update(webAPIToken)
	facultySections = ethosRequestGet(faculty_sectionsAPI(facultyID), apiHeader, '')
	if facultySections.status_code == 401:
		authAccept = {'Accept': colleagueAPIAcceptV2}
		webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
		accept = {'Accept': colleagueAPIAcceptV5}
		apiHeader = dict()
		apiHeader.update(accept)
		apiHeader.update(webAPIToken)
		facultySections = ethosRequestGet(faculty_sectionsAPI(facultyID), apiHeader, '')
	if facultySections.status_code == 200:
		return json.loads(facultySections.text)
	else:
		return None

def section_meeting_instances(sectionID):
	global webAPIToken
	accept = {'Accept': colleagueAPIAcceptV1}
	apiHeader = dict()
	apiHeader.update(accept)
	apiHeader.update(webAPIToken)
	sectionMeetingInstances = ethosRequestGet(section_meeting_instancesAPI(sectionID), apiHeader, '')
	if sectionMeetingInstances.status_code == 401:
		authAccept = {'Accept': colleagueAPIAcceptV2}
		webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
		accept = {'Accept': colleagueAPIAcceptV1}
		apiHeader = dict()
		apiHeader.update(accept)
		apiHeader.update(webAPIToken)
		sectionMeetingInstances = ethosRequestGet(section_meeting_instancesAPI(sectionID), apiHeader, '')
	if sectionMeetingInstances.status_code == 200:
		return json.loads(sectionMeetingInstances.text)
	else:
		return None

def academic_periods():
	global ethosToken
	accept = {'Accept': ethosAcceptV16}
	apiHeader = dict()
	apiHeader.update(ethosToken)
	apiHeader.update(accept)
	academicPeriods = ethosRequestGet(academic_periodsAPI, apiHeader, '')
	if printDebug == True:
		print("academicPeriods.status_code ", academicPeriods.status_code)
		time.sleep(5)
	if academicPeriods.status_code == 401:
		ethosToken = {'Authorization': 'Bearer ' + ethosRequestPost(ethosAuthURL, ethosAPIKey, '').text}
		accept = {'Accept': ethosAcceptV16}
		apiHeader = dict()
		apiHeader.update(ethosToken)
		apiHeader.update(accept)
		academicPeriods = ethosRequestGet(academic_periodsAPI, apiHeader, '')
	if academicPeriods.status_code == 200:
		return json.loads(academicPeriods.text)
	else:
		return None

def sections(currentTermID, offset):
	global ethosToken	
	accept = {'Accept': ethosAcceptV16}
	paramTerm = '{"academicPeriod":{"id":"' + currentTermID + '"}}'
	apiParams = {'criteria': paramTerm, 'limit': '100', 'offset': str(offset)}
	if printDebug == True:
		print(apiParams)
	apiHeader = dict()
	apiHeader.update(ethosToken)
	apiHeader.update(accept)
	sections = ethosRequestGet(sectionsAPI, apiHeader, apiParams)
	if sections.status_code == 401:
		ethosToken = {'Authorization': 'Bearer ' + ethosRequestPost(ethosAuthURL, ethosAPIKey, '').text}
		accept = {'Accept': ethosAcceptV16}
		paramTerm = '{"academicPeriod":{"id":"' + currentTermID + '"}}'
		apiParams = {'criteria': paramTerm, 'limit': '100', 'offset': str(offset)}
		if printDebug == True:
			print(apiParams)
		apiHeader = dict()
		apiHeader.update(ethosToken)
		apiHeader.update(accept)
		sections = ethosRequestGet(sectionsAPI, apiHeader, apiParams)
	if sections.status_code == 200:
		return json.loads(sections.text)
	else:
		return None

def currentAcademicTerm(mode):
	# Determine the current academic term in relation to today's date
	currentTerm = None
	currentTermID = None
	previousTerm = None
	previousTermID = None
	previousTermStartOnDate = None
	academicPeriods = academic_periods()
	for period in academicPeriods:
		periodStartOnDate = convertZDate(period['startOn'])
		periodEndOnDate = convertZDate(period['endOn'])
		if periodStartOnDate <= ZNow() and ZNow() <= periodEndOnDate:
			currentTerm = period['code']
			currentTermID = period['id']
			break
		if periodStartOnDate < ZNow() and periodEndOnDate < ZNow():
			if previousTermStartOnDate == None or periodStartOnDate > previousTermStartOnDate:
				previousTermStartOnDate = periodStartOnDate
				previousTerm = period['code']
				previousTermID = period['id']
	if currentTerm == None and currentTermID == None and previousTerm != None:
		currentTerm = previousTerm
		currentTermID = previousTermID
	if mode == 'TermID':
		return currentTermID
	else:
		return currentTerm

def recordAttendance(section):
	swipeLoop = True
	while swipeLoop == True:
		clear()
		activeStu = 0
		studentID = swipeCard('')
		if testStudentID == True:
			if studentID == '0752679':
				studentID = '0739311' # '0753825'
		
		if studentID == None:
			swipeLoop = False
		else:
			if (convertZNow(currentMeetingDate[section['Id']]['StartTime']) <= (ZNow() + attendanceStart)) and (convertZNow(currentMeetingDate[section['Id']]['EndTime']) >= (ZNow() - attendanceEnd)):
				for stu in section['ActiveStudentIds']:
					if stu == studentID:
						activeStu = 1

				if activeStu == 1:
					recordAttendance = {"StudentId": studentID,
						"SectionId": section['Id'],
						"MeetingDate": currentMeetingDate[section['Id']]['MeetingDate'],
						"AttendanceCategoryCode": 'P',
						"StartTime": currentMeetingDate[section['Id']]['StartTime'],
						"EndTime": currentMeetingDate[section['Id']]['EndTime'],
						"InstructionalMethod": currentMeetingDate[section['Id']]['InstructionalMethod'],
						"Comment": "Card Present Swipe"}

					if printDebug == True:
						print(recordAttendance)
					recordPUT = student_attendancesPUT(recordAttendance)

					if recordPUT == True:
						clear()
						print(f'Attendance for Student ID {studentID} has been recorded successfully.')
						#winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
						winsound.PlaySound(r"C:\Windows\Media\goodswipe.wav", winsound.SND_FILENAME)
						# time.sleep(1)
					else:
						clear()
						print('FAILED: COULD NOT UPDATE ATTENDANCE')
						#winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
						winsound.PlaySound(r"C:\Windows\Media\Windows Critical Stop.wav", winsound.SND_FILENAME)
						time.sleep(5)

				else:
					clear()
					print('You are not an active student in this class!  Please see the instructor.')
					#winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
					winsound.PlaySound(r"C:\Windows\Media\Windows Critical Stop.wav", winsound.SND_FILENAME)
					time.sleep(5)
			else:
				clear()
				print('Unable to record attendance at this time.')
				#winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
				winsound.PlaySound(r"C:\Windows\Media\Windows Critical Stop.wav", winsound.SND_FILENAME)
				time.sleep(5)

def recordAbsenses(section):
	clear()
	missingStudents = 0
	if printDebug == True:
		print(section)
	recordGET = student_attendances(section['Id'], currentMeetingDate[section['Id']]['MeetingDate'])
	if printDebug == True:
		print(recordGET)
	presentStudents = []
	for stu in recordGET:
		presentStudents.append(stu['StudentId'])
	if printDebug == True:
		print(presentStudents, 'presentStudents')
	activeStudents = section['ActiveStudentIds']
	if printDebug == True:
		print (activeStudents)
	for student in section['ActiveStudentIds']:
		if student not in presentStudents:
			if printDebug == True:
				print(student, 'not present')
			recordAttendance = {"StudentId": student,
			"SectionId": section['Id'],
			"MeetingDate": currentMeetingDate[section['Id']]['MeetingDate'],
			"AttendanceCategoryCode": 'A',
			"StartTime": currentMeetingDate[section['Id']]['StartTime'],
			"EndTime": currentMeetingDate[section['Id']]['EndTime'],
			"InstructionalMethod": currentMeetingDate[section['Id']]['InstructionalMethod'],
			"Comment": "Automated Absent Recording"}

			if printDebug == True:
				print(recordAttendance)
			recordPUT = student_attendancesPUT(recordAttendance)
			if recordPUT == True:
				print(student, "- recorded as absent.")
				missingStudents += 1

	print(missingStudents, "students were marked as Absent")
	time.sleep(10)

clear()

facultyID = swipeCard('Faculty')
if facultyID == '0746743':
	testDate = '2021-04-01'     # '2021-04-01'  # '2021-04-06T00:00:00'  # Set to None for system date
	testTime = 'T14:55:00Z'  # Set to None for system time
	testEnvironment = True  # Set to False for production
	facultyID = '0001010' # '0757955'  
	testStudentID = True
	webAPIURL = 'https://webapitest.hocking.edu/Colleagueapi' # TEST
	webQAPIURL = 'https://webapitest.hocking.edu/Colleagueapi/qapi' # TEST
	ethosAPIKey = {'Authorization': 'Bearer ' + ethosTestAPIKey.password} # TEST
	webAPIAuthURL = webAPIURL + '/session/login'
	student_attendancesPUTAPI = webAPIURL + '/student-attendances'
	#query_student_idsAPI = webQAPIURL + '/query-student-ids'
	student_attendancesAPI = webQAPIURL + '/student-attendances'
	webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
	ethosToken = {'Authorization': 'Bearer ' + ethosRequestPost(ethosAuthURL, ethosAPIKey, '').text}
else:
	webAPIAuthURL = webAPIURL + '/session/login'
	student_attendancesPUTAPI = webAPIURL + '/student-attendances'
	student_attendancesAPI = webQAPIURL + '/student-attendances'
	webAPIToken = {'X-CustomCredentials': ethosRequestPost(webAPIAuthURL, authAccept, webAPIBody).text}
	ethosToken = {'Authorization': 'Bearer ' + ethosRequestPost(ethosAuthURL, ethosAPIKey, '').text}

currentTerm = currentAcademicTerm('')
if printDebug == True:
	print('Current Academic Term:', currentTerm)
	print('\n')
	
clear()
		
mainLoop = True
while mainLoop:
	currentSections = []
	currentMeetingDate = dict()
	# currentSections.clear()
	# print(facultySections)

	if facultyID != None:
		facultySectionsList = faculty_sections(facultyID)
		if printDebug == True:
			print(len(facultySectionsList))
			# print(facultySectionsList)
		for section in facultySectionsList:
			#print(section, '\n')
			if (section['TermId'] == currentTerm) and (section['Location'] != 'WEB') and (dateNow() >= convertDate(section['StartDate'])) and (dateNow() <= convertDate(section['EndDate'])):
				currentSections.append(section)
				if printDebug == True:
					print(section)
					print('\n')
					for student in section['ActiveStudentIds']:
						print(student)

		if printDebug == True:
			print(currentSections)

		if len(currentSections):
			for i in range(len(currentSections), 0, -1):
				i = i - 1
				meetingInstances = section_meeting_instances(currentSections[i]['Id'])
				if meetingInstances != None:
					meetToday = 0
					for meeting in meetingInstances:
						if convertDate(meeting['MeetingDate']) == dateNow():
							meetToday = 1
							currentMeetingDate[currentSections[i]['Id']] = meeting
							if printDebug == True:
								print(meeting)
				if meetToday == 0:
					del currentSections[i]
					
	else:
		clear()
		print('Current Academic Term:', currentTerm)
		print('\n')
		print('Failure reading your Faculty ID')
		print('\n')
		print('Terminating Program')
		print('\n')
		os.system("shutdown /r /t 0")
		quit()

	if printDebug != True:
		clear()
	
	print('Current Academic Term:', currentTerm)
	print('\n')
	print('Faculty ID:', facultyID)
	print('\n')
	print('Current time is:', str(ZNow().astimezone(zoneinfo.ZoneInfo('US/Eastern')))[:16])
	print('\n')
	if len(currentSections) == 0:
		print('Unable to find any sections you teach that meet today.')
		print('\n')
		time.sleep(5)
		clear()
		facultyID = swipeCard('Faculty')
	else:
		# print('Current Academic Term:', currentTerm)
		# print('\n')
		# print('Faculty ID:', facultyID)
		# print('\n')
		for i in range(len(currentSections)):
			#print(currentSections[i]['Meetings'][0]['StartTime'])
			#.replace(tzinfo=zoneinfo.ZoneInfo('US/Eastern'))
			print('[' + str(i) + ']', currentSections[i]['Id'], currentSections[i]['CourseName'], str(convertZDate(currentSections[i]['Meetings'][0]['StartTime']).astimezone(zoneinfo.ZoneInfo('US/Eastern')))[11:16], str(convertZDate(currentSections[i]['Meetings'][0]['EndTime']).astimezone(zoneinfo.ZoneInfo('US/Eastern')))[11:16])
		print('\n')
		choice = input('Enter the index number of the section you would like to record attendance or Q to Quit: ')
		if choice.lower() == 'q':
			mainLoop = False
		else:
			if printDebug == True:
				print(convertZNow(currentMeetingDate[currentSections[int(choice)]['Id']]['StartTime']), ZNow())
				time.sleep(5)

			if (convertZNow(currentMeetingDate[currentSections[int(choice)]['Id']]['StartTime']) <= (ZNow() + attendanceStart)) and (convertZNow(currentMeetingDate[currentSections[int(choice)]['Id']]['EndTime']) >= (ZNow() - attendanceEnd)):
				recordAttendance(currentSections[int(choice)])
			elif ZNow() > convertZNow(currentMeetingDate[currentSections[int(choice)]['Id']]['EndTime']):
				print('\n')
				print('This class ended earlier today.')
				print('\n')
				recordChoice = input('Press Y to record absenses. ')
				if recordChoice.lower() == 'y':
					recordAbsenses(currentSections[int(choice)])
			else:
				clear()
				print('Unable to record attendance at this time.')
				time.sleep(5)
			# recordAttendance(currentSections[int(choice)])

print('\n')
os.system("shutdown /r /t 0")
quit()

