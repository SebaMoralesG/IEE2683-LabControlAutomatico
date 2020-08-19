from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models import ColumnDataSource, PreText, Panel, Tabs
from bokeh.layouts import layout
from user import Cliente, SubHandler
import random


class GUI():

    def __init__(self):

        self.cliente = Cliente("opc.tcp://localhost:4840/freeopcua/server/", suscribir_eventos=True, SubHandler=SubHandler)
        self.DataSource = ColumnDataSource(dict(time=[],H1=[],H2=[],H3=[],H4=[]))    # ,V1=[],V2=[]
        self.fig_H1 = figure(title = 'Altura Estanque H1', plot_width = 500, plot_height = 300, tools = "box_select,box_zoom,tap,undo,redo,reset,save",y_axis_location="left")
        self.fig_H2 = figure(title = 'Altura Estanque H2', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_H3 = figure(title = 'Altura Estanque H3', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.fig_H4 = figure(title = 'Altura Estanque H4', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
        self.cuadro_texto = {'color' : 'white', 'font' : '15px bold arial, sans-serif', 'background-color' : 'green', 'text-align ' : 'center', 'border-radius' : '7px'}
        self.H1_text = PreText(text='Valor actual H1: 0.00',width = 600, style = self.cuadro_texto)
        self.H2_text = PreText(text='Valor actual H2: 0.00',width = 600, style = self.cuadro_texto)
        self.H4_text = PreText(text='Valor actual H4: 0.00',width = 600, style = self.cuadro_texto)
        self.H3_text = PreText(text='Valor actual H3: 0.00',width = 600, style = self.cuadro_texto)


        self.fig_H1.line(x='time',y='H1', alpha= 0.8, line_width = 3, color = 'green', source = self.DataSource)
        self.fig_H2.line(x='time',y='H2', alpha= 0.8, line_width = 3, color = 'red', source = self.DataSource)
        self.fig_H3.line(x='time',y='H3', alpha= 0.8, line_width = 3, color = 'blue', source = self.DataSource)
        self.fig_H4.line(x='time',y='H4', alpha= 0.8, line_width = 3, color = 'brown', source = self.DataSource)

        self.t = 0
        self.l = layout([[self.fig_H1,self.fig_H2],[self.H1_text,self.H2_text],
            [self.fig_H3,self.fig_H4],[self.H3_text,self.H4_text],[self.fig_V1,self.fig_V2],[self.V1_text,self.V2_text]
            ])              # [fig_V1,fig_V2],[V1_text,V2_text]
        self.of = output_file('home.html')

    def GUI_update_client(self):        # , H1_c, H2_c, H3_c, H4_c
        # global t, H1_client, H2_client, H3_client, H4_client
        # global cliente.
        H1_client = round(self.cliente.alturas['H1'].get_value(),2)
        H2_client = round(self.cliente.alturas['H2'].get_value(),2)
        H3_client = round(self.cliente.alturas['H3'].get_value(),2)
        H4_client = round(self.cliente.alturas['H4'].get_value(),2)
        update = dict(time=[self.t],H1=[H1_client],H2=[H2_client],H3=[H3_client],H4=[H4_client])         # ,V1=[V1],V2=[V2]
        self.DataSource.stream(new_data = update, rollover = 100)
        self.H1_text.text = 'Valor actual H1: {}'.format(H1_client)
        self.H2_text.text = 'Valor actual H2: {}'.format(H2_client)
        self.H3_text.text = 'Valor actual H3: {}'.format(H3_client)
        self.H4_text.text = 'Valor actual H4: {}'.format(H4_client)

        self.V1_text.text = 'Valor actual V1: {}'.format(V1)
        self.V2_text.text = 'Valor actual V2: {}'.format(V2)
        self.t += 1



gui = GUI()
curdoc().add_root(gui.l)
curdoc().title = "GUI Client"
gui.cliente.conectar()
curdoc().add_periodic_callback(gui.GUI_update_client,100)



################################################################################333
# Figuras Estasnques
# fig_H1 = figure(title = 'Altura Estanque H1', plot_width = 500, plot_height = 300, tools = "box_select,box_zoom,tap,undo,redo,reset,save",y_axis_location="left")
# fig_H2 = figure(title = 'Altura Estanque H2', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
# fig_H3 = figure(title = 'Altura Estanque H3', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
# fig_H4 = figure(title = 'Altura Estanque H4', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")

# fig_H1.line(x='time',y='H1', alpha= 0.8, line_width = 3, color = 'green', source = DataSource)
# fig_H2.line(x='time',y='H2', alpha= 0.8, line_width = 3, color = 'red', source = DataSource)
# fig_H3.line(x='time',y='H3', alpha= 0.8, line_width = 3, color = 'blue', source = DataSource)
# fig_H4.line(x='time',y='H4', alpha= 0.8, line_width = 3, color = 'brown', source = DataSource)

# Figuras Valvulas
# fig_V1 = figure(title = 'Apertura valvula V1', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")
# fig_V2 = figure(title = 'Apertura valvula V2', plot_width = 500, plot_height = 300,tools = "box_select,box_zoom,tap,undo,redo,reset,save", y_axis_location="left")

# fig_V1.line(x='time',y='V1', alpha= 0.8, line_width = 3, color = 'orange', source = DataSource)
# fig_V2.line(x='time',y='V2', alpha= 0.8, line_width = 3, color = 'black', source = DataSource)

# Texto figuras valor actual
# cuadro_texto = {'color' : 'white', 'font' : '15px bold arial, sans-serif', 'background-color' : 'green', 'text-align ' : 'center', 'border-radius' : '7px'}
# H1_text = PreText(text='Valor actual H1: 0.00',width = 600, style = cuadro_texto)
# H2_text = PreText(text='Valor actual H2: 0.00',width = 600, style = cuadro_texto)
# H3_text = PreText(text='Valor actual H3: 0.00',width = 600, style = cuadro_texto)
# H4_text = PreText(text='Valor actual H4: 0.00',width = 600, style = cuadro_texto)
# V1_text = PreText(text='Valor actual V1: 0.00',width = 600, style = cuadro_texto)
# V2_text = PreText(text='Valor actual V2: 0.00',width = 600, style = cuadro_texto)
