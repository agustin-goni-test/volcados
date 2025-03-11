from inputvolcados import Comercio, Sucursal, VolcadoComercio
from registrosvolcado import RepresentativeRegister, Register, BranchRegister, ServiceRegister, BankAccountRegister
from volcadomanager import VolcadoManager
import requests
import json
from datetime import datetime




if __name__ == "__main__":
    
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)
    # print(volcado.to_json())

    manager = VolcadoManager(AUTH_TOKEN, volcado)

    # Preparando request para VolcadoComercio:
    comercio_register = Register.from_volcado_comercio(volcado)
    print("Request para volcado comercio: ")
    print(comercio_register.to_json())
    print ("\n")

    # Preparando request para Volcado Sucursal
    branch_register = BranchRegister.from_volcado_comercio(volcado)
    print("Request para volcado sucursal: ")
    print(branch_register.to_json())
    print("\n")

    # Preparando request para Volcado Servicio Sucursal
    branch_service_register = ServiceRegister.from_volcado_comercio(volcado)
    print("Request para volcado servicio sucursal: ")
    print(branch_service_register.to_json())
    print("\n")

    # Preparando volcado para Representante Legal
    representante_register = RepresentativeRegister.from_volcado_comercio(volcado)
    print("Request para volcado de representante legal: ")
    print(representante_register.to_json())
    print("\n")

    # Preparando volcado de cuenta bancaria
    cuenta_register = BankAccountRegister.from_volcado_comercio(volcado)
    print("Request para volcado de cuenta bancaria: ")
    print(cuenta_register.to_json())
    print("\n")


    # comercio_register = Register.from_volcado_comercio(volcado)

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
        
        # servicio = ServiceRegister.from_volcado_comercio(volcado)
        # print("\n")
        # print(servicio.to_json())

    
   



