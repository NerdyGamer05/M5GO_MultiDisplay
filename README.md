
# M5GO Multi-Display

UIFlow Micropython code for a multi-display that switches between screens using a motion sensor.

## Leetcode

The first screen is a Leetcode display, which shows various Leetcode stats, including contest rating, content top percentile, contents completed, the daily problem, the status of the daily problem, active streak, coins, along with the times for upcoming contests.

The color bar indicates whether or not the daily problem has been solved (green for solved, red for unsolved).

Additionally, an RGB unit (which is not shown in the image below) is used to show the difficulty of the daily problem. Green for easy, orange for medium, and red for hard. 

To use this display, you must load the images provided in the `assets/` folder to the M5GO

![LeetcodeDisplay](https://i.postimg.cc/RVcSNF4W/display-1.jpg)

## Weather (inside)

The second screen is a display provided by M5GO for displaying the temperature, humidity, and pressure using the ENV III sensor.

![WeatherDisplay](https://i.postimg.cc/59QNWgrq/display-3.jpg)

## Date & Time

The third (and final) screen just displays the date and time, while factoring in the time zone.

![TimeDisplay](https://i.postimg.cc/8P8kpWQ8/display-2.jpg)
