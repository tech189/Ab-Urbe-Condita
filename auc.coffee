# Written by tech189
# See https://github.com/tech189/Ab-Urbe-Condita for details!


# this is the shell command that gets executed every time this widget refreshes
command: "/usr/local/bin/python3 ab-urbe-condita.widget/auc.py --json"

# the refresh frequency in milliseconds
refreshFrequency: 60000

# render gets called after the shell command has executed. What it returns will get rendered as HTML.

render: -> """
  <div style="font-weight: bold" class="normal">Loading...</div>
  <!-- <div class="debug">Loading...</div> -->
  <div class="time">Loading...</div>
  <div class="day">Loading...</div>
  <div class="date">Loading...</div>
  <div style="font-weight: bold" class="year">Loading...</div>
"""

# update called as frequently as refreshFrequency, takes in the output from the command and the DOM for editing

update: (output, domEl) -> 

  # $(domEl).find(".debug").text output

  data = JSON.parse(output)

  $(domEl).find(".normal").text data["normal"]["day"] + ", " + data["normal"]["date"] + " " + data["normal"]["year"] + " AD"
  $(domEl).find(".time").text data["roman"]["time"]
  $(domEl).find(".day").text data["roman"]["day"]
  $(domEl).find(".date").text data["roman"]["date"]
  $(domEl).find(".year").text data["roman"]["idiomatic_year"]

# the CSS style for this widget, written using Stylus
# (http://learnboost.github.io/stylus/)

# light mode and dark mode support :D
style: """
  @media (prefers-color-scheme: light) {
    background: rgba(#fff, 0.50)
    -webkit-backdrop-filter: blur(10px) brightness(110%) contrast(105%) saturate(105%)
    color: black
  }
  @media (prefers-color-scheme: dark) {
      
    background: rgba(#000, 0.35)
    -webkit-backdrop-filter: blur(10px) brightness(110%) contrast(105%) saturate(105%)
    color: white
  }

  top: 2%
  left: 1%
  max-width: 30%
  box-sizing: border-box
  font-family: -apple-system
  font-weight: 400
  line-height: 1.5
  padding: 0.75rem 1.2rem
  text-align: left
  border-radius: 9px
  border: 1px solid rgba(255, 255, 255, 0.15)
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
  //alternative shadows for busier wallpapers:
  //box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  //box-shadow: rgba(0, 0, 0, 0.16) 0px 10px 36px 0px, rgba(0, 0, 0, 0.06) 0px 0px 0px 1px;
"""
