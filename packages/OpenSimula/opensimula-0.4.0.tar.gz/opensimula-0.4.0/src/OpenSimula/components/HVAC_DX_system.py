from OpenSimula.Parameters import Parameter_component, Parameter_float, Parameter_variable_list, Parameter_math_exp, Parameter_options
from OpenSimula.Component import Component
from OpenSimula.Variable import Variable
from OpenSimula.Iterative_process import Iterative_process
import psychrolib as sicro


class HVAC_DX_system(Component):
    def __init__(self, name, project):
        Component.__init__(self, name, project)
        self.parameter("type").value = "HVAC_DX_system"
        self.parameter("description").value = "HVAC Direct Expansion system for time simulation"
        self.add_parameter(Parameter_component("equipment", "not_defined", ["HVAC_DX_equipment"]))
        self.add_parameter(Parameter_component("space", "not_defined", ["Space"])) # Space, TODO: Add Air_distribution, Energy_load
        self.add_parameter(Parameter_component("file_met", "not_defined", ["File_met"]))
        self.add_parameter(Parameter_float("supply_air_flow", 1, "m³/s", min=0))
        self.add_parameter(Parameter_math_exp("outdoor_air_flow", "0", "m³/s"))
        self.add_parameter(Parameter_variable_list("input_variables", []))
        self.add_parameter(Parameter_math_exp("heating_setpoint", "20", "°C"))
        self.add_parameter(Parameter_math_exp("cooling_setpoint", "25", "°C"))
        self.add_parameter(Parameter_math_exp("system_on_off", "1", "on/off"))
        self.add_parameter(Parameter_options("control_type", "PERFECT", ["PERFECT", "TEMPERATURE"]))
        self.add_parameter(Parameter_float("cooling_bandwidth", 1, "ºC", min=0))
        self.add_parameter(Parameter_float("heating_bandwidth", 1, "ºC", min=0))
        self.add_parameter(Parameter_options("economizer", "NO", ["NO", "TEMPERATURE","TEMPERATURE_NOT_INTEGRATED","ENTHALPY","ENTHALPY_LIMITED"]))
        self.add_parameter(Parameter_float("economizer_DT", 0, "ºC", min=0))
        self.add_parameter(Parameter_float("economizer_enthalpy_limit", 0, "kJ/kg", min=0))
        
        # Variables
        self.add_variable(Variable("state", unit="flag")) # 0: 0ff, 1: Heating, 2: Heating max cap, -1:Cooling, -2:Cooling max cap, 3: Venting 
        self.add_variable(Variable("T_odb", unit="°C"))
        self.add_variable(Variable("T_owb", unit="°C"))
        self.add_variable(Variable("T_idb", unit="°C"))
        self.add_variable(Variable("T_iwb", unit="°C"))
        self.add_variable(Variable("F_air", unit="frac"))
        self.add_variable(Variable("F_load", unit="frac"))
        self.add_variable(Variable("outdoor_air_flow", unit="m³/s"))
        self.add_variable(Variable("T_supply", unit="°C"))
        self.add_variable(Variable("w_supply", unit="°C"))
        self.add_variable(Variable("Q_sensible", unit="W"))
        self.add_variable(Variable("Q_latent", unit="W"))
        self.add_variable(Variable("power", unit="W"))
        self.add_variable(Variable("heating_setpoint", unit="°C"))
        self.add_variable(Variable("cooling_setpoint", unit="°C"))
        self.add_variable(Variable("EER", unit="frac"))
        self.add_variable(Variable("COP", unit="frac"))
        self.add_variable(Variable("efficiency_degradation", unit="frac"))


         # Sicro
        sicro.SetUnitSystem(sicro.SI)
        self.CP_A = 1007 # (J/kg·K)
        self.DH_W = 2501 # (J/g H20)

    def check(self):
        errors = super().check()
        # Test equipment defined
        if self.parameter("equipment").value == "not_defined":
            errors.append(
                f"Error: {self.parameter('name').value}, must define its equipment.")
        # Test space defined
        if self.parameter("space").value == "not_defined":
            errors.append(
                f"Error: {self.parameter('name').value}, must define its space.")
        # Test file_met defined
        if self.parameter("file_met").value == "not_defined":
            errors.append(
                f"Error: {self.parameter('name').value}, file_met must be defined.")
        # Test enthalpy economizer not compatible with temperature control type
        if (self.parameter("economizer").value == "ENTHALPY" or self.parameter("economizer").value == "ENTHALPY_LIMITED") and self.parameter("control_type").value == "TEMPERATURE":
            errors.append(
                f"Error: {self.parameter('name').value}, enthalpy economizer not compatible with temperature control type. control typed changed to PERFECT.")
            self.parameter("control_type").value = "PERFECT"
        return errors

    def pre_simulation(self, n_time_steps, delta_t):
        super().pre_simulation(n_time_steps, delta_t)
        self._equipment = self.parameter("equipment").component
        self._space = self.parameter("space").component
        self._file_met = self.parameter("file_met").component
        self._supply_air_flow = self.parameter("supply_air_flow").value
        self._f_air = self._supply_air_flow / self._equipment.parameter("nominal_air_flow").value
        self.ATM_PRESSURE = sicro.GetStandardAtmPressure(self._file_met.altitude)
        self.RHO_A = sicro.GetMoistAirDensity(20,0.0073,self.ATM_PRESSURE)
        self._m_supply =  self.RHO_A * self._supply_air_flow # V_imp * rho 
        self._mrcp =  self.RHO_A * self._supply_air_flow * self.CP_A # V_imp * rho * c_p
        self._mrdh =  self.RHO_A * self._supply_air_flow * self.DH_W # V_imp * rho * Dh
        self._cool_band = self.parameter("cooling_bandwidth").value
        self._heat_band = self.parameter("heating_bandwidth").value
        # input_varibles symbol and variable
        self.input_var_symbol = []
        self.input_var_variable = []
        for i in range(len(self.parameter("input_variables").variable)):
            self.input_var_symbol.append(
                self.parameter("input_variables").symbol[i])
            self.input_var_variable.append(
                self.parameter("input_variables").variable[i])
        self._f_load = 0
        
        self._no_load_power = self._equipment.get_no_load_power()
        self._economizer = self.parameter("economizer").value != "NO"
        self._economizer_DT = self.parameter("economizer_DT").value

    def pre_iteration(self, time_index, date, daylight_saving):
        super().pre_iteration(time_index, date, daylight_saving)
        # Outdoor air
        self._T_odb = self._file_met.variable("temperature").values[time_index]
        self._T_owb = self._file_met.variable("wet_bulb_temp").values[time_index]
        self._w_o = self._file_met.variable("abs_humidity").values[time_index]
        self.variable("T_odb").values[time_index] = self._T_odb
        self.variable("T_owb").values[time_index] = self._T_owb
        # Control
        # variables dictonary
        var_dic = {}
        for i in range(len(self.input_var_symbol)):
            var_dic[self.input_var_symbol[i]] = self.input_var_variable[i].values[time_index]

        # outdoor air flow
        self._outdoor_air_flow = self.parameter("outdoor_air_flow").evaluate(var_dic)
        self.variable("outdoor_air_flow").values[time_index] = self._outdoor_air_flow
        self._f_oa = self._outdoor_air_flow/self._supply_air_flow

        # setpoints
        self._T_heat_sp = self.parameter("heating_setpoint").evaluate(var_dic)
        self.variable("heating_setpoint").values[time_index] = self._T_heat_sp
        self._T_cool_sp = self.parameter("cooling_setpoint").evaluate(var_dic)
        self.variable("cooling_setpoint").values[time_index] = self._T_cool_sp
        # on/off
        self._on_off = self.parameter("system_on_off").evaluate(var_dic)
        if self._on_off == 0:
            self._state = 0
            self.variable("state").values[time_index] = 0
            self._on_off = False
        else:
            self._on_off = True
        #self._f_load_pre = self._f_load

        # Add uncontrolled ventilation to the space
        if self._on_off:
            system_dic = {"name": self.parameter("name").value, 
                          "V": self._outdoor_air_flow, 
                          "T":self._T_odb, 
                          "w": self._w_o, 
                          "Q":self._no_load_power,
                          "M": 0}
            self._space.add_uncontrol_system(system_dic)
            # Iterative Process for outdoor air fraction with economizer
            self.itera_Foa = Iterative_process(self._outdoor_air_flow/self._supply_air_flow,tol=0.01,n_ini_relax=3,rel_vel=0.8)

    
    def iteration(self, time_index, date, daylight_saving, n_iter):
        super().iteration(time_index, date, daylight_saving, n_iter)
        control = {"V": 0, "T": 0, "w":0, "Q":0, "M":0 }
        if self._on_off:
            self._T_space = self._space.variable("temperature").values[time_index]
            self._w_space = self._space.variable("abs_humidity").values[time_index]
            if self.parameter("control_type").value == "PERFECT":
                control= self._perfect_control(n_iter)    
            elif self.parameter("control_type").value == "TEMPERATURE":
                control = self._air_temperature_control(n_iter)
        self._space.set_control_system(control)
        
         # Test convergence
        if self._on_off and self.parameter("control_type").value == "TEMPERATURE" and self._economizer:
            return self.itera_Foa.converged()
        else:
            return True

    def _mix_air(self, f, T1, w1, T2, w2):
        T = f * T1 + (1-f)*T2
        w = f * w1 + (1-f)*w2
        if (T > 100):
            T_wb = 50 # Inventado
        else:
            T_wb = sicro.GetTWetBulbFromHumRatio(T,w/1000,self.ATM_PRESSURE)
        return (T,w,T_wb)        
    
    def _perfect_control(self, n_iter):
        # Venting
        state = 3
        f_load = 0
        Q_sen = 0
        M_w = 0
        
        # Economizer
        Q_required = self._economizer_perfect()

        # Mix air
        self._T_idb, self._w_i, self._T_iwb = self._mix_air(self._f_oa, self._T_odb, self._w_o, self._T_space, self._w_space)

        if Q_required > 0: # Heating    
            heat_cap = self._equipment.get_heating_capacity(self._T_idb, self._T_iwb, self._T_odb, self._T_owb,self._f_air)
            if heat_cap > 0:
                if Q_required > heat_cap:
                    state = 1
                    Q_sen = heat_cap
                    f_load = 1
                else:
                    state = 2
                    Q_sen = Q_required
                    f_load = Q_sen/heat_cap
        elif Q_required < 0: # Cooling
            tot_cool_cap, sen_cool_cap = self._equipment.get_cooling_capacity(self._T_idb, self._T_iwb, self._T_odb,self._T_owb,self._f_air)
            if sen_cool_cap > 0:
                if -Q_required > sen_cool_cap:
                    state = -2
                    Q_sen = -sen_cool_cap
                    Q_tot = -tot_cool_cap
                    f_load = -1
                else:
                    state = -1
                    Q_sen = Q_required  
                    f_load = Q_sen/sen_cool_cap                     
                    Q_tot = tot_cool_cap*f_load
                M_w = (Q_tot - Q_sen) / self.DH_W
        # relaxing coef        
        #r_coef = (0.01-self._r_coef)/self._n_max_iter * n_iter + self._r_coef
        #self._M_w = r_coef * M_w + (1-r_coef)*self._M_w_pre # Always relaxing
        #self._Q_sen = r_coef * Q_sen + (1-r_coef)*self._Q_sen_pre
        #self._f_load = r_coef * f_load + (1-r_coef)*self._f_load_pre
        #self._state = state
        #self._M_w_pre = self._M_w
        #self._Q_sen_pre = self._Q_sen
        #self._f_load_pre = self._f_load

        self._state = state
        self._Q_sen = Q_sen
        self._M_w = M_w
        self._f_load = f_load

        control = {"V": 0, "T": 0, "w":0, "Q":self._Q_sen, "M":self._M_w }
        return control    
    
    def _economizer_perfect(self): 
        Q_required = self._space.get_Q_required(self._T_cool_sp, self._T_heat_sp)
        if (self._economizer):
            if (self.parameter("economizer").value == "TEMPERATURE" or self.parameter("economizer").value == "TEMPERATURE_NOT_INTEGRATED"):
                use_economizer = self._T_odb < self._T_space-self._economizer_DT
            elif (self.parameter("economizer").value == "ENTHALPY"):
                h_odb = sicro.GetMoistAirEnthalpy(self._T_odb,self._w_o/1000)
                h_space = sicro.GetMoistAirEnthalpy(self._T_space,self._w_space/1000)
                use_economizer = h_odb < h_space
            elif (self.parameter("economizer").value == "ENTHALPY_LIMITED"):
                h_odb = sicro.GetMoistAirEnthalpy(self._T_odb,self._w_o/1000)
                use_economizer = h_odb < self.parameter("economizer_enthalpy_limit").value * 1000
            if (Q_required < 0 and use_economizer):
                Q_rest_ae = self._mrcp * (1-self._f_oa)*(self._T_odb - self._T_space)
                if  Q_rest_ae < Q_required:
                    self._f_oa += Q_required/(self._mrcp*(self._T_odb-self._T_space))
                    Q_required = 0
                else:        
                    if (self.parameter("economizer").value == "TEMPERATURE_NOT_INTEGRATED"):
                        self._f_oa = self._outdoor_air_flow/self._supply_air_flow
                    elif (self.parameter("economizer").value == "TEMPERATURE"):
                        self._f_oa = 1
            else:
                self._f_oa = self._outdoor_air_flow/self._supply_air_flow
            system_dic = {"name": self.parameter("name").value, 
                                  "V": self._supply_air_flow*self._f_oa, 
                                "T":self._T_odb, 
                                "w": self._w_o, 
                                "Q":self._no_load_power,
                            "M": 0}
            self._space.add_uncontrol_system(system_dic)
            Q_required = self._space.get_Q_required(self._T_cool_sp, self._T_heat_sp)
        return Q_required

            
    def _air_temperature_control(self, n_iter):
    
        # Venting
        state = 3
        f_load = 0
        Q_sen = 0
        M_w = 0

        # Economizer
        T_flo, K_tot, F_tot = self._economizer_temperature()

        # Mix air
        self._T_idb, self._w_i, self._T_iwb = self._mix_air(self._f_oa, self._T_odb, self._w_o, self._T_space, self._w_space)

        if (T_flo >= self._T_cool_sp - self._cool_band/2):
            tot_cool_cap, sen_cool_cap = self._equipment.get_cooling_capacity(self._T_idb, self._T_iwb, self._T_odb,self._T_owb, self._f_air)
            if sen_cool_cap > 0:
                T_max_cap = (F_tot - sen_cool_cap) / K_tot
                if T_max_cap > self._T_cool_sp + self._cool_band/2:
                    state = -2
                    f_load = -1 
                    Q_sen = -sen_cool_cap
                else:
                    state = -1
                    T_c = (F_tot+sen_cool_cap*(self._T_cool_sp - self._cool_band/2)/self._cool_band)/(K_tot + sen_cool_cap /self._cool_band)
                    Q_sen = K_tot * T_c - F_tot
                    f_load = Q_sen / sen_cool_cap
                Q_tot = tot_cool_cap * f_load 
                M_w = ( Q_tot - Q_sen) / self.DH_W  
        elif (T_flo <= self._T_heat_sp + self._heat_band/2):
            heat_cap = self._equipment.get_heating_capacity(self._T_idb, self._T_iwb, self._T_odb, self._T_owb,self._f_air)
            if heat_cap > 0:
                T_max_cap = (F_tot + heat_cap) / K_tot
                M_w = 0
                if T_max_cap < self._T_heat_sp - self._heat_band/2:
                    state = 2
                    f_load = 1 
                    Q_sen = heat_cap
                else:
                    T_c = (F_tot+heat_cap*(self._T_heat_sp + self._heat_band/2)/self._heat_band)/(K_tot + heat_cap /self._heat_band)
                    Q_sen = K_tot * T_c - F_tot
                    f_load = Q_sen / heat_cap
                    state = 1

        # relaxing coef        
        #r_coef = (0.01-self._r_coef)/self._n_max_iter * n_iter + self._r_coef
        #self._M_w = r_coef * M_w + (1-r_coef)*self._M_w_pre
        #self._Q_sen = r_coef * Q_sen + (1-r_coef)*self._Q_sen_pre
        #self._f_load = r_coef * f_load + (1-r_coef)*self._f_load_pre
        #self._state = state
        #self._M_w_pre = self._M_w
        #self._Q_sen_pre = self._Q_sen
        #self._f_load_pre = self._f_load
     
        self._state = state
        self._Q_sen = Q_sen
        self._M_w = M_w
        self._f_load = f_load

        control = {"V": 0, "T": 0, "w":0, "Q":self._Q_sen, "M":self._M_w }
        return control    

    def _economizer_temperature(self): 
        K_tot, F_tot =  self._space._calculate_K_F_tot(False) # Space Equation
        T_flo = F_tot/K_tot   
        if (self._economizer):
            if (self._T_odb < self._T_space - self._economizer_DT):
                if (T_flo >= self._T_cool_sp - 1.5*self._cool_band and T_flo < self._T_cool_sp - 0.5*self._cool_band ):
                    f_oa_min = self._outdoor_air_flow/self._supply_air_flow
                    T_min = self._T_cool_sp - 1.5*self._cool_band
                    f_oa = (T_flo - T_min)/self._cool_band*(1-f_oa_min) + f_oa_min
                elif (T_flo >= self._T_cool_sp - 0.5*self._cool_band):
                    if (self.parameter("economizer").value == "TEMPERATURE_NOT_INTEGRATED"):
                        f_oa = self._outdoor_air_flow/self._supply_air_flow
                    elif (self.parameter("economizer").value == "TEMPERATURE"):
                        f_oa = 1
                else: 
                    f_oa = self._outdoor_air_flow/self._supply_air_flow
            else:
                f_oa = self._outdoor_air_flow/self._supply_air_flow
            
            self._f_oa = self.itera_Foa.x_next(f_oa)
            system_dic = {"name": self.parameter("name").value, 
                                  "V": self._supply_air_flow*self._f_oa, 
                                "T":self._T_odb, 
                                "w": self._w_o, 
                                "Q":self._no_load_power,
                            "M": 0}
            self._space.add_uncontrol_system(system_dic)
            K_tot, F_tot =  self._space._calculate_K_F_tot(False) # Space Equation
            T_flo = F_tot/K_tot                 
        return T_flo, K_tot, F_tot

    def post_iteration(self, time_index, date, daylight_saving, converged):
        super().post_iteration(time_index, date, daylight_saving, converged)
        self.variable("state").values[time_index] = self._state
        self._T_supply = self._Q_sen/self._mrcp + self._T_idb
        self._w_supply = self._M_w/self._supply_air_flow +self._w_i 
        if self._state != 0 : # on
            self.variable("T_idb").values[time_index] = self._T_idb
            self.variable("T_iwb").values[time_index] = self._T_iwb
            self.variable("T_supply").values[time_index] = self._T_supply
            self.variable("w_supply").values[time_index] = self._w_supply
            self.variable("F_air").values[time_index] = self._f_air
            self.variable("F_load").values[time_index] = self._f_load
            self.variable("power").values[time_index] = self._no_load_power
            self.variable("outdoor_air_flow").values[time_index] = self._supply_air_flow * self._f_oa

            if self._state == 1 or self._state == 2: # Heating
                Q,power,F_COP = self._equipment.get_heating_state(self._T_idb,self._T_iwb,self._T_odb,self._T_owb,self._f_air,self._f_load)
                self.variable("Q_sensible").values[time_index] = Q
                self.variable("power").values[time_index] = power
                if power>0:
                    self.variable("COP").values[time_index] = Q/power
                    self.variable("efficiency_degradation").values[time_index] = F_COP
                    
            elif self._state == -1 or self._state == -2: #Cooling
                Q_t,Q_s,power,F_EER = self._equipment.get_cooling_state(self._T_idb,self._T_iwb,self._T_odb,self._T_owb,self._f_air,-self._f_load)
                self.variable("Q_sensible").values[time_index] = -Q_s
                self.variable("Q_latent").values[time_index] = -(Q_t - Q_s)
                self.variable("power").values[time_index] = power
                if power>0: 
                    self.variable("EER").values[time_index] = Q_t/power
                    self.variable("efficiency_degradation").values[time_index] = F_EER
