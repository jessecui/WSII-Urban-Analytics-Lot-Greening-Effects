greened = read.csv("../data/crime_counts/greened_lots_crime_counts.csv", header = T)
vacant = read.csv("../data/crime_counts/matched_vacant_lots_crime_counts.csv", header = T)

# --------------------------------------------------------------------
# CRIME AND ATTRIBUTES CALCULATIONS
# --------------------------------------------------------------------
# Calculate differences before and after intervention date
for (radii in c(100, 200, 500)) {
  for (crime_type in c("violent", "nonviolent", "total")) {
    column_name = paste(c("diff", radii, crime_type), collapse="_")
    if (crime_type == "violent" || crime_type == "nonviolent") {
      greened[column_name] = greened[paste(c(crime_type, radii, "after"), collapse="_")] - greened[paste(c(crime_type, radii, "before"), collapse="_")]  
      vacant[column_name] = vacant[paste(c(crime_type, radii, "after"), collapse="_")] - vacant[paste(c(crime_type, radii, "before"), collapse="_")]  
    } else if (crime_type == "total") {
      greened[column_name] = greened[paste(c("diff", radii, "violent"), collapse="_")] + greened[paste(c("diff", radii, "nonviolent"), collapse="_")]
      vacant[column_name] = vacant[paste(c("diff", radii, "violent"), collapse="_")] + vacant[paste(c("diff", radii, "nonviolent"), collapse="_")]
    }
  }
  greened[paste(c("total", radii, "before"), collapse="_")] = greened[paste(c("violent", radii, "before"), collapse="_")] + greened[paste(c("nonviolent", radii, "before"), collapse="_")]
  vacant[paste(c("total", radii, "before"), collapse="_")] = vacant[paste(c("violent", radii, "before"), collapse="_")] + vacant[paste(c("nonviolent", radii, "before"), collapse="_")]
}

# Merged the two separate data frames together using the matches
colnames(greened)[2] <- "greened_id"
merged = merge(greened, vacant, by="greened_id", suffixes = c(".greened", ".vacant"))

# Pull attributes data for greened and vacant
greened_attr = read.csv("../data/lot_attributes/greened_lots_attributes.csv")
greened_attr$X <- NULL
colnames(greened_attr)[1] <- "greened_id"
colnames(greened_attr)[-1:-2] <- paste(colnames(greened_attr)[-1:-2], ".g", sep="")

vacant_attr = read.csv("../data/lot_attributes/vacant_lots_attributes.csv")
vacant_attr$X <- NULL
colnames(vacant_attr)[-1:-2] <- paste(colnames(vacant_attr)[-1:-2], ".v", sep="")  
colnames(vacant_attr)[1] <- "vacant_id"

# Merge crime data with the attributes data
merged <- merge(merged, greened_attr, by="greened_id")
merged <- merge(merged, vacant_attr, by="vacant_id")

# --------------------------------------------------------------------
# TESTING (GENERAL)
# --------------------------------------------------------------------
# General testing for crime change differences between greened and ungreened/vacant lots
output_all <- data.frame(matrix(ncol=11, nrow=9))
colnames(output_all) <- c('stratum', 'percentile', 't', 'p', 'est', 'se', 'dof', 'type', 'radius', 'avg_total_bef_vac', 'perc_of_vacant')

tests <- vector("list", 9)
index = 1

for (crime_type in c("violent", "nonviolent", "total")) {
  for (radii in c(100, 200, 500)) {
    crime_col_base = paste(c("diff", radii, crime_type), collapse="_")
    x <- merged[,paste0(crime_col_base, ".greened")]
    y <- merged[,paste0(crime_col_base, ".vacant")] 
    test <- c(t.test(x, y, paired = TRUE, alternative = "two.sided"), crime_type, radii)
    tests[[index]] <- test
    index <- index + 1
  }
}

count = 1
for (test in tests) {
  avg_total_bef_vac = mean(vacant[[paste(c(test[11], test[[12]], 'before'), collapse="_")]])
  perc = test$estimate / avg_total_bef_vac 
  test_row = c('all', 'all', test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12], avg_total_bef_vac, perc) 
  output_all[count, ] <- test_row
  count <- count + 1
}

write.csv(output_all, "../analysis_results/tests/general_t_tests.csv", row.names=FALSE)

# --------------------------------------------------------------------
# TESTING (LAND ZONING)
# --------------------------------------------------------------------
output_land <- data.frame(matrix(ncol=11, nrow=9*2*8))
colnames(output_land) <- c('stratum', 'percentile', 't', 'p', 'est', 'se', 'dof', 'type', 'radius', 'avg_total_bef_vac', 'perc_of_vacant')
strata = c("Civic", "Commercial", "Cultural", "Industrial", "Transportation", "Vacant", "Water", "Residential")

