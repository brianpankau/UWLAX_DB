#1a. Type your full name: Dr. Brian Pankau, UWL DS7100Summer2017Assigment1.r 1 June 2017

#1b. Open R

#1c. . Calculate the cube root of 2017:
> 2017^(1/3)
[1] 12.63481
> 

#1d. Find the absolute value of 5.7 minus 6.8 divided by .58:
> abs(5.7-6.8)/.58
[1] 1.896552
> 

#1e. Create a list of integers from 1 to 12 and call it “a”:
> a = 1:12
> a
 [1]  1  2  3  4  5  6  7  8  9 10 11 12
> 

#1f. Create a sequence of odd numbers from 1 to 11:
> b = c(1, 3, 5, 7, 9, 11)
> b
[1]  1  3  5  7  9 11
> 

#1g. Create the same sequence in another way:
> c = seq(1,11, 2)
> c
[1]  1  3  5  7  9 11
> 

#1h. Take the natural log (ln) of a:
> ln.a = log(a)
> ln.a
 [1] 0.0000000 0.6931472 1.0986123 1.3862944 1.6094379 1.7917595 1.9459101
 [8] 2.0794415 2.1972246 2.3025851 2.3978953 2.4849066
> 

#1i. Compute the squares of the odd numbers from 1 to 11:
> c
[1]  1  3  5  7  9 11
> csquared <- c^2
> csquared
[1]   1   9  25  49  81 121
> 

#1j. Use ?sd to view the help file for the sd function: What does the sd function do?
This function computes the standard deviation of the values in x. If na.rm is TRUE then missing values are removed before computation proceeds.

#1k. Create a variable Name that contains your first name:
> Name = "Brian Lee"
> paste("My name is: ", Name)
[1] "My name is:  Brian Lee"
> 
