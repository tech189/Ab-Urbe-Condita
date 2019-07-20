# Ab Urbe Condita

A small program to convert times and dates into the Roman system.

Call `auc.py` with the following arguments:

```
--help      shows this help text
--now       convert current date and time
--custom    convert a custom date (ISO 8601)
--simple    only print the Roman format
```

For example:
```
python auc.py --now
    23:27, Thursday, 13 June 2019 AD
    hora II post solis occasum, dies Iovis, Idus Junii MMDCCLXXII AUC
```

To use a custom date, you must use the ISO 8601 format, for example:
```
python auc.py --custom 1234-05-06
    06 May 1234 AD
    dies Saturni, diem II ante Nonas Maii MCMLXXXVII AUC
```

## Rainmeter Widget (Windows)

1. (Install [Rainmeter](https://www.rainmeter.net/) and open it at least once)
2. Download `AUCRainmeterWidget.ini` from this repository ([here](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/AUCRainmeterWidget.ini))
3. Find your Rainmeter skins folder (usually in `%USERPROFILE%\Documents\Rainmeter\Skins`)
4. Create a new folder (e.g. tech189) and place the downloaded `.ini` file into it
5. Right click the Rainmeter icon on the taskbar in the notification area and press "Refresh all"
6. Right click the Rainmeter icon again and click on "Skins" then "tech189" (the name of the folder created in step 3) and select `AUCRainmeterWidget.ini`
7. The widget should appear on your desktop for you to move around

## BitBar Plugin (macOS)

### Summary
- Install `python3` via [Homebrew](www.brew.sh) if not already installed
- Install [my BitBar build](http://www.tech189.duckdns.org/BitBar.zip)
- Copy [my BitBar plugin](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.1m.py) to your plugin folder
- Allow plugin to be executed (`chmod +x`)
- Remove date from built-in clock and rearrange the BitBar plugin next to the clock

### Step by step

1. Open Terminal (command+space to search, then type `terminal`, and press enter)
2. Go to the [Homebrew website](www.brew.sh) and copy and paste the installation command into the Terminal window
3. Press enter to start and press enter at any prompts
4. After it says "installation successful", type `brew install python3` into the terminal window and press enter
5. Click your clock on your menu bar and press "Open Date & Time Preferences…" then untick "Show the day of the week"
6. Close the System Preferences window
7. Download `BitBar` (from [here](http://www.tech189.duckdns.org/BitBar.zip)) and double click the downloaded file to unzip it
8. Now copy `BitBar` to your Applications folder, and open it (same way as opening Terminal in step 1) - it will appear hopefully on your menubar, if not, minimize all your windows and click on the desktop
9. Ignore the insecure update error (it's an unsigned build I made because the official version hasn't been released yet), then it will prompt you to choose a plugins folder (I'd go for `~/Documents/BitBar Plugins`)
10. Copy my [my BitBar plugin](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.1m.py) file into the plugin folder you just chose
11. Navigate up one folder from the plugin folder (command+up arrow key)
12. Right click on the plugin folder and press "New Terminal Tab at Folder"
13. Type in `chmod +x auc.1m.py` and press enter
14. Click the BitBar button on your menu bar and press "Reset all"
15. The date should now appear on your menu bar: command+click and drag the date next to your normal clock
16. Click on the date and behold the Roman date/time, then click on Preferences and make sure Open at Login is ticked
