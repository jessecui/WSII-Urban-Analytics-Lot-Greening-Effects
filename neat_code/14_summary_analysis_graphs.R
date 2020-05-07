# This code runs graphs for summary data analysis on the plots
# I.e. this code will plot box and whisker plots comparing characteristics
# between greened and vacant lots.
setwd("~/!Projects/WISE Fellow/WSII-Urban-Analytics-Business-Vibrancy/neat_code")
library(reshape2)
library(ggplot2)
library(plyr)

# Pull Data
data = read.csv("../neat_data/processed_data/all_lots_attributes_with_business_new.csv")
greened_data$greened <- as.factor(greened_data$greened)

# -- Graphs --

# Demograhpic Data
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

ggsave("../analysis_imgs/chart_demog.jpg")

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
ggsave("../analysis_imgs/chart_inc_pov.jpg")

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
ggsave("../analysis_imgs/chart_pci.jpg")

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
ggsave("../analysis_imgs/chart_pop_count.jpg")

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
ggsave("../analysis_imgs/chart_land_use.jpg")

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
ggsave("../analysis_imgs/chart_bus_vib.jpg")

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

ggsave("../analysis_imgs/chart_bus_count.jpg")

# ---- Numeric Attributes Data ----
greened_data <- data[data$greened == 1,]
vacant_data <- data[data$greened == 0,]

green_summary <- t(data.frame(apply(greened_data[,3:35], MARGIN=2, FUN=summary)))
vacant_summary <- t(data.frame(apply(vacant_data[,3:35], MARGIN=2, FUN=summary)))

write.csv(green_summary, "../analysis_results/green_summary.csv")
write.csv(vacant_summary, "../analysis_results/vacant_summary.csv")

# Graph of Greening vs Crimes
greened_data$date <- as.Date(greened_data$date)
greened_data$year <- as.numeric(format(greened_data$date,"%Y"))

greened_year_counts <- data.frame(table(greened_data$year))

crimes_df <- read.csv("../neat_data/cleaned_data/cleaned_crimes.csv")
crimes_df$dispatch_date <- as.Date(crimes_df$dispatch_date)
crimes_df$year <- as.numeric(format(crimes_df$dispatch_date, "%Y"))

crime_year_counts <- data.frame(table(crimes_df$year)[2:12])

year_counts <- cbind(greened_year_counts, crime_year_counts)
colnames(year_counts) <- c("Year", "Greened_Lots", "year2", "Crime_Count")

ggplot(year_counts) + 
  geom_col(aes(x = Year, y = Greened_Lots), size = 1, color = "darkblue", fill = "white") +
  geom_line(aes(x = Year, y = Crime_Count), size = 1.5, color="red", group = 1)

ggplot(year_counts) + 
  geom_col(aes(x = Year, y = Greened_Lots), size = 1, color = "darkblue", fill = "white") +
  geom_line(aes(x = Year, y = Crime_Count/100), size = 1.5, color="red", group = 1) + 
  scale_y_continuous(sec.axis = sec_axis(~.*100, name = "Crime Count"))

ggplot(year_counts) +  + geom_line(aes(color = variable)) + 
  facet_grid(variable ~ ., scales = "free_y") + theme(legend.position = "none")

year_counts$Year <- as.numeric(as.character(year_counts$Year))

p8 <- ggplot(year_counts, aes(Year, Greened_Lots)) + geom_bar(stat="identity") + xlim(2006, 2018) + ylab("Lots Greened")+
  theme(
    axis.text.x = element_text(angle=90),
    axis.text.y = element_text(angle = 90)
  )

p9 <- ggplot(year_counts, aes(Year, Crime_Count)) + geom_line() + xlim(2006, 2018) +ylab("Crimes Occured")+
  theme(
    axis.title.x = element_blank(), 
    axis.text.x = element_blank(),
    axis.text.y = element_text(angle = 90)
  )

require(gridExtra)

jpeg("../analysis_imgs/chart_crime_vs_green_lots.jpg", width=800, height=500)
grid.arrange(p9, p8, ncol = 1, heights = c(1, 1))
dev.off()

ggsave("../analysis_imgs/chart_crime_vs_green_lots.jpg")

write.csv(year_counts, "../analysis_results/crime_vs_greening.csv")

# T-test
vacant <- read.csv("../data/processed_data/vacant_lots_crimes_final.csv")
greened <- read.csv("../neat_data/processed_data/greened_lots_crime_counts.csv")

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

output_all <- data.frame(matrix(ncol=10, nrow=10))
colnames(output_all) <- c('stratum', 'percentile', 't', 'p', 'est_green', 'est_vacant', 'se', 'dof', 'type', 'radius')

t1 <- c(t.test(greened$diff_100_t, vacant$diff_100_t, paired = FALSE, alternative = "two.sided"), "total", 100)
t2 <- c(t.test(greened$diff_200_t, vacant$diff_200_t, paired = FALSE, alternative = "two.sided"), "total", 200)
t3 <- c(t.test(greened$diff_500_t, vacant$diff_500_t, paired = FALSE, alternative = "two.sided"), "total", 500)

# Non-violent
t4 <- c(t.test(greened$diff_100_nv, vacant$diff_100_nv, paired = FALSE, alternative = "two.sided"), "nonviolent", 100)
t5 <- c(t.test(greened$diff_200_nv, vacant$diff_200_nv, paired = FALSE, alternative = "two.sided"), "nonviolent", 200)
t6 <- c(t.test(greened$diff_500_nv, vacant$diff_500_nv, paired = FALSE, alternative = "two.sided"), "nonviolent", 500)

# Violent
t7 <- c(t.test(greened$diff_100_v, vacant$diff_100_v, paired = FALSE, alternative = "two.sided"), "violent", 100)
t8 <- c(t.test(greened$diff_200_v, vacant$diff_200_v, paired = FALSE, alternative = "two.sided"), "violent", 200)
t9 <- c(t.test(greened$diff_500_v, vacant$diff_500_v, paired = FALSE, alternative = "two.sided"), "violent", 500)

tests <- list(t1, t2, t3, t4, t5, t6, t7, t8, t9)
count = 1

for (test in tests) {
  test_row = c('all', 'all', test$statistic, test$p.value, test$estimate, test$stderr, test$parameter, test[11], test[12]) 
  output_all[count, ] <- test_row
  count <- count + 1
}

write.csv(output_all, "../analysis_results/tests_uncontrolled.csv", row.names=FALSE)

# Getting mean crime counts
greened_crimes <- greened[,4:24]
greened_crimes_summary <- t(data.frame(apply(greened_crimes, MARGIN=2, FUN=summary)))
write.csv(greened_crimes_summary, "../analysis_results/green_crimes_summary.csv")

vacant_crimes <- vacant[,4:24]
vacant_crimes_summary <- t(data.frame(apply(vacant_crimes, MARGIN=2, FUN=summary)))
write.csv(vacant_crimes_summary, "../analysis_results/vacant_crimes_summary.csv")

greened_crimes_200 <- greened_crimes[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
greened_crimes_200$greened <- 1


vacant_crimes_200 <- vacant_crimes[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
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
ggsave("../analysis_imgs/chart_crimes_before_match_200.jpg")
