import re

from collections import UserDict
from datetime import date, datetime


class AddressBook(UserDict):
    def add_record(self, rec):
        self.data = Record.add(rec)

    def iterator(self, n):
        result_list = list(self.data.items())
        contacts_count = len(self.data)
        while True:
            if n <= contacts_count:
                yield result_list[:n]
            else:
                yield result_list[:contacts_count]


class Field:
    pass


class Name(Field):
    def __init__(self, name):
        self.value = name

    def __repr__(self):
        return f"{self.value}"


class Phone(Field):
    def __init__(self, phone=None):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        phone = re.sub('\W+', '', phone)
        check_phone = re.match(
            r"([0-9]{3}[0-9]{3}[0-9]{2}[0-9]{2}$)", phone)

        if not check_phone:
            raise ValueError(
                "Incorrect phone number format (+380xxxxxxxxx")

        if phone.startswith("0"):
            phone = "+38" + phone
        elif phone.startswith("380"):
            phone = "+" + phone

        self.__value = phone

    def __repr__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, bday=None):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, bday):
        try:
            datetime_obj = datetime.strptime(bday, "%d-%m-%Y")
        except ValueError:
            print("Incorrect birthday format (dd-mm-yyyy)")
        else:
            self.__value = datetime_obj.date()
        # if bday:
        #     datetime_obj = datetime.strptime(bday, "%d-%m-%Y")

    def __repr__(self):
        return f"{self.value}"


class Record():
    def __init__(self, name: Name, phone: Phone = None, bday: Birthday = None):
        self.name = name
        self.phones = []
        if phone.value:
            self.phones.append(phone)
        self.bday = bday

    def days_to_birthday(self):
        if self.bday.value != None:
            today = date.today()
            next_bday = self.bday.value.replace(year=today.year)
            if next_bday < today:
                next_bday = next_bday.replace(year=today.year + 1)

            days_to_bday = (next_bday - today).days
            return days_to_bday

    def add(rec):
        return {rec.name.value: rec}

    def delete(self):
        del self.phones

    def edit(self, phone):
        self.phones[0].value = phone


# Test
if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone()
    phone.value = "097-7777777 "
    bday = Birthday()
    bday.value = '23-01-20091'
    rec = Record(name, phone, bday)
    rec.days_to_birthday()
    ab = AddressBook()
    ab.add_record(rec)
    print(next(ab.iterator(1)))
    print(ab['Bill'].bday.value)
    print(rec.days_to_birthday())
