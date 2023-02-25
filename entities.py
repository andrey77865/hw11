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
        check_phone = re.match(
            r"(\+?([0-9]{3})?\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{4,5}$)", phone)
        if not check_phone:
            raise ValueError(
                "Incorrect phone number format")
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
        if bday:
            datetime_obj = datetime.strptime(bday, "%d-%m-%Y")
            self.__value = datetime_obj.date()

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
    phone.value = "0977777777"
    bday = Birthday()
    bday.value = '23-01-2009'
    rec = Record(name, phone, bday)
    rec.days_to_birthday()
    ab = AddressBook()
    ab.add_record(rec)
    print(next(ab.iterator(1)))
    print(ab['Bill'].bday.value)
    print(rec.days_to_birthday())
