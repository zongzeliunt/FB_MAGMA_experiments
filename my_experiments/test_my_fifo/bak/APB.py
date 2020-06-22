#https://github.com/leonardt/magma_register_file_tutorial/blob/master/2-Defining%20an%20APB%20Model%20in%20Python.ipynb
from functools import lru_cache
import inspect
from functools import wraps
from hwtypes import Enum, Product
from hwtypes import Bit, BitVector
import math
import pprint
from waveform import WaveForm

import magma as m

pp = pprint.PrettyPrinter()

def canonicalize_args(f):
#{{{
    """Wrapper for functools.lru_cache() to canonicalize default
    and keyword arguments so cache hits are maximized."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        sig = inspect.getfullargspec(f.__wrapped__)

        # build newargs by filling in defaults, args, kwargs
        newargs = [None] * len(sig.args)
        if sig.defaults is not None:
            newargs[-len(sig.defaults):] = sig.defaults
        newargs[:len(args)] = args
        for name, value in kwargs.items():
            newargs[sig.args.index(name)] = value

        return f(*newargs)

    return wrapper
#}}}

class APBCommand(Enum):
#{{{
    READ = 0
    WRITE = 1
    IDLE = 2
#}}}

#[9]
@canonicalize_args
@lru_cache(maxsize=None)
#存cache，存default值
def APB(addr_width, data_width, num_slaves=1):
#{{{
    """
    Constructs a concrete APB type based on the `addr_width`, `data_width` and
    `num_slaves` parameters.  Rather than using the standard subclassing
    syntax, we dynamically construct a dictionary containing our field names
    and types, then use Python's `type` function to construct our new type
    definition.

    This allows us to dynamically add more fields based on the number of
    slaves.
    """
    strobe_width = math.ceil(data_width / 8)

    fields = {
        "PADDR": BitVector[addr_width],
        "PWRITE": Bit,
    }

    # Dynamically add `PSELx` fields based on `num_slaves` parameter
    for i in range(num_slaves):
        fields[f"PSEL{i}"] = Bit

    fields.update({
        "PENABLE": Bit,
        "PWDATA": BitVector[data_width],
        "PRDATA": BitVector[data_width],
        "PREADY": Bit,
        "PSTRB": BitVector[strobe_width],
        "PPROT": Bit,
        "SLVERR": Bit,
    })

	#Product 是hwtypes里引用来的，以下语句是把result声明成一个Product类型的数据，
	#type函数的三个变量的用法：name -- 类的名称。bases -- 基类的元组。dict -- 字典，类内定义的命名空间变量。
	#Product 里的field_dict可以打出来field的数据，但是field里的数据类型必须得是Bit或者BitVector类型
	#Product 是APB，以及后面的Request，IO的基类
    result = type("_APB", (Product, ), fields)
    return result
#}}}

def default_APB_instance(_APB):
#{{{
    """
    Convenience function to instantiate an _APB object with default values of 0
    """
    fields = {}
    for key, value in _APB.field_dict.items():
        fields[key] = value(0)
    return _APB(**fields)
#}}}

#[11]
@canonicalize_args
@lru_cache(maxsize=None)
def Request(addr_width, data_width, num_slaves):
#{{{
    class _Request(Product):
        command = APBCommand
        address = BitVector[addr_width]
        data = BitVector[data_width]
        slave_id = BitVector[max(math.ceil(math.log2(num_slaves)), 1)]
    return _Request
#}}}

#[13]
@canonicalize_args
@lru_cache(maxsize=None)
def APBBusIO(addr_width, data_width, num_slaves=1):
#{{{
    class IO(Product):
        apb = APB(addr_width, data_width, num_slaves)
        request = Request(addr_width, data_width, num_slaves)
    return IO
#}}}

@canonicalize_args
@lru_cache(maxsize=None)
def APBBus(addr_width, data_width, num_slaves=1):
#{{{
    # TODO: Does this need to be a generator?
    class APBBus:
        """
        This defines a coroutine that impelements the behavior of an APBBus.  The interface
        to the coroutine is via the `__call__` method which accepts an instance
        of the `APBBusIO` type.
        """
        def __init__(self):
            # Store the type of the interface so users can easily fetch it
            #这个IO是一个APBBusIO类型
            self.IO = APBBusIO(addr_width, data_width, num_slaves)

            # The main functionality of the coroutine is defined the `_main`
            # method.  Because of how Python generators work, to emulate the
            # standard behavior of a coroutine, the main function should be
            # invoked once to create the generator object, then `next` is
            # called to initialize the coroutine
            # See http://www.dabeaz.com/coroutines/ for more info on Python
            # coroutines
            self.main = self._main()
            next(self.main)
            # TODO: This logic should move to the infrastructure and be
            # provided as a simple way to construct a coroutine

        def __call__(self, io):
            """
            Calling the object equates to advancing the coroutine once.
            IO is performed through the `io` attribute.
            """
            self.io = io
            self.main.send(None)

        def _main(self):
            """
            This main coroutine implements a state machine with three top-level
            states corresponding to: reading, writing, and idleing.
            """
            yield  # Initial state
            while True:
                if self.io.request.command == APBCommand.READ:
                    yield from self.read(self.io.request.address,
                                         self.io.request.data)
                elif self.io.request.command == APBCommand.WRITE:
                    yield from self.write(self.io.request.address,
                                          self.io.request.data)
                else:
                    yield

        def set_psel(self, value):
            """
            Helper function that sets the correct PSEL line based on the
            `slave_id` of the current request
            """
            setattr(self.io.apb, f"PSEL{self.io.request.slave_id}", value)

        def write(self, address, data):
            """
            Issue a write as a sequence of output values:
                * Set the address and write data lines based on the input
                * Set PSEL for the requested slave
                * Set PWRITE
                * Wait one clock cycle
                * Set PENABLE
                * Wait one clock cycle
                * Wait for PREADY to be high (from the slave)
                * Clear PENABLE and PSEL
            """
            self.io.apb.PADDR = address
            self.io.apb.PWDATA = data
            self.set_psel(Bit(1))
            self.io.apb.PWRITE = Bit(1)
            yield
            self.io.apb.PENABLE = Bit(1)
            yield
            while not self.io.apb.PREADY:
                # TODO: Insert timeout logic
                yield
            self.io.apb.PENABLE = Bit(0)
            self.set_psel(Bit(0))

        def read(self, address, data):
            """
            Issue a read as a sequence of output values:
                * Set the address line based on the input
                * Set PSEL for the requested slave
                * Clear PWRITE
                * Wait one clock cycle
                * Set PENABLE
                * Wait one clock cycle
                * Wait for PREADY to be high (from the slave)
                * Clear PENABLE and PSEL
            """
            self.io.apb.PADDR = address
            self.set_psel(Bit(1))
            self.io.apb.PWRITE = Bit(0)
            yield
            self.io.apb.PENABLE = Bit(1)
            yield
            while not self.io.apb.PREADY:
                # TODO: Insert timeout logic
                yield
            self.io.apb.PENABLE = Bit(0)
            self.set_psel(Bit(0))

            # TODO: Handle PSLVERR and checking the expected data
    return APBBus()
#}}}





















#TEST
#=================================================
#[1] [2]
#{{{
#两次返回的A的地址不一样
"""
def make_A(n):
    class A:
        __n = n
    return A

