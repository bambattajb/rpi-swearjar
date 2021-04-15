import os
import sqlite3
import json
from calendar import monthrange
from datetime import datetime, timedelta
import time
year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())

con = sqlite3.connect('swears.db')

class SwearsDb:
	def __init__(self):
		cur = con.cursor()
		cur.execute('''CREATE TABLE IF NOT EXISTS users
               (uid TEXT, name TEXT, welcome TEXT)''')
		cur.execute('''CREATE TABLE IF NOT EXISTS swears
               (time DATETIME DEFAULT CURRENT_TIMESTAMP, uid TEXT)''')
		self.import_json()

	def insert_user(self, uid, name, welcome):
		cur = con.cursor()
		cur.execute("INSERT INTO users VALUES ('%s','%s','%s')" % (uid, name, welcome))
		con.commit()
		return

	def get_user(self, uid):
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE uid='%s'" % (uid))
		user = cur.fetchall()
		con.commit()
		if not user:
			return False

		return user[0]

	def get_swear_count(self, uid):
		cur = con.cursor()

		#Total
		cur.execute("SELECT count(*) from swears WHERE uid='%s' GROUP BY uid" % (uid))
		total = cur.fetchall()
		con.commit()

		#Today
		todayBase = str(year).zfill(2) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
		todayStart = todayBase + " 00:00:00"
		todayEnd = todayBase + " 23:59:59"
		cur.execute("SELECT count(*) from swears WHERE uid='%s' AND time BETWEEN '%s' AND '%s'" % (uid, todayStart, todayEnd))
		today = cur.fetchall()
		con.commit()

		#Week
		weekStartTimestamp = datetime.strptime(todayBase, "%Y-%m-%d")
		weekStart = weekStartTimestamp - timedelta(days=weekStartTimestamp.weekday())
		weekEnd = weekStart + timedelta(days=6)
		cur.execute("SELECT count(*) from swears WHERE uid='%s' AND time BETWEEN '%s' AND '%s'" % (uid, weekStart, weekEnd))
		thisweek = cur.fetchall()
		con.commit()


		# Month
		daysInMonth = monthrange(year, month)[1]
		monthStart = str(year).zfill(2) + '-' + str(month).zfill(2) + '-01' + " 00:00:00"
		monthEnd = str(year).zfill(2) + '-' + str(month).zfill(2) + '-' + str(daysInMonth).zfill(2) + '59:59:00'
		cur.execute("SELECT count(*) from swears WHERE uid='%s' AND time BETWEEN '%s' AND '%s'" % (uid, monthStart, monthEnd))
		thismonth = cur.fetchall()
		con.commit()

		counts = {
			"Total" : total[0][0],
			"Today" : today[0][0],
			"Week"	: thisweek[0][0],
			"Month" : thismonth[0][0]
		}

		return counts

	def get_all_swears(self):
		cur = con.cursor()
		cur.execute("SELECT * FROM swears")
		results = cur.fetchall()
		con.commit()
		return results

	def insert_swear(self, uid):
		cur = con.cursor()
		cur.execute("INSERT INTO swears (uid) VALUES ('%s')" % (uid))
		con.commit()
		return self.get_swear_count(uid)

	def import_json(self):
		full_path = os.path.realpath(__file__)
		with open(os.path.dirname(full_path) + "/users.json") as user_file:
			users = json.load(user_file)
			for u in users:
				exists = self.get_user(u['uid'])
				if not exists:
					self.insert_user(u['uid'], u['name'], u['welcome'])
