# Candidate  model 5: fda
# Flexible Discriminant Analysis
# Source: https://topepo.github.io/caret/train-models-by-tag.html
library(earth,mda)
fdaModel <- train(Dst_class ~ ., data = training,
                  method = "fda",
                  trControl= ctrl,
                  preProcess = c("pca","scale","center"),
                  na.action = na.omit
)

fdaPredictions <-predict(fdaModel, testing)
# Create confusion matrix
trueclasses <- as.factor(testing$Dst_class)
cmfda <-confusionMatrix(fdaPredictions, trueclasses)
print(cmfda)

#importance <- varImp(SVModel, scale=FALSE)
#plot(importance)