print (make_A(3) == make_A(3))
"""
#False
#}}}

#[3]
#{{{
#因为用了lru_cache，记下了上次用的A的地址在cache里
"""
@lru_cache(maxsize=None)
def make_A(n):
    class A:
        __n = n
    return A

print (make_A(3) == make_A(3))
"""
#True
#}}}

#[4]
#{{{
#即使cache记下了地址，但是不会存default值
"""
@lru_cache(maxsize=None)
def make_A(n=3):
    class A:
        __n = n
    return A

print (make_A(3) == make_A())
"""
#False
#}}}

#[6]
#{{{
#用了canonicalize_args，连default值也能存了
"""
@canonicalize_args
@lru_cache(maxsize=None)
def make_A(n=3):
    class A:
        __n = n
    return A

print(make_A(3) == make_A())
#True
"""
#}}}

#[8]
#{{{
"""
a = Bit(0)
b = Bit(1)
print(f"a ^ b = {a ^ b}")


c = BitVector[4](0xE)
d = BitVector[4](0xF)
print(f"~c & d = {~c & d}")
"""
#}}}

#[10]
#{{{
_APB = APB(16, 32, num_slaves=2)
"""
print("========= Type  ==========")
pp.pprint(dict(_APB.field_dict))
print("==========================")
# For an instance of the type, we can use `value_dict` to fetch a dictionary
# mapping fields to values
print("===== Default Value ======")
pp.pprint(dict(default_APB_instance(_APB).value_dict))
print("==========================")
"""
#}}}

#[12]
#{{{
_Request = Request(16, 32, 2)
request_val = _Request(APBCommand.WRITE, BitVector[16](0xDE), BitVector[32](0xBEEF), BitVector[1](1))

"""
print("========= Type  ==========")
pp.pprint(dict(_Request.field_dict))
print("==========================")
print("===== Default Value ======")
pp.pprint(dict(request_val.value_dict))
print("==========================")
"""
#}}}

#[14]
_APBBusIO = APBBusIO(16, 32, 2)

#{{{
"""
print("========= Type  ==========")
pp.pprint(dict(_APBBusIO.field_dict))
print("==========================")
print("===== Default Value ======")
pp.pprint(dict(_APBBusIO(default_APB_instance(_APB), request_val).value_dict))
print("==========================")
"""
#}}}

#[16]
#{{{
_APB = APB(16, 32)
apb_fields = (field for field in _APB.field_dict)

waveform = WaveForm(apb_fields, clock_name="PCLK")
apb = default_APB_instance(_APB)

# Record intial state
waveform.step(apb)

# Step the clock
apb.PCLK = Bit(1)
waveform.step(apb)

# Set some other fields
apb.PWDATA = BitVector[32](0xDEADBEEF)
apb.PADDR = BitVector[16](0xFEED)
apb.PENABLE = Bit(1)
apb.PSEL0 = Bit(1)
apb.PWRITE = Bit(1)
apb.PCLK = Bit(0)
waveform.step(apb)

for i in range(2):
# Step the clock
    apb.PCLK ^= apb.PCLK
    waveform.step(apb)

apb.PREADY = Bit(1)
apb.PENABLE = Bit(0)

for i in range(2):
    apb.PCLK ^= apb.PCLK
    waveform.step(apb)

waveform.render_ipynb("waveform_example")
#}}}

#[17]
#{{{
"""
addr_width = 16
data_width = 32
bus = APBBus(addr_width, data_width)
addr = 13
data = 45
request = Request(addr_width, data_width, 1)(
    APBCommand.IDLE, BitVector[addr_width](addr),
    BitVector[data_width](data), BitVector[1](0))

