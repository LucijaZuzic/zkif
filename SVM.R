## Development of candidate models 

# Candidate  model 1: svmPoly
# Least Squares Support Vector Machine with Polynomial Kernel
# Source: https://topepo.github.io/caret/train-models-by-tag.html

SVModel <- train(Dst_class ~ ., data = training,
                 method = "svmPoly",
                 trControl= ctrl,
                 tuneGrid = data.frame(degree = 1,
                                       scale = 1,
                                       C = 1),
                 preProcess = c("pca","scale","center"),
                 na.action = na.omit
)

SVMPredictions <-predict(SVModel, testing)
# Create confusion matrix
trueclasses <- as.factor(testing$Dst_class)
cmSVM <-confusionMatrix(SVMPredictions, trueclasses)
print(cmSVM)

#importance <- varImp(SVModel, scale=FALSE)
#plot(importance)