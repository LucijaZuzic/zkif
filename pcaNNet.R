# Candidate  model 6: glmStepAIC
# Flexible Discriminant Analysis
# Source: https://topepo.github.io/caret/train-models-by-tag.html
library(nnet)
fdaModel <- train(Dst_class ~ ., data = training,
                  method = "pcaNNet",
                  trControl= ctrl,
                  preProcess = c("scale","center"),
                  na.action = na.omit
)

fdaPredictions <-predict(fdaModel, testing)
# Create confusion matrix
trueclasses <- as.factor(testing$Dst_class)
cmfda <-confusionMatrix(fdaPredictions, trueclasses)
print(cmfda)

#importance <- varImp(fdaModel, scale=FALSE)
#plot(importance)