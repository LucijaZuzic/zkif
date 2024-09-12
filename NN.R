# train model with neural networks
NNModel <- train(training, training$Dst_class,
                 method = "nnet",
                 trControl= ctrl,
                 preProcess=c("scale","center"),
                 na.action = na.omit
)

NNPredictions <-predict(NNModel, testing)
# Create confusion matrix
trueclasses <- as.factor(testing$Dst_class)
cmNN <-confusionMatrix(NNPredictions, trueclasses)
print(cmNN)