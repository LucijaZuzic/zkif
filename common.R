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

# Reading the annual observed TEC data at Darwin, NT in 2014 and
# data frame arrangement

iono <- matrix(nrow=0, ncol = 3)
data <- as.data.frame(read.csv('darwin2014.csv', header=TRUE, 
                               sep =',', skip=0))

data <- data[,-1]
summary(data)
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

dataset2 <- dataset[,-c(1,2)]

# Data set reduction by expelling TEC>=300 outliers
iono3 <- dataset2[dataset2$TEC<300,]

#iono3 <- iono3[c(1:8000),]

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
E <- iono3[(iono3$Dst < -85),]

# Adding estimate class (a categorical variable) to the data set
for(i in 1:length(iono3$TEC)){
  if(iono3$Dst[i]>=15){
    Dst_class[i] <- 'P'
  }else if(iono3$Dst[i]< 15 & iono3$Dst[i]>= -20){
    Dst_class[i] <- 'N'
  }else if(iono3$Dst[i]< -20 & iono3$Dst[i]>= -55){
    Dst_class[i] <- 'R'
  }else if(iono3$Dst[i]< -55 & iono3$Dst[i]>= -85){
    Dst_class[i] <- 'T'
  }else if(iono3$Dst[i]< -85){
    Dst_class[i] <- 'E'
  }
}
classdata <- as.data.frame(cbind(iono3, Dst_class))

classdata_no_Dst <- classdata[c("ap", "Bx", "By", "Bz", "TEC", "dTEC", "Dst_class")]
colnames(classdata_no_Dst) <- c("ap", "Bx", "By", "Bz", "TEC", "dTEC", "Dst_class")

classdata_no_TEC <- classdata[c("ap", "Bx", "By", "Bz", "Dst_class")]
colnames(classdata_no_TEC) <- c("ap", "Bx", "By", "Bz", "Dst_class")

classdata_coord <- classdata[c("Bx", "By", "Bz", "Dst_class")]
colnames(classdata_coord) <- c("Bx", "By", "Bz", "Dst_class")

classdata_xy_ap <- classdata[c("ap", "Bx", "By", "Dst_class")]
colnames(classdata_xy_ap) <- c("ap", "Bx", "By", "Dst_class")

classdata_xz_ap <- classdata[c("ap", "Bx", "Bz", "Dst_class")]
colnames(classdata_xz_ap) <- c("ap", "Bx", "Bz", "Dst_class")

classdata_yz_ap <- classdata[c("ap", "By", "Bz", "Dst_class")]
colnames(classdata_yz_ap) <- c("ap", "By", "Bz", "Dst_class")

### Classification model development

library(caret)
library(mlbench)
library(MLmetrics)
#data(Sonar)

# Data set splitting into training and testing set
set.seed(13)
inTrain <- createDataPartition(
  y = classdata$Dst_class,
  ## the outcome data are needed
  p = .8, # partition value: .8 = 80%
  ## The percentage of data in the
  ## training set
  list = FALSE
)

str(inTrain)

training_all <- classdata[ inTrain,]
testing_all  <- classdata[-inTrain,]

training_no_Dst <- classdata_no_Dst[ inTrain,]
testing_no_Dst <- classdata_no_Dst[-inTrain,]
  
training_no_TEC <- classdata_no_TEC[ inTrain,]
testing_no_TEC <- classdata_no_TEC[-inTrain,]
  
training_coord <- classdata_coord[ inTrain,]
testing_coord <- classdata_coord[-inTrain,]

training_xy_ap <- classdata_xy_ap[ inTrain,]
testing_xy_ap <- classdata_xy_ap[-inTrain,]

training_xz_ap <- classdata_xz_ap[ inTrain,]
testing_xz_ap <- classdata_xz_ap[-inTrain,]

training_yz_ap <- classdata_yz_ap[ inTrain,]
testing_yz_ap <- classdata_yz_ap[-inTrain,]

nrow(training_all)
nrow(testing_all)

ctrl <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 10,
  classProbs = TRUE, 
  summaryFunction = multiClassSummary
)