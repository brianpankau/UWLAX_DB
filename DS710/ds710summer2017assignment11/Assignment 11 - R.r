# Author: Brian Pankau
# Class: UWLAX DS700
# Assignment: 11 R


# clear environment
rm(list=ls())

# set working directory
setwd("C:/_DS710/Temp11/R")


# ----------------------------------------------------------------------------
# PROBLEM 1A
# read data without header
input_data <- scan("foods.csv", sep=",", quote="\"", fill=TRUE, 
                   fileEncoding="utf-8", na.strings="", what="character",
                   skip=1, nlines=-1)


# ----------------------------------------------------------------------------
# PROBLEM 1B
# read header
input_header <- scan("foods - Copy.csv", skip=0, sep=",", quote="\"", nlines=1, 
                     what="character")

# convert input_data from a list of vectors to a matrix
ary <- t(simplify2array(input_data))
m <- matrix(data=ary, byrow=TRUE, ncol=12)

# convert data & header into a data frame
df <- data.frame(m)

# replace the df column names with the input header
colnames(df) <- input_header

# sumarize the df result
summary(df)


# ----------------------------------------------------------------------------
# PROBLEM 1C
# convert calculated columns from character to numeric
df$Voted_helpful      <- as.numeric(as.character(df$Voted_helpful))
df$Voted_total        <- as.numeric(as.character(df$Voted_total))
df$Review_length      <- as.numeric(as.character(df$Review_length))
df$Exclamation_count  <- as.numeric(as.character(df$Exclamation_count))
df$Percentage_helpful <- as.numeric(as.character(df$Percentage_helpful))


# ----------------------------------------------------------------------------
# PROBLEM 1D
# identify which records have a ratio of helpful votes to total votes > 1
unrealistic_voted_total <- which(df$Percentage_helpful > 1)

