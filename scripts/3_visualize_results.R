library(ggplot2)
library(gridExtra)
library(grid)
library(gtable)
library(reshape2)

# -----------------------------------------------
# PLOTS BY STRATA (LAND USE AND BUSINESS)
# -----------------------------------------------
all_tests = read.csv("../analysis_results/tests/general_t_tests.csv")

# EFFECTS BY LAND USE:
segment_tests = read.csv("../analysis_results/tests/land_zones_t_tests.csv")
segment_tests$is_signif = segment_tests$p <= 0.05

for (crime_radius in c(100, 200, 500)) {
  # Get the relevant scores for the crimes
  sub_tests = subset(segment_tests, type == "total" & radius == crime_radius)
  all_relevant_scores = subset(all_tests, type == "total" & radius == crime_radius)
  
  # Plot the stratum scores
  p <- ggplot(sub_tests, aes(est, stratum))
  p <- p + geom_point(aes(colour = factor(percentile), shape = factor(is_signif), size=5)) + guides(size=FALSE)+
    scale_color_manual(labels = c("25th", "75th"), values=c('#aaaaaa','#111111'))+
    scale_shape_manual(labels = c("False", "True"), values=c(1, 16))
  
  # Mark the line for the basic score
  p <- p + geom_vline(xintercept = all_relevant_scores$est)
  p <- p + labs(y ="Land Use", x = "Effect on Total Crime", shape = "Is Significant", color="Percentile")
  p
  
  filename <- paste0("../analysis_results/images/crimes/land_use_effects_", "total", "_", crime_radius, ".png")
  
  ggsave(filename, width = 6, height = 4)
}

# EFFECTS BY BUSINESS STRATA:
segment_tests = read.csv("../analysis_results/tests/business_t_tests.csv")
segment_tests$is_signif = segment_tests$p <= 0.05

for (crime_radius in c(100, 200, 500)) {
  # Get the relevant scores for the crimes
  sub_tests = subset(segment_tests, type == "total" & radius == crime_radius)
  all_relevant_scores = subset(all_tests, type == "total" & radius == crime_radius)
  
  # Plot the stratum scores
  p <- ggplot(sub_tests, aes(est, stratum))
  p <- p + geom_point(aes(colour = factor(percentile), shape = factor(is_signif), size=5)) + guides(size=FALSE)+
    scale_color_manual(labels = c("Absent", "Present"), values=c('#aaaaaa','#111111'))+
    scale_shape_manual(labels = c("False", "True"), values=c(1, 16))
  
  # Mark the line for the basic score
  p <- p + geom_vline(xintercept = all_relevant_scores$est)
  p <- p + labs(y ="Business Type", x = "Effect on Total Crime", shape = "Is Significant", color="Presence of Type")
  p <- p + scale_y_discrete(labels=c("restaurant" = "Restaurant", "pharmacy" = "Pharmacy",
                                     "nightlife" = "Nightlife", "lodging" = "Lodging", "liquor" = "Liquor", "gym" = "Gym", "convenience" = "Convenience", "cafe" = "Cafe", "business_count"="Business Count"))
  
  p
  
  filename <- paste0("../analysis_results/images/crimes/business_effects_", "total", "_", crime_radius, ".png")
  
  ggsave(filename, width = 6, height = 4)
}

# -----------------------------------------------
# DISTRIBUTION OF VIOLENT VS. NON-VIOLENT CRIMES FOR UNCONTROLLED LAND PLOTS
# -----------------------------------------------

# T-test
vacant <- read.csv("../data/crime_counts/unmatched_vacant_lots_crime_counts.csv")
greened <- read.csv("../data/crime_counts/greened_lots_crime_counts.csv")

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

output <- data.frame(matrix(ncol=10, nrow=9))
colnames(output) <- c('stratum', 'percentile', 't', 'p', 'est_green', 'est_vacant', 'se', 'dof', 'type', 'radius')

tests <- vector("list", 9)
index = 1

for (crime_type in c("violent", "nonviolent", "total")) {
  for (radii in c(100, 200, 500)) {
    crime_col_base = paste(c("diff", radii, crime_type), collapse="_")
    x <- greened[,crime_col_base]
    y <- vacant[,crime_col_base] 
    test <- c(t.test(x, y, paired = FALSE, alternative = "two.sided"), crime_type, radii)
    tests[[index]] <- test
    index <- index + 1
  }
}

count = 1
for (test in tests) {
  test_row = c('all', 'all', test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12]) 
  output[count, ] <- test_row
  count <- count + 1
}

write.csv(output, "../analysis_results/tests/unmatched_t_tests.csv", row.names=FALSE)

# Save summary data about plots
greened_crimes <- greened[,4:27]
greened_crimes_summary <- t(data.frame(apply(greened_crimes, MARGIN=2, FUN=summary)))
write.csv(greened_crimes_summary, "../analysis_results/summary/green_crimes_summary.csv")

vacant_crimes <- vacant[,3:26]
vacant_crimes_summary <- t(data.frame(apply(vacant_crimes, MARGIN=2, FUN=summary)))
write.csv(vacant_crimes_summary, "../analysis_results/summary/vacant_crimes_summary.csv")

