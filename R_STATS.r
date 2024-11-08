library(readr)
library(dplyr)
library(purrr)
library(tidyr)
library(ggplot2)
library(reshape2)
library(broom)

model_name_list <- c("svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet")
wd_list <- c("all", "no_Dst", "no_TEC", "coord", "xyap", "xzap", "yzap")

if (!file.exists("mcnemar.csv")) {
  values_compare <- list()
  
  for (model_name in model_name_list) {
    for (wd in wd_list) {
      values_compare[[paste0(model_name, "_", wd)]] <- list()
      file_open <- read_csv(paste0(wd, "/", model_name, ".csv"))
      actual <- as.list(file_open$true_classes)
      preds <- as.list(file_open$model_predictions)
      values_compare[[paste0(model_name, "_", wd)]][[1]] <- preds
      
      if (!"actual" %in% names(values_compare)) {
        values_compare[["actual"]] <- list()
        values_compare[["actual"]][[1]] <- actual
      }
      
      for (class_one in 1:5) {
        values_compare[[paste0(model_name, "_", wd)]][[class_one + 1]] <- sapply(preds, function(p) p == class_one)
        values_compare[["actual"]][[class_one + 1]] <- sapply(actual, function(p) p == class_one)
      }
    }
  }
  
  new_data_frame <- data.frame(model1 = character(), model2 = character(), class = integer(), 
                                test_type = character(), correction = logical(), 
                                pvalue = numeric(), statistic = numeric(), stringsAsFactors = FALSE)
  
  list_of_keys <- names(values_compare)
  
  for (model_ix1 in seq_along(list_of_keys)) {
    for (model_ix2 in (model_ix1 + 1):length(list_of_keys)) {
      m1 <- list_of_keys[model_ix1]
      m2 <- list_of_keys[model_ix2]
      a1 <- values_compare[[m1]][[1]]
      a2 <- values_compare[[m2]][[1]]
      matr <- list()
      corr_use <- FALSE
      
      for (class_one in 1:5) {
        matr[[class_one]] <- numeric(5)
        for (class_two in 1:5) {
          val_add <- sum(a1 == class_one & a2 == class_two)
          matr[[class_one]][class_two] <- val_add
          if (val_add <= 4) {
            corr_use <- TRUE
          }
        }
      }
      
      mnc <- mcnemar.test(matrix(unlist(matr), nrow = 2))
      new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = 0, 
                                                          test_type = "correction", correction = corr_use, 
                                                          pvalue = mnc$p.value, statistic = mnc$statistic))
      
      mn <- mcnemar.test(matrix(unlist(matr), nrow = 2, correct = FALSE))
      new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = 0, 
                                                          test_type = "no", correction = corr_use, 
                                                          pvalue = mn$p.value, statistic = mn$statistic))
      
      mnbc <- mcnemar.test(matrix(unlist(matr), nrow = 2, correct = TRUE))
      new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = 0, 
                                                          test_type = "exactcorrection", correction = corr_use, 
                                                          pvalue = mnbc$p.value, statistic = mnbc$statistic))
      
      mnb <- mcnemar.test(matrix(unlist(matr), nrow = 2, correct = FALSE))
      new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = 0, 
                                                          test_type = "exact", correction = corr_use, 
                                                          pvalue = mnb$p.value, statistic = mnb$statistic))
      
      for (class_one in 1:5) {
        a1 <- values_compare[[m1]][[class_one + 1]]
        a2 <- values_compare[[m2]][[class_one + 1]]
        pp <- which(a1 == 1 & a2 == 1)
        nn <- which(a1 == 0 & a2 == 0)
        pn <- which(a1 == 1 & a2 == 0)
        np <- which(a1 == 0 & a2 == 1)
        matr <- matrix(c(length(pp), length(pn), length(np), length(nn)), nrow = 2)
        corr_use <- any(c(length(pp), length(pn), length(np), length(nn)) <= 4)
        
        mnc <- mcnemar.test(matr)
        new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = class_one, 
                                                            test_type = "correction", correction = corr_use, 
                                                            pvalue = mnc$p.value, statistic = mnc$statistic))
        
        mn <- mcnemar.test(matr, correct = FALSE)
        new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = class_one, 
                                                            test_type = "no", correction = corr_use, 
                                                            pvalue = mn$p.value, statistic = mn$statistic))
        
        mnbc <- mcnemar.test(matr, correct = TRUE)
        new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = class_one, 
                                                            test_type = "exactcorrection", correction = corr_use, 
                                                            pvalue = mnbc$p.value, statistic = mnbc$statistic))
        
        mnb <- mcnemar.test(matr, correct = FALSE)
        new_data_frame <- rbind(new_data_frame, data.frame(model1 = m1, model2 = m2, class = class_one, 
                                                            test_type = "exact", correction = corr_use, 
                                                            pvalue = mnb$p.value, statistic = mnb$statistic))
      }
    }
  }
  
  write_csv(new_data_frame, "mcnemar.csv")
} else {
  dfnew <- read_csv("mcnemar.csv")
}

