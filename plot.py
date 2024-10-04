import seaborn as sns
import seaborn.objects as so
import math
import numpy as np
import pandas as pd
import motion
import matplotlib.pyplot as plt
import itertools

# acc from above traffic data (USA)
acc = -6.5

def mph_to_mps(s):
    return s * 0.44704

def mps_to_mph(s):
    return s / 0.44704

def plot_velocity_time():
    va = mph_to_mps(65)
    vb = mph_to_mps(60)
    sb0 = 10
    tr = 600 / 1000 # ms

    time_points = np.linspace(0, 60, num=1000)
    pts = [{'t': t, 'v': motion.find_velocity(acc, va, sb0, vb, tr, t)} for t in time_points]
    df = pd.DataFrame(pts)

    p = sns.lineplot(df, x = 't', y = 'v')

    p.get_figure().savefig('velo_plot.pdf')

def plot():
    vb_mph = 60
    vb = mph_to_mps(vb_mph)
    tr = 1.5

    def entry(s, va_mph):
        va = mph_to_mps(va_mph)
        res = motion.find_collision(acc, va, s, vb, tr)
        if res is not None:
            t, v, ct= res
            return {'s': s, 'ts': (s / va), 'v': mps_to_mph(float(v)), 't' : float(t), 'collision_type': ct, 'va' : va_mph - vb_mph}

    def get_dsts(va):
        va = mph_to_mps(va)
        v_zero = motion.find_stop_point(acc, va, vb, tr)
        return np.linspace(0, v_zero - 1e-12, num=200)

    def flatten(lls):
        return list(itertools.chain.from_iterable(lls))

    df = pd.DataFrame([x for x in flatten([
           [ entry(s,va) for s in get_dsts(va) ]
           for va in [61, 62, 64, 68]
         ]) if x is not None])

    p = (
            so.Plot(df, "s", 'v')
            .add(so.Line(), color='va')
            .label(
                    x = 'Distance from car in front (m)',
                    y = 'Collision speed (mph)',
                    color = 'Extra speed (mph)',
                    title = f"Collision speed during emergency braking when from car is travelling at {vb_mph} mph"
                    )
        )

    p.save('collision_plot.pdf', bbox_inches="tight")

    p = (
            so.Plot(df, "ts", 'v')
            .add(so.Line(), color='va')
            .label(
                    x = 'Distance to car in front (seconds)',
                    y = 'Collision speed (mph)',
                    color = 'Speed delta (mph)',
                    #title = f"Collision speed during emergency braking when from car is travelling at {vb_mph} mph"
                    title = "\n".join([
                            f"Collision speed when the car in front emergency brakes",
                            f"The front car initially travels at {vb_mph} mph",
                            f"Your are initially travelling <speed delta> faster and brake {tr} seconds later",
                        ]),
                    )
        )

    p.save('collision_plot_time.pdf', bbox_inches="tight")
    p.save('collision_plot_time.png', bbox_inches="tight")

plot()