# T-test among land use strata
tests <- vector("list", 9 * 2 * length(strata))
index = 1

for (land_attr in strata) {
  for (subset_type in c("top", "bot")) {
    for (crime_type in c("violent", "nonviolent", "total")) {
      for (radii in c(100, 200, 500)) {
        cutoffs = quantile(c(merged[[paste0(land_attr, ".g")]], merged[[paste0(land_attr, ".v")]]), probs = c(0.25, 0.75))
        
        cutoff_val = 0
        if (subset_type == "top") {
          cutoff_val = cutoffs[2]
        } else if (subset_type == "bot") {
          cutoff_val = cutoffs[1]
        }
        
        if (subset_type == "top") {
          subset = merged[merged[paste0(land_attr, ".g")] >= cutoff_val & merged[paste0(land_attr, ".v")] >= cutoff_val,]  
        } else if (subset_type == "bot") {
          subset = merged[merged[paste0(land_attr, ".g")] <= cutoff_val & merged[paste0(land_attr, ".v")] <= cutoff_val,]
        }
        
        col_base = paste(c("diff", radii, crime_type), collapse="_")
        
        x <- subset[,paste0(col_base, '.greened')]
        y <- subset[,paste0(col_base, '.vacant')]
        
        test <- c(t.test(x, y, paired = TRUE, alternative = "two.sided"), crime_type, radii, subset_type, land_attr)
        tests[[index]] <- test
        index <- index + 1
      }
    }
  }  
}

count = 1
for (test in tests) {
  avg_total_bef_vac = mean(vacant[[paste(c(test[11], test[[12]], 'before'), collapse="_")]])
  perc = test$estimate / avg_total_bef_vac 
  test_row = c(test[14], test[13], test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12], avg_total_bef_vac, perc)
  output_land[count, ] <- test_row
  count <- count + 1
}

write.csv(output_land, "../analysis_results/tests/land_zones_t_tests.csv", row.names=FALSE)

# --------------------------------------------------------------------
# TESTING (BUSINESS)
# --------------------------------------------------------------------
# Start a new data frame for results by stratified by business use
output_business <- data.frame(matrix(ncol=11, nrow=9*2*9))
colnames(output_business) <- c('stratum', 'percentile', 't', 'p', 'est', 'se', 'dof', 'type', 'radius', 'avg_total_bef_vac', 'perc_of_vacant')
strata = c("cafe", "convenience", "gym", "liquor", "lodging", "nightlife", "pharmacy", "restaurant")

# T-test among business attribute strata
tests <- vector("list", 9 * 2 * length(strata))
index = 1

for (business_attr in strata) {
  for (subset_type in c("top", "bot")) {
    for (crime_type in c("violent", "nonviolent", "total")) {
      for (radii in c(100, 200, 500)) {
        cutoffs = c()
        if (business_attr == "business_count") {
          cutoffs = quantile(c(merged[[paste0(business_attr, ".g")]], merged[[paste0(business_attr, ".v")]]), probs = c(0.25, 0.75)) 
        } else {
          cutoffs = c(0,1)
        }
        
        cutoff_val = 0
        if (subset_type == "top") {
          cutoff_val = cutoffs[2]
        } else if (subset_type == "bot") {
          cutoff_val = cutoffs[1]
        }
        
        if (business_attr == "business_count") {
          if (subset_type == "top") {
            subset = merged[merged[paste0(business_attr, ".g")] >= cutoff_val & merged[paste0(business_attr, ".v")] >= cutoff_val,]  
          } else if (subset_type == "bot") {
            subset = merged[merged[paste0(business_attr, ".g")] <= cutoff_val & merged[paste0(business_attr, ".v")] <= cutoff_val,]
          }  
        } else {
          subset = merged[merged[paste0(business_attr, ".g")] == cutoff_val & merged[paste0(business_attr, ".v")] == cutoff_val,]
        }
        
        col_base = paste(c("diff", radii, crime_type), collapse="_")
        
        x <- subset[,paste0(col_base, '.greened')]
        y <- subset[,paste0(col_base, '.vacant')]
        
        test <- c(t.test(x, y, paired = TRUE, alternative = "two.sided"), crime_type, radii, subset_type, business_attr)
        tests[[index]] <- test
        index <- index + 1
      }
    }
  }  
}

count = 1
for (test in tests) {
  avg_total_bef_vac = mean(vacant[[paste(c(test[11], test[[12]], 'before'), collapse="_")]])
  perc = test$estimate / avg_total_bef_vac 
  test_row = c(test[14], test[13], test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12], avg_total_bef_vac, perc)
  output_business[count, ] <- test_row
  count <- count + 1
}

write.csv(output_business, "../analysis_results/tests/business_t_tests.csv", row.names=FALSE)