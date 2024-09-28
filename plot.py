import seaborn as sns
import math
import numpy as np

def ft_to_mt(ft): 
    return ft * 0.304

speed_in = [ft_to_mt(v) for v in [14.7, 22.0, 29.3, 36.7, 44, 51.3, 58.7, 66, 73.3, 80.7, 88, 95.3, 102.7]]
stop_dist = [ft_to_mt(d) for d in [5,   11,   19,   30,   43, 58,   76,   96, 119,  144,  171, 201, 233]]

# acc from above traffic data (USA)
acc = -6.5

def linear_acc_collision_velocity(acc, va0, vb0, s0):
    return va0 + acc * s0 / (va0 - vb0)

pts = [
        {
            "s0": s0,
            "vd": vd,
            "vb0": vb0,
            "vc": linear_acc_collision_velocity(acc, vb0 + vd, vb0, s0)
        }
        for s0 in [1, 10, 20]
        for vd in [0.5, 1, 2, 4, 8]
        for vb0 in [30]
    ]

def col_time_before_reaction_roots(acc, va0, vb0, s0):
    return np.roots([0.5 * acc, (vb0 - va0), s0])

def col_time_after_reaction(acc, va0, vb0, s0, tr):
    return 0.5 * (acc * tr*tr - 2 * s0) / (acc * tr - va0 - vb0)

def col_time(acc, va0, vb0, s0, tr):
    ct_pre_reaction = col_time_before_reaction_roots(acc, va0, vb0, s0).max()
    ct_post_reaction = col_time_after_reaction(acc, va0, vb0, s0, tr)

    if ct_pre_reaction < tr:
        return ct_pre_reaction
    else:
        return ct_post_reaction

def rel_speed(acc, va0, vb0, s0, tr):
    ct = col_time(acc, va0, vb0, s0, tr)
    return va0 - vb0 - acc * min(ct, tr)

# movement equations
# v_a = | v_a                                                                   0 <= t <  t_r         
#       | v_a + a (t - t_r)                                                   t_r <= t < t_r + v_a / a
#       | 0                                                         t_r + v_a / a <= t                
#
# s_a = | v_a t                                                                 0 <= t < t_r             (1)
#       | v_a t_r + v_a t + 0.5 a t^2 - a t_r t                               t_r <= t < t_r + v_a / a   (2)
#       | 1.5 v_a^2 / a - a t_r v_a / a + v_a t_r                   t_r + v_a / a <= t                   (3)
#
# v_b = | v_b + a t                                                           0   <= t <  v_b / a     
#       | 0                                                               v_b / a <= t                
#
# s_b = | v_b t + 0.5 a t^2 + s0                                                0 <= t < v_b / a         (4)
#       | v_b^2 / abs(a) + (0.5 a v_b^2) / abs(a)^2 + s0                      v_b / a <= t                   (5)


# 1 & 4
def t_solve_steady_a_slow_b(a, va, vb, s0):
    return np.roots([-0.5 * a, va - vb, s0])

# 2 & 4
def t_solve_slow_a_slow_b(a, va, vb, s0, tr):
    #return (a * tr ** 2 - 2 * s0) / ( 2 * (a * tr - va + vb))
    #return (s0 - va*tr) / (va-vb)
    return (va * tr - s0) / (a * tr - va + vb)


# 1 & 5
def t_solve_steady_a_stop_b(a, va, vb, s0, _):
    absa = abs(a)
#    return np.roots([-0.5 * a, va - vb, -s0])
    return ((vb**2 / absa) + (0.5 * a * vb**2) / (absa**2) + s0) / va

# 2 & 5
def t_solve_slow_a_stop_b(a, va, vb, s0, tr):
    absa = abs(a)
    sb = (vb**2 / absa + (0.5 * a * vb**2) / (absa**2) + s0)
    return np.roots([0.5 * a, va - a * tr, va*tr - sb ])

def v_solve_a(t, a, va, _vb, _s0, tr):
    if t < tr:
        return va
    elif t < va / a:
        return va + a * (t - tr)
    return 0

def v_solve_b(t, a, _va, vb, _s0, _tr):
    if t < vb / a:
        return vb + a * t
    return 0

def collision_point(a, va, vb, s0, tr):
    print({'a': a, 'va': va, 'vb': vb, 's0': s0, 'tr': tr})
    print(f"tsa: {tr + va / a}, tsb: {vb / a}")
    t_steady_slow = t_solve_steady_a_slow_b(a, va, vb, s0)
    print(f"steady-slow: {t_steady_slow}")
    t_slow_slow = t_solve_slow_a_slow_b(a, va, vb, s0, tr)
    print(f"slow-slow: {t_slow_slow}")
    t_steady_stop = t_solve_steady_a_stop_b(a, va, vb, s0, tr)
    print(f"steady-stop: {t_steady_stop}")
    t_slow_stop = t_solve_slow_a_stop_b(a, va, vb, s0, tr)
    print(f"slow-stop: {t_slow_stop}")

collision_point(-1, 11, 10, 10, 0)

#pts = [
#        {
#            "s0": s0,
#            "vd": vd,
#            "vb0": vb0,
#            "tr": tr,
#            "vc": rel_speed(acc, vb0 + vd, vb0, s0, tr)
#        }
#        for s0 in [1, 10, 20]
#        for vd in [1, 2, 5]
#        for vb0 in [30]
#        for tr in [0, 0.67]
#      ]
#
#for pt in pts:
#    print(pt)