ix_dfnew <- c()
ix_dfnew_unfiltered <- c()
dicti_model <- setNames(vector("list", length(model_name_list)), model_name_list)
dict_wd <- setNames(vector("list", length(wd_list)), wd_list)
dict_class <- setNames(vector("list", 6), 0:5)
pvcls <- list()
allpv <- list()
allpvno <- list()
allpok <- list()
allpsignificant <- list()

for (ix in seq_len(nrow(dfnew))) {
  m1 <- dfnew$model1[ix]
  m2 <- dfnew$model2[ix]
  cls <- dfnew$class[ix]
  t <- dfnew$test_type[ix]
  c <- dfnew$correction[ix]
  p <- dfnew$pvalue[ix]
  
  if (!m1 %in% names(allpv)) {
    allpv[[m1]] <- list()
  }
  if (!m2 %in% allpv[[m1]]) {
    allpv[[m1]][[m2]] <- list()
  }
  allpv[[m1]][[m2]] <- append(allpv[[m1]][[m2]], list(c(cls, t, c, p)))
  
  if (!m2 %in% names(allpv)) {
    allpv[[m2]] <- list()
  }
  if (!m1 %in% allpv[[m2]]) {
    allpv[[m2]][[m1]] <- list()
  }
  allpv[[m2]][[m1]] <- append(allpv[[m2]][[m1]], list(c(cls, t, c, p)))
  
  if (grepl("all", m1) || grepl("all", m2)) {
    next
  }
  
  if (!m1 %in% names(allpvno)) {
    allpvno[[m1]] <- list()
  }
  if (!m2 %in% allpvno[[m1]]) {
    allpvno[[m1]][[m2]] <- list()
  }
  allpvno[[m1]][[m2]] <- append(allpvno[[m1]][[m2]], list(c(cls, t, c, p)))
  
  if (!m2 %in% allpvno) {
    allpvno[[m2]] <- list()
  }
  if (!m1 %in% allpvno[[m2]]) {
    allpvno[[m2]][[m1]] <- list()
  }
  allpvno[[m2]][[m1]] <- append(allpvno[[m2]][[m1]], list(c(cls, t, c, p)))
  
  if (cls != 0) {
    next
  }
  
  if (grepl("exact", t)) {
    next
  }
  
  if (grepl("correction", t) && !c) {
    next
  }
  
  if (!grepl("correction", t) && c) {
    next
  }
  
  if (!m1 %in% names(allpok)) {
    allpok[[m1]] <- list()
  }
  if (!m2 %in% allpok[[m1]]) {
    allpok[[m1]][[m2]] <- list()
  }
  allpok[[m1]][[m2]] <- append(allpok[[m1]][[m2]], list(c(cls, t, c, p)))
  
  if (!m2 %in% allpok) {
    allpok[[m2]] <- list()
  }
  if (!m1 %in% allpok[[m2]]) {
    allpok[[m2]][[m1]] <- list()
  }
  allpok[[m2]][[m1]] <- append(allpok[[m2]][[m1]], list(c(cls, t, c, p)))
  
  ix_dfnew_unfiltered <- c(ix_dfnew_unfiltered, ix)
  
  if (p < 0.05 / (21 * 43)) {
    next
  }
  
  if (!m1 %in% names(allpsignificant)) {
    allpsignificant[[m1]] <- list()
  }
  if (!m2 %in% allpsignificant[[m1]]) {
    allpsignificant[[m1]][[m2]] <- list()
  }
  allpsignificant[[m1]][[m2]] <- append(allpsignificant[[m1]][[m2]], list(c(cls, t, c, p)))
  
  if (!m2 %in% allpsignificant) {
    allpsignificant[[m2]] <- list()
  }
  if (!m1 %in% allpsignificant[[m2]]) {
    allpsignificant[[m2]][[m1]] <- list()
  }
  allpsignificant[[m2]][[m1]] <- append(allpsignificant[[m2]][[m1]], list(c(cls, t, c, p)))
  
  ix_dfnew <- c(ix_dfnew, ix)
  
  if (!m1 %in% names(pvcls)) {
    pvcls[[m1]] <- list()
  }
  if (!m2 %in% pvcls[[m1]]) {
    pvcls[[m1]][[m2]] <- list()
  }
  pvcls[[m1]][[m2]] <- append(pvcls[[m1]][[m2]], list(c(cls, t, c, p)))
  
  dict_class[[cls + 1]] <- c(dict_class[[cls + 1]], ix)
  
  for (m in model_name_list) {
    if (grepl(m, m1) && grepl(m, m2)) {
      dicti_model[[m]] <- c(dicti_model[[m]], ix)
    }
  }
  
  for (wd in wd_list) {
    if (grepl(wd, m1) && grepl(wd, m2)) {
      dict_wd[[wd]] <- c(dict_wd[[wd]], ix)
    }
  }
  
  s <- dfnew$statistic[ix]
}

