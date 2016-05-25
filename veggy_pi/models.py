from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from . funcs import is_number, all_numbers


class VeggyModel(models.Model):
    """
    this is the shared base class for our models, it just provides
    some common fields and a "state"
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Input(VeggyModel):
    """
    Everything that was read in by all of the sensors
    """
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    sensor_name = models.TextField()
    value = models.TextField()


class Sensor(object):
    def __init__(self, name, rpi_deps=None):
        """
        this is where rpi_deps can be injected into your instances of Sensors
        @TODO define what's actually needed in the sensor classes
        """
        pass

    def read(self):
        raise NotImplemented("you must implement this in your Sensor")


class Thermometer(Sensor):
    def read(self):
        # return self.rpi_deps.xxx ...
        return 32


class Operator(object):
    """
    An Eumm of operators used in the evaluating conditions
    and condition groups.
    """
    # logic:
    AND = 1
    OR = 2
    XOR = 3
    # compare:
    EQUALS = 4
    NOT_EQUALS = 5
    # >, <, >=, <=
    GT = 6
    LT = 7
    GTE = 8
    LTE = 9
    

class SensorState(dict):
    """
    this is an extended dict which catches call to key lookups ( my_dict['xxx'] )
    and can delegate them to do "calculated values".
    """
    def __init__(self, *args, **kwargs):
        if 'senors' in kwargs:
            self._sensors = kwargs.pop('sensors')
        else:
            self._sensors = {}
        super(SensorState, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        try:
            func = self._sensors[key]
            return func()
        except KeyError:
            return super(SensorState, self).__getitem__(key)


class ConditionGroup(VeggyModel):
    """
    Groups together multiple conditions with logic operators
    """
    operator = models.PositiveIntegerField(default=Operator.AND, choices=(
        (Operator.AND, 'AND'),
        (Operator.OR, 'OR'),
    ))

    def evaluate(self, sensor_state):
        """
        evaluates each of the children Conditions usings the logic operator
        of self to determine the groups overall value.
        expects a dict (like) sensor_state (see SensorState)
        """
        if self.operator == Operator.AND:
            for c in self.condition_set.all():
                if not c.evaluate(sensor_state):
                    return False
            return True

        if self.operator == Operator.OR:
            for c in self.condition_set.all():
                if c.evaluate(sensor_state):
                    return True
            return False

        raise NotImplemented("missing operator: %s" % (self.operator))


class Condition(VeggyModel):
    """
    represents a logic condition comparing the left hand side to the right
    (lhs, rhs) using a compare operator.
    """
    group = models.ForeignKey("ConditionGroup", null=True, default=None)
    lhs = models.TextField(null=False, blank=True, default=None)
    rhs = models.TextField(null=False, blank=True, default=None)
    operator = models.PositiveIntegerField(default=Operator.EQUALS, choices=(
        (Operator.EQUALS, '=='),
        (Operator.NOT_EQUALS, '!='),
        (Operator.GT, '>'),
        (Operator.LT, '<'),
        (Operator.GTE, '>='),
        (Operator.LTE, '<='),
    ))

    def evaluate(self, sensor_state):
        """
        expects a dict (like) sensor_state (see SensorState)
        """
        lhs_val = sensor_state[self.lhs]
        rhs_val = self.rhs

        if all_numbers(lhs_val, rhs_val):
            lhs_val = float(lhs_val)
            rhs_val = float(rhs_val)

        _funcs = {
            Operator.EQUALS: lambda l,r: l == r,
            Operator.NOT_EQUALS: lambda l,r: l != r,
            Operator.GT: lambda l,r: l > r,
            Operator.LT: lambda l,r: l < r,
            Operator.GTE: lambda l,r: l >= r,
            Operator.LTE: lambda l,r: l <= r,
        }

        func = _funcs[self.operator]

        return func(lhs_val, rhs_val)

    def __unicode__(self):
        return u"%s [[operator code %s]] %s" % (self.lhs, self.operator, self.rhs)