# Specialized instance of APB for addr/data width
_APB = APB(addr_width, data_width)

io = APBBusIO(addr_width, data_width)(default_APB_instance(_APB), request)

apb_fields = (field for field in _APB.field_dict)
waveform = WaveForm(apb_fields, clock_name="PCLK")

# check idle stae
for i in range(1):
    bus(io)
    waveform.step(bus.io.apb)

# Send request
request.command = APBCommand.WRITE
bus(io)
assert io.apb.PSEL0 == 1

waveform.step(bus.io.apb)

request.command = APBCommand.IDLE

# No wait state
io.apb.PREADY = Bit(1)
bus(io)
waveform.step(bus.io.apb)

assert io.apb.PENABLE == 1
assert io.apb.PSEL0 == 1

bus(io)
# Slave pulls PREADY down at the same time
io.apb.PREADY = Bit(0)
waveform.step(bus.io.apb)

assert io.apb.PENABLE == 0
assert io.apb.PSEL0 == 0

io.apb.PWDATA = BitVector[data_width](0)

bus(io)
waveform.step(bus.io.apb)
waveform.render_ipynb("write_no_wait")
"""
#}}}

#[18]
#{{{
"""
addr_width = 16
data_width = 32
bus = APBBus(addr_width, data_width)
addr = 13
data = 45
request = Request(addr_width, data_width, 1)(
    APBCommand.IDLE, BitVector[addr_width](addr), BitVector[data_width](data), BitVector[1](0))

# Specialized instance of APB for addr/data width
_APB = APB(addr_width, data_width)

io = APBBusIO(addr_width, data_width)(
    default_APB_instance(_APB), request)

