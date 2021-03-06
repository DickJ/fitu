from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
from psycopg2 import IntegrityError
import unittest
from urllib import parse
from utils import u_db
from worker import online_schedule

class OnlineScheduleTestCase(unittest.TestCase):
    def setUp(self):
        self.today = datetime.now()
        self.yesterday = self.today - timedelta(days=1)
        self.vt3url = "https://www.cnatra.navy.mil/scheds/schedule_data.aspx?sq=vt-3"
        self.conn, self.cur = u_db.get_db_conn_and_cursor()
        try:
            # TODO Is this needed now that I have an actual test database setup?
            self.cur.execute(
            "INSERT INTO schedule (type, brief, edt, rtb, instructor, student,"\
                " event, remarks, location, date) VALUES ('T-6B Flight', "\
                "'07:00', '08:45', '10:15', 'TEST, INSRUCTOR', 'TEST, STUDENT'"\
                ", 'C4101', 'OnlineScheduleTestCase', 'NASWF', 'January 1');")
            self.conn.commit()
        except IntegrityError as e:
            self.conn.rollback()

    def tearDown(self):
        self.cur.execute("DELETE FROM schedule WHERE remarks LIKE 'OnlineScheduleTestCase';")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def test_sched_uploaded(self):
        self.assertTrue(
            online_schedule.sched_uploaded(self.cur, datetime(2016, 1, 1)))
        self.assertFalse(
            online_schedule.sched_uploaded(self.cur, datetime(2016, 2, 1)))

    def test_get_schedule_page(self):
        # TODO
        # get_schedule_page cannot jump to arbitrary dates, but rather only to
        # dates that are shown on the calendar (current month and last week of
        # previous month)
        #
        # Additionally, dt will only work if the schedule was available on the
        # previous day. This could cause problems if the test is ran after the
        # schedule has been down or if it is run on a Sunday or Monday.
        #
        # Consider creating a dummy page for this so that the same thing will
        # always be returned (if the function runs correctly), this will help
        # you make a better test than that weak one below
        self.page = online_schedule.get_schedule_page(self.vt3url,
                                                      self.yesterday)
        self.assertEqual(type(self.page), type(BeautifulSoup("", "lxml")))


    def test_process_raw_schedule(self):
        # TODO Shorten the amount of data stored, I don't need a full days worth
        # TODO Add some pages with faults to ensure they are caught

        self.cur.execute(
            "SELECT value FROM datablobs WHERE key='raw_schedule_oct_4';")
        raw_page = self.cur.fetchone()[0]
        page = BeautifulSoup(raw_page, 'lxml')

        self.cur.execute(
            "SELECT value FROM datablobs WHERE key='process_raw_schedule_oct_4_result';")
        correct_result = json.loads(self.cur.fetchone()[0])

        self.assertEqual(online_schedule.process_raw_schedule(page),
                         correct_result)

    def test_insert_in_pg(self):
        d = datetime.now()
        s = [{'type':       "T-6B Flight",
              'brief':      "06:30",
              'edt':        "08:15",
              'rtb':        "09:45",
              'instructor': "Test, Instructor",
              'student':    "Test, Student",
              'event':      "C4101",
              'remarks':    "OnlineScheduleTestCase",
              'location':   " ",
              'vt':         "VT-3"},
             ]
        online_schedule.insert_in_pg(self.cur, s, d)


    def test_delete_old_sched(self):
        pass

    def test_send_all_texts(self):
        pass

    def test_generate_message(self):
        pass

    def test_send_squadron_notes(self):
        pass

    def test_run_online_schedule(self):
        pass