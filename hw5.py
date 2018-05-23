import random
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

class VisualStimData:
	"""
	Holding the data and methods of the experiment.
	inputs: data: dict with DataArray or Dataset values
	methods: plot_electrode, experimenter_bias
	"""
	def __init__(self,data):
		self.data= data
	
	def plot_electrode(self, rep_number, rat_id, elec_number):
		"""
		Plots the voltage of the electrodes in "elec_number" for the rat "rat_id" in the repetition
		"rep_number". Shows a single figure with subplots.
		"""
		plt.figure()
		plot_num= len(elec_number)
		for i in range (0, len(elec_number)):
			plt.subplot(plot_num, 1, i+1)
			sub_plot_data= self.data[rat_id].isel(repetition=rep_number).isel(elec_number=elec_number[i])
			sub_plot_data_voltage=sub_plot_data.voltage
			sub_plot_data_voltage.plot()
		plt.subplots_adjust()
		plt.tight_layout()
		plt.show()	
	
	def experimenter_bias(self):
		""" Shows the statistics of the average recording across all experimenters """
		Experimenter_name=['Alon', 'Dor', 'Gal', 'Ben']
		mean_dict={'Alon':[], 'Dor':[], 'Gal':[], 'Ben':[]}
		
		Experimenter_data= pd.DataFrame(columns=['mean', 'std', 'median'], index=['Alon', 'Dor', 'Gal', 'Ben'])
		#extracting std, mean and median values
		for key in self.data:
			for Experimenter in Experimenter_name:
				if (self.data[key].Experimenter_name==Experimenter):
					Experimenter_mean = self.data[key].mean().voltage
					mean_dict[Experimenter].append(Experimenter_mean.values)
		for key in mean_dict:
			if (mean_dict[key] != []):
				Experimenter_data['mean'][key]=np.mean(mean_dict[key])
				Experimenter_data['std'][key]=np.std(mean_dict[key])
				Experimenter_data['median'][key]=np.median(mean_dict[key])
				
		#creating plot 
		Experimenter_data.plot(kind='bar')
		plt.title('Experimenters bias statistics')
		plt.xlabel('Experimenter')
		plt.ylabel('Value')
		
		plt.show()

		
def mock_stim_data(n):
	""" Creates a new VisualStimData instance with mock data """
	Experimenter_name=['Alon', 'Dor', 'Gal', 'Ben']
	Gender=['Female','Male']
	Rats_Ids= list(range(0,20))
	data_dict={}
	electrodes=10
	samples=10000
	ex_time_sec=2
	repetitions=4
	pre= ['pre']*5000
	during=['during']*500
	post=['post']*4500
	Stimulus_index= pre+ during +post
	
	for i in list(range(0,n)):
		dims = ('time', 'repetition', 'elec_number')
		coords = {'time': np.linspace(0, ex_time_sec, num=samples),'repetition': np.arange(repetitions), 'elec_number': np.linspace(0, electrodes, num=electrodes, dtype=int)}
		da2 = xr.DataArray(np.random.uniform(-70,70, size=(samples, repetitions,electrodes)), dims=dims, coords=coords)
		dims2 = ('time', 'repetition')
		coords2 = {'time': np.linspace(0, ex_time_sec, num=samples),'repetition': np.arange(repetitions)}
		room_temp = xr.DataArray((np.random.uniform(20,50,[samples,repetitions])), dims=dims2, coords=coords2)
		room_humidity = xr.DataArray((np.random.uniform(0,100,[samples,repetitions])), dims=dims2, coords=coords2)
		ds = xr.Dataset({'voltage': da2, 'Room_temp':room_temp, 'Room_humidity':room_humidity,'Stimulus_index': ('time',Stimulus_index) }, 
		attrs={'Rat_ID': Rats_Ids.pop(), 'Experimenter_name': random.choice(Experimenter_name), 'Rat_gender': random.choice(Gender)})
		data_dict[ds.Rat_ID]=ds

	return VisualStimData(data_dict)
	
x= mock_stim_data(20)
x.plot_electrode(2, 19, (0,2,4))
x.experimenter_bias()


