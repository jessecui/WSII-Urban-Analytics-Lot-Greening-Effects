# This repeats propensity scoring and matching, but includes business features as well.

library(MatchIt)
library(ggplot2)
library(caret)
library(cobalt)
library(optmatch)
library(pROC)

set.seed(1)
# ------ Part 1 (Final preprocessing adjustments)

# Todo fixed the total column
greened_data = read.csv("../data/lot_attributes/greened_lots_attributes.csv")
greened_data['greened'] = 1
greened_data$X <- NULL
greened_data$id.1 <- NULL

vacant_data = read.csv("../data/lot_attributes/vacant_lots_attributes.csv")
vacant_data['greened'] = 0
vacant_data$X <- NULL
vacant_data$objectid.1 <- NULL

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


# ------ Part 2 (The official model part) ----------
lots_data_ids <- lots_data['id']

# Drop columns that aren't predictors
# Dropping date and id
lots_data[1:2] <- list(NULL)

# Drop columns that would be bad for dummy variables
# We are dropping columns:
# "Other"
lots_data$Other <- NULL

lots_data$income_to_poverty_over_2.00 <- NULL

# Log the income data to smooth skew
lots_data$block_per_capita_income <- log(lots_data$block_per_capita_income)

# --------- LOGIT REGRESSION ------------------
# Create a logistic regression model on all data
logit_model <- glm(greened ~ ., data = lots_data, family = "binomial")
results_df<-summary(logit_model)$coefficients
write.csv(results_df,"../analysis_results/scoring/model_coefs.csv")
lots_data_results <- lots_data

# Get the confusion matrix
class_percent = sum(lots_data$greened == 1) / nrow(lots_data)

preds_all <- predict(logit_model, newdata = lots_data[, -32], type = "response")
cm_all <- confusionMatrix(table(as.numeric(preds_all>class_percent), reference = lots_data$greened))

lots_data_results$preds_all <- preds_all
g_all <- roc(greened ~ preds_all, data=lots_data_results)

# Create a model on just economic data
logit_model_econ <- glm(greened ~ block_per_capita_income + income_to_poverty_under_.50 + income_to_poverty_.50_to_.99 +income_to_poverty_1.00_to_1.24+income_to_poverty_1.25_to_1.49+income_to_poverty_1.50_to_1.84+income_to_poverty_1.85_to_1.99, data = lots_data, family = "binomial")
summary(logit_model_econ)
preds_econ <- predict(logit_model_econ, newdata = lots_data[, -32], type = "response")
cm_econ <- confusionMatrix(table(as.numeric(preds_econ>class_percent), reference = lots_data$greened))

lots_data_results$preds_econ <- preds_econ
g_econ <- roc(greened ~ preds_econ, data=lots_data_results)

# Create a model on just demographic data
logit_model_demo <- glm(greened ~ block_total_count + white_percent + black_percent + asian_percent + hispanic_percent, data = lots_data, family = "binomial")
summary(logit_model_demo)
preds_demo <- predict(logit_model_demo, newdata = lots_data[, -32], type = "response")
cm_demo <- confusionMatrix(table(as.numeric(preds_demo>class_percent), reference = lots_data$greened))

lots_data_results$preds_demo <- preds_demo
g_demo <- roc(greened ~ preds_demo, data=lots_data_results)

# Create a model on just land use data
logit_model_land <- glm(greened ~ Civic + Commercial + Cultural + Industrial + Transportation + Vacant + Water + Residential, data = lots_data, family = "binomial")
summary(logit_model_land)
preds_land <- predict(logit_model_land, newdata = lots_data[, -32], type = "response")
cm_land <- confusionMatrix(table(as.numeric(preds_land>class_percent), reference = lots_data$greened))

lots_data_results$preds_land <- preds_land
g_land <- roc(greened ~ preds_land, data=lots_data_results)

# Create a model on just business use data
logit_model_bus <- glm(greened ~ cafe + convenience + gym + liquor + lodging + nightlife + pharmacy + restaurant, data = lots_data, family = "binomial")
summary(logit_model_bus)
preds_bus <- predict(logit_model_bus, newdata = lots_data[, -32], type = "response")
cm_bus <- confusionMatrix(table(as.numeric(preds_bus>class_percent), reference = lots_data$greened))

lots_data_results$preds_bus <- preds_bus
g_bus <- roc(greened ~ preds_bus, data=lots_data_results)

# Plot an image for ROC AUC
jpeg(file="../analysis_results/images/scoring/rocs.jpg", width=600, height=600)
plot(g_all)
plot(g_econ, add=TRUE, col='red')
plot(g_demo, add=TRUE, col='blue')
plot(g_land, add=TRUE, col='green')
plot(g_bus, add=TRUE, col='purple')
legend("bottomright",
       c("All","Economic", "Demographic", "Land Use", "Business Vibrancy"),
       fill=c("black", "red","blue", "green", "purple")
)
dev.off()

# Get the data for each
all_data_overall <- cbind(data.frame(cm_all$overall), data.frame(cm_econ$overall), data.frame(cm_demo$overall), data.frame(cm_land$overall), data.frame(cm_bus$overall))
all_data_byClass <- cbind(data.frame(cm_all$byClass), data.frame(cm_econ$byClass), data.frame(cm_demo$byClass), data.frame(cm_land$byClass), data.frame(cm_bus$byClass))
all_data_auc <- cbind(data.frame(g_all$auc), data.frame(g_econ$auc), data.frame(g_demo$auc), data.frame(g_land$auc), data.frame(g_bus$auc))
rownames(all_data_auc)<-"auc"

all_metrics <- rbind(all_data_overall, setNames(all_data_byClass, names(all_data_overall)), setNames(all_data_auc, names(all_data_overall)))
write.csv(all_metrics, "../analysis_results/scoring/all_log_modelling_metrics.csv")

# -------- PROPENSITY SCORING -----------------
# Get logit model scores
propensity_scores = as.data.frame(predict(logit_model, lots_data[, -32], type="response"))
colnames(propensity_scores)[1] <- "score"

# Create a matching algorithm
n <- names(lots_data)
f <- as.formula(paste("greened ~", paste(n[!n %in% "greened"], collapse = " + ")))

variables = colnames(lots_data[, -32])

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

jpeg(file="../analysis_results/images/scoring/matches.jpg", width=720, height=420)
love.plot(mod_match, binary = "std", threshold = 0.2, shapes = c("circle", "triangle"), sample.names = c("Unmatched", "matched"), colors = c("#aaaaaa", "#333333"))
dev.off()

lots_data_with_id <- lots_data
lots_data_with_id['id'] <- lots_data_ids

# Look at matches
matches <- as.data.frame(mod_match$match.matrix)

# Append the match date to vacant lot id
matches["match_greened_date"] <- greened_data['date']
matches["greened_id"] <- greened_data['id']

# Drop the null data
matches = na.omit(matches)

vacant_match_index <- as.numeric(as.vector(unlist(matches['V1'], use.names = FALSE)))

matches["vacant_id"] <- sapply(vacant_match_index, function(x) lots_data_with_id$id[x])

write.csv(matches, "../data/matches/lots_paired_matches.csv")
