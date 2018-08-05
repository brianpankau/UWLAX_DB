# Author: Brian Pankau
# Class: DS710 Summer 2017
# Assignment: R 9-1

# Problem 1(a)
# Read the modified data into R using the Python portion of 
# homework 9 that is the modified version of the data set 
setwd ("c:/Temp9")
f = read.csv(file="Assignment_9_python.csv", header=TRUE, sep=",")
df <- data.frame(f)

# check a few vectors for read accuracy
head(df)


# Problem 1(b)
# Examine data
for (n in 1:ncol(df)){
  print(summary(df[colnames(df[n])]))
  print("---------------")
}

# Attributes examined:
# - Looked for unusual outliers, values outside of normal range
# - Looked for negative values
# - Looked for inconsistencies in paired attributes


# Problem 1(c)
# Find the mean percentage of alumni who donate, for private and public schools.
# Public schools
colMeans(
  alumni_public <- subset(
    df,
    Public.private == 1 & Pct.alumni.who.donate > 0,
    c(Pct.alumni.who.donate)
  )
)

# Result
# Pct.alumni.who.donate 
#             13.56374 

# Private schools
colMeans(
  alumni_private <-  subset(
    df,
    Public.private == 2 & Pct.alumni.who.donate > 0,
    c(Pct.alumni.who.donate)
  )
)

# Result:
# Pct.alumni.who.donate 
#             24.58287 


# Problem 1(d)
# Test whether there is evidence that a higher percentage of alumni 
# from private schools donate to their schools, compared to alumni 
# from public schools.  
# State your conclusion in context.

# Samples
#   1: alumni from private schools who donate (alumni_private)
#   2: alumni from public  schools who donate (alumni_public)

# Assumptions:
# - samples are independent data populations
# - samples are random
# - conform to a normal distribution with unknown but equal variances

# Hypothesis: 
# Find the 95% confidence interval estimate of the difference between 
# the mean of the percentage of the alumni from private schools who donate, and
# the mean of the percentage of the alumni from public schools who donate

# Null Hypothesis: The two means are equal
# mean(alumni_private) == mean(alumni_public)

# Test: unpaired t-test
# t.test(alumni_private, alumni_public)

# convert lists into vectors
a = unlist(alumni_private, use.names = FALSE)
b = unlist(alumni_public,  use.names = FALSE)

"""
# characterize the data
> summary(a)
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
   1.00   15.00   24.00   24.58   33.00   81.00 
> summary(b)
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
   1.00    8.00   12.00   13.56   17.00   51.00 


# verify homoskedasticity
> ftest <- var.test(a, b)
> ftest

        F test to compare two variances

data:  a and b
F = 2.6022, num df = 723, denom df = 352, p-value < 2.2e-16
alternative hypothesis: true ratio of variances is not equal to 1
95 percent confidence interval:
 2.166517 3.107710
sample estimates:
ratio of variances 
          2.602176 

# calculate a tabulated value for F
> qtest <- qf(0.95, 723, 352)
> qtest
[1] 1.166072

# Observation: the value of F computed is greater than the tabulated value of F
# and since computed F test p-value < 0.05, then this implies that 
# the two variances are NOT homogeneous ==> need for Welch Two sample t-test

# Means t-test:
> ttest <- t.test(a, b)
> ttest

        Welch Two Sample t-test

data:  a and b
t = 17.166, df = 1015.8, p-value < 2.2e-16
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
  9.759472 12.278795
sample estimates:
mean of x mean of y 
 24.58287  13.56374 

# compare data graphically
> qqplot(a, b)
> abline(0,1) 
# ==> the points plotted fall under the diagonal ab line, indicating 
#     that the two samples are from two different distributions
"""
# Means t-test Conclusion:
# Since the t test p-value is less than 0.05, 
# the null hypothesis is rejected
# Therefore, it is concluded that there is sufficient evidence at the 
# alpha = 0.05 level to conclude that the average percentage of 
# private school doners differs from the average percentage of 
# public school donors.


# Problem 1(e)
# Use write.csv() to save your updated data set.  
# Your output file should not have row names or row numbers, and 
# it should not have quotation marks around the entries.
write.csv(df, file = "c:/Temp9/Assignment_9_r.csv", row.names=FALSE, quote=FALSE)
