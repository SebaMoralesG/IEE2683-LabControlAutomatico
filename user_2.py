from opcua import ua, Client
import threading
import time
from math import log, exp

#  Actualizar
def funcion_handler(node, val):
    key = node.get_parent().get_display_name().Text
    # print('key: {} | val: {}'.format(key, val))
    if key in {f"Tanque{i}" for i in {1,2,3,4}}:
        if val < 10:
            print(f"El nivel del {key} es menor a 10")

# Actualizar
class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        thread_handler = threading.Thread(target=funcion_handler, args=(node, val))  # Se realiza la descarga por un thread
        thread_handler.start()

    def event_notification(self, event):
        # print("Python: New event", event)
        pass


class Cliente():
    def __init__(self, direccion, suscribir_eventos, SubHandler):
        self.direccion = direccion
        self.client = Client(direccion)
        self.alturas = {'H1': 0, 'H2': 0, 'H3':0, 'H4':0}
        self.temperaturas = {'T1': 0, 'T2': 0, 'T3':0, 'T4':0}
        self.valvulas = {'valvula1':0, 'valvula2':0}
        self.razones = {'razon1':0, 'razon2': 0}
        self.subscribir_eventos = suscribir_eventos
        self.periodo = 100 # cantidad de milisegundos para revisar las variables subscritas
        self.SubHandlerClass = SubHandler

        self.kp = {1: 1, 2: 1}
        self.ki = {1: 0.1, 2: 0.1}
        self.kd = {1: 0.1, 2: 0.1}

        # Referencia
        self.h_ref_1 = 20
        self.h_ref_2 = 35

        self.int_limit = 2

    def sat(x, A, B):
        return min(max(x, A), B)

    def inicializar_PID(self):

        # Inicialización de error
        self.h_1 = self.alturas['H1'].get_value()
        self.h_2 = self.alturas['H2'].get_value()
        self.err = {1: self.h_ref_1 - self.h_1, 2: self.h_ref_2 - self.h_2}
        self.err_1 = {1: 0, 2: 0}
        self.err_2 = {1: 0, 2: 0}
        self.err_3 = {1: 0, 2: 0}

        self.v_i_1 = {1: 0, 2: 0}
        self.v_i_2 = {1: 0, 2: 0}


        self.valvula_dict = {'v_1': self.valvulas['valvula1'], 'v_2': self.valvulas['valvula2']}

    def actualizar_PID_con_filtro(self):
        a = 1*3.1416*1
        b = exp(-a)

        print(f"kp: {self.kp[1]}, ki: {self.ki[1]}, kd: {self.kd}")

        self.err_3 = self.err_2
        self.err_2 = self.err_1
        self.err_1 = self.err

        self.h_1 = self.alturas['H1'].get_value()
        self.h_2 = self.alturas['H2'].get_value()
        self.err = {1: self.h_ref_1 - self.h_1, 2: self.h_ref_2 - self.h_2}

        self.v_i_2 = self.v_i_1

        for i in {1, 2}:
            v_i = self.valvula_dict[f"v_{i}"].get_value()

            self.v_i_1[i] = v_i

            nuevo_valor = (1-b)*self.v_i_1[i] - b*self.v_i_2[i] + (self.kp[i]+self.ki[i])*self.err[i]
            nuevo_valor += (-(1-b)*self.kp[i] - b*self.ki[i] + (1-b)/a*self.kd[i])*self.err_1[i]
            nuevo_valor += (self.kp[i]*b - 2*self.kd[i]*(1-b)/a)*self.err_2[i] + self.kd[i]*(1-b)/a*self.err_3[i]

            if nuevo_valor > 1:
                nuevo_valor = 1
            elif nuevo_valor < 0:
                nuevo_valor = 0
            self.valvula_dict[f"v_{i}"].set_value(nuevo_valor)




    def actualizar_PID(self):
        self.err_2 = self.err_1
        self.err_1 = self.err

        self.h_1 = self.alturas['H1'].get_value()
        self.h_2 = self.alturas['H2'].get_value()
        self.err = {1: self.h_ref_1 - self.h_1, 2: self.h_ref_2 - self.h_2}

        # print(err, err_1, err_2)

        for i in {1, 2}:
            '''
            # Anti wind-up
            limit = 2
            factor = 1
            if -limit < self.err[i] < limit:
                factor = self.err[i]/limit

            '''
            v_i = self.valvula_dict[f"v_{i}"].get_value()
            # nuevo_valor = v_i + (self.kp[i] + self.ki[i]*factor + self.kd[i])*self.err[i] - (self.kp[i] + 2*self.kd[i])*self.err_1[i] + self.kd[i]*self.err_2[i]
            nuevo_valor = v_i + (self.kp[i] + self.ki[i] + self.kd[i])*self.err[i] - (self.kp[i] + 2*self.kd[i])*self.err_1[i] + self.kd[i]*self.err_2[i]


            if nuevo_valor > 1:
                nuevo_valor = 1
            elif nuevo_valor < 0:
                nuevo_valor = 0
            self.valvula_dict[f"v_{i}"].set_value(nuevo_valor)


    def Instanciacion(self):
        self.root = self.client.get_root_node()
        self.objects = self.client.get_objects_node()
        self.Tanques = self.objects.get_child(['2:Proceso_Tanques','2:Tanques'])
        self.Valvulas = self.objects.get_child(['2:Proceso_Tanques', '2:Valvulas'])
        self.Razones = self.objects.get_child(['2:Proceso_Tanques', '2:Razones'])


        # Obtención de las alturas
        self.alturas['H1'] = self.Tanques.get_child(['2:Tanque1', '2:h'])
        self.alturas['H2'] = self.Tanques.get_child(['2:Tanque2', '2:h'])
        self.alturas['H3'] = self.Tanques.get_child(['2:Tanque3', '2:h'])
        self.alturas['H4'] = self.Tanques.get_child(['2:Tanque4', '2:h'])

        # Obtención de temperaturas
        self.temperaturas['T1'] = self.Tanques.get_child(['2:Tanque1', '2:T'])
        self.temperaturas['T2'] = self.Tanques.get_child(['2:Tanque2', '2:T'])
        self.temperaturas['T3'] = self.Tanques.get_child(['2:Tanque3', '2:T'])
        self.temperaturas['T4'] = self.Tanques.get_child(['2:Tanque4', '2:T'])

        # Obtención de los pumps
        self.valvulas['valvula1'] = self.Valvulas.get_child(['2:Valvula1', '2:u'])
        self.valvulas['valvula2'] = self.Valvulas.get_child(['2:Valvula2', '2:u'])

        # Obtención de los switches
        self.razones['razon1'] = self.Razones.get_child(['2:Razon1', '2:gamma'])
        self.razones['razon2'] = self.Razones.get_child(['2:Razon2', '2:gamma'])

        # Evento (alarma en este caso)
        if self.subscribir_eventos:
            self.myevent = self.root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:Alarma_nivel"])#Tipo de evento
            self.obj_event = self.objects.get_child(['2:Proceso_Tanques', '2:Alarmas', '2:Alarma_nivel'])#Objeto Evento
            self.handler_event = self.SubHandlerClass()
            self.sub_event = self.client.create_subscription(self.periodo, self.handler_event)#Subscripción al evento
            self.handle_event = self.sub_event.subscribe_events(self.obj_event, self.myevent)


    def subscribir_cv(self): # Subscripción a las variables controladas
        self.handler_cv = self.SubHandlerClass()
        self.sub_cv = self.client.create_subscription(self.periodo, self.handler_cv)
        for key, var in self.alturas.items():
            self.sub_cv.subscribe_data_change(var)
        for key, var in self.temperaturas.items():
            self.sub_cv.subscribe_data_change(var)


    def subscribir_mv(self): # Subscripación a las variables manipuladas
        self.handler_mv = self.SubHandlerClass()
        self.sub_mv = self.client.create_subscription(self.periodo, self.handler_mv)
        for key, var in self.valvulas.items():
            self.sub_mv.subscribe_data_change(var)
        for key, var in self.razones.items():
            self.sub_mv.subscribe_data_change(var)


    def conectar(self):
        try:
            self.client.connect()
            self.objects = self.client.get_objects_node()
            print('Cliente OPCUA se ha conectado')
            self.Instanciacion()

        except:
            self.client.disconnect()
            print('Cliente no se ha podido conectar')


'''
cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
cliente.conectar()
cliente.subscribir_mv() # Se subscribe a las variables manipuladas
cliente.subscribir_cv() # Se subscribe a las variables controladas

#cliente.razones['razon2'].set_value(0.5)

cliente.razones['razon1'].set_value(1)
cliente.razones['razon2'].set_value(1)


cliente.inicializar_PID()
print("PID")
while(True):
    cliente.actualizar_PID()
'''
