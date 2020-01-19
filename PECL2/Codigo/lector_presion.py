import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep

def inicializar():
    # Creo bus SPI
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Cargo Chip Select
    cs = digitalio.DigitalInOut(board.D5)

    # Creo el objeto MCP asociado
    mcp = MCP.MCP3008(spi, cs)
    # y lo devuelvo
    return mcp

def get_canales(mcp):
    # creo canales
    canal1 = AnalogIn(mcp, MCP.P0)
    canal2 = AnalogIn(mcp, MCP.P1)
    canal3 = AnalogIn(mcp, MCP.P2)
    canales = [canal1, canal2, canal3]
    return canales

def get_valor(numero_canal, canales):
    return canales[numero_canal].value
# Main
#mcp = inicializar()

#canales = get_canales(mcp)

#while(True):
#    print('Valor C1: ', get_valor(0, canales))
#    print('Valor C2: ', get_valor(1, canales))
#    print('Valor C3: ', get_valor(2, canales))
    #print('ADC Voltage: ' + str(chan.voltage) + 'V')
#    sleep(0.5)
