# Author: Brian Pankau
# Class: DS710 Summer 2017
# Assignment: R 9-2
# See: Homework 9-2_R.docx for plots


# Problem 2(a)
# Read the data from cps.csv into R and 
# plot wages versus education.  
# Comment on the appropriateness of linear regression.

# load the graphics library
library(ggplot2)
require(ggplot2)

# load the data
setwd ("c:/Temp9")
f = read.csv(file="cps.csv", header=TRUE, sep=",")
df <- data.frame(f)

# create a subset of the data for plotting
dat = data.frame(df$wage, df$educ)

"""
# characterize the data
> summary(dat)
    df.wage          df.educ     
 Min.   : 1.000   Min.   : 2.00  
 1st Qu.: 5.250   1st Qu.:12.00  
 Median : 7.780   Median :12.00  
 Mean   : 9.024   Mean   :13.02  
 3rd Qu.:11.250   3rd Qu.:15.00  
 Max.   :44.500   Max.   :18.00  
> 
"""

# generate a linear regression scatter plot
ggplot(dat, aes(x=df.educ, y=df.wage)) +
  geom_point(shape=1) +
  labs(x = "Education") +
  labs(y = "Wage") +
  labs(title = "Wage versus Education") 

# Comment:
# This scatter plot of Wage versus Education indicates that there 
# is a positive and an increasing association between the number 
# of years of education and the predicted Wage in dollars earned. 
# These is a high degree of dispersal and range in the predicted 
# value of Wage for a specific years of education. 
# This scatter plot shows that the data is skewed left, indicating 
# that a transformation of the Wage variable may be appropriate 
# for application – prehaps using a square transformation.


# Problem 2(b)
# Perform the linear regression and 
# examine the diagnostic plots.  
# Explain why transforming the wages variable is a good idea in 
# this case.

ggplot(dat, aes(x=df.educ, y=df.wage)) +
  geom_point(shape=1) +
  labs(x = "Education") +
  labs(y = "Wage") +
  labs(title = "Wage versus Education") +
  geom_smooth(method=lm)

# generate diagnostic plots
fit = lm(df.wage~df.educ, dat)
plot(fit)

# set up model for diagnostic plots
# source: https://rpubs.com/therimalaya/43190
lm.model<-lm(df.wage~df.educ, data=dat)

# Diagnostic Plots - Residual vs Fitted Plot
p1<-ggplot(lm.model, aes(.fitted, .resid))+geom_point()
p1<-p1+stat_smooth(method="loess")+geom_hline(yintercept=0, col="red", linetype="dashed")
p1<-p1+xlab("Fitted values")+ylab("Residuals")
p1<-p1+ggtitle("Residual vs Fitted Plot")+theme_bw()  
 
# Theoretical Quantiles Plot
p2<-ggplot(lm.model, aes(qqnorm(.stdresid)[[1]], .stdresid))+geom_point(na.rm = TRUE)
p2<-p2+geom_abline(aes(qqline(.stdresid)))+xlab("Theoretical Quantiles")+ylab("Standardized Residuals")
p2<-p2+ggtitle("Normal Q-Q")+theme_bw()

# Diagnostic Plots - Scale-Location
p3<-ggplot(lm.model, aes(.fitted, sqrt(abs(.stdresid))))+geom_point(na.rm=TRUE)
p3<-p3+stat_smooth(method="loess", na.rm = TRUE)+xlab("Fitted Value")
p3<-p3+ylab(expression(sqrt("|Standardized residuals|")))
p3<-p3+ggtitle("Scale-Location")+theme_bw()

# Diagnostic Plots - Cook's Distance
p4<-ggplot(lm.model, aes(seq_along(.cooksd), .cooksd))+geom_bar(stat="identity", position="identity")
p4<-p4+xlab("Obs. Number")+ylab("Cook's distance")
p4<-p4+ggtitle("Cook's distance")+theme_bw()
  
# Diagnostic Plots - Residual vs Leverage Plot
p5<-ggplot(lm.model, aes(.hat, .stdresid))+geom_point(aes(size=.cooksd), na.rm=TRUE)
p5<-p5+stat_smooth(method="loess", na.rm=TRUE)
p5<-p5+xlab("Leverage")+ylab("Standardized Residuals")
p5<-p5+ggtitle("Residual vs Leverage Plot")
p5<-p5+scale_size_continuous("Cook's Distance", range=c(1,5))
p5<-p5+theme_bw()+theme(legend.position="bottom")

