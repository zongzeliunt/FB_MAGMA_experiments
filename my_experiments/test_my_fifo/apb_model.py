import math
from hwtypes import Enum, Product, Bit, BitVector
from functools import lru_cache, wraps
import inspect
from waveform import WaveForm
import pprint


pp = pprint.PrettyPrinter()
#======================================

#用这种方法可以看field_dict里有多少信号
#pp.pprint(dict(_APB.field_dict)["PRDATA"])

#用这种方法可以看每一步的信号的值
#for attr in apb:
#	print (attr)

#======================================

cycle_count = 0



#这个跟cache相关
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
    fields[f"PSEL0"] = Bit

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

def print_signal_value(_APB, apb):
	global cycle_count
	#这个东西是我自己写的，我要用这个东西来看每个cycle的信号值
	print ("Cycle: " + str(cycle_count) + "============")
	cycle_count += 1
	for sign in dict(_APB.field_dict):
		print (str(sign) + " : " + str(getattr(apb, sign)))
	print ("\n")

#[16]
#{{{
_APB = APB(16, 32)

print ("ARES APB")
print (_APB)
print (_APB.field_dict)
print (_APB.field_dict.items())
for key, value in _APB.field_dict.items():
	print (str(key) + " : ", str(value))

apb_fields = (field for field in _APB.field_dict)

waveform = WaveForm(apb_fields, clock_name="PCLK")
apb = default_APB_instance(_APB)

# Record intial state
waveform.step(apb)
#print_signal_value(_APB, apb)


# Step the clock
apb.PCLK = Bit(0)
waveform.step(apb)
#print_signal_value(_APB, apb)

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
    #print_signal_value(_APB, apb)

apb.PREADY = Bit(1)
apb.PENABLE = Bit(0)

for i in range(2):
    apb.PCLK ^= apb.PCLK
    waveform.step(apb)
    #print_signal_value(_APB, apb)

waveform.render_ipynb("waveform_example")
#}}}



