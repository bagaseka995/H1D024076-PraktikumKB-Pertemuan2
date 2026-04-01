import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

suhu['Dingin'] = fuzz.trimf(suhu.universe, [0, 10, 20])
suhu['Normal'] = fuzz.trimf(suhu.universe, [15, 25, 35])
suhu['Panas'] = fuzz.trimf(suhu.universe, [30, 40, 40])

kelembapan['Kering'] = fuzz.trimf(kelembapan.universe, [0, 25, 50])
kelembapan['Lembap'] = fuzz.trimf(kelembapan.universe, [40, 60, 80])
kelembapan['Basah'] = fuzz.trimf(kelembapan.universe, [70, 100, 100])

kecepatan['Lambat'] = fuzz.trimf(kecepatan.universe, [0, 25, 50])
kecepatan['Sedang'] = fuzz.trimf(kecepatan.universe, [40, 60, 80])
kecepatan['Cepat'] = fuzz.trimf(kecepatan.universe, [70, 100, 100])

rule1 = ctrl.Rule(suhu['Dingin'], kecepatan['Lambat'])
rule2 = ctrl.Rule(suhu['Normal'] & kelembapan['Lembap'], kecepatan['Sedang'])
rule3 = ctrl.Rule(suhu['Panas'] | kelembapan['Kering'], kecepatan['Cepat'])

basispengetahuan = ctrl.ControlSystem([rule1, rule2, rule3])
pengambilankeputusan = ctrl.ControlSystemSimulation(basispengetahuan)

pengambilankeputusan.input['suhu'] = 35
pengambilankeputusan.input['kelembapan'] = 30

pengambilankeputusan.compute()

print(f"Input Suhu: {pengambilankeputusan.input['suhu']} C")
print(f"Input Kelembapan: {pengambilankeputusan.input['kelembapan']} %")
print(f"Hasil Kecepatan Kipas (Defuzzifikasi Centroid): {pengambilankeputusan.output['kecepatan']:.2f}")

kecepatan.view(sim=pengambilankeputusan)
plt.show() 