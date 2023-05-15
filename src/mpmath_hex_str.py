# mpmath does not have a way of formatting a number as hexadecimal form
# (%a in C)
# I'm shamelessly stealing the code from the bug report for this:
# https://github.com/mpmath/mpmath/issues/345

import mpmath as mp

def mpmath_hex_str(a):
  """
  Convert multiprecison float to hexadecimal representation with a defined
  precision
  """
  assert type(a) == mp.mpf, "Wrong type!"
  prec = mp.mp.prec
  # exponent
  if a == mp.mpf('0.0'):
    return_str = "0x0."
    for l_i in range(prec):
      return_str += "0"
    return_str += "p+00L"
  else:
    minus = False
    if a < 0 :
      a = -a
      minus = True
    e = mp.floor(mp.log(a) / mp.log(mp.mpf('2.0')))
    a = a * mp.power(mp.mpf('2.0'), -e) - mp.mpf('1.0')
    if minus:
      return_str = "-0x1."
    else:
      return_str = "+0x1."
    for l_i in range(prec):
      a = a * mp.mpf('16')
      b = int(a)
      a = a - mp.mpf(b)
      return_str += "%.1x" % b

    return_str += "p%+.2d" % e
  return return_str


if __name__ == "__main__":
  print(mpmath_hex_str(mp.mpf("1.0")))