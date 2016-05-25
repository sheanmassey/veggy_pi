from django.test import TestCase

from . funcs import (
    is_number,
    all_numbers,
    )

from . models import (
    Condition,
    ConditionGroup,
    Operator,
    SensorState,
    )


class TestPureFunctions(TestCase):
    def test_is_number(self):
        self.assertTrue(is_number(42))
        self.assertTrue(is_number(1.2))
        self.assertTrue(is_number("-5393"))
        self.assertTrue(is_number("123.9"))

    def test_not_numbers(self):
        self.assertFalse(is_number("hello"))
        self.assertFalse(is_number("0x80"))

    def test_all_numbers(self):
        self.assertTrue(all_numbers(1,2,3))
        self.assertTrue(all_numbers(3.14))
        self.assertTrue(all_numbers("2", "1"))
        self.assertTrue(all_numbers("3.243", 7))
        self.assertTrue(all_numbers(7, "7", "8", "2.44", 2.1, -1, "-123"))

    def test_not_all_numbers(self):
        self.assertFalse(all_numbers("hacker"))
        self.assertFalse(all_numbers(1,2,3,"four"))


class TestCondition(TestCase):
    def test_equals(self):
        c1 = Condition(lhs='SENSOR_1', rhs=13, operator=Operator.EQUALS)
        c2 = Condition(lhs='SENSOR_2', rhs='hacker', operator=Operator.EQUALS)

        self.assertTrue(c1.evaluate(SensorState(SENSOR_1=13)))
        self.assertFalse(c1.evaluate(SensorState(SENSOR_1=12)))
        self.assertTrue(c2.evaluate(SensorState(SENSOR_2='hacker')))
        self.assertFalse(c2.evaluate(SensorState(SENSOR_2='script kiddie')))

    def test_not_equals(self):
        c1 = Condition(lhs='SENSOR_1', rhs=13, operator=Operator.NOT_EQUALS)
        c2 = Condition(lhs='SENSOR_2', rhs='hacker', operator=Operator.NOT_EQUALS)

        self.assertTrue(c1.evaluate(SensorState(SENSOR_1='12')))
        self.assertFalse(c1.evaluate(SensorState(SENSOR_1='13')))
        self.assertTrue(c2.evaluate(SensorState(SENSOR_2='jack daniels')))


class TestConditionGroup(TestCase):
    def setUp(self):
        self.g1 = ConditionGroup(operator=Operator.AND)
        self.g2 = ConditionGroup(operator=Operator.OR)
        self.g1.save()
        self.g2.save()

    def test_and(self):
        c1 = Condition(lhs='SENSOR_1', operator=Operator.LT, rhs=32.5, group=self.g1)
        c2 = Condition(lhs='SENSOR_1', operator=Operator.GT, rhs=28.0, group=self.g1)
        c1.save()
        c2.save()

        self.assertTrue(self.g1.evaluate({'SENSOR_1': 30}))
        self.assertFalse(self.g1.evaluate({'SENSOR_1': 40}))
        self.assertFalse(self.g1.evaluate({'SENSOR_1': 20}))
    
    def test_or(self):
        c1 = Condition(lhs='X', operator=Operator.EQUALS, rhs=42, group=self.g2)
        c2 = Condition(lhs='X', operator=Operator.LT, rhs='0', group=self.g2)
        c1.save()
        c2.save()

        self.assertTrue(self.g2.evaluate(SensorState(X=42)))
        self.assertTrue(self.g2.evaluate(SensorState(X="-100")))
        self.assertFalse(self.g2.evaluate(SensorState(X=0)))
        self.assertFalse(self.g2.evaluate(SensorState(X=13)))
