# Ab Urbe Condita

A small program to convert times and dates into the Roman system.

Run `auc.py` with no arguments to output current date and time or use the following arguments:

```text
--json          output in JSON for portability
--simple        only print the Roman format
--idiomatic     abbreviated dates to be more idiomatic
--custom        convert a custom date (ISO 8601)
--debug         print calculations etc. for debugging
```

For example:

```text
python3 auc.py
    23:27, Thursday, 13 June 2019 AD
    hora II post solis occasum
    dies Iovis
    Idus Junias
    MMDCCLXXII AUC
```

To use a custom date, you must use the ISO 8601 format, for example:

```text
python3 auc.py --custom 1234-05-06
    Saturday, 6 May 1234 AD
    dies Saturni
    pridie Nonas Majas
    MCMLXXXVII AUC
```

To use the data in other programs, simply use the `--json` argument:

```json
python3 auc.py --json
    {"normal": {"time": "00:21", "day": "Thursday", "date": "17 June", "year": "2021"}, "roman": {"time": "hora IV ante solis ortum", "day": "dies Jovis", "date": "ante diem XV Kalendas Quintiles", "idiomatic_date": "a.d. XV Kal. Qui.", "year": "MMDCCLXXIV"}}
```

Or, if you're writing in Python, you could `import` it in your program:

```python
>>> import auc, datetime
>>> print("hodie est " + auc.get_day(datetime.datetime.now()) + "!")
hodie est dies Jovis!
```

## Widgets!

There are desktop widgets for both Windows and macOS - if you're stuck installing them feel free to raise an issue [here](https://github.com/tech189/Ab-Urbe-Condita/issues). For now, updating the widgets is a manual process until I figure out some kind of automatic update checker ([see issue #7](https://github.com/tech189/Ab-Urbe-Condita/issues/7)).

### Rainmeter Widget (Windows)

#### Step by step

1. (Install [Rainmeter](https://www.rainmeter.net/) and open it at least once)
2. Download `AUCRainmeterWidget.ini` from [here](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/AUCRainmeterWidget.ini) (you can download it by right-clicking the link and pressing "Save Link As...")
3. Find your Rainmeter skins folder (usually in `%USERPROFILE%\Documents\Rainmeter\Skins`)
4. Create a new folder (e.g. tech189) and place the downloaded `.ini` file into it
5. Right click the Rainmeter icon on the taskbar in the notification area and press "Refresh all"
6. Right click the Rainmeter icon again and click on "Skins" then "tech189" (the name of the folder created in step 3) and select `AUCRainmeterWidget.ini`
7. The updated widget should appear on your desktop

#### Updating

1. Find your Rainmeter skins folder (usually in `%USERPROFILE%\Documents\Rainmeter\Skins`)
2. Open the folder where you placed `AUCRainmeterWidget.ini` and delete the old .ini file
3. Copy into this folder [`AUCRainmeterWidget.ini`](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/AUCRainmeterWidget.ini) (you can download it by right-clicking the link and pressing "Save Link As...")
4. Right click the Rainmeter icon on the taskbar in the notification area and press "Refresh all"
5. The updated widget should appear on your desktop for you to move around

### Übersicht Widget (macOS)

#### Summary

- Install [Python 3](https://www.python.org/) and [Übersicht](http://tracesof.net/uebersicht/) via [Homebrew](https://brew.sh):

    ```text
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    brew install python3 && brew cask install ubersicht
    ```

- Übersicht menu bar > Open Widgets Folder
- Copy [auc.coffee](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.coffee) and [auc.py](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.py) into a folder called `ab-urbe-condita.widget` located in your Übersicht widget folder (the one you just opened)
- Übersicht menu bar > Refresh All Widgets
- Übersicht menu bar > Preferences... > Launch Übersicht when I login

#### Step by step

1. Open Terminal (command+space to search, then type `terminal`, and press enter)
2. Go to the [Homebrew website](https://brew.sh) and copy and paste the installation command into the Terminal window:

    ```text
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ```

3. Press enter to start and press enter at any prompts
4. After it says "installation successful", type the following command into the terminal window and press enter

    ```text
    brew install python3 && brew cask install ubersicht
    ```

5. Open Übersicht (command+space to search, then type `ubersicht`, and press enter)
6. Click on the Übersicht menubar icon at the top of your screen (a 'u' with glasses on top), then on "Open Widgets Folder"
7. Delete the files in the folder you just opened
8. Create a new folder called "ab-urbe-condita.widget" and copy into it [auc.coffee](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.coffee) and [auc.py](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.py) (you can download them by right-clicking these links and pressing "Save Link As...")
9. Click on the Übersicht menubar icon again and click "Refresh All Widgets", the AUC widget should appear on your desktop by this point if it hadn't already.
10. Finally click on the Übersicht menubar icon for the last time and open its "Preferences..." option, then tick "Launch Übersicht when I login" to make sure the widget loads at start-up!

#### Updating

1. Click on the Übersicht menubar icon and click "Open Widgets Folder"
2. Open the "ab-urbe-condita.widget" folder and delete the old auc.coffee and auc.py files inside it
3. Copy into this folder [auc.coffee](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.coffee) and [auc.py](https://raw.githubusercontent.com/tech189/Ab-Urbe-Condita/master/auc.py) (you can download them by right-clicking these links and pressing "Save Link As...")
4. Click on the Übersicht menubar icon again and click "Refresh All Widgets", the AUC widget should refresh and the updated files should work

<!-- 
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
16. Click on the date and behold the Roman date/time, then click on Preferences and make sure Open at Login is ticked -->
