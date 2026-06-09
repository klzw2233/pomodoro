# 🍅 Pomodoro Timer

A beautiful and minimalist Pomodoro timer desktop application with a warm, soothing color scheme inspired by sleep and wellness apps.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## ✨ Features

- **4-Phase Pomodoro Cycle**
  - 🎯 **FOCUS** (25 min) - Deep work sessions
  - 🧘 **STRETCH** (3 min) - Stand up and move
  - 📋 **REVIEW** (5 min) - Check your progress
  - 🌙 **LONG BREAK** (15 min) - Full rest after 4 focus sessions

- **Intuitive UI**
  - Clean, warm cream color scheme designed for long work sessions
  - Progress dots (F1-F4) showing completed focus sessions
  - Circular progress ring with real-time countdown
  - Single toggle button (Start → Pause → Resume)

- **Smart Controls**
  - **Start/Pause/Resume** - Single button for all playback states
  - **Reset** - Reset current phase timer
  - **Skip** - Jump to next phase
  - **Always on Top** - Optional window pinning

- **Visual Feedback**
  - Color-coded phases with soft pastel accents
  - Real-time progress tracking
  - Session completion sound notification

## 🎨 Color Scheme

Inspired by wellness and sleep apps, featuring:
- **Warm Cream Background** - Easy on the eyes
- **Soft Pastels** - Calming accent colors
- **Medium Contrast** - Comfortable for long sessions

| Phase | Color | Purpose |
|-------|-------|---------|
| Focus | Warm Orange-Brown | Work mode |
| Stretch | Soft Mint Green | Movement |
| Review | Soft Golden | Reflection |
| Long Break | Soft Lavender Blue | Rest |

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- tkinter (included with Python on Windows)
- winsound (Windows only, for notifications)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/klzw2233/pomodoro.git
cd pomodoro
```

2. Run the application:
```bash
python src/pomodoro.py
```

That's it! No external dependencies required.

## 🎯 Usage

### Basic Workflow

1. Click **Start** to begin a focus session
2. Work for 25 minutes until the timer completes
3. Take a 3-minute stretch break
4. Repeat for 4 focus sessions
5. After F4, enjoy a 15-minute long break

### Keyboard Shortcuts

- The window can be set to **Always on Top** via the checkbox

### Customization

All timing constants are at the top of `src/pomodoro.py`:

```python
FOCUS_SEC = 25 * 60      # 25 minutes
STRETCH_SEC = 3 * 60     # 3 minutes
REVIEW_SEC = 5 * 60      # 5 minutes
LONG_BREAK_SEC = 15 * 60 # 15 minutes
```

Color scheme can be customized by editing the constants:
```python
BG = "#fff4dc"           # Background color
MODE_COLORS = {
    "focus": "#d4845c",
    "stretch": "#8ab88f",
    "review": "#e8b563",
    "long_break": "#9ba8c7",
}
```

## 📁 Project Structure

```
pomodoro/
├── src/
│   └── pomodoro.py      # Main application
├── README.md            # This file
└── CLAUDE.md            # Project documentation for Claude Code
```

## 🛠️ Technical Details

- **Framework**: tkinter (Python standard library)
- **Platform**: Windows (uses winsound for alerts)
- **Architecture**: Single-file application with custom Canvas widgets
- **Design Pattern**: Object-oriented with clear separation of UI and logic

### Key Components

- `RoundedButton` - Custom Canvas-based button with hover effects
- `PomodoroTimer` - Main application class
  - Timer engine with automatic phase transitions
  - Progress tracking across 4 focus sessions
  - Visual state updates and notifications

## 🎓 Learning Resources

This project demonstrates:
- tkinter GUI development
- Custom widget creation
- Timer and event loop management
- State machine implementation (phase transitions)
- Color theory and UI design

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Color scheme inspired by wellness and sleep apps
- Pomodoro Technique® by Francesco Cirillo
- Built with Claude Code

## 🐛 Known Issues

- Windows-only due to `winsound` dependency
- No cross-platform sound support yet

## 🚧 Future Enhancements

- [ ] Cross-platform sound notifications
- [ ] Customizable timer durations via UI
- [ ] Statistics and session history
- [ ] Multiple theme options
- [ ] System tray integration
- [ ] Configurable phase order

## 📧 Contact

Created by [@klzw2233](https://github.com/klzw2233)

---

⭐ If you find this useful, consider giving it a star on GitHub!
