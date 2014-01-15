#coding: utf-8
'''
This file implements different methods to validate a crontab/plannification entry


@author: jcazor
@date: 2014/01/11
'''

import os.path

MONTHS=('jan','feb','mar','apr','may','jun','jul','ago','sep','oct','nov','dec')
DAYS=('sun','mon','tue','wed','thu','fri','sat')

class CrontabEntry:
    def __init__(self, min, hour, dom, month, dow, script_name):
        self.minute=min
        self.hour=hour
        self.day_of_month=dom
        self.month=month
        self.day_of_week=dow
        self.script_name=script_name

    def validate_entry(self):
        if self._validate_minutes() and self._validate_hours() and self._validate_day_of_month() \
            and self._validate_month() and self._validate_day_of_week() and self._validate_script_name():
            return True
        return False

    def __get_elements(self, string, separator, position=None):
        if position is not None:
            try:
                return string.split(separator)[position]
            except Exception:
                return None
        else:
            try:
                return string.split(separator)
            except Exception:
                return None

    def _validate_minutes(self):
        for item in self.__get_elements(self.minute,','):
            numerator=self.__get_elements(item,'/',0)
            denominator=self.__get_elements(item,'/',1)
            numerator_elements=self.__get_elements(numerator,'-')
            for numerator_element in numerator_elements:
                try:
                    value=int(numerator_element)
                    if value>59:
                        return False
                except ValueError:
                    if not numerator_element in ('-','*'):
                        return False
            if denominator is not None:
                try:
                    value=int(denominator)
                    if value>59 or value<1:
                        return False
                except ValueError:
                    return False
            if len(numerator_elements)>2:
                return False
            if denominator and len(numerator_elements)>1:
                return False
        print 'Minutes ok'
        return True

    def _validate_hours(self):
        for item in self.__get_elements(self.hour,','):
            numerator=self.__get_elements(item,'/',0)
            denominator=self.__get_elements(item,'/',1)
            numerator_elements=self.__get_elements(numerator,'-')
            for numerator_element in numerator_elements:
                try:
                    value=int(numerator_element)
                    if value>23:
                        return False
                except ValueError:
                    if not numerator_element in ('-','*'):
                        return False
            if denominator is not None:
                try:
                    value=int(denominator)
                    if value>23 or value<1:
                        return False
                except ValueError:
                    return False
            if len(numerator_elements)>2:
                return False
            if denominator and len(numerator_elements)>1:
                return False
        print 'Hour OK'
        return True

    def _validate_day_of_month(self):
        for item in self.__get_elements(self.day_of_month,','):
            numerator=self.__get_elements(item,'/',0)
            denominator=self.__get_elements(item,'/',1)
            numerator_elements=self.__get_elements(numerator,'-')
            for numerator_element in numerator_elements:
                try:
                    value=int(numerator_element)
                    if value>31 or value<1:
                        return False
                except ValueError:
                    if not numerator_element in ('-','*'):
                        return False
            if denominator is not None:
                try:
                    value=int(denominator)
                    if value>31 or value<1:
                        return False
                except ValueError:
                    return False
            if len(numerator_elements)>2:
                return False
            if denominator and len(numerator_elements)>1:
                return False
        print 'Day of Month OK'
        return True

    def _validate_month(self):
        for item in self.__get_elements(self.month,','):
            numerator=self.__get_elements(item,'/',0)
            denominator=self.__get_elements(item,'/',1)
            numerator_elements=self.__get_elements(numerator,'-')
            for numerator_element in numerator_elements:
                try:
                    value=int(numerator_element)
                    if value>12 or value<1:
                        return False
                except ValueError:
                    if not numerator_element.lower() in ('-','*')+MONTHS:
                        return False
            if denominator is not None:
                try:
                    value=int(denominator)
                    if value>12 or value<1:
                        return False
                except ValueError:
                    return False
            if len(numerator_elements)>2:
                return False
            if denominator and len(numerator_elements)>1:
                return False
        print 'Month OK'
        return True

    def _validate_day_of_week(self):
        for item in self.__get_elements(self.day_of_week,','):
            numerator=self.__get_elements(item,'/',0)
            denominator=self.__get_elements(item,'/',1)
            numerator_elements=self.__get_elements(numerator,'-')
            for numerator_element in numerator_elements:
                try:
                    value=int(numerator_element)
                    if value>7:
                        return False
                except ValueError:
                    if not numerator_element.lower() in ('-','*')+DAYS:
                        return False
            if denominator is not None:
                try:
                    value=int(denominator)
                    if value>7 or value<1:
                        return False
                except ValueError:
                    return False
            if len(numerator_elements)>2:
                return False
            if denominator and len(numerator_elements)>1:
                return False
        print 'Day of Week OK'
        return True

    def _validate_script_name(self):
        if os.path.split(self.script_name)[0] not in ('./',''):
            return False
        else:
            print 'Script Name OK'
            return True

