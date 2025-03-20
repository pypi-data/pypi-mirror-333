# TESpy-based CHP

***Important: This model is still unfinished and under active development! Use it with caution.***

This project contains a CHP implemetation using TESpy. To install the package run

```bash
pip install tes-chp
```

The CHP is implemented as TESpy subsystem. A simple usage could look like:

```py
from tes_chp import CHP
from tespy.networks import Network

net = Network(fluids=["H2O", "CH4", "H2", "O2", "CO2", "Ar", "N2"], p_unit='bar', T_unit='C', iterinfo=False)
chp = CHP("CHP")
net.add_subsys(chp)

chp.set_attr(P=-1e6)

mode= "design"
net.solve(mode=mode, design_path=".")
net.save("tmp")
net.print_results()

chp.set_attr(P=-5e5)

mode= "offdesign"
net.solve(mode=mode, design_path="tmp")
net.print_results()
```

