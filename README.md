# Diablo Experience Tracker

A simple tool to track and calculate experience gain rates in Diablo games. This program captures experience values from the game screen and calculates statistics like experience per hour.

## Features

- Screen region selection for experience tracking
- Real-time experience capture using OCR
- Calculation of:
  - Total experience gained
  - Time elapsed
  - Experience per hour
- Hotkey controls for easy usage while gaming

## Prerequisites

- Python 3.x
- Tesseract OCR installed on your system
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

## Installation

1. Clone this repository or download the files
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Setup

1. Run the program:
```bash
python diablo-exp-tracker.py
```

2. Press `Ctrl+0` to select the region of your screen where the experience text appears
   - A window will open showing your screen
   - Click and drag to select the region containing the experience text
   - Press Enter to confirm selection
   - A screenshot of the selected region will be saved as "exp-region-screenshot.png"

## Usage

The program uses the following hotkeys:

- `Ctrl+0`: Define screen region for experience tracking
- `Ctrl+1`: Start tracking (captures initial experience value)
- `Ctrl+2`: End tracking (captures final experience value and shows statistics)
- `Ctrl+3`: Display current tracking statistics

## Other

This is for personal use and I made it a while ago so might not even work anymore.