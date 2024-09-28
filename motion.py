# type: ignore
import sympy as sm

# a behind b

# initially
# sa = 0, sb = sb0
# va = va0, vb = vb0
# acc_a = 0, acc_b = acc

# reaction time
# at t = tr
# acc_a = acc

# a stops
# when va = 0
# acc_a = 0

# b stops
# when vb = 0
# acc_b = 0

# constants
acc = sm.symbols('acc')
va0, sb0, vb0 = sm.symbols('va0 sb0 vb0')
tr = sm.symbols('tr')

# variables
t = sm.symbols('t')

def integrate(f, t0, x0):
    c = sm.symbols('c')
    integral = sm.integrate(f, t).subs(t, t0)
    c_const = sm.solve(integral + c - x0, c)[0]
    return integral + c_const

# Pre reaction
va_pre_reaction = va0
sa_pre_reaction = sm.integrate(va_pre_reaction, t)
vb_pre_reaction = vb0 + acc * t
sb_pre_reaction = sm.integrate(vb_pre_reaction, t) + sb0

# at reaction
sa_at_reaction = sa_pre_reaction.subs(t, tr)
sb_at_reaction = sb_pre_reaction.subs(t, tr)

# after reaction
va_after_reaction = va_pre_reaction + acc * (t - tr)
sa_after_reaction = sm.integrate(va_after_reaction, t) + sa_pre_reaction.subs(t, tr)
vb_after_reaction, sb_after_reaction = vb_pre_reaction, sb_pre_reaction

# after stops
ta_stop = sm.solve(va_after_reaction, t)
va_after_stop = 0.
sa_after_stop = sa_after_reaction.subs(t, ta_stop[0])

tb_stop = sm.solve(vb_after_reaction, t)
vb_after_stop = 0.
sb_after_stop = sb_after_reaction.subs(t, tb_stop[0])

# criticial times
# time of reaction
# time of collision assuming before reaction
tc_pre_reaction = sm.solve(sa_pre_reaction - sb_pre_reaction, t)
# time of collision assuming after reaction but before b stops
tc_pre_stop = sm.solve(sa_after_reaction - sb_after_reaction, t)
# time of collision assuming after b stops
tc_post_stop = sm.solve(sa_after_reaction - sb_after_stop, t)

def find_collision(acc, va0, sb0, vb0, tr):
    def sub_all(f):
        lf = f.subs('acc', acc)
        lf = lf.subs('va0', va0)
        lf = lf.subs('sb0', sb0)
        lf = lf.subs('vb0', vb0)
        lf = lf.subs('tr', tr)
        return lf.evalf()
    print("pre reaction")
    for t in tc_pre_reaction:
        t = sub_all(t)
        print(t)
        if t.is_real and t >= 0 and t < tr:
            return t, sub_all((va_pre_reaction - vb_pre_reaction).subs('t', t))
    ltb_stop = sub_all(tb_stop[0])
    if tr < ltb_stop: # tr < tb_stop
        print("pre stop")
        for t in tc_pre_stop:
            t = sub_all(t)
            print(tr, t, ltb_stop)
            if t.is_real and tr <= t and t < ltb_stop:
                return t, sub_all((va_after_reaction - vb_after_reaction).subs('t', t))
        print("post stop")
        for t in tc_post_stop:
            t = sub_all(t)
            print(ltb_stop, t, )
            if t.is_real and ltb_stop <= t and t < sub_all(ta_stop[0]):
                return t, sub_all((va_after_reaction - vb_after_stop).subs('t', t))
        return None
    else:
        print("Stops before reaction")
        pass
