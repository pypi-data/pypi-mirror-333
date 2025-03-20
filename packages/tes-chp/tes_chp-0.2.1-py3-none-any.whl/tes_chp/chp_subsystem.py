# based on chp_test.ipynb
from dataclasses import dataclass

from tespy.components import Sink, Source, CombustionEngine, Merge, Splitter, HeatExchanger, Subsystem
from tespy.connections import Connection, Ref
from tespy.networks import Network

AMBIENT_KEY = "Ambient"
FUEL_KEY = "Fuel"
CW_IN_KEY = "Cooling Water Inlet"
SPLITTER_KEY = "Splitter"
MERGE_KEY = "Cooling Water Merge"
ENGINE_KEY = "Internal Combustion Engine"
AMBIENT_OUT_KEY = "Ambient Out"
HOT_WATER_OUT_KEY = "Hot Water Out"
HEX_KEY = "HeatExchanger"

AMBIENT_INLET_CONN_KEY = "ambient_inlet"
FUEL_INLET_CONN_KEY = "fuel_inlet"
CW_TO_SPLITTER_CONN_KEY = "cooling_water_to_splitter"
SPLITTER_OUTLET_1_CONN_KEY = "splitter_outlet_1"
SPLITTER_OUTLET_2_CONN_KEY = "splitter_outlet_2"
MERGE_INLET_1_CONN_KEY = "merge_inlet_1"
MERGE_INLET_2_CONN_KEY = "merge_inlet_2"
FLUE_GAS_TO_HEX_CONN_KEY = "flue_gas_to_hex"
HEX_TO_OUTDOOR_CONN_KEY= "hex_to_outdoor"
MERGE_HEX_CONN_KEY= "merge_hex"
HEX_TO_NETWORK = "hex_to_network"

@dataclass
class CHP(Subsystem):
    
    ambient_source: Source = None
    fuel_source: Source = None
    cooling_water_source: Source = None
    splitter: Splitter = None
    merge: Merge = None
    cw_out: Sink = None
    engine: CombustionEngine = None
    ambient_out: Sink = None
    supply_hot_water: Sink = None
    hex: HeatExchanger = None
    
    
    def __init__(self, label):
        super().__init__(label)

        # set defaults
        self.set_attr()

    def create_comps(self):
        self.ambient_source = self.comps[AMBIENT_KEY] = Source(f'{self.label}_{AMBIENT_KEY}')
        self.fuel_source = self.comps[FUEL_KEY] = Source(f'{self.label}_{FUEL_KEY}')
        self.cooling_water_source = self.comps[CW_IN_KEY] = Source(f'{self.label}_{CW_IN_KEY}')
        self.splitter = self.comps[SPLITTER_KEY] = Splitter(f'{self.label}_{SPLITTER_KEY}', num_out=2)
        self.merge = self.comps[MERGE_KEY] = Merge(f'{self.label}_{MERGE_KEY}', num_in=2)
        self.engine = self.comps[ENGINE_KEY] = CombustionEngine(f'{self.label}_{ENGINE_KEY}')
        self.ambient_out = self.comps[AMBIENT_OUT_KEY] = Sink(f'{self.label}_{AMBIENT_OUT_KEY}')
        self.supply_hot_water = self.comps[HOT_WATER_OUT_KEY] = Sink(f'{self.label}_{HOT_WATER_OUT_KEY}')
        self.hex = self.comps[HEX_KEY] = HeatExchanger(f'{self.label}_{HEX_KEY}')

    def create_conns(self):
        self.conns[AMBIENT_INLET_CONN_KEY] = Connection(self.ambient_source, 'out1', self.engine, 'in3') 
        self.conns[FUEL_INLET_CONN_KEY] = Connection(self.fuel_source, 'out1', self.engine, 'in4') 
        self.conns[CW_TO_SPLITTER_CONN_KEY] = Connection(self.cooling_water_source, 'out1', self.splitter, 'in1') 
        self.conns[SPLITTER_OUTLET_1_CONN_KEY] = Connection(self.splitter, 'out1', self.engine, 'in1') 
        self.conns[SPLITTER_OUTLET_2_CONN_KEY] = Connection(self.splitter, 'out2', self.engine, 'in2') 
        self.conns[MERGE_INLET_1_CONN_KEY] = Connection(self.engine, 'out1', self.merge, 'in1') 
        self.conns[MERGE_INLET_2_CONN_KEY] = Connection(self.engine, 'out2', self.merge, 'in2') 
        self.conns[FLUE_GAS_TO_HEX_CONN_KEY] = Connection(self.engine, 'out3', self.hex, 'in1')
        self.conns[HEX_TO_OUTDOOR_CONN_KEY] = Connection(self.hex, 'out1', self.ambient_out, 'in1') 
        self.conns[MERGE_HEX_CONN_KEY] = Connection(self.merge, 'out1', self.hex, 'in2')
        self.conns[HEX_TO_NETWORK] = Connection(self.hex, 'out2', self.supply_hot_water, 'in1')

    def set_attr(self, P=-1e6, 
                 engine_eta_mech=0.93,
                 p_ambient_inlet=1,
                 p_cw_to_splitter=3,
                 T_ambient_inlet=30,
                 T_fuel_inlet=40,
                 T_supply=104.3):

        self.engine.set_attr(P=P, pr1=0.99, lamb=1.0, design=["pr1"], offdesign=['zeta1'], eta_mech=engine_eta_mech)
        
        self.conns[AMBIENT_INLET_CONN_KEY].set_attr(p=p_ambient_inlet, 
                                                    T=T_ambient_inlet, 
                                                    fluid={'Ar': 0.0129, 'N2': 0.7553, 'CO2': 0.0004, 'O2': 0.2314})
        self.conns[FUEL_INLET_CONN_KEY].set_attr(T=T_fuel_inlet, fluid={'CH4': 1})
        self.conns[CW_TO_SPLITTER_CONN_KEY].set_attr(p=p_cw_to_splitter, T=80, m=12, fluid={'H2O': 1}, design=["T"])
        self.conns[SPLITTER_OUTLET_2_CONN_KEY].set_attr(m=Ref(self.conns[SPLITTER_OUTLET_1_CONN_KEY], 1, 0))
        self.hex.set_attr(pr1=0.95, pr2=0.95, design=["pr1", "pr2"], offdesign=["zeta1", "zeta2", "kA_char"])
        self.conns[HEX_TO_NETWORK].set_attr(T=T_supply)

    @staticmethod
    def as_network(label="CHP"):
        net = Network(fluids=["H2O", "CH4", "H2", "O2", "CO2", "Ar", "N2"], p_unit='bar', T_unit='C', iterinfo=False)
        net.add_subsys(CHP(label))
        return net
    

if __name__ == "__main__":
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
