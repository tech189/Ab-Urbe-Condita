# Written by tech189
# See https://github.com/tech189/Ab-Urbe-Condita for details!


# this is the shell command that gets executed every time this widget refreshes
command: "/usr/local/bin/python3 ab-urbe-condita.widget/auc.py --now --json"

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

  $(domEl).find(".normal").text data["normal"]["date"]
  $(domEl).find(".time").text data["roman"]["time"]
  $(domEl).find(".day").text data["roman"]["day"]
  $(domEl).find(".date").text data["roman"]["date"]
  $(domEl).find(".year").text data["roman"]["year"]

# the CSS style for this widget, written using Stylus
# (http://learnboost.github.io/stylus/)

# light mode and dark mode support :D
style: """
  @media (prefers-color-scheme: light) {
    background: rgba(#fff, 0.50)
    -webkit-backdrop-filter: blur(100px)
    color: black
  }
  @media (prefers-color-scheme: dark) {
      
    background: rgba(#000, 0.35)
    -webkit-backdrop-filter: blur(100px)
    color: white
  }
  
  border-radius: 3px
  box-sizing: border-box
  font-family: -apple-system
  font-weight: 400
  right: 1%
  line-height: 1.5
  padding: 0.75rem 1.2rem
  top: 2%
  text-align: left
"""
