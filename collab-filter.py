import csv
from math import sqrt

def covar(a,b):											#calculate pearson correlation

	mean_a=mean_b=var_a=var_b=correlation=length=0
	for (i,j) in list(zip(a,b)):						#calculating mean of both lists
		if not(i==-1 or j==-1):
 			mean_a=mean_a+i
 			mean_b=mean_b+j
 			length+=1

	if length!=0:										#error handling if no element in set of common movies watched
 		mean_a=mean_a/length;
 		mean_b=mean_b/length;

	
	for (i,j) in list(zip(a,b)):						#calculating variance and corelation of both lists
		if not(i==-1 or j==-1):
			var_a= var_a+(i-mean_a)**2
			var_b= var_b+(j-mean_b)**2
			correlation = correlation+(i-mean_a)*(j-mean_b)

	if length!=0:										#error handling if no element in set of common movies watched
		var_a= var_a/length
		var_b= var_b/length
		correlation=correlation/length

	if var_a!=0 and var_b!=0:							#error handling if dividing by 0
		p_corr=correlation/(sqrt(var_a)*sqrt(var_b))
	else:
		p_corr=0	

	return p_corr

critic_file=open('movie-ratings.csv','rt')					#opening critics rating file
critic_review=csv.reader(critic_file)
movie_name=next(critic_review)								#iterating first row of movie-ratings.csv
movie_list=list(movie_name)		
movie_list.pop(0)											#remove "name" nod ein begining


dict={}														#Dictionary that stores critic name and ratings sorted according to movie_list
for row in critic_review:									#adding data to dictionary
	temp=list(row)
	name=temp.pop(0)
	temp=list(map(float,temp))		
	dict[name]=temp

user_file = open('user_preference.csv')
user_review = csv.reader(user_file)
user_movie=next(user_review)
					

for row in user_review:										#sorts movie name if not in order to positions according to movie list
	list1 = []
	for col in row:
		z=float(col)
		list1.append(z)
userlist = list(list1)
indexlist1 = 0
for iterator in user_movie:
	index = movie_list.index(iterator)
	userlist[index] = list1[indexlist1]
	indexlist1+=1
user_rating=list(userlist)									#contains rating entered by user

user_correlation={}
for key,value in dict.items():								#storing user's correlation with critics
	p_corr=covar(value,user_rating)
	user_correlation[key]=p_corr

weighted_average=[]
for i in range(0,len(movie_list)-1):						#stores weighted average taking effect of correlation
	length=0
	temp=0
	for key,value in dict.items():
		corr=user_correlation[key]							#consider user dislikes movie if rating is less than 5
		if value[i]!=-1:									
			if corr>=0:										
				if value[i]>4:
					temp+=corr*value[i]						#if correlation is positive then rating greater than 4 mean user will also like movie
				else:
					temp-=corr*value[i]						#if correlation negative and rating less than 4 means user will like the movie
			else:
				if value[i]>4:
					temp+=corr*value[i]
				else:
					temp+=corr*value[i]*-1
			length+=1
	if length!=0:											#error handling to prevent division by 0
		temp=temp/length
	weighted_average.append(temp)


result = list(zip(weighted_average,user_rating,movie_list))	#prints top three unwatched movies
result.sort(reverse = True)
noofprints = 0;
for x,y,movie in result:
	if(noofprints==3):												
		break
	if(y==-1):
		print(movie)
		noofprints+=1
