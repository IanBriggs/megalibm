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
  a2 = mp.mpmath(a)
  # exponent
  if a2 == mp.mpf('0.0'):
    return_str = "0x0."
    for l_i in range(prec):
      return_str += "0"
    return_str += "p+00L"
  else:
    minus = False
    if a2 < 0 :
      a2 = -a2
      minus = True
    e = mp.floor(mp.log(a2) / mp.log(mp.mpf('2.0')))
    a2 = a2 * mp.power(mp.mpf('2.0'), -e) - mp.mpf('1.0')
    if minus:
      return_str = "-0x1."
    else:
      return_str = "+0x1."
    for l_i in range(prec):
      a2 = a2 * mp.mpf('16')
      b = int(a2)
      a2 = a2 - mp.mpf(b)
      return_str += "%.1x" % b

    return_str += "p%+.2dL" % e
  return return_str