# Diagnostic Plots - Cook's Distance versus Leverage Hii/(1-hii)   
p6<-ggplot(lm.model, aes(.hat, .cooksd))+geom_point(na.rm=TRUE)+stat_smooth(method="loess", na.rm=TRUE)
p6<-p6+xlab("Leverage hii")+ylab("Cook's Distance")
p6<-p6+ggtitle("Cook's dist vs Leverage hii/(1-hii)")
p6<-p6+geom_abline(slope=seq(0,3,0.5), color="gray", linetype="dashed")
p6<-p6+theme_bw()

# Comment:
# This scatter plot of Wage versus Education and the accompaning 
# regression line indicates a positive and an increasing correlation 
# between the number of years of education and the resulting income 
# in wages. As indicated by the regression line, as the number of 
# years increase, so does the size of the wage that is earned. 
# The confidence of the association as indicated by the shaded area 
# around the regression line.  Since there is limited information at 
# low levels of eduction, one can not say with a high degree of 
# confidence about the predicted wage; in addition, there seems to be 
# a high degree of variability in these few data points at the lower 
# end of the education range (< ~7). Confidence of the prediction 
# looks to be higher towards the median of the education range, but 
# again there is a dispersal of data points both above and below 
# (almost equally) the regression line at these higher education 
# ranges.


# Problem 2(c)
# The variable wage has units of dollars/hour.  
# Create a new variable, time, equal to 1/wage.
dat$time <- with(
  dat,
  1/df.wage
)


# Problem 2(d)
# Plot time versus education.  
# Comment on the appropriateness of linear regression.
ggplot(dat, aes(x=df.educ, y=time)) +
  geom_point(shape=1) +
  labs(x = "Education") +
  labs(y = "Time") +
  labs(title = "Time versus Education")

# Comment: By applying the inverse transformation on the Wage 
# variable to generate Time (Time = 1/Wage), the distribution of 
# the data points is less skewed to the left and the data points 
# have less dispersion along the Time axis. However, there is still 
# a grouping / concentration of the data points as the number of 
# years of education increases, and there does not seem to be any 
# indication of a linear assocation between the number of years of 
# education and the predicted wage.


# Problem 2(e)
# Perform the linear regression. Based on these results, are you 
# happy with your decision to pursue a master’s degree?  Explain.
ggplot(dat, aes(x=df.educ, y=time)) +
  geom_point(shape=1) +
  labs(x = "Education") +
  labs(y = "Time") +
  labs(title = "Time versus Education") +
  geom_smooth(method=lm)

# Comment:The regression line in this transformed scatter plot 
# indicates that as the number of years of education increases, 
# the length of time that a person has to work to earn $1 decreases. 
# There is a negative correlation between the years of education 
# versus the amount of hours it takes a person to earn $1.
# Based on this negative relationship, I am very happy with my 
# decision to persue this advanced degree in data science, for 
# this relationship indicates that it is probable that my earning 
# power per time unit will increase once I achieve the degree.


# Problem 2(f)
# Examine the diagnostic plots.  
# Which individuals appear to be outliers on the residual vs. predicted plot?  
# Re-do the regression without these individuals.  
# Does your conclusion change?

# load modified data file with outlier removed
m = read.csv(file="cps_modified_outlier_removed.csv", header=TRUE, sep=",")
df_m <- data.frame(m)
dat_m = data.frame(df_m$wage, df_m$educ)
lm.model<-lm(df_m.wage~df_m.educ, data=dat_m)

# generate a linear regression scatter plot
ggplot(dat_m, aes(x=df_m.educ, y=df_m.wage)) +
  geom_point(shape=1) +
  labs(x = "Education") +
  labs(y = "Wage") +
  labs(title = "Wage versus Education w/o outlier") 

p1_m<-ggplot(lm.model, aes(.fitted, .resid))+geom_point()
p1_m<-p1+stat_smooth(method="loess")+geom_hline(yintercept=0, col="red", linetype="dashed")
p1_m<-p1+xlab("Fitted values")+ylab("Residuals")
p1_m<-p1+ggtitle("Residual vs Fitted Plot w/o outlier")+theme_bw()  

# Comment
# By removing the outlier, the distribution in the scatter plot 
# improves, but there still is a outlier in the Residual vs Fitted 
# plot. My conclusion remains the same that there is an association 
# between years of education and the predicted wage. 

# One could attempt at removing the outliers at the lower end of 
# the education~wage ranges.

