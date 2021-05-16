import time
import logging
from datetime import datetime

from spotcam_utils.base_page import BasePage
from spotcam_utils.pages.camera_page_locators import CameraPageLocators

import ipdb

class CameraPage(BasePage):

    _locators = CameraPageLocators()

    def get_camera_page(self, camera_place):
        url = 'https://www.myspotcam.com/tc/myspotcam/'
        self.get_page(url)
        self.click_element(self._locators.CAMERA_PAGE[camera_place])
        self.wait_page_until_loading()
        self.remove_element(self.find_element(self._locators.STREAM))
        self.click_element(self._locators.PAUSE_BTN)
    
    def check_month_and_year_on_calendar(self, date: datetime) -> bool:
        self.click_element(self._locators.CALENDAR_BOX)
        month_year_expect = date.strftime('%B , %Y')
        CHECK_TIMES = 3

        for _ in range(CHECK_TIMES):
            month_year_actual = \
                self.find_element(self._locators.DATE_TITLE).get_attribute("innerText")
            logging.info(f'month_year_expect = {month_year_expect}')
            logging.info(f'month_year_actual = {month_year_actual}')

            if month_year_expect == month_year_actual:
                return True
            else:
                logging.info(f'Click last month.')
                self.click_element(self._locators.PREVIOUS_MONTH)

        return False

    def check_day_on_calendar(self, date: datetime):
        date_on_calendar = \
            self.find_element(self._locators.DATE_ON_CALENDAR(date=date))

        logging.info(f'The day of the date = {date_on_calendar.get_attribute("innerText")}')
        logging.info(f'The class name of the date = {date_on_calendar.get_attribute("class")}')
        if 'disabled' in date_on_calendar.get_attribute("class"):
            return False
        self.click_element(self._locators.DATE_ON_CALENDAR(date=date))
        return True

    def get_motion_events(self) -> list:
        self.click_element(self._locators.EVENT_LIST)
        self.click_element(self._locators.SLIDE_OF_EVENT_LIST)
        self.click_element(self._locators.MOTION_EVENT_LIST)
        motion_events = self.find_elements(self._locators.MOTION_EVENT)
        motion_events.reverse()
        return motion_events


