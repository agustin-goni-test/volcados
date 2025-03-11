from inputvolcados import Comercio, Sucursal, VolcadoComercio
from registrosvolcado import RepresentativeRegister, Register, BranchRegister, ServiceRegister
from volcadomanager import VolcadoManager
import requests
import json
from datetime import datetime




if __name__ == "__main__":
    
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)
    print(volcado.to_json())

    manager = VolcadoManager(AUTH_TOKEN, volcado)

    comercio_register = Register.from_volcado_comercio(volcado)

    print ("\n")
    # print (comercio_register.to_json())

    if manager.isResponding():
        print("Servicio contestando en forma correcta...")
        # manager.volcadoRepresentanteLegal()
        # manager.volcadoCuentaBancaria()
        # manager.volcadoConfiguracionCuentaBancaria()
        # comercio_register = Register.from_volcado_comercio(volcado)
        # manager.volcadoComercio(comercio_register)

        # Construye el objeto de volcado de sucursal y vuelca la sucursal
        # sucursal_register = BranchRegister.from_volcado_comercio(volcado)
        # print(sucursal_register.to_json())
        # branch_id, local_code = manager.volcadoSucursal(sucursal_register)

        # print("\n")
        # print(f"branch_id = {branch_id}, local_code = {local_code}")
        
        servicio = ServiceRegister.from_volcado_comercio(volcado)
        print("\n")
        print(servicio.to_json())

    
   



