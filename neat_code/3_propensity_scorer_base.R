# This file creates a propensity scorer based on attributes data
# Note, this is for data without business attributes (i.e. only demographic, economic and land use.)

# Author: Jesse Cui

library(MatchIt)
library(ggplot2)
library(caret)
library(cobalt)
library(optmatch)
library(stargazer)
library(broom)

set.seed(1)
# ------ Part 1 (Final preprocessing adjustments)

# Todo fixed the total column
greened_data = read.csv("../neat_data/processed_data/greened_lots_attr_new.csv")
greened_data['greened'] = 1

vacant_data = read.csv("../neat_data/processed_data/vacant_lots_attr_new.csv")
vacant_data['greened'] = 0

# Consistent naming
colnames(greened_data)[1] <- "id"
colnames(greened_data)[2] <- "date" 
colnames(vacant_data)[1] <- "id"
colnames(vacant_data)[2] <- "date"

# Stack dataframes on top of each other
lots_data <- rbind(greened_data, vacant_data)

# Drop Missing Data
lots_data <- lots_data[complete.cases(lots_data),]

# Select only White, Black, Asian, and Hispanic for demographic data
lots_data[,c(13,16,18:20,22:28)] <- list(NULL)

# Rename long columns and save
colnames(lots_data)[12] <- "block_total_count"
colnames(lots_data)[13] <- "white_percent"
colnames(lots_data)[14] <- "black_percent"
colnames(lots_data)[15] <- "asian_percent"
colnames(lots_data)[16] <- "hispanic_percent"
colnames(lots_data)[17] <- "block_per_capita_income"

write.csv(lots_data, "../neat_data/processed_data/all_lots_attributes_new.csv", row.names=FALSE)

# ------ Part 2 (The official model part) ----------
lots_data = read.csv("../neat_data/processed_data/all_lots_attributes_new.csv")
lots_data_ids <- lots_data['id']

# Drop columns that aren't predictors
# Dropping date and id
lots_data[1:2] <- list(NULL)

# Drop columns that would be bad for dummy variables
# We are dropping columns:
# "Other"
lots_data[,c(5)] <- list(NULL)

# "income_to_poverty_over_2.00"
lots_data[,c(21)] <- list(NULL)

# Log the income data to smoothen skew
lots_data[, 14] <- log(lots_data[, 14])

# --------- LOGIT REGRESSION ------------------
# Create a logistic regression model on all data
logit_model <- glm(greened ~ ., data = lots_data, family = "binomial")
summary(logit_model)

# Get the confusion matrix
class_percent = sum(lots_data$greened == 1) / nrow(lots_data)

preds <- predict(logit_model, newdata = lots_data[, -21], type = "response")
confusionMatrix(table(as.numeric(preds>class_percent), reference = lots_data$greened))

# Create a model on just economic data
logit_model_econ <- glm(greened ~ block_per_capita_income, data = lots_data, family = "binomial")
summary(logit_model_econ)
preds <- predict(logit_model_econ, newdata = lots_data[, -21], type = "response")
confusionMatrix(table(as.numeric(preds>class_percent), reference = lots_data$greened))

# Create a model on just demographic data
logit_model_demo <- glm(greened ~ block_total_count + white_count + black_count + asian_count + hispanic_count, data = lots_data, family = "binomial")
summary(logit_model_demo)
preds <- predict(logit_model_demo, newdata = lots_data[, -21], type = "response")
confusionMatrix(table(as.numeric(preds>class_percent), reference = lots_data$greened))

# Create a model on just land use data
logit_model_land <- glm(greened ~ Civic + Commercial + Cultural + Industrial + Transportation + Vacant + Water + Residential, data = lots_data, family = "binomial")
summary(logit_model_land)
preds <- predict(logit_model_land, newdata = lots_data[, -21], type = "response")
confusionMatrix(table(as.numeric(preds>class_percent), reference = lots_data$greened))

# Get data on all, but using the 0.5 probability decision boundary
preds <- predict(logit_model, newdata = lots_data[, -21], type = "response")
confusionMatrix(table(as.numeric(preds>0.5), reference = lots_data$greened))

# -------- PROPENSITY SCORING -----------------

# Get logit model scores
propensity_scores = as.data.frame(predict(logit_model, lots_data[, -21], type="response"))
colnames(propensity_scores)[1] <- "score"

# Create a matching algorithm
n <- names(lots_data)
f <- as.formula(paste("greened ~", paste(n[!n %in% "greened"], collapse = " + ")))

variables = colnames(lots_data[, -21])

lots_data2 = lots_data[1:nrow(lots_data),]

# Single match
mod_match <- matchit(f,
                     method = "nearest", 
                     data = lots_data2,
                     caliper = 0.2,
                     mahvars=variables,
                     distance=propensity_scores$score)

match_results <- summary(mod_match)

# Make a love plot of the data
set.cobalt.options(binary = "std")
love.plot(mod_match, binary = "std", threshold = 0.2, shapes = c("circle", "triangle"), sample.names = c("Unmatched", "matched"), colors = c("#aaaaaa", "#333333"))

lots_data_with_id <- lots_data
lots_data_with_id['id'] <- lots_data_ids

# Look at matches
matches <- as.data.frame(mod_match$match.matrix)

# Append the match date to vacant lot id
matches["match_greened_date"] <- greened_data['date']
matches["greened_id"] <- greened_data['id']

# Drop the null data
matches = na.omit(matches)

vacant_match_index <- as.numeric(as.vector(unlist(matches['1'], use.names = FALSE)))

matches["vacant_id"] <- sapply(vacant_match_index, function(x) lots_data_with_id$id[x])

write.csv(matches, "../neat_data/processed_data/lot_paired_matches_new.csv")

