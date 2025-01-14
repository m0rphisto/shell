#!/usr/bin/python
################################################################################
fid='$Id: arithmetics.py v0.3 2024-03-15 10:18:27 +0100 .m0rph $'
################################################################################
# Description:
#  This was a homework during my recent educational cource, where we had to
#  calculate with binary values.
################################################################################
# No shebang under Windows !!!

line = '-' * 80

# hello world!
print(f'{line}\n{fid}\n{line}')
print('''
Boolesche Arithmetik ist ein Teilgebiet der Mathematik,
das sich mit der Verarbeitung und Manipulation von
binären Zahlen unter Verwendung der Prinzipien der
Booleschen Algebra beschäftigt.

Lese dir die an die Aufgabe angehängte Markdowndatei
zur Booleschen Arithmetik durch oder informiere dich
über das Thema im Internet.

Löse die folgenden Aufgaben.
''')

def bitwise_bin(n1, n2, op):
   if op == 'AND':
      r = n1 & n2
   if op == 'OR':
      r = n1 | n2
   if op == 'XOR':
      r = n1 ^ n2
   else:
      pass
   print(format(n1, '#016b'))
   print(format(n2, '#016b'), op)
   print(format(r,  '#016b'))
   print(line)

def bit_not(n, bits=14):
   # A little helper function, cause we don't have a bitwise not operator.
   return (1 << bits) - 1 - n

def bitwise_notbin(n):
   r = bit_not(n)
   print(format(n, '#016b'), 'NOT')
   print(format(r,  '#016b'))
   print(line)



# main section
binaries = {
   'n1': [0b0101, 0b1011],
   'n2': [0b01001100, 0b10011010],
   'n3': [0b010111001111, 0b110100001010]
}

# Do some loopings :-D
print(f'{line}\nBINARY VALUES (AND, OR, XOR)\n{line}')
for op in ['AND', 'OR', 'XOR']:
   for k, l in binaries.items():
      bitwise_bin(l[0], l[1], op)
print('#' * 80)

print(f'{line}\nBINARY VALUES (NOT)\n{line}')
for k, l in binaries.items():
   bitwise_notbin(l[0])
   bitwise_notbin(l[1])
print('#' * 80)

print(f'{line}\nHEX VALUES (AND, OR, XOR, NOT)\n{line}')
n1, n2 = 0xb53a, 0xcd20
r1 = n1 & n2
print('%4x' % n1, '{0:016b}'.format(n1))
print('%4x' % n2, '{0:016b}'.format(n2), 'AND')
print('%4x' % r1, '{0:016b}'.format(r1))
print(line)

n1, n2 = 0x27b1, 0x51a9
r1 = n1 | n2
print('%4x' % n1, '{0:016b}'.format(n1))
print('%4x' % n2, '{0:016b}'.format(n2), 'OR')
print('%4x' % r1, '{0:016b}'.format(r1))
print(line)

n1, n2 = 0xe211, 0x1a52
r1 = n1 ^ n2
print('%4x' % n1, '{0:016b}'.format(n1))
print('%4x' % n2, '{0:016b}'.format(n2), 'XOR')
print('%4x' % r1, '{0:016b}'.format(r1))
print(line)

n1 = 0x4f8e
r1 = bit_not(n1, 16)
print('%4x' % n1, '{0:016b}'.format(n1), 'NOT')
print('%4x' % r1, '{0:016b}'.format(r1))
print(line)

# Homework here finished !!!
################################################################################
# We just do some further testing for better understanding.

h = '#' * 80
print(f'{h}\n{line}\n>> Just a little testing: understanding bit shifting.\n')
print('%4x' % n1, '{0:016b}'.format(n1), 'NOT')
r = n1 << 16
print('####', '{0:016b}'.format(r), 'n << 16')
r = n1 << 16 - 1
print('####', '{0:016b}'.format(r), 'n << 16 - 1')
print(line)


print('%4x' % 1,  '{0:016b}'.format(1),  '1')
r = 1 << 16
print('####', '{0:016b}'.format(r), '1 << 16')
r = (1 << 16) - 1
print('####', '{0:016b}'.format(r), '(1 << 16) - 1')
r = (1 << 16) - 1 - n1
print('%4x' % r, '{0:016b}'.format(r), '(1 << 16) - 1 - n1')
print('%4x' % n1, '{0:016b}'.format(n1), 'n1')
print(line)


# EOF
