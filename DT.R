# Candidate  model 2: C5.0
# Decision Tree C5.0
# Source: https://topepo.github.io/caret/train-models-by-tag.html

DecTreeModel <- train(Dst_class ~ ., data = training, 
                      method = "C5.0",
                      preProcess=c("scale","center"),
                      trControl= ctrl,
                      na.action = na.omit
)

#Predictions
DTPredictions <-predict(DecTreeModel, testing, na.action = na.pass)
# Print confusion matrix and results
trueclasses <- as.factor(testing$Dst_class)
cmTree <-confusionMatrix(DTPredictions, trueclasses)
print(cmTree)