# set the calculated fields to NA for any records that were found
if (length(unrealistic_voted_total > 0)) {
    # print the current vote values for the unrealistic_voted_total records
    for (n in unrealistic_voted_total) {
        message(sprintf("Current value of df$Voted_helpful[%s] = %s", 
                        n, df$Voted_helpful[n]))
        message(sprintf("Current value of df$Voted_total  [%s] = %s", 
                        n, df$Voted_total[n]))
        message(sprintf("Current value of df$Voted_[%s] = %s", 
                        n, df$Percentage_helpful[n]))
    }
    
    # update the vote values for the unrealistic_voted_total records to NA
    for (n in unrealistic_voted_total) {
        df$Voted_helpful[n] = NA
        df$Voted_total[n] = NA
        df$Percentage_helpful[n] = NA
    }
    
    # print the updated vote values for the unrealistic_voted_total records
    for (n in unrealistic_voted_total) {
        message(sprintf("Updated value of df$Voted_helpful[%s] = %s", 
                        n, df$Voted_helpful[n]))
        message(sprintf("Updated value of df$Voted_total  [%s] = %s", 
                        n, df$Voted_total[n]))
        message(sprintf("Updated value of df$Voted_[%s] = %s", 
                        n, df$Percentage_helpful[n]))
    }
} else {
    message("No records that have a ratio of helpful votes to total votes > 1 
            were found.")
}

# ----------------------------------------------------------------------------
# PROBLEM 1E
# Two records (44727 64412) were found in the data frame where the total number 
#     votes were less than the votes voted as helpful which is an unrealistic 
#     scenario for the ratio of votes helpful / votes total > 1.


# ----------------------------------------------------------------------------
# PROBLEM 1F
# create a new variable on whether there was zero helpfull feedback
df$Zero_helpfullness <- df$Helpfullness == "0/0"

# create a new variable that describes whether more than 50% of people who 
#     voted considered it helpful
df$Helpful_review <- df$Percentage_helpful > 0.5

# summarize helpful review findings
summary(df$Helpful_review)
summary(df$Zero_helpfullness)

# OBSERVATION: There were 270054 missing values for helpful reviews, of which
#    270052 values were due to no review feedback ("0/0"); the remaining 
#    2 observations were the two unrealistic records.


# ----------------------------------------------------------------------------
# PROBLEM 1G
# create a df containing the helpful reviews
df_helpful_reviews <- df[ which(df$Helpful_review == TRUE), ]

# create a df containing the unhelpful reviews
df_unhelpful_reviews <- df[ which(df$Helpful_review == FALSE), ]


# install package required for advanced plotting
require(prettyR)
require(rcompanion)


# calculate descriptive statistics ------------------------------------------
# determine the mode for review length
Mode(df_helpful_reviews$Review_length)
Mode(df_unhelpful_reviews$Review_length)

# determine the variation in review length
var(df_helpful_reviews$Review_length)
var(df_unhelpful_reviews$Review_length)

# determine the standard deviation in review length
sd(df_helpful_reviews$Review_length)
sd(df_unhelpful_reviews$Review_length)

# determine the range for review length
range(df_helpful_reviews$Review_length)
range(df_unhelpful_reviews$Review_length)

quantile(df_helpful_reviews$Review_length)
quantile(df_unhelpful_reviews$Review_length)

quantile(df_helpful_reviews$Review_length_invlog)
quantile(df_unhelpful_reviews$Review_length_invlog)


# determine the Mean Absolute Deviation (MAD)
mad(df_helpful_reviews$Review_length)
mad(df_unhelpful_reviews$Review_length)


# Generate initial graphs ---------------------------------------------------
# generate box plot for review length
boxplot(df_helpful_reviews$Review_length, main="boxplot for df_helpful_reviews$Review_length")
boxplot(df_unhelpful_reviews$Review_length, main="boxplot for df_unhelpful_reviews$Review_length")

# generate frequency distribution histograph for reveiw lengths
hist(df_helpful_reviews$Review_length)
hist(df_unhelpful_reviews$Review_length)

# create a grouped frequency distribution for helpful reviews
helpful_breaks   <- seq(0,2000, by=10)
helpful_group_freq <- cut(df_helpful_reviews$Review_length, helpful_breaks, right=FALSE)
helpful_group_freq_m <- cbind(table(helpful_group_freq))
hist(helpful_group_freq_m)
plot(helpful_group_freq_m)

# create a grouped frequency distribution for unhelpful reviews
unhelpful_breaks <- seq(0, 1400, by=10)
unhelpful_group_freq <- cut(df_unhelpful_reviews$Review_length, unhelpful_breaks, right=FALSE)
unhelpful_group_freq_m <- cbind(table(unhelpful_group_freq))
hist(unhelpful_group_freq_m)
plot(unhelpful_group_freq_m)

# generate Histogram with added normal distribution curve
plotNormalHistogram(df_helpful_reviews$Review_length)
plotNormalHistogram(df_unhelpful_reviews$Review_length)

# attempt transformations ---------------------------------------------------
# apply a sqrt transformation on review lengths
df_helpful_reviews$Review_length_sqrt <- sqrt(df_helpful_reviews$Review_length)
df_unhelpful_reviews$Review_length_sqrt <- sqrt(df_unhelpful_reviews$Review_length)

# apply a log transformation on review lengths
df_helpful_reviews$Review_length_log <- log(df_helpful_reviews$Review_length)
df_unhelpful_reviews$Review_length_log <- log(df_unhelpful_reviews$Review_length)

# apply a reciprocal/inverse log transformation on review lengths
df_helpful_reviews$Review_length_invlog <- log(df_helpful_reviews$Review_length)^-1
df_unhelpful_reviews$Review_length_invlog <- log(df_unhelpful_reviews$Review_length)^-1


# Generate graphical representations of applied transformations -------------
# regenerate a grouped frequency distribution for sqrt transformed helpful reviews
range(df_helpful_reviews$Review_length_sqrt)
helpful_breaks_sqrt   <- seq(0,150, by=5)
helpful_group_freq_sqrt <- cut(df_helpful_reviews$Review_length_sqrt, helpful_breaks_sqrt, right=FALSE)
helpful_group_freq_m_sqrt <- cbind(table(helpful_group_freq_sqrt))
hist(helpful_group_freq_m_sqrt)

# regenerate a grouped frequency distribution for sqrt transformed unhelpful reviews
range(df_unhelpful_reviews$Review_length_sqrt)
unhelpful_breaks_sqrt <- seq(0, 150, by=5)
unhelpful_group_freq_sqrt <- cut(df_unhelpful_reviews$Review_length_sqrt, unhelpful_breaks_sqrt, right=FALSE)
unhelpful_group_freq_m_sqrt <- cbind(table(unhelpful_group_freq_sqrt))
hist(unhelpful_group_freq_m_sqrt)


# regenerate a grouped frequency distribution for log transformed helpful reviews
range(df_helpful_reviews$Review_length_log)
helpful_breaks_log   <- seq(0,150, by=5)
helpful_group_freq_log <- cut(df_helpful_reviews$Review_length_log, helpful_breaks_log, right=FALSE)
helpful_group_freq_m_log <- cbind(table(helpful_group_freq_log))
hist(helpful_group_freq_m_log)

# regenerate a grouped frequency distribution for log transformed unhelpful reviews
range(df_unhelpful_reviews$Review_length_log)
unhelpful_breaks_log   <- seq(0,150, by=5)
unhelpful_group_freq_log <- cut(df_unhelpful_reviews$Review_length_log, unhelpful_breaks_log, right=FALSE)
unhelpful_group_freq_m_log <- cbind(table(unhelpful_group_freq_log))
hist(unhelpful_group_freq_m_log)


# regenerate a grouped frequency distribution for reciprocal log transformed helpful reviews
range(df_helpful_reviews$Review_length_invlog)
helpful_breaks_invlog   <- seq(0,150, by=5)
helpful_group_freq_invlog <- cut(df_helpful_reviews$Review_length_invlog, helpful_breaks_invlog, right=FALSE)
helpful_group_freq_m_invlog <- cbind(table(helpful_group_freq_invlog))
hist(helpful_group_freq_m_invlog)

# regenerate a grouped frequency distribution for reciprocal log transformed unhelpful reviews
range(df_unhelpful_reviews$Review_length_invlog)
unhelpful_breaks_invlog   <- seq(0,150, by=5)
unhelpful_group_freq_invlog <- cut(df_unhelpful_reviews$Review_length_invlog, unhelpful_breaks_invlog, right=FALSE)
unhelpful_group_freq_m_invlog <- cbind(table(unhelpful_group_freq_invlog))
hist(unhelpful_group_freq_m_invlog)


# generate qqplots: df_helpful_reviews$Review_length
qqnorm(df_helpful_reviews$Review_length, ylab="df_helpful_reviews$Review_length")
qqline(df_helpful_reviews$Review_length, col="red")

# generate qqplots: df_unhelpful_reviews$Review_length
qqnorm(df_unhelpful_reviews$Review_length, ylab="df_unhelpful_reviews$Review_length")
qqline(df_unhelpful_reviews$Review_length, col="red")


# generate qqplots: df_helpful_reviews$Review_length_sqrt
qqnorm(df_helpful_reviews$Review_length_sqrt, ylab="df_helpful_reviews$Review_length_sqrt")
qqline(df_helpful_reviews$Review_length_sqrt, col="red")

# generate qqplots: df_unhelpful_reviews$Review_length_sqrt
qqnorm(df_unhelpful_reviews$Review_length_sqrt, ylab="df_unhelpful_reviews$Review_length_sqrt")
qqline(df_unhelpful_reviews$Review_length_sqrt, col="red")


# generate qqplots: df_helpful_reviews$Review_length_log
qqnorm(df_helpful_reviews$Review_length_log, ylab="df_helpful_reviews$Review_length_log")
qqline(df_helpful_reviews$Review_length_log, col="red")

# generate qqplots: df_unhelpful_reviews$Review_length_log
qqnorm(df_unhelpful_reviews$Review_length_log, ylab="df_unhelpful_reviews$Review_length_log")
qqline(df_unhelpful_reviews$Review_length_log, col="red")


# generate qqplots: df_helpful_reviews$Review_length_invlog
qqnorm(df_helpful_reviews$Review_length_invlog, ylab="df_helpful_reviews$Review_length_invlog")
qqline(df_helpful_reviews$Review_length_invlog, col="red")

# generate qqplots: df_unhelpful_reviews$Review_length_invlog
qqnorm(df_unhelpful_reviews$Review_length_invlog, ylab="df_unhelpful_reviews$Review_length_invlog")
qqline(df_unhelpful_reviews$Review_length_invlog, col="red")


# perform hypothesis testing ------------------------------------------------
# extract a random sample of 1000 observations from the length of the review text 
# source: https://dataissexy.wordpress.com/2013/06/09/random-samples-from-r-data-frames/
randomSample = function(df,n) { 
    return (df[sample(nrow(df), n),])
}
df_helpful_reviews_sample   <- randomSample(df_helpful_reviews, 1000)
df_unhelpful_reviews_sample <- randomSample(df_unhelpful_reviews, 1000)

# setup variables
x <- df_helpful_reviews_sample$Review_length_log
y <- df_unhelpful_reviews_sample$Review_length_log
alpha_value <- 0.05

# verify homoskedasticity: use the F-test to evaluate the two group variances
var.test(x,y)

# perform the Welch two sample t-test (one-tailed test)
t.test(x, y, paired=FALSE, alternative = "greater")


# generate plots for samples
# helpful reviews
plotNormalHistogram(df_helpful_reviews_sample$Review_length_invlog)
qqnorm(df_helpful_reviews_sample$Review_length_invlog, ylab="df_helpful_reviews_sample$Review_length_invlog")
qqline(df_helpful_reviews_sample$Review_length_invlog, col="red")

# unhelpful reviews
plotNormalHistogram(df_unhelpful_reviews_sample$Review_length_invlog)
qqnorm(df_unhelpful_reviews_sample$Review_length_invlog, ylab="df_unhelpful_reviews_sample$Review_length_invlog")
qqline(df_unhelpful_reviews_sample$Review_length_invlog, col="red")


# ----------------------------------------------------------------------------
# PROBLEM 1H
# Investigate whether products with more reviews tend to have more votes on their reviews.

# for each unique productID in the population, 
# find the maximum number of votes received, and 
# find the total number of reviews
# find all unique ProductID

# find all unique ProductID
ProductID_unique <- unique(df$ProductId)
head(ProductID_unique)

# count the number of reviews per unique ProductID
ProductID_votedtotal_count <- tapply(df$Voted_total, df$ProductId, length)
head(ProductID_votedtotal_count)

# find the maximum number of votes per ProductID
head(ProductID_votedtotal_max)
ProductID_votedtotal_max   <- tapply(df$Voted_total, df$ProductId, max)

# find the total number of votes per ProductID
ProductID_votedtotal_sum   <- tapply(df$Voted_total, df$ProductId, sum)
head(ProductID_votedtotal_sum)


# ----------------------------------------------------------------------------
# PROBLEM 1I
# Make a scatterplot of max number of votes as a function of number of reviews. 
# Is there a visible trend?  If so, describe it.

# plot number of votes vy number of reviews
plot(ProductID_votedtotal_count, ProductID_votedtotal_sum, main="max votes by reviews")


# ----------------------------------------------------------------------------
# PROBLEM 1J
# Histograms of the review counts and number of votes indicate that both variables are right-skewed
plotNormalHistogram(ProductID_votedtotal_count, xlim=c(0,200))
plotNormalHistogram(ProductID_votedtotal_sum)
plotNormalHistogram(ProductID_votedtotal_max)

# Subset the variables max.votes and number.of.reviews to only those values 
# corresponding to products with 1 or more votes.
df_one_or_more_votes <- df[df$Voted_total > 0, ]
ProductID_votedtotal_count_pos <- tapply(df_one_or_more_votes$Voted_total, df_one_or_more_votes$ProductId, length)
ProductID_votedtotal_sum_pos   <- tapply(df_one_or_more_votes$Voted_total, df_one_or_more_votes$ProductId, sum)
ProductID_votedtotal_max_pos   <- tapply(df_one_or_more_votes$Voted_total, df_one_or_more_votes$ProductId, max)




# ----------------------------------------------------------------------------
# PROBLEM 1K
# Make a scatterplot of log(max.votes) as a function of log(number.of.reviews).
# Is there a visible trend?  If so, describe it.  
# Does this tell us anything about the relationship between the 
# untransformed max.votes and number.of.reviews?

plot(log(ProductID_votedtotal_count_pos), log(ProductID_votedtotal_sum_pos))

