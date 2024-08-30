from m5stack import *
from m5ui import *
from uiflow import *
from flow import ezdata
import urequests
import wifiCfg
import time
import unit
import random

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
COLORS = {'easy': 0x33ff33, 'medium': 0xff9900, 'hard': 0xff0000 } 
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TIME_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

display_idx = 0
display_count = 3

color = 0x3e3e3e
color2 = 0x1E1E1E
lcd.setBrightness(100)
rgb_unit = unit.get(unit.RGB, unit.PORTC)
env3_unit = unit.get(unit.ENV3, unit.PORTA)

time_label = None
date_label = None
year_label = None

def connect_to_wifi():
  print('Connecting to wifi...')
  wifiCfg.doConnect('<name>', '<pass>')
  print('WiFi Status: ', wifiCfg.wlan_sta.isconnected())
  
# Connect to wifi (very important)
connect_to_wifi()

def get_time():
  try:
    time_request = urequests.get(url='http://worldtimeapi.org/api/timezone/America/New_York', headers={})
    data = time_request.json()
    time_request.close()
    return data
  except Exception as e:
    print("Error: {}".format(e))

# Get unixtime for the start of the day
def get_day_start_unixtime(data):
  try:
    time_tuple = time.localtime(data['unixtime'])
    hour, minute, second = time_tuple[3], time_tuple[4], time_tuple[5]
    # Find unix time for the start of the day by subtracting based on the current hour, minute, and second
    unixtime = data['unixtime'] - (60 * 60 * hour) - (60 * minute) - second
  except Exception as e:
    print("Error: {}".format(e))
  finally:
    return unixtime
    
def check_if_daily_solved(problems_solved, start_of_day, daily_problem_title, daily_problem_date):
  # Daily is not marked as solved in database (manual check required)
  flag = False
  for problem in problems_solved:
    if int(problem['timestamp']) < start_of_day:
      break
    if problem['title'] == daily_problem_title:
      # Update the database
      req_url = '<url>' # This url is used to update a variable in a database on whether or not the daily problem has been solved (rather than manually checking each time)
      flag = True
      urequests.get(url=req_url).close()
      break
  return flag
  
# Format unixtime like the following example: Sat, Aug 18, 10:30 AM
def format_time(unixtime):
  time_tuple = time.localtime(unixtime)
  return 'Sat, {} {}, {}:{} {}'.format(MONTHS[time_tuple[1]-1], time_tuple[2], time_tuple[3] % 12, time_tuple[4], 'AM' if time_tuple[3] < 12 else 'PM')
    
