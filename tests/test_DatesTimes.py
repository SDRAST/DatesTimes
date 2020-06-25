"""
unittest for DatesTimes
"""
import unittest
import datetime
import DatesTimes

class testDatesTimes(unittest.TestCase):

  def test_VSR_to_datetime(self):
    self.assertEqual(DatesTimes.VSR_to_datetime((2010,15,16212)),
      datetime.datetime(2010, 1, 15, 4, 30, 12, tzinfo=datetime.timezone.utc))

  def test_VSR_to_timetuple(self):
    self.assertEqual(DatesTimes.VSR_to_timetuple((2010,101,12345)),
                    (2010, 4, 11, 3, 25, 45, 6, 101, -1))
  
  def test_VSR_timestring_to_ISOtime(self):
    self.assertEqual(DatesTimes.VSR_timestring_to_ISOtime((2010,101,12345)),
                     '20100411T032545')
  
  def test_VSR_script_time(self):
    self.assertEqual(DatesTimes.VSR_script_time(101,3,25,45),
                     '101/03:25:45')
  
  def test_day_of_week(self):
    self.assertEqual(DatesTimes.day_of_week(2020,171), 6)
  
  def test_julian_date(self):
    self.assertEqual(DatesTimes.julian_date(-4713,328.5), 0)
  
  def test_day_of_year(self):
    self.assertEqual(DatesTimes.day_of_year(2020,6,19), 171)
  
  def test_MJD(self):
    self.assertEqual(DatesTimes.MJD(1858,11,17), 0)
    
if __name__ == "__main__":
  unittest.main()