# Create a box plot comparing crime before and after
greened_crimes_200 <- greened[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
greened_crimes_200$greened <- 1

vacant_crimes_200 <- vacant[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
vacant_crimes_200$greened <- 0

# Chart box plots of crimes before and after for 200m radius
crimes_200m <- melt(rbind(greened_crimes_200, vacant_crimes_200), id="greened")

# Plot
p11 <- ggplot(crimes_200m, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Crime Count",x = "Crime Type") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)"))+
  scale_x_discrete(labels=c("Violent Before", "Violent After", "Non-Violent Before", "Non-Violent After"))
p11
ggsave("../analysis_results/images/crimes/chart_crimes_unmatched_200_meters.jpg")

# ----------------------------------------------------------------------------------------------
# PLOTS OF ATTRIBUTES OF LOTS
# ----------------------------------------------------------------------------------------------
greened_attr = read.csv("../data/lot_attributes/greened_lots_attributes.csv")[,4:49]
vacant_attr = read.csv("../data/lot_attributes/vacant_lots_attributes.csv")[,4:49]

greened_attr$greened = 1
vacant_attr$greened = 0

colnames(vacant_attr) = colnames(greened_attr)
data <- rbind(greened_attr, vacant_attr)

colnames(data)[12] <- "white_percent"
colnames(data)[13] <- "black_percent"
colnames(data)[15] <- "asian_percent"
colnames(data)[19] <- "hispanic_percent"

# -----------------------------------------------
# DEMOGRAPHIC DATA
# -----------------------------------------------
demo_data <- melt(data[c("white_percent", "black_percent", "asian_percent", "hispanic_percent", "greened")], id="greened")

# Plot
p1 <- ggplot(demo_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Proportion",x = "Demographic") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)")) +
  scale_x_discrete(labels=rev(c("hispanic", "asian", "black", "white")))
p1

ggsave("../analysis_results/images/lot_attributes/chart_demog.jpg")

# Economic Income to Poverty data
econ_itp_data <- melt(data[c("income_to_poverty_under_.50", "income_to_poverty_.50_to_.99", "income_to_poverty_1.00_to_1.24", "income_to_poverty_1.25_to_1.49", "income_to_poverty_1.50_to_1.84", "income_to_poverty_1.85_to_1.99", "income_to_poverty_over_2.00", "greened")], id="greened")
p2 <- ggplot(econ_itp_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Proportion",x = "Income to Poverty Ratio") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)")) +
  scale_x_discrete(labels=rev(c("Over 2.00", "1.85 to 1.99", "1.50 to 1.85", "1.25 to 1.49", "1.00 to 1.24", ".50 to .99", "under .50")))
p2

ggsave("../analysis_results/images/lot_attributes/chart_inc_pov.jpg")

# Economic Per Capita Income Data
econ_pci_data <- melt(data[c("block_per_capita_income","greened")], id="greened")
p3 <- ggplot(econ_pci_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Per Capita Income",x = "") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)")) +
  theme(aspect.ratio = 1)+
  scale_x_discrete(labels=c(""))

p3
ggsave("../analysis_results/images/lot_attributes/chart_pci.jpg")

# Population Count
pop_data <- melt(data[c("block_total_count","greened")], id="greened")
p4 <- ggplot(pop_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Population",x = "") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)"))+
  theme(aspect.ratio = 1)+
  scale_x_discrete(labels=c("")) 

p4
ggsave("../analysis_results/images/lot_attributes/chart_pop_count.jpg")

# Land Use Proportions
land_data = melt(data[c("Civic", "Commercial", "Cultural", "Industrial", "Other", "Transportation", "Vacant", "Water", "Residential", "greened")], id="greened")
p5 <- ggplot(land_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Proportion",x = "") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)")) +
  scale_x_discrete(labels=rev(c("Residential", "Water", "Vacant", "Transportation", "Other", "Industrial", "Cultural/Park", "Commercial", "Civic/Inst")))

p5
ggsave("../analysis_results/images/lot_attributes/chart_land_use.jpg")

# Business Vibrancy
business_data = melt(data[c("convenience", "gym", "institution", "liquor", "lodging", "nightlife", "pharmacy", "restaurant", "retail", "greened")], id="greened")

business_prop_data <- aggregate(value ~ variable + greened, business_data, mean)

p6 <- ggplot(business_prop_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_bar(stat="identity", position=position_dodge()) + 
  labs(y="Proportion",x = "Business Type") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)"))

p6
ggsave("../analysis_results/images/lot_attributes/chart_bus_vib.jpg")

# Business Count
bus_count_data <- melt(data[c("business_count","greened")], id="greened")
p7 <- ggplot(bus_count_data, aes(x=variable,y=value,fill=factor(greened))) +
  geom_boxplot() + 
  labs(y="Business Count",x = "") + 
  scale_fill_manual(values=c("royalblue1", "springgreen2"),
                    name="Lot Type",
                    labels=c("Untreated (Vacant)", "Treated (Greened)"))+
  theme(aspect.ratio = 1)+
  scale_x_discrete(labels=c("")) 

p7

ggsave("../analysis_results/images/lot_attributes/chart_bus_count.jpg")

# ---- Numeric Attributes Data ----
greened_data <- data[data$greened == 1,]
vacant_data <- data[data$greened == 0,]

green_summary <- t(data.frame(apply(greened_data[,3:35], MARGIN=2, FUN=summary)))
vacant_summary <- t(data.frame(apply(vacant_data[,3:35], MARGIN=2, FUN=summary)))

write.csv(green_summary, "../analysis_results/summary/green_summary.csv")
write.csv(vacant_summary, "../analysis_results/summary/vacant_summary.csv")