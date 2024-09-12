# Create four models as an ensemble
#library(caretEnsemble)
#library(caret)
#econtrol <- trainControl(method="cv", number=10, 
#                         savePredictions=TRUE, classProbs=TRUE)
#model_list <- caretList(Dst_class ~., data=training,
#                        methodList=c("svmPoly", "nnet", "C5.0", "nb"),
#                        preProcess=c("scale","center"),
#                        trControl = econtrol
#)

#results <- resamples(model_list)
# What is model correlation?
#mcr <-modelCor(results)
#print (mcr)

# Candidate  model 3: nb
# Naive Bayes
# Source: https://topepo.github.io/caret/train-models-by-tag.html

# Candidate  model 4: pls
# Partial Least Squares
# Source: https://topepo.github.io/caret/train-models-by-tag.html

plsFit <- train(
  Dst_class ~ .,
  data = training,
  method = "pls",
  preProc = c("center", "scale"),
  tuneLength = 15,
  trControl = ctrl,
  metric = "ROC"
)
plsFit

ggplot(plsFit)
plsClasses <- predict(plsFit, newdata = testing)
str(plsClasses)

plsProbs <- predict(plsFit, newdata = testing, type = "prob")
head(plsProbs)

trueclasses <- as.factor(testing$Dst_class)
confusionMatrix(data = plsClasses, trueclasses)