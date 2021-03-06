# stb-tester-automation

##  Disclaimer
Demo project with stb-tester that runs test case scenarios for Movistar+ decoders.
These test cases run with a test manager that is no present inside this code due to be private code.
> Here you can find a demo of the automation framework launcher with mock tests: [Framework Demo](https://youtu.be/K1gkAeynEDY)

##  Table of Content
* [Page Object Model](#page-object-model)
* [Page Object Classes](#page-object-classes)
* [Test Case Scenarios and Results](#test-case-scenarios)


##  Page Object Model
The project is made using Page Object Model, creating an unique class for each menu screen
The page objects are present inside the ```common``` directory following the pattern bellow:
```
  ├── exceptions.py
  ├── __init__.py
  ├── la
  │   ├── living_app1
  │   │   ├── images
  │   │   ├── __init__.py
  │   │   └── page_living_app1.py
  ├── pages
  │   ├── menu_1
  │   │   ├── images
  │   │   ├── __init__.py
  │   │   └── page_menu1.py
  └── utils
      ├── get_time_and_date.py
      ├── __init__.py
      ├── navigation_utils.py
      ├── ocr_corrections.py
      ├── plot.py
      └── rcu.py
 ```
 ##  Page Object Classes
The classes for the Page Objects follow the structure bellow. The aim is to define properties of static elements inside the class and then implement mehtods that instantiate the class and perform the desired actions in each page, so there is no need to isntantiate any class inside the test cases.
```python
import stbt
from common.exceptions import NotInScreen


class Img:
    """List of reference images locators"""
    REF_IMG1 = "./images/ref_img1.png"


class Menu(stbt.FrameObject):
    """Page Object for Menu

    When instantiated, an image capture is done and
    de property is_visible is set to True if we are
    in Menu page.
    """
    def __bool__(self):
        return self.is_visible

    def __repr__(self):
        if self.is_visible:
            return "Menu(is_visible=True)"
        else:
            return "Menu(is_visible=False)"

    @property
    def is_visible(self):
        """Returns True if in Menu page"""

        region = stbt.Region(475, 335, width=315, height=80)
        element = stbt.match(Img.REF_IMG1, frame=self._frame, region=region)

        return element


def is_visible():
    """Check if in Menu
    Returns:
        [boolean]: [Returns True if in Menu]
    """
    menu = Menu()
    return menu.is_visible


def assert_screen():
    """Raises Exception if not in Menu
    Returns:
        [obj]: [Returns instance of page]
    """
    if is_visible():
        page = Menu()
        return page
    else:
        raise NotInScreen(__name__)
   
def perform_some_action():
    """Actions in screen
    Returns:
        [obj]: [Returns instance of page]
    """
    assert_screen()
    # do something
```

##  Test Case Scenarios
1. [TC-1](test_cases/TC-1.py): Block live channel - [video](https://youtu.be/1Q1WcNrqEow)
2. [TC-2](test_cases/TC-2.py): Unblock live channel
3. [TC-3](test_cases/TC-3.py): Get event metadata from EPG - [video](https://youtu.be/ci8N95PuhzA) - [files](https://drive.google.com/drive/folders/1ZwVJssdKgyCIasFFw4b4lQqFY1KL3OpJ?usp=sharing)
4. [TC-4](test_cases/TC-4.py): Splash screen for COVID Living App - [video](https://youtu.be/zl11btFt9FI) - [files](https://drive.google.com/drive/folders/1vNHh3P3u8ymFxEVGImSyTVAkDlHp_MTq?usp=sharing)
5. [TC-5](test_cases/TC-5.py): Reply quiz for COVID - [video](https://youtu.be/Vtn5wIbvnUs)
6. [TC-6](test_cases/TC-6.py): KPI for opening Living App: Atletico de Madrid - [video](https://youtu.be/19jJDsqOks4) - [files](https://drive.google.com/drive/folders/15p7-u2DKkVzT4S6qVb2LPjBaCL8E8CJd?usp=sharing)
7. [TC-7](test_cases/TC-7.py): Validates all options have a video stream
8. [TC-8](test_cases/TC-8.py): Validates Adaptive Bitstream profile from MPEG-DASH video - [video](https://youtu.be/scA_RGUPmL8) - [files](https://drive.google.com/drive/folders/1JnqFJp48KAvsV34_gy-C0Dx9WSHMSj-4?usp=sharing)
9. [TC-9](test_cases/TC-9.py): KPI for opening Living App: Asistente COVID - [video](https://youtu.be/QM0bFDE9jzc) - [file](https://drive.google.com/drive/folders/17-VdV0-OkQyBhhDpVuLHbNOwRMirZlPV?usp=sharing)
10. [TC-10](test_cases/TC-10.py): Fast Channel Change network capture (Unicast UDP) - [files](https://drive.google.com/drive/folders/1oe7RwRs9CfAijnQcZ9iDr3eqBo1qWUVD?usp=sharing)
11. [TC-12](test_cases/TC-12.py): Zapping Endurance 10s for 6 hours

> Note: TC-8 and TC-10 uses an external package to analyze and generate charts for network capture in real time
This code is private property and can't be shared


##  Device Access
Mock module to implement device access to decoder through SSH/Telnet/RESTAPI/etc

##  Test Management
Mock module to implement test plan access through JIRA/csv/etc
