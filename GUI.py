from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models import ColumnDataSource, PreText, Slider, RadioGroup, Toggle, RadioButtonGroup
from bokeh.layouts import layout
from user_2 import Cliente, SubHandler
from bokeh.models.callbacks import CustomJS
import random



class GUI():

    def __init__(self):
        # init cliente
        self.cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)

        # Init datos para graficos
        self.DataSource = ColumnDataSource(dict(time=[],H1=[],H2=[],H3=[],H4=[],V1=[],V2=[],g1=[],g2=[],Hr1=[],Hr2=[]))

        # init figuras estanques y voltajes
        self.fig_H1 = figure(title = 'Altura Estanque H1', plot_width = 500, plot_height = 300, tools = "box_select,box_zoom,tap,undo,redo,reset,save",y_axis_location="left")
        self.fig_H2 = figure(title = 'Altura Estanque H2', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_H3 = figure(title = 'Altura Estanque H3', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_H4 = figure(title = 'Altura Estanque H4', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_V1 = figure(title = 'Voltaje aplicado valvula 1', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_V2 = figure(title = 'Voltaje aplicado valvula 2', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_H1.line(x='time',y='H1', alpha= 0.8, line_width = 3, color = 'green', source = self.DataSource)
        self.fig_H2.line(x='time',y='H2', alpha= 0.8, line_width = 3, color = 'red', source = self.DataSource)
        self.fig_H3.line(x='time',y='H3', alpha= 0.8, line_width = 3, color = 'blue', source = self.DataSource)
        self.fig_H4.line(x='time',y='H4', alpha= 0.8, line_width = 3, color = 'brown', source = self.DataSource)
        self.fig_V1.line(x='time',y='V1', alpha= 0.8, line_width = 3, color = 'grey', source = self.DataSource)
        self.fig_V2.line(x='time',y='V2', alpha= 0.8, line_width = 3, color = 'purple', source = self.DataSource)
        self.Hr1_visible = self.fig_H1.line(x='time',y='Hr1',alpha= 0.8, line_width = 3, color = 'orange', source = self.DataSource)
        self.Hr2_visible = self.fig_H2.line(x='time',y='Hr2',alpha= 0.8, line_width = 3, color = 'orange', source = self.DataSource)

        # init estilo textos
        self.cuadro_texto = {'color' : 'white', 'font' : '15px bold arial, sans-serif', 'background-color' : 'green', 'text-align ' : 'center', 'border-radius' : '7px'}
        self.cuadro_alarma = {'color' : 'white', 'font' : '15px bold arial, sans-serif', 'background-color' : 'red', 'text-align ' : 'center', 'border-radius' : '7px'}
        self.cuadro_blanco = {'color' : 'white', 'font' : '15px bold arial, sans-serif', 'background-color' : 'white', 'text-align ' : 'center', 'border-radius' : '7px'}
        self.cuadro_titulo = {'color' : 'white', 'font' : '20px bold arial, sans-serif', 'background-color' : 'blue', 'text-align ' : 'center', 'border-radius' : '7px'}
        self.cuadro_titulo1 = {'color' : 'white', 'font' : '20px bold arial, sans-serif', 'background-color' : 'white', 'text-align ' : 'center', 'border-radius' : '7px'}

        # init textos titulos y alturas
        self.titulo = PreText(text = '                                  Monitor usuario                                  ', width = 600,style = self.cuadro_titulo)
        self.H1_text = PreText(text='Valor actual H1: 0.00',width = 600, style = self.cuadro_texto)
        self.H2_text = PreText(text='Valor actual H2: 0.00',width = 600, style = self.cuadro_texto)
        self.H4_text = PreText(text='Valor actual H4: 0.00',width = 600, style = self.cuadro_texto)
        self.H3_text = PreText(text='Valor actual H3: 0.00',width = 600, style = self.cuadro_texto)
        self.V1_text = PreText(text='Valor actual V 1: 0.00',width = 600, style = self.cuadro_texto)
        self.V2_text = PreText(text='Valor actual V 2: 0.00',width = 600, style = self.cuadro_texto)

        # Widgets y textos
        self.sl_V1 = Slider(start = 0,end = 1,value = 0, step = 0.01, title = "Voltaje valvula 1")
        self.sl_V2 = Slider(start = 0,end = 1,value = 0, step = 0.01, title = "Voltaje valvula 2")
        self.sl_G1 = Slider(start = 0,end = 1,value = 0, step = 0.01, title = "Razón de flujo valvula 1")
        self.sl_G2 = Slider(start = 0,end = 1,value = 0, step = 0.01, title = "Razón de flujo valvula 2")
        self.sl_P = Slider(start = 0, end = 5, value = 0,step = 0.1, title = "Ganancia Proporcional")
        self.sl_I = Slider(start = 0, end = 5, value = 0,step = 0.1, title = "Ganancia Integral")
        self.sl_D = Slider(start = 0, end = 5, value = 0,step = 0.1, title = "Ganancia Derivativa")
        # self.sl_G1_text = PreText(text='Valor actual Razón de flujo 1: 0.00',width = 600, style = self.cuadro_texto)
        # self.sl_G2_text = PreText(text='Valor actual Razón de flujo 2: 0.00',width = 600, style = self.cuadro_texto)
         # boton modo
        self.slct_mode = RadioGroup(labels=["Modo Manual","Modo Automático"],active = 0)
        self.toggle_datos = Toggle(label="Guardar datos", button_type="success", active=True)
        self.alarm_button = RadioButtonGroup(labels = ["Alarma activada","Alarma desactivada"], active = 1 )
        self.extencion_datos = RadioButtonGroup(labels = ["txt","csv"], active = 0 )
        # self.toggle_datos.js_link('active',self.boolean_toggle)
        self.mode_anterior = True
        self.boolean_toggle = True



        # tiempo entregado en grafico y ref alturas
        self.t = 0
        self.Hr1 = 0
        self.Hr2 = 0
        self.P = 0
        self.I = 0
        self.D = 0

        # Layout navegador
        self.l = layout([[self.titulo],[self.slct_mode,self.alarm_button],
            [self.fig_H1,self.fig_H2],[self.H1_text,self.H2_text],
            [self.fig_H3,self.fig_H4],[self.H3_text,self.H4_text],
            [self.fig_V1,self.fig_V2],[self.V1_text,self.V2_text],
            [self.sl_V1,self.sl_V2],[self.sl_G1,self.sl_G2],
            [self.sl_P,self.sl_I,self.sl_D],[self.toggle_datos,self.extencion_datos]])

    def GUI_update_client(self):
        # se indica si activa alarma
        self.GUI_alarm()
        if (self.toggle_datos.active == False) and (self.boolean_toggle == True):
            self.toggle_datos.label = "Dejar de guardar datos"
            self.file = open("localdata.{}".format(self.extencion_datos.labels[self.extencion_datos.active]),"w")
            self.file.write("H1,H2,H3,H4,H_ref1,H_ref2,V1,V2,kp,ki,kd,gamma_1,gamma_2,\n")
            self.boolean_toggle = False
        elif (self.toggle_datos.active == True) and (self.boolean_toggle == False):
            self.file.close()
            self.boolean_toggle = True
            self.toggle_datos.label = "Guardar datos"
        elif (self.toggle_datos.active == False) and (self.boolean_toggle == False):
            self.data_saver()


        # Obtencion datos alturas y valvulas
        H1_client = self.cliente.alturas['H1'].get_value()
        H2_client = self.cliente.alturas['H2'].get_value()
        H3_client = self.cliente.alturas['H3'].get_value()
        H4_client = self.cliente.alturas['H4'].get_value()
        V1_client = self.cliente.valvulas['valvula1'].get_value()
        V2_client = self.cliente.valvulas['valvula2'].get_value()

        r1 = round(self.sl_G1.value,1)
        self.cliente.razones['razon1'].set_value(r1)
        r2 = round(self.sl_G2.value,1)
        self.cliente.razones['razon2'].set_value(r2)

        # se actualiza diccionario
        update = dict(time=[self.t],H1=[H1_client],H2=[H2_client],
            H3=[H3_client],H4=[H4_client],V1=[V1_client],V2=[V2_client],g1=[r1],g2=[r2],Hr1=[self.Hr1],Hr2=[self.Hr2])
        self.DataSource.stream(new_data = update, rollover = 100)
        self.GUI_mode()

        # Se actualiza textos
        self.H1_text.text = 'Valor actual H1: {}'.format(round(H1_client,2))
        self.H2_text.text = 'Valor actual H2: {}'.format(round(H2_client,2))
        self.H3_text.text = 'Valor actual H3: {}'.format(round(H3_client,2))
        self.H4_text.text = 'Valor actual H4: {}'.format(round(H4_client,2))
        self.V1_text.text = 'Valor actual V1: {}'.format(round(V1_client,2))
        self.V2_text.text = 'Valor actual V2: {}'.format(round(V2_client,2))

        self.t += 1

    def GUI_alarm(self):
        if (self.cliente.alturas['H1'].get_value() < 10) and (self.alarm_button.active == 0):
            self.H1_text.style = self.cuadro_alarma
        else:
            self.H1_text.style = self.cuadro_texto
        if self.cliente.alturas['H2'].get_value() < 10 and (self.alarm_button.active == 0):
            self.H2_text.style = self.cuadro_alarma
        else:
            self.H2_text.style = self.cuadro_texto
        if self.cliente.alturas['H3'].get_value() < 10 and (self.alarm_button.active == 0):
            self.H3_text.style = self.cuadro_alarma
        else:
            self.H3_text.style = self.cuadro_texto
        if self.cliente.alturas['H4'].get_value() < 10 and (self.alarm_button.active == 0):
            self.H4_text.style = self.cuadro_alarma
        else:
            self.H4_text.style = self.cuadro_texto

    def GUI_mode(self):
        if self.slct_mode.active == 0:
            # Modo manual
            self.slider_logic()
            self.mode_anterior = True
            self.Hr1_visible.visible = False
            self.Hr2_visible.visible = False
            V1_client = round(self.sl_V1.value,1)
            V2_client = round(self.sl_V2.value,1)
            self.cliente.valvulas['valvula1'].set_value(V1_client)
            self.cliente.valvulas['valvula2'].set_value(V2_client)
            self.sl_V1.title = "Voltaje Valvula 1"
            self.sl_V2.title = "Voltaje Valvula 2"
            self.sl_V1.start = 0
            self.sl_V1.end = 1
            self.sl_V2.start = 0
            self.sl_V2.end = 1
        else:
            # Modo Automatico
            if self.mode_anterior == True:
                self.cliente.inicializar_PID()
            self.mode_anterior = False
            self.slider_logic()
            self.Hr1_visible.visible = True
            self.Hr2_visible.visible = True
            self.sl_V1.title = "Referencia Altura 1"
            self.sl_V2.title = "Referencia Altura 2"
            ###  AQUI SE DEBEN ENTREGAR VALORES DE REFERENCIA PID
            self.sl_V1.start = 0
            self.sl_V1.end = 50
            self.sl_V2.start = 0
            self.sl_V2.end = 50
            self.Hr1 = self.sl_V1.value
            self.Hr2 = self.sl_V2.value
            self.P = self.sl_P.value
            self.I = self.sl_I.value
            self.D = self.sl_D.value
            self.cliente.kp[1] = self.P
            self.cliente.kp[2] = self.P
            self.cliente.ki[1] = self.I
            self.cliente.ki[2] = self.I
            self.cliente.kd[1] = self.D
            self.cliente.kd[2] = self.D
            self.cliente.h_ref_1 = self.Hr1
            self.cliente.h_ref_2 = self.Hr2
            self.cliente.actualizar_PID_con_filtro()

    def slider_logic(self):
        if self.slct_mode.active == 0:  # Modo Manual
            if self.sl_V1.value > 1:    # sobre limite voltaje 1
                self.sl_V1.value = 1
            if self.sl_V2.value > 1:    # sobre limite voltaje 2
                self.sl_V2.value = 1
        else:
            if self.sl_V1.value < 0:
                self.sl_V1.value = 0
            if self.sl_V2.value < 0:
                self.sl_V2.value = 0

    def data_saver(self):
        self.file.write(str(self.cliente.alturas['H1'].get_value()))
        self.file.write(",")
        self.file.write(str(self.cliente.alturas['H2'].get_value()))
        self.file.write(",")
        self.file.write(str(self.cliente.alturas['H3'].get_value()))
        self.file.write(",")
        self.file.write(str(self.cliente.alturas['H4'].get_value()))
        self.file.write(",")
        self.file.write(str(self.Hr1))
        self.file.write(",")
        self.file.write(str(self.Hr2))
        self.file.write(",")
        self.file.write(str(self.cliente.valvulas['valvula1'].get_value()))
        self.file.write(",")
        self.file.write(str(self.cliente.valvulas['valvula2'].get_value()))
        self.file.write(",")
        self.file.write(str(self.P))
        self.file.write(",")
        self.file.write(str(self.I))
        self.file.write(",")
        self.file.write(str(self.D))
        self.file.write(",")
        self.file.write(str(self.cliente.razones['razon1'].get_value()))
        self.file.write(",")
        self.file.write(str(self.cliente.razones['razon2'].get_value()))

        self.file.write(str(self.t))
        self.file.write("\n")












###################################################################  MAIN ##############################################################

gui = GUI()
curdoc().add_root(gui.l)
curdoc().title = "GUI Client"
gui.cliente.conectar()
curdoc().add_periodic_callback(gui.GUI_update_client,1000)