apb_fields = (field for field in _APB.field_dict)
waveform = WaveForm(apb_fields, clock_name="PCLK")

# check idle stae
for i in range(1):
    bus(io)
    waveform.step(bus.io.apb)

# Send request
request.command = APBCommand.WRITE
bus(io)
waveform.step(bus.io.apb)
assert io.apb.PSEL0 == 1
assert io.apb.PWRITE == 1

request.command = APBCommand.IDLE

# Wait by holding PREADY down
io.apb.PREADY = Bit(0)
bus(io)
waveform.step(bus.io.apb)
assert io.apb.PENABLE == 1
assert io.apb.PSEL0 == 1
assert io.apb.PWRITE == 1

for i in range(2):
    bus(io)
    waveform.step(bus.io.apb)
    assert io.apb.PENABLE == 1
    assert io.apb.PSEL0 == 1
    assert io.apb.PWRITE == 1

bus(io)
# PREADY high when done
io.apb.PREADY = Bit(1)
waveform.step(bus.io.apb)
bus(io)
io.apb.PREADY = Bit(0)
io.apb.PWDATA = BitVector[data_width](0)
waveform.step(bus.io.apb)
assert io.apb.PENABLE == 0
assert io.apb.PSEL0 == 0
waveform.render_ipynb("write_with_wait")
"""
#}}}

#[19]
#{{{
"""
addr_width = 16
data_width = 32
bus = APBBus(addr_width, data_width)
addr = 13
data = 0
request = Request(addr_width, data_width, 1)(
    APBCommand.IDLE, BitVector[addr_width](addr), BitVector[data_width](data), BitVector[1](0))

# Specialized instance of APB for addr/data width
_APB = APB(addr_width, data_width)

io = APBBusIO(addr_width, data_width)(default_APB_instance(_APB), request)

apb_fields = (field for field in _APB.field_dict)
waveform = WaveForm(apb_fields, clock_name="PCLK")

# check idle stae
for i in range(1):
    bus(io)
    waveform.step(bus.io.apb)

# Send request
request.command = APBCommand.READ
bus(io)
waveform.step(bus.io.apb)

request.command = APBCommand.IDLE

bus(io)
waveform.step(bus.io.apb)
assert io.apb.PENABLE == 1

# No wait state
bus(io)
io.apb.PREADY = Bit(1)
io.apb.PRDATA = BitVector[data_width](13)
waveform.step(bus.io.apb)

bus(io)
io.apb.PREADY = Bit(0)
io.apb.PRDATA = BitVector[data_width](0)
waveform.step(bus.io.apb)

assert io.apb.PENABLE == 0
assert io.apb.PSEL0 == 0
waveform.render_ipynb("read_no_wait")
"""
#}}}

#[20]
#{{{
"""
addr_width = 16
data_width = 32
bus = APBBus(addr_width, data_width)
addr = 13
data = 0
request = Request(addr_width, data_width, 1)(
    APBCommand.IDLE, BitVector[addr_width](addr), BitVector[data_width](data), BitVector[1](0))

# Specialized instance of APB for addr/data width
_APB = APB(addr_width, data_width)

io = APBBusIO(addr_width, data_width)(default_APB_instance(_APB), request)

apb_fields = (field for field in _APB.field_dict)
waveform = WaveForm(apb_fields, clock_name="PCLK")

# check idle stae
for i in range(1):
    bus(io)
    waveform.step(bus.io.apb)

# Send request
request.command = APBCommand.READ
bus(io)
waveform.step(bus.io.apb)

request.command = APBCommand.IDLE

bus(io)
waveform.step(bus.io.apb)
assert io.apb.PENABLE == 1

for i in range(2):
    bus(io)
    waveform.step(bus.io.apb)

bus(io)
io.apb.PREADY = Bit(1)
io.apb.PRDATA = BitVector[data_width](13)
waveform.step(bus.io.apb)

bus(io)
io.apb.PREADY = Bit(0)
io.apb.PRDATA = BitVector[data_width](0)
waveform.step(bus.io.apb)

assert io.apb.PENABLE == 0
assert io.apb.PSEL0 == 0
waveform.render_ipynb("write_no_wait_1")
"""
#}}}





