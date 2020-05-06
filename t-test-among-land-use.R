greened = read.csv("data/processed_data/greened_lots_crimes.csv", header = T)
vacant = read.csv("data/processed_data/vacant_lots_crimes_matched_final.csv", header = T)

# calculate differences before and after
greened["diff_100_nv"] = greened$nonviolent_100_after - greened$nonviolent_100_before
greened["diff_200_nv"] = greened$nonviolent_200_after - greened$nonviolent_200_before
greened["diff_500_nv"] = greened$nonviolent_500_after - greened$nonviolent_500_before
greened["diff_100_v"] = greened$violent_100_after - greened$violent_100_before
greened["diff_200_v"] = greened$violent_200_after - greened$violent_200_before
greened["diff_500_v"] = greened$violent_500_after - greened$violent_500_before
greened["diff_100_t"] = greened$diff_100_nv + greened$diff_100_v
greened["diff_200_t"] = greened$diff_200_nv + greened$diff_200_v
greened["diff_500_t"] = greened$diff_500_nv + greened$diff_500_v

vacant["diff_100_nv"] = vacant$nonviolent_100_after - vacant$nonviolent_100_before
vacant["diff_200_nv"] = vacant$nonviolent_200_after - vacant$nonviolent_200_before
vacant["diff_500_nv"] = vacant$nonviolent_500_after - vacant$nonviolent_500_before
vacant["diff_100_v"] = vacant$violent_100_after - vacant$violent_100_before
vacant["diff_200_v"] = vacant$violent_200_after - vacant$violent_200_before
vacant["diff_500_v"] = vacant$violent_500_after - vacant$violent_500_before
vacant["diff_100_t"] = vacant$diff_100_nv + vacant$diff_100_v
vacant["diff_200_t"] = vacant$diff_200_nv + vacant$diff_200_v
vacant["diff_500_t"] = vacant$diff_500_nv + vacant$diff_500_v

colnames(greened)[2] <- "greened_id"
merged = merge(greened, vacant, by="greened_id", suffixes = c(".greened", ".vacant"))
colnames(merged)

# Pull land use data for greened and vacant
greened_attr = read.csv("data/processed_data/greened_lots_attributes.csv")
colnames(greened_attr)[1] <- "greened_id"
colnames(greened_attr)[-1:-2] <- paste(colnames(greened_attr)[-1:-2], ".g", sep="")

vacant_attr = read.csv("data/processed_data/vacant_lots_attributes.csv")
colnames(vacant_attr)[-1:-2] <- paste(colnames(vacant_attr)[-1:-2], ".v", sep="")  
colnames(vacant_attr)[1] <- "vacant_id"

# Inner merge
merged <- merge(merged, greened_attr, by="greened_id")
merged <- merge(merged, vacant_attr, by="vacant_id")

# Start a new dataframe for results

output <- data.frame(matrix(ncol=9, nrow=9*2*8))
colnames(output) <- c('stratum', 'percentile', 't', 'p', 'est', 'se', 'dof', 'type', 'radius')
strata = c("Civic", "Commercial", "Cultural", "Industrial", "Transportation", "Vacant", "Water", "Residential")

# T-test among land use strata
count = 1
for (land_attr in strata) {
  print(land_attr)
  top_cutoff = quantile(c(merged[[paste(land_attr, ".g", sep="")]], merged[[paste(land_attr, ".v", sep="")]]), probs = c(0.25, 0.75))
  
  # Top percentile of strata
  subset_top = merged[merged[,paste(land_attr, ".g", sep="")] >= top_cutoff[2] & merged[,paste(land_attr, ".v", sep="")] >= top_cutoff[2],]
  
  # Total
  t1 <- c(t.test(subset_top$diff_100_t.greened, subset_top$diff_100_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 100)
  t2 <- c(t.test(subset_top$diff_200_t.greened, subset_top$diff_200_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 200)
  t3 <- c(t.test(subset_top$diff_500_t.greened, subset_top$diff_500_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 500)
  
  # Non-violent
  t4 <- c(t.test(subset_top$diff_100_nv.greened, subset_top$diff_100_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 100)
  t5 <- c(t.test(subset_top$diff_200_nv.greened, subset_top$diff_200_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 200)
  t6 <- c(t.test(subset_top$diff_500_nv.greened, subset_top$diff_500_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 500)
  
  # Violent
  t7 <- c(t.test(subset_top$diff_100_v.greened, subset_top$diff_100_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 100)
  t8 <- c(t.test(subset_top$diff_200_v.greened, subset_top$diff_200_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 200)
  t9 <- c(t.test(subset_top$diff_500_v.greened, subset_top$diff_500_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 500)
  
  tests <- list(t1, t2, t3, t4, t5, t6, t7, t8, t9)
  
  for (test in tests) {
    test_row = c(land_attr, 'top_75th', test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12]) 
    output[count, ] <- test_row
    count <- count + 1
  }
  
  # Bottom percentile of strata
  subset_bot = merged[merged[,paste(land_attr, ".g", sep="")] <= top_cutoff[1] & merged[,paste(land_attr, ".v", sep="")] <= top_cutoff[1],]
  
  # Total
  t1 <- c(t.test(subset_bot$diff_100_t.greened, subset_bot$diff_100_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 100)
  t2 <- c(t.test(subset_bot$diff_200_t.greened, subset_bot$diff_200_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 200)
  t3 <- c(t.test(subset_bot$diff_500_t.greened, subset_bot$diff_500_t.vacant, paired = TRUE, alternative = "two.sided"), "total", 500)
  
  # Non-violent
  t4 <- c(t.test(subset_bot$diff_100_nv.greened, subset_bot$diff_100_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 100)
  t5 <- c(t.test(subset_bot$diff_200_nv.greened, subset_bot$diff_200_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 200)
  t6 <- c(t.test(subset_bot$diff_500_nv.greened, subset_bot$diff_500_nv.vacant, paired = TRUE, alternative = "two.sided"), "nonviolent", 500)
  
  # Violent
  t7 <- c(t.test(subset_bot$diff_100_v.greened, subset_bot$diff_100_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 100)
  t8 <- c(t.test(subset_bot$diff_200_v.greened, subset_bot$diff_200_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 200)
  t9 <- c(t.test(subset_bot$diff_500_v.greened, subset_bot$diff_500_v.vacant, paired = TRUE, alternative = "two.sided"), "violent", 500)
  
  tests <- list(t1, t2, t3, t4, t5, t6, t7, t8, t9)
  
  for (test in tests) {
    test_row = c(land_attr, 'bot_25th', test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12]) 
    output[count, ] <- test_row
    count <- count + 1
  }
}

write.csv(output, "data/processed_data/land_use_strata_tests.csv", row.names=FALSE)
