# Wrestling Scoreboard - Design Document

## Overview

A Python Tkinter application to track wrestling match scores and display them on a live scoreboard.
Designed for wrestlers, coaches, and tournaments to provide a free and lightweight alternative to hardware scoreboards.

## Architecture

* `wrestling_scoreboard.py` contains the main `WrestlingScoringApp` class
* GUI divided into:

  * **Intro Screen**: Input wrestler names and bout number
  * **Match Screen**: Real-time scoring, timer, and undo functionality
  * **Scoreboard Screen**: Live scoreboard display on a second monitor

### File Structure

```
wrestling-scoreboard/
├── wrestling_scoreboard.py
├── wrestling_scoreboard.exe
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── assets/
├── docs/
│   └── design.md
└── old_versions/
```

## Key Features

* Scoring buttons (1, 2, 4 points)
* Timer with automatic periods and breaks
* Undo last action (Backspace key)
* PIN, TECH FALL, DECISION match results
* Fullscreen scoreboard view
* Reset and restart bouts quickly

## Future Improvements

* Save match history to CSV or JSON
* Tournament bracket mode
* Mobile/tablet-friendly interface
* Additional keyboard shortcuts for faster scoring

## Notes

* `screeninfo` is required to detect multiple monitors for the scoreboard display.
* Tkinter handles all GUI elements.
