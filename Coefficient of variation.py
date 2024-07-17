#Function to find coefficient of variation for every year given a 3d xarray dataset and a threshold
def coeff_var(ds,threshold):
    df = pd.DataFrame(ds.to_dataframe())
    df = df.reset_index(level=["x","y"], drop=True).dropna()
    df_ehr = df[df["RAINFALL"]>threshold]
    cv = []
    empty_years = []
    no_std = []
    for i in df_ehr.index.year:
        df_i = df_ehr[df_ehr.index.year == i]
        if not df_i.empty:
            yearly_mean = df_i["RAINFALL"].mean()
            yearly_std = df_i["RAINFALL"].std()
            cv.append(yearly_std / yearly_mean)
        elif df_i["RAINFALL"].count() == 1:
            no_std.append(i)
        elif df_i.empty:
            empty_years.append(i)
            cv.append(np.nan)
    return cv

#function to find years with no coefficient of variation
def nan_year(cv_list):
    years = np.arange(1979,2024)
    nan_years = []
    for i in range(len(cv_list)):
        if np.isnan(cv_list[i]) == True:
            nan_years.append(years[i])
    return nan_years

#visualizing coefficient of variation
fig, ax = plt.subplots()
nona = [x for x in coeff_var(jjas, 150) if not np.isnan(x)]
arr = np.arange (1979,2024)
years_range = [i for i in arr if i not in [2002, 2011, 2012, 2015, 2021]]
plt.plot(years_range, nona)
plt.plot(years_range,nona)
fit = stats.linregress(years_range,nona)
fitted_line = fit.slope * np.array(years_range) + fit.intercept
plt.plot(years_range, fitted_line, "r")
plt.title("Coefficient of variaton of >150mm Rainfall")
plt.xlabel("years")
plt.ylabel("cv")
plt.xticks(np.arange(1979,2024,3))
plt.grid(linestyle="-")  
plt.gcf().autofmt_xdate()
plt.text(0.6, 0.96, f"slope:{fit.slope:.3f}, pvalue: {fit.pvalue:.3f}", transform = ax.transAxes) 
plt.show()
