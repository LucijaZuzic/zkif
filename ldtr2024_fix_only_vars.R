rm(list=ls())

#Set path to the working directory containing:
#1. INTERMAGNET data set - to be taken from the INTERMAGNET web-site, and reformatted 
#accordingly - #reformatted original data enclosed
#2. TEC data set, as derived from the RINEX GPS observations using 
# GPS TEC software - enclosed

library(tidyverse)
getCurrentFileLocation <-  function()
{
    this_file <- commandArgs() %>% 
    tibble::enframe(name = NULL) %>%
    tidyr::separate(col=value, into=c("key", "value"), sep="=", fill='right') %>%
    dplyr::filter(key == "--file") %>%
    dplyr::pull(value)
    if (length(this_file)==0)
    {
      this_file <- rstudioapi::getSourceEditorContext()$path
    }
    return(dirname(this_file))
}

setwd(getCurrentFileLocation())

#Declaration of the R libraries utilised

library(data.table)
library(DataExplorer)
library(corrplot)
library(lubridate)
library(fitdistrplus)
library(weird)

oldw <- getOption("warn")
options(warn = -1)

sink("data_vars.txt")

# Reading the annual observed TEC data at Darwin, NT in 2014 and
# data frame arrangement

iono <- matrix(nrow=0, ncol = 3)
data <- as.data.frame(read.csv('darwin2014.csv', header=TRUE, 
                               sep =',', skip=0))

data <- data[,-1]
print(summary(data))
pe <- data[data$min==0 & data$sec==0,]

# Reading the annual estimated Dst and ap data in 2014 and
# data frame arrangement

geo <- as.data.frame(read.csv('Dstap2014.dat',header=FALSE,sep=''))
colnames(geo) <- c('year','DOY','hr','Dst','ap')
summary(geo)

# Merging TEC and Dst&ap data frames
dataset <- merge(pe, geo, by = c('DOY', 'hr'))
dataset <- dataset[,-c(3,4,10)]
summary(dataset)

# Exloratory analysis of observations per variables
plot_histogram(dataset, title = 'over-all TEC')
dev.copy(pdf, "allTEC.pdf")
dev.off()
# Data set reduction by expelling TEC>=300 outliers
iono2 <- dataset[dataset$TEC<300,]
iono2 <- dataset[c(1:8000),]
plot_histogram(iono2, title = 'TEC<300')
dev.copy(pdf, "300TEC.pdf")
dev.off()
#boxplot(dataset, col = 'red', names = c('overall TEC','TEC<200'), 
#ylab='values [TECU]', cex.axis=1.5, cex.lab=1.5)
dataset2 <- dataset[,-c(1,2)]
plot_correlation(dataset2, maxcat = 5L)
dev.copy(pdf, "correlation.pdf")
dev.off()
#Box-plots per Dst values, source of the classification criteria
plot_boxplot(dataset2, by = "Dst")
dev.copy(pdf, "dataset2boxplot.pdf")
dev.off()
iono3 <- iono2[,-c(1,2)]
plot_boxplot(iono3, by = "Dst")
dev.copy(pdf, "iono3boxplot.pdf")
dev.off()
plot_scatterplot(dataset2, by = 'TEC', sampled_rows = 1000L)
dev.copy(pdf, "dataset2scatterplot.pdf")
dev.off()
plot_scatterplot(iono3, by = 'Dst', sampled_rows = 1000L)
dev.copy(pdf, "iono3scatterplot.pdf")
dev.off()

### Dst-based classification under the following rule:
# 15 ... 50 positive phase of the storm -> P
# -20 ... 15 normal -> N
# -55 ... -20 recovery phase (mostly) -> R
# -85 ... -55 through -> T
# -120 ... -85 extreme -> E

Dst_class <- character()
P <- iono3[iono3$Dst >= 15,]
N <- iono3[(iono3$Dst < 15 & iono3$Dst >= -20),]
R <- iono3[(iono3$Dst < (-20) & iono3$Dst >= (-55)),]
T <- iono3[(iono3$Dst < (-55) & iono3$Dst >= (-85)),]
E <- iono3[(iono3$Dst <= -85),]