# visualize trends in mean monsoon rainfall given a 3d NetCDF (xarray) dataset of a region
# Assuming "TIME" is a coordinate variable
months_to_keep = [6, 7, 8, 9]  # Months to include (adjust as needed)

# Advanced indexing expression
kljjas = klds.sel(TIME=klds["TIME.month"].isin(months_to_keep))
kljjas = kljjas.where(kljjas.RAINFALL >=0)
kljjas = kljjas

#mean monsoon rainfall
fish = kljjas.mean(dim=["x","y"]).groupby("TIME.year").sum(dim=["TIME"])
#graphing it
from scipy import stats
fit = stats.linregress(fish["year"], fish["RAINFALL"])
fig, ax = plt.subplots(figsize=(16,8))
plt.scatter(fish["year"],fish["RAINFALL"], label="Rainfall")
plt.xticks(np.arange(1979,2024))
plt.gcf().autofmt_xdate()
plt.grid(True, linestyle="-.")
plt.title("annual mean monsson rainfall")
plt.xlabel("year")
plt.ylabel("Mean Rainfall (mm)")
#plt.yscale("log")
plt.plot(fish["year"], fit.intercept+fit.slope*fish["year"],"r", label="fit" )
std_err = fish.std()/np.sqrt(45)
plt.legend(loc='best')
plt.text(0.05,0.9, f"slope = {fit.slope:.2f}, R-squared = {fit.rvalue**2:.2f}, P-value = {fit.pvalue:.2f}", transform=ax.transAxes, fontsize=12)
fish["RAINFALL"].std()

#stats module from scipy library is used for linear regression
