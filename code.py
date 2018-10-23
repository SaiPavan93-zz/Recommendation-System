import pandas as pd
import numpy as np

def similar(totaldata):
#print(totaldata.head())
    movie=totaldata.pivot_table(index=['user_id'],columns=['title'],values='rating')
    starwarratings=movie['Star Wars (1977)']
    similarmovies=movie.corrwith(starwarratings)
    similarmovies=similarmovies.dropna()
    df=pd.DataFrame(similarmovies)
    moviestats=totaldata.groupby('title').agg({'rating':[np.size,np.mean]})
    popmovies=moviestats['rating']['size']>=100
    df=moviestats[popmovies].join(pd.DataFrame(similarmovies,columns=['similarity']))
    df=df.sort_values(['similarity'],ascending=False)
    Recommendation(movie)

def Recommendation(movie):
    corrMatrix=movie.corr(method="pearson",min_periods=100)
    myratings=movie.loc[0].dropna()
    sim=pd.Series()
    simsum=pd.Series()
    for i in range(0,len(myratings.index)):
        s=corrMatrix[myratings.index[i]].dropna()
        ssum=s.map(lambda x:abs(x))
        s=s.map(lambda x:x*myratings[i])
        sim=sim.append(s)
        simsum=simsum.append(ssum)
    sim.sort_values(inplace=True,ascending=False)
    sim=sim.groupby(sim.index).sum()
    sim.sort_values(inplace=True,ascending=False)
    simsum.sort_values(inplace=True, ascending=False)
    simsum = simsum.groupby(simsum.index).sum()
    simsum.sort_values(inplace=True, ascending=False)
    weighted=sim/simsum
    weighted.sort_values(inplace=True,ascending=False)
    d=sim.to_dict()
    d1=myratings.to_dict()
    d2=weighted.to_dict()
    simset=set(d.keys())
    ratset=set(d1.keys())
    wset=set(d2.keys())
    b=list(wset-ratset)
    a=list(simset-ratset)
    print("The recommended movies are:",a)
    print("The recommended movie using weighted approach is :",b)


def main():
    col = ["user_id", "movie_id", "rating"]
    data = pd.read_csv("u.data", sep="\t", names=col, usecols=range(3), encoding="ISO-8859-1")
    cols = ["movie_id", "title"]
    data1 = pd.read_csv("u.item", sep='|', names=cols, usecols=range(2), encoding="ISO-8859-1")
    totaldata = pd.merge(data, data1)
    similar(totaldata)

if __name__=="__main__":
    #for i in range(10):
    main()