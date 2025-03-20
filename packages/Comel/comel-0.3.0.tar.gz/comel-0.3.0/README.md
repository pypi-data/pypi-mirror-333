# Comel

Opinionated PySide6 Light/Dark Theme Toggler. Oh wait yet another ~~Qt for Python~~ PySide6 light/dark theme package?
Yes it is!

![](docs/images/comel_takusan.gif)

> **ATTENTION:** This package is designed with writing/deploying standalone PySide6 application in mind.

## Features

1. Custom QMainWindow widget with built-in light/dark mode toggler. Connect the `toggle_theme` function to QtWidgets
   callback function and you're done.
2. Very simple package (for now). Not bloated from trying to cater various Qt for Python packages.

## Getting Started

Last tested with **Python 3.10+** but any Python version that PySide6 supports. Highly recommend using virtual
environment when testing/implementing this.

### Install using pip

```shell
pip install Comel
```

### Cloning this repo

Clone this repo and copy the `comel` package into your project. Ensure both `darkdetect` and `PySide6` is installed in
your Python environment.

## Usage

Import `ComelMainWindowWrapper` class and connect `toggle_theme` to a widget action. That's it!

Refer to examples directory for `barebone_app.py` for boilerplate code or `takusan_app.py` for a typical PySide app
written from scratch without using Qt Designer.

### Custom Widgets

There is **CCheckBox** and **CRadioButton** which uses custom icons and size override. Using the regular **QCheckBox**
and
**QRadioButton** will result in bigger than usual size as it displays the 32x32 size icon image.

## Examples

```shell
# Barebone app
python examples/barebone_app.py

# Takusan app
python examples/takusan_app.py

# Run this for normal and disabled state comparison 
python examples/check_disabled_state_app.py
```

## Customizing Qt Style Sheets (QSS)

> Refer to https://doc.qt.io/qt-6/stylesheet-examples.html for examples on the correct CSS selectors. Search on Stack
> Overflow/Qt Forum/etc if you cannot find the specific CSS selectors.

1. Edit `base.qss` and `presets.py` with the relevant variable and color.
2. Run `generate_qss.py` to generate `light.qss` and `dark.qss` located in `qss/themes` and `comel/themes` folder.

## Known Issues

1. The default Qt arrow icons does not play nicely when using Qt Style Sheets. While there is a way to bundle custom
   icons, I'm not fancy with the extra steps needed to compile Qt `.qrc` into Python file. I might create wrapper class
   for the affected widgets in future updates.
2. This library does not cover every single widget styles. Create an issue if you encounter a widget that is missing
   either light or dark styling.
3. **QMdiArea** and **QMdiSubWindow** is missing the window resize handle after applying Comel stylesheets. Suspecting
   one of the selector override to be the root cause.

## Why Comel?

![](examples/icons/icons8-fat-cat-96.png)

Qt is pronounced as "cute". Comel means **cute** in Bahasa Melayu aka Malay language. Also, the name of my childhood
cat.

## Credits

- Uses [darkdetect](https://github.com/albertosottile/darkdetect) for detecting the operating system dark mode.
- Uses icons from [Icons8](https://icons8.com).
- Special thanks to [izzthedude](https://github.com/izzthedude) for experimenting with this idea.