def setup():
  if display_idx == 2:
    try:
      global time_label
      global date_label
      global year_label
      
      r = urequests.request(method='GET', url='http://worldtimeapi.org/api/timezone/America/New_York', headers={})
      data = r.json()
      time_tuple = time.localtime(data['unixtime'] + data['raw_offset'] + data['dst_offset'])
      
      year = data['datetime'][0:4]
      month = time_tuple[1]
      day = time_tuple[2]
      hour = time_tuple[3]
      minute = time_tuple[4]
      weekday = time_tuple[6]
            
      formatted_hour = "12" if hour == 0 or hour == 12 else ("0" + str(hour % 12) if hour % 12 < 10 else hour % 12)
      formatted_minute = "0" + str(minute) if minute < 10 else minute
      clock_cycle = "PM" if hour >= 12 else "AM"
      formatted_day = "0" + str(day) if day < 10 else day
    
      formatted_time = "{}:{} {}".format(formatted_hour, formatted_minute, clock_cycle)
      formatted_date = "{}, {} {}".format(WEEKDAYS[weekday-1], MONTHS[month-1], formatted_day)
  
      if time_label is not None:
        time_label.hide()
        date_label.hide()
        year_label.hide()

      time_label = M5TextBox(64, 70, "", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)
      date_label = M5TextBox(34, 140, "", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
      year_label = M5TextBox(120, 168, "", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
      time_label.setText(formatted_time)
      date_label.setText(formatted_date)
      year_label.setText(year)
  
      r.close()
      gc.collect()
      rgb.setColorAll(0)
      rgb_unit.setColorAll(0)
    except Exception as e:
      print("Error: {}".format(e))
    return
  
  if display_idx == 1:
    circle4 = M5Circle(56, 61, 20, 0xff9900, 0x000000)
    circle2 = M5Circle(108, 99, 20, 0xFFFFFF, 0xFFFFFF)
    circle0 = M5Circle(137, 98, 32, 0xFFFFFF, 0xFFFFFF)
    circle9 = M5Circle(115, 110, 20, 0xFFFFFF, 0xFFFFFF)
    circle3 = M5Circle(88, 111, 20, 0xFFFFFF, 0xFFFFFF)
    label0 = M5TextBox(218, 104, "T :", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label1 = M5TextBox(208, 144, "hP :", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label2 = M5TextBox(218, 185, "H :", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label3 = M5TextBox(249, 104, "", lcd.FONT_Default, 0xffffff, rotate=0)
    title0 = M5Title(title="UNIT ENV III", x=120, fgcolor=0xFFFFFF, bgcolor=0xff0000)
    label4 = M5TextBox(247, 144, "", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    label5 = M5TextBox(247, 184, "", lcd.FONT_Default, 0xFFFFFF, rotate=0)
    rect3 = M5Rect(91, 134, 1, 2, 0xFFFFFF, 0xFFFFFF)
    rect4 = M5Rect(112, 134, 1, 2, 0xFFFFFF, 0xFFFFFF)
    rect5 = M5Rect(135, 134, 1, 2, 0xFFFFFF, 0xFFFFFF)
    rect6 = M5Rect(159, 134, 1, 2, 0xFFFFFF, 0xFFFFFF)
    circle12 = M5Circle(164, 110, 20, 0xFFFFFF, 0xFFFFFF)
    
    # Update the values based on the sensor value
    # Convert temperature from celsius to fahrenheit
    temperature = round(((9 * env3_unit.temperature) / 5) + 32, 2)
    # Limit temperature to 2 decimal places
    pressure = env3_unit.pressure
    humidity = env3_unit.humidity
    label3.setText(str(temperature)+" 'F")
    label4.setText(str(pressure))
    label5.setText(str(humidity)+'%')
    if humidity >= 50:
      circle4.setBgColor(0x000000)
      rgb.setColorAll(0x000099)
      rect3.setBorderColor(0x3333ff)
      rect4.setBorderColor(0x3333ff)
      rect5.setBorderColor(0x3333ff)
      rect6.setBorderColor(0x3333ff)
      random2 = random.randint(2, 50)
      rect3.setSize(height=random2)
      random2 = random.randint(2, 50)
      rect4.setSize(height=random2)
      random2 = random.randint(2, 50)
      rect5.setSize(height=random2)
      random2 = random.randint(2, 50)
      rect6.setSize(height=random2)
    else:
      rect3.setBorderColor(0x000000)
      rect4.setBorderColor(0x000000)
      rect5.setBorderColor(0x000000)
      rect6.setBorderColor(0x000000)
      circle4.setBgColor(0xff6600)
      rgb.setColorAll(0xff6600)
      for i in range(20, 31):
        lcd.circle(56, 61, i, color=0xff9900)
        lcd.circle(56, 61, i-1, color=0x000000)
        wait(0.05)
      lcd.circle(56, 61, 30, color=0x000000)
    rgb_unit.setColorAll(0)
    return
  
  time_obj = get_time()
  time_offset = time_obj['raw_offset'] + time_obj['dst_offset']
  
  # Fetch useful data using the leetcode graphql endpoint
  payload = "{\"query\":\"query getData($username: String!) {\\r\\n  matchedUser(username: $username) {\\r\\n    contestBadge {\\r\\n      name\\r\\n      expired\\r\\n    }\\r\\n  }\\r\\n  userContestRanking(username: $username) {\\r\\n    rating\\r\\n    topPercentage\\r\\n  }\\r\\n  activeDailyCodingChallengeQuestion {\\r\\n    date\\r\\n    question {\\r\\n      acRate\\r\\n      difficulty\\r\\n      title\\r\\n      questionFrontendId\\r\\n    }\\r\\n  }\\r\\n  upcomingContests {\\r\\n    startTime\\r\\n  }\\r\\n  recentAcSubmissionList(username: $username, limit: 20) {\\r\\n    title\\r\\n    timestamp    \\r\\n  } \\r\\n}\\r\\n\",\"variables\":{\"username\":\"NerdyGamer\"}}"
  response = urequests.post(url='https://leetcode.com/graphql', headers={'Content-Type':'application/json'}, data=payload)
  json = response.json()
  data = json['data']
  
  # Fetch leetcode data for streak and coins (data is populated using private browser extension)
  req = urequests.get(url='<url>') # This url is used to retrieve your leetcode coins and streak (I used a private addon to store these values in a database, then retrieved the values using a REST API)
  leetcode_data = req.json()
  
  # Parse the useful data
  is_knight_active = not data['matchedUser']['contestBadge']['expired']
  problem_name = data['activeDailyCodingChallengeQuestion']['question']['questionFrontendId'] + '. ' + data['activeDailyCodingChallengeQuestion']['question']['title']
  problem_diff = data['activeDailyCodingChallengeQuestion']['question']['difficulty'].lower() # "easy" / "medium" / "hard"
  contest_rating = str(round(data['userContestRanking']['rating']))
  top_percentile = str(data['userContestRanking']['topPercentage'])+'%'
  daily_problem_accrate = str(round((data['activeDailyCodingChallengeQuestion']['question']['acRate']), 1)) + '%'
  
  length = len(problem_name)
  problem_name_half1 = problem_name if length <= 22 else problem_name[0:length//2]+'-'
  problem_name_half2 = "" if length <= 22 else problem_name[length//2:]
  
  daily_problem_streak = str(leetcode_data['streak'])
  coins = str(leetcode_data['coins'])
  # If the daily is marked as solved in the database, then use that, or else check manually
  is_daily_solved = leetcode_data['daily'] == data['activeDailyCodingChallengeQuestion']['date'] or check_if_daily_solved(data['recentAcSubmissionList'], get_day_start_unixtime(time_obj), data['activeDailyCodingChallengeQuestion']['question']['title'], data['activeDailyCodingChallengeQuestion']['date'])
  
  # Get the contest rating data and populate the graph
  r = urequests.post(url='<url>', headers={'Content-Type': 'application/json'}, json={"username":"NerdyGamer"}) # This url is used to get a user's contest rating and extract the necessary information. A REST API was used because the graphql endpoint returns more data then necessary, which causes memory issues
  points = r.json()
  
  # Create and configure elements for the leetcode display
  background = M5Rect(0, 0, 320, 240, color, color)
  
  leetcode_logo = M5Img(0, 0, "Leetcode.png", True)
  avatar = M5Img(256, 2, "avatar.png", True)
  contest_badge = M5Img(162 + 8, 44, "Knight.png" if is_knight_active else "InactiveKnight.png", True)
  
  leetcode_label = M5TextBox(62, 20 - 12, "LeetCode", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)
  leetcode_username = M5TextBox(62, 44 + 5, "NerdyGamer", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
  contest_badge_label = M5TextBox(175 + 24, 44 + 5, "Knight", lcd.FONT_Ubuntu, 0x1890FF if is_knight_active else 0x888888)
  
  contest_rating_label = M5TextBox(0, 66 + 10, "Contest Rating:", lcd.FONT_DejaVu18, 0xCECECE)
  top_percentile_label = M5TextBox(0, 87 + 10, "Top:", lcd.FONT_DejaVu18, 0xCECECE)
  contests_attended_label = M5TextBox(0, 109 + 12, "Attended:", lcd.FONT_DejaVu18, 0xCECECE)
  
  contest_rating_value = M5TextBox(140 + 12, 66 + 10, contest_rating, lcd.FONT_Ubuntu, 0xFFFFFF)
  top_percentile_value = M5TextBox(48, 87 + 7, top_percentile, lcd.FONT_Comic, 0xFFFFFF)
  contests_attended_value = M5TextBox(98, 109 + 8, str(len(points)), lcd.FONT_Comic, 0xFFFFFF)
  
  daily_problem_label = M5TextBox(192 + 12, 66 + 10, "Daily Problem:", lcd.FONT_Ubuntu, 0xCECECE)
  
  daily_problem_name = M5TextBox(192 - 32, 66 + 10 + 18, problem_name_half1, lcd.FONT_DefaultSmall, 0xFFFFFF)
  daily_problem_name2 = M5TextBox(192 - 32, 66 + 10 + 18 + 10, problem_name_half2, lcd.FONT_DefaultSmall, 0xFFFFFF)
  
  daily_problem_accrate_label = M5TextBox(192 - 32 - 2 + 40 + 2, 109 + 7, "ACRate:", lcd.FONT_Ubuntu, 0xCECECE)
  daily_problem_accrate_value = M5TextBox(192 - 32 - 2 + 40 + 2 + 68 + 2, 109 + 10, daily_problem_accrate, lcd.FONT_Default, 0xFFFFFF)
  
  daily_problem_streak_img = M5Img(192 - 32 - 2, 109 + 7, problem_diff + ".png", True)
  
  streak_label = M5TextBox(192 - 32 - 2 + 40 - 8 - 5, 109 + 10 + 10 + 8, "Streak:", lcd.FONT_Ubuntu, 0xCECECE)
  streak_value = M5TextBox(192 - 32 - 2 + 40 - 6 + 48 + 4 + 36 - 8 - 4, 109 + 10 + 10 + 8, daily_problem_streak, lcd.FONT_DejaVu18, 0xFFFFFF)
  
  streak_img = M5Img(192 - 32 - 2 + 40 - 6 + 48 + 3 - 2, 109 + 10 + 9, "solved.png" if is_daily_solved else "unsolved.png", True)
  
  coins_label = M5TextBox(192 - 32 - 2 + 40 - 8 - 5, 109 + 10 + 10 + 10 + 18 + 6, "Coins:", lcd.FONT_Ubuntu, 0xCECECE)
  coins_value = M5TextBox(192 - 32 - 2 + 40 - 6 + 48 + 4 + 36 - 8 - 10, 109 + 10 + 10 + 10 + 18 + 6, coins, lcd.FONT_DejaVu18, 0xFEA116)
  
  coins_img = M5Img(192 - 32 - 2 + 40 - 6 + 48 + 3 - 7, 109 + 10 + 10 + 10 + 17 + 5, "LeetCoin.png", True)
  
  upcoming_contests_label = M5TextBox(192 - 32 - 2 + 40 - 8 - 5, 109 + 10 + 10 + 10 + 10 + 26 + 10, "Contests:", lcd.FONT_DejaVu18, 0xCECECE)
    
  first_time = None
  second_time = None
  
  if len(data['upcomingContests']) == 2:
    first_time = min(data['upcomingContests'][0]['startTime'], data['upcomingContests'][1]['startTime'])
    second_time = max(data['upcomingContests'][0]['startTime'], data['upcomingContests'][1]['startTime'])
  elif len(data['upcomingContests']) == 1:
    # Only one contest (probably means that there is a contest occurring right now)
    first_time = data['upcomingContests'][0]['startTime']
  
  # Date for closest contest
  contest_first = M5TextBox(192 - 32 - 2 + 40 - 8 - 6, 109 + 10 + 10 + 10 + 10 + 18 + 26 + 14, format_time(first_time + time_offset), lcd.FONT_DefaultSmall, 0xFFFFFF)
  # Date for the following contest
  contest_biweekly = M5TextBox(192 - 32 - 2 + 40 - 8 - 6, 109 + 10 + 10 + 10 + 10 + 16 + 16 + 26 + 14, format_time(second_time + time_offset) if second_time is not None else '', lcd.FONT_DefaultSmall, 0xFFFFFF)
  
  contest_rating_graph = M5ChartGraph(0, 128 + 12, 188 - 6, 88 + 12, len(points)+3, min(points)-50, max(points)+50, M5ChartGraph.LINE, lcd.ORANGE, color2, 1, 10)
  
  for point in points:
    contest_rating_graph.addSample(point)
  
  contest_rating_graph.show()
  rgb_unit.setColorAll(COLORS[problem_diff])
    
  rgb.setColorAll(0x009900 if is_daily_solved else 0xcc0000)
  r.close()
  response.close()
  req.close()
  gc.collect()

# Wait time is 3 minutes
wait_seconds = 3 * 60
wait_ms_time = 2
wait_intervals = 1000 * wait_seconds / wait_ms_time

no_motion_flag = True
motion_detected = False

pir_0 = unit.get(unit.PIR, unit.PORTB)

def check_for_motion():
  global no_motion_flag
  global motion_detected
  if pir_0.state and no_motion_flag:
    no_motion_flag = False
    motion_detected = True
  elif not pir_0.state:
    no_motion_flag = True
    motion_detected = False
  return motion_detected
    
while True:
  print("Clearing display...")
  lcd.clear()
  # Show the label to avoid the stutter from refreshing
  if display_idx == 2 and time_label is not None:
    time_label.show()
    date_label.show()
    year_label.show()
  gc.collect()
  setup()
  print("Waiting now...")
  if display_idx == 2:
    for i in range(0, 10):
      if check_for_motion():
        display_idx = (display_idx + 1) % display_count
        break
      wait_ms(500)
    continue
  for i in range(0, (wait_intervals if display == 0 else wait_intervals // 3)):
    if check_for_motion():
      display_idx = (display_idx + 1) % display_count
      wait_ms(3000)
      break
    wait_ms(wait_ms_time)
