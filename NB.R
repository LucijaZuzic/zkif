# Candidate  model 3: nb
# Naive Bayes
# Source: https://topepo.github.io/caret/train-models-by-tag.html
NaiveModel <- train(training, training$Dst_class, 
                    method = "nb",
                    preProcess=c("scale","center"),
                    trControl= ctrl,
                    na.action = na.omit
)

#Predictions
NaivePredictions <-predict(NaiveModel, testing, na.action = na.pass)
trueclasses <- as.factor(testing$Dst_class)
cmNaive <-confusionMatrix(NaivePredictions, trueclasses)
print(cmNaive)