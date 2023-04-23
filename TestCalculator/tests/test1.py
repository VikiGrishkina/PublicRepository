import pytest
from Calculator import Calculator

class TestCalc:

    def setup(self):
        self.calc = Calculator

    def test_zero_division(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(self,1,0)

    def test_adding_unsuccess(self):
        assert self.calc.adding(self, 1, 1) == 3

    def test_adding_success(self): #проверка сложения позитивный
        assert self.calc.adding(self,1,1) == 2

    def test_multiply_calculate_correctly(self): #проверка умножения позитивный
        assert self.calc.multiply(self, 2, 3) == 6

    def test_division_calculate_correctly(self): #проверка деления позитивный
        assert self.calc.division(self, 6, 2) == 3

    def test_subtraction_calculate_correctly(self): #проверка вычитания позитивный
        assert self.calc.subtraction(self, 6, 2) == 4

    def test_adding_success2(self): #проверка сложения позитивный, 2-й тест
        assert self.calc.adding(self,23,4) == 27

    def teardown(self):
        print('Выполнение метода Teardown')