from modelling_utils.read import read_specs
import numpy as np
import pandas as pd
from modelling_utils import(
    plot_function,
    plot_hist,
    timer,
    read_data,
    read_lut
)
from modelling_utils import __version__
import unittest
class TestModellingFramework(unittest.TestCase):

    def test_version(self):
        self.assertEqual(__version__, '0.2.1')
    
    def test_single_plot_2d(self):
        x = np.arange(0, 2*(np.pi), 0.1)
        y = np.cos(x)
        y = np.log(np.abs(y))
        plot_function(x=x, y=y, labels=["cosine"], xlabel="domain", ylabel="func", title="Simple Plot", show=False, filename="test1.png")
        self.assertTrue(True)
    
    def test_multiple_plot_signle_domain_2d(self):
        x = np.arange(0, 2*(np.pi), 0.1)
        yy =[
            np.cos(x),
            np.sin(x),
            np.tan(x)
        ]
        plot_function(x=x, y=yy, labels=["cosine", "sine", "tangent"], xlabel="domain", ylabel="func", title="Simple Plot2", filename="test2.png")
        self.assertTrue(True)
    
    def test_multiple_plot_multiple_domain_2d(self):
        xx = [
            np.arange(0, 2*(np.pi), 0.1),
            np.arange(0, 1*(np.pi), 0.1),
            np.arange(0, 0.5*(np.pi), 0.1)
        ]
        yy =[
            np.cos(xx[0]),
            np.sin(xx[1]),
            np.tan(xx[2])
        ]
        plot_function(x=xx, y=yy, labels=["cosine", "sine", "tangent"], xlabel="domain", ylabel="func", title="Simple Plot3", show=False, filename="test3.png")
        self.assertTrue(True)
        
    def test_plot_3d(self):
        z = np.arange(0, 2*(np.pi), 0.1)
        x = np.cos(z)
        y = np.sin(z)
        
        x2 = np.outer(np.linspace(-2, 2, 10), np.ones(10))
        y2 = x2.copy().T
        z2 = np.cos(x2 ** 2 + y2 ** 3)
        plot_function(x=x, y=y, z=z, labels=["3D func"], xlabel="abciss", ylabel="ordinate", title="A 3D plot", filename="line3d.png")
        plot_function(x=x, y=y, z=z, labels=["3D func"], xlabel="abciss", ylabel="ordinate", title="A 3D plot", type="scatter", filename="scatter3d.png")
        plot_function(x=x2, y=y2, z=z2, labels=["3D func"], xlabel="abciss", ylabel="ordinate", title="A 3D plot", type="surface", filename="surface3d.png")
        plot_function(x=x2, y=y2, z=z2, labels=["3D func"], xlabel="abciss", ylabel="ordinate", title="A 3D plot", type="wireframe", filename="wireframe3d.png")
        self.assertTrue(True)

    def test_histogram(self):
        x = np.random.randn(100)
        plot_hist(data=x, labels=["histogram"], xlabel="random val", title="Simple Histogram", show=False, filename="hist.png")
        xx = [
            np.random.randn(100),
            np.random.randn(100),
            np.random.randn(100)
        ]
        plot_hist(data=xx, labels=["rand1","rand2","rand3"], xlabel="random val", title="Triple Histogram", show=False, filename="hist2.png")
        self.assertTrue(True)
    
    def test_read_specs(self):
        path1 = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/m0.toml"
        path2 = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/specs.toml"
        devices1=read_specs(path1)
        self.assertIsNotNone(devices1)
        print(devices1)
        
        devices2=read_specs(path2)
        self.assertIsNotNone(devices2)
        print(devices2)
        pass

    def test_read_data(self):
        path = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/simulations_28nm_cmos/simulations/ncell/vsb-0_w-2-3-u_l-30-n_sweep-vgs-vds.csv"
        df = read_data(path)
        self.assertEqual(type(df), pd.DataFrame)
        print(df)
        pass
    
    def test_read_lut(self):
        path = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/simulations_28nm_cmos/simulations/ncell/vsb-0_w-2-3-u_l-30-n_sweep-vgs-vds.csv"
        df_lut = read_lut(path)
        self.assertEqual(type(df_lut), pd.DataFrame)
        print(df_lut)
        pass

    def test_read_lut2(self):
        path = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/simulations_28nm_cmos/simulations/pcell/vbs-0_w-2-3-u_l-30-n_sweep-vsg-vsd.csv"
        df_lut = read_lut(path)
        self.assertEqual(type(df_lut), pd.DataFrame)
        print(df_lut)
        pass
    
    def test_read_varactor(self):
        path1 = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/v0.toml"
        path2 = "/Users/dasdias/Documents/PhD-NOVA/Circuits/ResidueAmplifier_Gain8_28nmTSMC/modelling_utils/resources/var_specs.toml"
        devices1=read_specs(path1)
        self.assertIsNotNone(devices1)
        print(devices1)
        
        devices2=read_specs(path2)
        self.assertIsNotNone(devices2)
        print(devices2)
        
if __name__ == "__main__":
    unittest.main()