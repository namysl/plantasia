# plantasia
 Grow some plants and don't let them die - that kind of Arduino project. Using plots and charts in data visualization as well. 

Python files are heavily personalized for my use. I added some of my data in example_plant_data.csv for a start.  
The all_charts_imported.py file is the lazy-but-fast way to try it out.
 
## Used modules and sensors:

Arduino Uno  
DHT11 humidity and temperature sensor, SE012 photoresistor, FC-28 soil moisture sensor  
128x64 OLED I2C SSD1306, 1 channel relay module (5V), 5050 plant grow LED strip lights (12V), piezo buzzer  
1k Ω and 10k Ω resistors

## Arduino's features:

* Measures relative air humidity, temperature (in Celsius), soil moisture and insolation.
* Presents the measured data on OLED display.
* Buzzer alerts when soil is too dry. Buzzer function doesn't use delay(), smooth execution of the code.
* Turns on the LED lights when it's getting too dark.
* Calculates means of the measured values, so the LED lights won't blink and value of temperature will be more precise.
* Informs when DHT11 is disconnected.
* Sends data via Serial.


![oled](oled_demo.png?raw=true "oled_demo")
