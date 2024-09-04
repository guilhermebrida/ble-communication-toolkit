import asyncio
from bleak import BleakScanner, BleakClient
import XVM

WRITE_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"  # UUID para escrita
READ_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"   # UUID para leitura
NOTIFY_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"


def notification_handler(sender, data):
    output_numbers = list(data)
    print(f"Notification from {sender}: {data}")

async def scan_and_connect(device_name):
    devices = await BleakScanner.discover()
    target_device = None

    for device in devices:
        if "VIRTEC" in device.name: 
            print(f"Device: {device.name}, Address: {device.address}")
        if device.name == device_name:
            target_device = device
            break

    if target_device:
        async with BleakClient(target_device.address) as client:
            if client.is_connected:
                print(f"Connected to {target_device.name}")
                
                for service in client.services:
                    print(f"[Service] {service.uuid}: {service.description}")
                    for char in service.characteristics:
                        print(f"\t[Characteristic] {char.uuid}: {char.description} : {char.properties}")

                
                await client.start_notify(NOTIFY_CHARACTERISTIC_UUID, notification_handler)
                print(f"Started notifications for {NOTIFY_CHARACTERISTIC_UUID}")

                await send_command_to_device(client, device_name)

                await client.stop_notify(NOTIFY_CHARACTERISTIC_UUID)
                print(f"Stopped notifications for {NOTIFY_CHARACTERISTIC_UUID}")
            else:
                print(f"Failed to connect to {target_device.name}")
    else:
        print(f"Device {device_name} not found.")

async def send_command_to_device(client, device_name):
    try:
        while True:
            command = input("Digite a mensagem a ser enviada (ou 'exit' para sair): ")
            if command == "exit":
                break
            else:
                device = device_name.replace("VIRTEC_VL8_", "").replace("\"", "")
                xvm = XVM.generateXVM(device, '8000', command)
                command_bytes = xvm.encode()
                
                await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, command_bytes)
                print(f"Command '{command}' sent to characteristic {WRITE_CHARACTERISTIC_UUID}")

                await asyncio.sleep(1.0)

                # try:
                #     response = await client.read_gatt_char(READ_CHARACTERISTIC_UUID)
                #     response_text = response.decode('utf-32')
                #     print(f"Response received: {response_text}")
                # except Exception as read_e:
                #     print(f"Failed to read response: {read_e}")

    except Exception as e:
        print(f"Failed to send command: {e}")

device_name = "\"VIRTEC_VL8_G3P0\""
asyncio.run(scan_and_connect(device_name))






# async def scan_ble_devices():
#     devices = await BleakScanner.discover()
#     for device in devices:
#         if "VIRTEC" in device.name: 
#             print(f"Device: {device.name}, Address: {device.address}")


# async def connect_ble_device(address):
#     async with BleakClient(address) as client:
#         if client.is_connected:
#             print(f"Connected to {address}")
#             # Exemplo: Ler uma característica
#             # uuid = "00002a37-0000-1000-8000-00805f9b34fb"  # Substitua pelo UUID da característica que você deseja ler
#             # value = await client.read_gatt_char(uuid)
#             # print(f"Characteristic value: {value}")
#         else:
#             print(f"Failed to connect to {address}")

# async def send_command_to_device(address, characteristic_uuid):
#     async with BleakClient(address) as client:
#         if client.is_connected:
#             print(f"Connected to {address}")
#             device = device_name.replace("VIRTEC_VL8_","")
#             try:
#                 while True:
#                     command = input("Digite a mensagem a ser enviada (ou 'exit' para sair): ")
#                     if command == "exit":
#                         break
#                     else:
#                         xvm = XVM.generateXVM(device,'8000',command)
#                         command_bytes = xvm.encode()    
#                         await client.write_gatt_char(characteristic_uuid, command_bytes)
#                         print(f"Command '{command}' sent to characteristic {characteristic_uuid}")

#             except Exception as e:
#                 print(f"Failed to send command: {e}")
#         else:
#             print(f"Failed to connect to {address}")

# asyncio.run(scan_ble_devices())
