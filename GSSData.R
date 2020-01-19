library(foreign)
library(Hmisc)
dataset1 = read.spss('GSS2018.sav', to.data.frame=TRUE)
write.csv(dataset1, file='GSS2018_Original.csv')