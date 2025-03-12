from inputvolcados import Comercio, Sucursal, VolcadoComercio
from registrosvolcado import RepresentativeRegister, Register, BranchRegister, ServiceRegister, BankAccountRegister
from registrosvolcado import PaymentTypeRegister, ContractRegister, MerchantDiscountRegister, TerminalRegister
from registrosvolcado import BankAccConfigRegister, BranchCCRegister, TerminalCCRegister, IswitchCommerceRegister
from registrosvolcado import IswitchBranchRegister, IswitchTerminalRegister, CommercePciRegister, CommerceSwitchRegister
from registrosvolcado import TicketRegister, MonitorRegister, RedPosRegister
from volcadomanager import VolcadoManager
from resultvolcado import ResultadoVolcado
import requests
import json
from datetime import datetime

# Este código lee un archivo Excel con la información de un comercio y generar los
# request para hacer el volcado según el camino tradicional (sin multiplicidad).
# Estamos mostrando cada request en pantalla

if __name__ == "__main__":
    
    AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJtcy1jZW50cmFsLWFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpbyIsImlzcyI6ImFmLWF5Yy1yZWdpc3Ryby1jb21lcmNpby1jZW50cmFsIn0.gxrgQE6Oae1-gw3Gaif0j3e-uY2sMjR2IWPwRS-5mL0"
    
    file_path = "InfoComercio.xlsx"
    volcado = VolcadoComercio.from_excel(file_path)
    print(volcado.to_json())

    manager = VolcadoManager(AUTH_TOKEN, volcado)

    # Este código lee un archivo Excel con la información de un comercio y generar los
    # request para hacer el volcado según el camino tradicional (sin multiplicidad).
    # Estamos mostrando cada request en pantalla

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

    payment_type_register = PaymentTypeRegister.from_volcado_comercio(volcado)
    print("Request para volcado de payment type: ")
    print(payment_type_register.to_json())
    print("\n")

    contract_register = ContractRegister.from_volcado_comercio(volcado)
    print("Request para volcado de contrato: ")
    print(contract_register.to_json())
    print("\n")

    merchant_register = MerchantDiscountRegister.from_volcado_comercio(volcado)
    print("Request para volcado de merchant discount: ")
    print(merchant_register.to_json())
    print("\n")

    terminal_register = TerminalRegister.from_volcado_comercio(volcado)
    print("Request para volcado de terminal: ")
    print(terminal_register.to_json())
    print("\n")

    bank_config_register = BankAccConfigRegister.from_volcado_comercio(volcado)
    print("Request para volcado de configuración de cuenta bancaria: ")
    print(bank_config_register.to_json())
    print("\n")

    branch_cc_register = BranchCCRegister.from_volcado_comercio(volcado)
    print("Request para volcado Branch CC: ")
    print(branch_cc_register.to_json())
    print("\n")

    terminal_cc_register = TerminalCCRegister.from_volcado_comercio(volcado)
    print("Request para terminal CC: ")
    print(terminal_cc_register.to_json())
    print("\n")

    iswitch_commerce_register = IswitchCommerceRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en Iswitch: ")
    print(iswitch_commerce_register.to_json())
    print("\n")

    iswitch_branch_register = IswitchBranchRegister.from_volcado_comercio(volcado)
    print("Request para volcado de sucursal en Iswitch: ")
    print(iswitch_branch_register.to_json())
    print("\n")

    iswitch_terminal_register = IswitchTerminalRegister.from_volcado_comercio(volcado)
    print("Request para volcado de terminal en Iswitch: ")
    print(iswitch_terminal_register.to_json())
    print("\n")

    commerce_pci_register = CommercePciRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en réplica PCI: ")
    print(commerce_pci_register.to_json())
    print("\n")

    commerce_switch_register = CommerceSwitchRegister.from_volcado_comercio(volcado)
    print("Request para volcado de comercio en switch: ")
    print(commerce_switch_register.to_json())
    print("\n")

    ticket_register = TicketRegister.from_volcado_comercio(volcado)
    print("Request para volcado para ticket de comercio: ")
    print(ticket_register.to_json())
    print("\n")

    monitor_register = MonitorRegister.from_volcado_comercio(volcado)
    print("Request para volcado en Monitor Plus: ")
    print(monitor_register.to_json())
    print("\n")

    red_pos_register = RedPosRegister.from_volcado_comercio(volcado)
    print("Request para volcado de ticket en RedPos: ")
    print(red_pos_register.to_json())
    print("\n")

    


    # comercio_register = Register.from_volcado_comercio(volcado)

    print ("Comenzando volcado...")
    print("los pasos serán los siguientes:")

    step_list = '''    1. VolcadoComercio
    2. VolcadoTicket
    3. VolcadoSucursal
    4. VolcadoRepresentante
    5. VolcadoServicio
    6. VolcadoTipoPago
    7. VolcadoMerchant
    8. VolcadoTerminal
    9. VolcadoContrato
    10. VolcadoCuentaBancaria
    11. VolcadoConfiguraciónCuenta
    12. VolcadoCCSucursal
    13. VolcadoCCTerminal
    14. VolcadoIswitchComercio
    15. VolcadoIswitchSucursal
    16. VolcadoIswitchTerminal
    17. VolcadoPci
    18. VolcadoSwitch
    19. VolcadoMonitor
    20. VolcadoRedPos
    '''

    print(step_list)

    seleccion_usuario = input("Ingrese el paso desde el cuál empezar (por defecto 1)")
    seleccion = int(seleccion_usuario) if seleccion_usuario else 1

    print(f'El paso seleccionado es el {seleccion} \n')

    result = ResultadoVolcado()
    print("Objeto resultado creado...")

    
    print(result)
    
    # result_json = json.dumps(result_dict, indent=2)

    

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