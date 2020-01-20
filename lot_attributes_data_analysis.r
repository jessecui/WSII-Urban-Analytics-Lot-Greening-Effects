library(reshape2)
library(ggplot2)
library(plyr)
# This file creates graphs for the economic, demographic, and land use data
# for both greened and vacant lots

greened_data = read.csv("data/processed_data/greened_lots_attributes.csv")
vacant_data = read.csv("data/processed_data/vacant_lots_attributes.csv")
vacant_data <- vacant_data[which(vacant_data$Civic > 0),] # Deletes bad outlier

land_greened_data <- greened_data[c(3:11)]
land_greened_data$greened<-"greened"

land_vacant_data <- vacant_data[c(3:11)]
land_vacant_data$greened<-"not greened"

land_data <- rbind(land_greened_data, land_vacant_data)

# Zone Proportion Data
melted_land_data <- melt(land_data, id=c("greened"))
p <- ggplot(melted_land_data, aes(x=reorder(variable, desc(variable)), y=value, fill=greened)) + 
        geom_boxplot() + 
        labs(y="Proportion", x = "Land Use Category") +
        scale_fill_manual(values=c("chartreuse", "firebrick1"))
p + coord_flip()
ggsave("img/land_use_proportions.jpg")


# Demographic and Economic Data
#Nonhispanic Data
nh_greened_data <- greened_data[c(13:20)]
nh_greened_data$greened<-"greened"

nh_vacant_data <- vacant_data[c(13:20)]
nh_vacant_data$greened<-"not greened"

nh_data <- rbind(nh_greened_data, nh_vacant_data)

melted_nh_data <- melt(nh_data, id=c("greened"))
p <- ggplot(melted_nh_data, aes(x=reorder(variable, desc(variable)), y=value, fill=greened)) + 
        geom_boxplot() + 
        labs(y="Proportion",x = "Demographic") +
        scale_fill_manual(values=c("chartreuse", "firebrick1")) +
        scale_x_discrete(labels=c("Two or More Races", 
                                  "Some Other Race", 
                                  "Native Hawaiian and Other Pacific Islander", 
                                  "Asian",
                                  "American Indian and Alaska Native",
                                  "Black or African American",
                                  "White",
                                  "Total Not Hispanic or Latino"))
p + coord_flip()
ggsave("img/demographic/not_hispanic_demographic_proportions.jpg")

# Hispanic Data
h_greened_data <- greened_data[c(21:28)]
h_greened_data$greened<-"greened"

h_vacant_data <- vacant_data[c(21:28)]
h_vacant_data$greened<-"not greened"

h_data <- rbind(h_greened_data, h_vacant_data)

melted_h_data <- melt(h_data, id=c("greened"))
p <- ggplot(melted_h_data, aes(x=reorder(variable, desc(variable)), y=value, fill=greened)) + 
        geom_boxplot() + 
        labs(y="Proportion",x = "Demographic") +
        scale_fill_manual(values=c("chartreuse", "firebrick1")) +
        scale_x_discrete(labels=c("Two or More Races", 
                                  "Some Other Race", 
                                  "Native Hawaiian and Other Pacific Islander", 
                                  "Asian",
                                  "American Indian and Alaska Native",
                                  "Black or African American",
                                  "White",
                                  "Total Hispanic or Latino"))
p + coord_flip()
ggsave("img/demographic/hispanic_demographic_proportions.jpg")

# Neighborhood Size
size_greened_data <- greened_data[c(12)]
size_greened_data$greened<-"greened"

size_vacant_data <- vacant_data[c(12)]
size_vacant_data$greened<-"not greened"

size_data <- rbind(size_greened_data, size_vacant_data)

melted_size_data <- melt(size_data, id=c("greened"))
p <- ggplot(melted_size_data, aes(x=reorder(variable, desc(variable)), y=value, fill=greened)) + 
        geom_boxplot() + 
        labs(x="Lot Type",y = "Population Size") +
        scale_fill_manual(values=c("chartreuse", "firebrick1"))
p + coord_flip()
ggsave("img/demographic/lot_population_size.jpg")

# Economic Data Size
econ_greened_data <- greened_data[c(29)]
econ_greened_data$greened<-"greened"

econ_vacant_data <- vacant_data[c(29)]
econ_vacant_data$greened<-"not greened"

econ_data <- rbind(econ_greened_data, econ_vacant_data)

melted_econ_data <- melt(econ_data, id=c("greened"))
p <- ggplot(melted_econ_data, aes(x=reorder(variable, desc(variable)), y=value, fill=greened)) + 
        geom_boxplot() + 
        labs(x="Lot Type",y = "Per Capita Income") +
        scale_fill_manual(values=c("chartreuse", "firebrick1")) +
        scale_x_discrete(labels=c(""))
p + coord_flip()
ggsave("img/demographic/lot_wealth.jpg")


