---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

```
.text:  executable functions
.data:  initialized global/static data.
.bss:   uninitialized global/static data.
.stack: function call frames, local variables, function parameters
.heap:  object created by new/delete

=== Memory Segments (addresses in hex) ===
.text (code)   : 0x555555554000 - 0x5555555567f1
.data          : 0x555555559000 - 0x555555559098
.bss           : 0x555555559098 - 0x5555555591f0
```
```
================================================================================
Object: a  (dynamic type: A)
================================================================================
Object address: 0x7fffffffddf0
vptr: 0x555555558cc0
Virtual table:
  [  0] 0x5555555564a2  A::foo()
  [  1] 0x5555555564b2  A::bar()
  [  2] 0x5555555564de  A::dog()

Data members (including bases):
  _vptr.A: @ +0  -> 0x7fffffffddf0  (sizeof int (**)(void) = 8)
  i: @ +8  -> 0x7fffffffddf8  (sizeof int = 4)
  d: @ +16  -> 0x7fffffffde00  (sizeof double = 8)
  _i: @ +24  -> 0x7fffffffde08  (sizeof int = 4)
  _d: @ +32  -> 0x7fffffffde10  (sizeof double = 8)

================================================================================
Object: b1  (dynamic type: B1)
================================================================================
Object address: 0x7fffffffde70
vptr: 0x555555558c48
Virtual table:
  [  0] 0x5555555564ee  B1::foo()
  [  1] 0x55555555650a  B1::bar()
  [  2] 0x555555556526  B1::hello()
  [  0] 0x5555555564fd  virtual thunk to B1::foo()
  [  1] 0x555555556519  virtual thunk to B1::bar()
  [  2] 0x5555555564de  A::dog()

Data members (including bases):
  _vptr.B1: @ +0  -> 0x7fffffffde70  (sizeof int (**)(void) = 8)
  i: @ +8  -> 0x7fffffffde78  (sizeof int = 4)
  d: @ +16  -> 0x7fffffffde80  (sizeof double = 8)
  _i: @ +24  -> 0x7fffffffde88  (sizeof int = 4)
  _d: @ +32  -> 0x7fffffffde90  (sizeof double = 8)

================================================================================
Object: b2  (dynamic type: B2)
================================================================================
Object address: 0x7fffffffdec0
vptr: 0x555555558bd0
Virtual table:
  [  0] 0x555555556536  B2::foo()
  [  1] 0x555555556552  B2::bar()
  [  0] 0x555555556545  virtual thunk to B2::foo()
  [  1] 0x555555556561  virtual thunk to B2::bar()
  [  2] 0x5555555564de  A::dog()

Data members (including bases):
  _vptr.B2: @ +0  -> 0x7fffffffdec0  (sizeof int (**)(void) = 8)
  i: @ +8  -> 0x7fffffffdec8  (sizeof int = 4)
  d: @ +16  -> 0x7fffffffded0  (sizeof double = 8)
  _i: @ +24  -> 0x7fffffffded8  (sizeof int = 4)
  _d: @ +32  -> 0x7fffffffdee0  (sizeof double = 8)

================================================================================
Object: b  (dynamic type: B)
================================================================================
Object address: 0x7fffffffde20
vptr: 0x5555555589f0
Virtual table:
  [  0] 0x5555555565ba  B::foo()
  [  1] 0x5555555565ca  B::bar()
  [  2] 0x5555555564de  A::dog()
  [  3] 0x5555555565da  B::cat()

Data members (including bases):
  [base] A: @ +0  -> 0x7fffffffde20  (sizeof A = 40)
  A::_vptr.A: @ +0  -> 0x7fffffffde20  (sizeof int (**)(void) = 8)
  A::i: @ +8  -> 0x7fffffffde28  (sizeof int = 4)
  A::d: @ +16  -> 0x7fffffffde30  (sizeof double = 8)
  A::_i: @ +24  -> 0x7fffffffde38  (sizeof int = 4)
  A::_d: @ +32  -> 0x7fffffffde40  (sizeof double = 8)
  i: @ +40  -> 0x7fffffffde48  (sizeof int = 4)
  d: @ +48  -> 0x7fffffffde50  (sizeof double = 8)
  _i: @ +56  -> 0x7fffffffde58  (sizeof int = 4)
  _d: @ +64  -> 0x7fffffffde60  (sizeof double = 8)

================================================================================
Object: c  (dynamic type: C)
================================================================================
Object address: 0x7fffffffdf10
vptr: 0x555555558a28
Virtual table:
  [  0] 0x55555555656e  C::foo()
  [  1] 0x555555556594  C::bar()
  [  0] 0x55555555658a  non-virtual thunk to C::foo()
  [  1] 0x5555555565b0  non-virtual thunk to C::bar()
  [  2] 0x555555556526  B1::hello()
  [  0] 0x55555555657d  virtual thunk to C::foo()
  [  1] 0x5555555565a3  virtual thunk to C::bar()
  [  2] 0x5555555564de  A::dog()

Data members (including bases):
  [base] B2: @ +0  -> 0x7fffffffdf10  (sizeof B2 = 80)
  B2::_vptr.B2: @ +0  -> 0x7fffffffdf10  (sizeof int (**)(void) = 8)
  B2::i: @ +8  -> 0x7fffffffdf18  (sizeof int = 4)
  B2::d: @ +16  -> 0x7fffffffdf20  (sizeof double = 8)
  B2::_i: @ +24  -> 0x7fffffffdf28  (sizeof int = 4)
  B2::_d: @ +32  -> 0x7fffffffdf30  (sizeof double = 8)
  [base] B1: @ +40  -> 0x7fffffffdf38  (sizeof B1 = 80)
  B1::_vptr.B1: @ +40  -> 0x7fffffffdf38  (sizeof int (**)(void) = 8)
  B1::i: @ +48  -> 0x7fffffffdf40  (sizeof int = 4)
  B1::d: @ +56  -> 0x7fffffffdf48  (sizeof double = 8)
  B1::_i: @ +64  -> 0x7fffffffdf50  (sizeof int = 4)
  B1::_d: @ +72  -> 0x7fffffffdf58  (sizeof double = 8)
  i: @ +80  -> 0x7fffffffdf60  (sizeof int = 4)
  d: @ +88  -> 0x7fffffffdf68  (sizeof double = 8)
  _i: @ +96  -> 0x7fffffffdf70  (sizeof int = 4)
  _d: @ +104  -> 0x7fffffffdf78  (sizeof double = 8)

================================================================================
Class: A — static & non-virtual methods/data
================================================================================
Static data members (addresses):
  &A::s_i = 0x555555559010
  &A::s_d = 0x555555559018
  &A::_s_i = 0x555555559050
  &A::_s_d = 0x555555559058

Static functions (addresses):

Non-virtual member functions (symbol addresses):
  A::dog() @ 0x5555555564de

(For virtuals use: showobj <expr> to see per-object vtable slots.)

================================================================================
Class: B1 — static & non-virtual methods/data
================================================================================
Static data members (addresses):
  &B1::s_i = 0x5555555591d8
  &B1::s_d = 0x5555555591e0
  &B1::_s_i = 0x5555555591e8
  &B1::_s_d = 0x555555559060

Static functions (addresses):

Non-virtual member functions (symbol addresses):
  B1::hello() @ 0x555555556526
  B1::dog() @ 0x5555555564de

(For virtuals use: showobj <expr> to see per-object vtable slots.)

================================================================================
Class: B2 — static & non-virtual methods/data
================================================================================
Static data members (addresses):
  &B2::s_i = 0x555555559020
  &B2::s_d = 0x555555559028
  &B2::_s_i = 0x555555559068
  &B2::_s_d = 0x555555559070

Static functions (addresses):

Non-virtual member functions (symbol addresses):
  B2::dog() @ 0x5555555564de

(For virtuals use: showobj <expr> to see per-object vtable slots.)

================================================================================
Class: B — static & non-virtual methods/data
================================================================================
Static data members (addresses):
  &B::s_i = 0x555555559030
  &B::s_d = 0x555555559038
  &B::_s_i = 0x555555559078
  &B::_s_d = 0x555555559080

Static functions (addresses):

Non-virtual member functions (symbol addresses):
  B::cat() @ 0x5555555565da
  B::dog() @ 0x5555555564de

(For virtuals use: showobj <expr> to see per-object vtable slots.)

================================================================================
Class: C — static & non-virtual methods/data
================================================================================
Static data members (addresses):
  &C::s_i = 0x555555559040
  &C::s_d = 0x555555559048
  &C::_s_i = 0x555555559088
  &C::_s_d = 0x555555559090

Static functions (addresses):

Non-virtual member functions (symbol addresses):
  C::hello() @ 0x555555556526
  C::dog() @ 0x5555555564de
```

https://wenfh2020.com/2023/08/22/cpp-inheritance/

https://selfboot.cn/en/2024/05/10/c++_object_model/
{% endraw %}