print(length(ix_dfnew))
print(length(ix_dfnew_unfiltered))

for (m in model_name_list) {
  if (m != "nb") {
    next
  }
  pvs <- unique(unlist(lapply(dicti_model[[m]], function(ix) {
    m1 <- dfnew$model1[ix]
    m2 <- dfnew$model2[ix]
    c(m1, m2)
  })))
  
  for (p in pvs) {
    print(p[1], p[2], pvcls[[p[1]]][[p[2]]])
  }
}

for (wd in wd_list) {
  if (wd != "no_Dst") {
    next
  }
  pvs <- unique(unlist(lapply(dict_wd[[wd]], function(ix) {
    m1 <- dfnew$model1[ix]
    m2 <- dfnew$model2[ix]
    c(m1, m2)
  })))
  
  for (p in pvs) {
    print(p[1], p[2], pvcls[[p[1]]][[p[2]]])
  }
}

for (wd in wd_list) {
  if (grepl("all", wd)) {
    next
  }
  
  df_new_unfiltered <- list(best = list())
  for (t in unique(dfnew$test_type)) {
    df_new_unfiltered[[t]] <- list()
  }
  
  tick_labels <- c()
  for (m1 in names(allpvno)) {
    if (!grepl(wd, m1)) {
      next
    }
    tick_labels <- c(tick_labels, strsplit(m1, "_")[[1]][1])
    for (t in names(df_new_unfiltered)) {
      df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- list()
    }
    for (m2 in names(allpvno)) {
      if (!grepl(wd, m2)) {
        next
      }
      if (m1 != m2) {
        for (val in allpvno[[m1]][[m2]]) {
          cls <- val[1]
          t <- val[2]
          c <- val[3]
          p <- val[4]
          if (cls) {
            next
          }
          if (val %in% allpok[[m1]][[m2]]) {
            df_new_unfiltered$best[[length(df_new_unfiltered$best) + 1]] <- p
          }
          df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- p
        }
      } else {
        for (t in names(df_new_unfiltered)) {
          df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- 1.0
        }
      }
    }
  }
  
  for (t in names(df_new_unfiltered)) {
    print(length(df_new_unfiltered[[t]]), length(df_new_unfiltered[[t]][[1]]))
  }
  
  ggplot() + 
    geom_tile(data = melt(df_new_unfiltered$best), aes(x = Var1, y = Var2, fill = value)) +
    ggtitle(wd) +
    scale_x_discrete(labels = tick_labels) +
    scale_y_discrete(labels = tick_labels) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    geom_text(aes(label = round(value, 2)), color = "white")
}

for (m in model_name_list) {
  df_new_unfiltered <- list(best = list())
  for (t in unique(dfnew$test_type)) {
    df_new_unfiltered[[t]] <- list()
  }
  
  tick_labels <- c()
  for (m1 in names(allpvno)) {
    if (!grepl(m, m1)) {
      next
    }
    tick_labels <- c(tick_labels, gsub(paste0(m, "_"), "", m1))
    for (t in names(df_new_unfiltered)) {
      df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- list()
    }
    for (m2 in names(allpvno)) {
      if (!grepl(m, m2)) {
        next
      }
      if (m1 != m2) {
        for (val in allpvno[[m1]][[m2]]) {
          cls <- val[1]
          t <- val[2]
          c <- val[3]
          p <- val[4]
          if (cls) {
            next
          }
          if (val %in% allpok[[m1]][[m2]]) {
            df_new_unfiltered$best[[length(df_new_unfiltered$best) + 1]] <- p
          }
          df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- p
        }
      } else {
        for (t in names(df_new_unfiltered)) {
          df_new_unfiltered[[t]][[length(df_new_unfiltered[[t]]) + 1]] <- 1.0
        }
      }
    }
  }
  
  for (t in names(df_new_unfiltered)) {
    print(length(df_new_unfiltered[[t]]), length(df_new_unfiltered[[t]][[1]]))
  }
  
  ggplot() + 
    geom_tile(data = melt(df_new_unfiltered$best), aes(x = Var1, y = Var2, fill = value)) +
    ggtitle(m) +
    scale_x_discrete(labels = tick_labels) +
    scale_y_discrete(labels = tick_labels) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    geom_text(aes(label = round(value, 2)), color = "white")
}