col_names <- c("Civic-G", "Civic-V",
               "Commercial-G", "Commercial-V",
               "Cultural-G", "Cultural-V",
               "Industrial-G", "Industrial-V",
               "Other-G", "Other-V",
               "Transportation-G", "Transportation-V",
               "Vacant-G", "Vacant-V",
               "Water-G", "Water-V",
               "Residential-G", "Residential-V")


# Graph boxplot of zones per lot type
jpeg('img/zone_proportions.jpg', width = 800, height = 600)
par(mar=c(5,10,4,1)+.1)
boxplot(greened_data$Civic,
        vacant_data$Civic,
        greened_data$Commercial, 
        vacant_data$Commercial,
        greened_data$Cultural, 
        vacant_data$Cultural,
        greened_data$Industrial, 
        vacant_data$Industrial,
        greened_data$Other, 
        vacant_data$Other,
        greened_data$Transportation, 
        vacant_data$Transportation,
        greened_data$Vacant, 
        vacant_data$Vacant,
        greened_data$Water, 
        vacant_data$Water,
        greened_data$Residential, 
        vacant_data$Residential,
        main = "Land Use Proportions in Greened vs. Vacant Lots",
        at = c(1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26),
        las = 2,
        names = col_names,
        col = c("green", "red"),
        horizontal = TRUE,
        notch = TRUE
        )
dev.off()

col_names <- c("Not Hispanic or Latino-G", "Not Hispanic or Latino-V",
               "Not Hispanic or Latino White-G", "Not Hispanic or Latino White-V",
               "Not Hispanic or Latino Black-G", "Not Hispanic or Latino Black-V",
               "Not Hispanic or Latino Native American-G", "Not Hispanic or Latino Native American-V",
               "Not Hispanic or Latino Asian-G", "Not Hispanic or Latino Asian-V",
               "Not Hispanic or Latino Pacific Islander-G", "Not Hispanic or Latino Pacific Islander-V",
               "Not Hispanic or Latino Some Other Race-G", "Not Hispanic or Latino Some Other Race-V",
               "Not Hispanic or Latino Two or More Races-G", "Not Hispanic or Latino Two or More Races-V")

# Get the boxplot of the racial proportions (Non-hispanic)
jpeg('img/not_hispanic_demographic.jpg', width = 800, height = 600)
par(mar=c(5,18,4,1)+.1)
boxplot(greened_data[,13], vacant_data[,13],
        greened_data[,14], vacant_data[,14],
        greened_data[,15], vacant_data[,15],
        greened_data[,16], vacant_data[,16],
        greened_data[,17], vacant_data[,17],
        greened_data[,18], vacant_data[,18],
        greened_data[,19], vacant_data[,19],
        greened_data[,20], vacant_data[,20],
        main = "Proportion of Block that is Non-Hispanic Demographic",
        at = c(1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23),
        las=2,
        names=col_names,
        col = c("green", "red"),
        horizontal = TRUE,
        notch = TRUE
        )
dev.off()

# Get the boxplot of racial proportions (Hispanic)
col_names <- c("Hispanic or Latino-G", "Hispanic or Latino-V",
               "Hispanic or Latino White-G", "Hispanic or Latino White-V",
               "Hispanic or Latino Black-G", "Hispanic or Latino Black-V",
               "Hispanic or Latino Native American-G", "Hispanic or Latino Native American-V",
               "Hispanic or Latino Asian-G", "Hispanic or Latino Asian-V",
               "Hispanic or Latino Pacific Islander-G", "Hispanic or Latino Pacific Islander-V",
               "Hispanic or Latino Some Other Race-G", "Hispanic or Latino Some Other Race-V",
               "Hispanic or Latino Two or More Races-G", "Hispanic or Latino Two or More Races-V")

# Get the boxplot of the racial proportions (Non-hispanic)
jpeg('img/hispanic_demographic.jpg', width = 800, height = 600)
par(mar=c(5,18,4,1)+.1)
boxplot(greened_data[,21], vacant_data[,21],
        greened_data[,22], vacant_data[,22],
        greened_data[,23], vacant_data[,23],
        greened_data[,24], vacant_data[,24],
        greened_data[,25], vacant_data[,25],
        greened_data[,26], vacant_data[,26],
        greened_data[,27], vacant_data[,27],
        greened_data[,28], vacant_data[,28],
        main = "Proportion of Block that is Non-Hispanic Demographic",
        at = c(1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23),
        las=2,
        names=col_names,
        col = c("green", "red"),
        horizontal = TRUE,
        notch = TRUE
)
dev.off()

# Plot economic comparison
jpeg('img/economic_comparison.jpg', width = 800, height = 600)
par(mar=c(5,5,4,1)+.1)
boxplot(greened_data[,29], vacant_data[,29],
        main = "Per Capita Income 2015",
        las=2,
        names=c("Greened", "Vacant"),
        col = c("green", "red"),
        horizontal = TRUE,
        notch = TRUE
        )
dev.off()
