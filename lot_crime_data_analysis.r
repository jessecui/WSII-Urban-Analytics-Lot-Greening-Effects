library(reshape2)
library(ggplot2)
library(plyr)
# Analyzes the crime data for greened and vacant lots

greened_data = read.csv("data/processed_data/greened_lots_crimes.csv")
summary(greened_data)

# Box and whisker plot for 100m radius data
data_100_meters = greened_data[,c("violent_100_before", "violent_100_after", "nonviolent_100_before", "nonviolent_100_after")]
stacked_data = stack(data_100_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_100_before", "violent_100_after", "nonviolent_100_before", "nonviolent_100_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/100_meters_ggplot.jpg")

# Box and whisker plot for 200m radius data
data_200_meters = greened_data[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
stacked_data = stack(data_200_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/200_meters_ggplot.jpg")


# Box and whisker plot for 500m radius data
data_500_meters = greened_data[,c("violent_500_before", "violent_500_after", "nonviolent_500_before", "nonviolent_500_after")]
stacked_data = stack(data_500_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_500_before", "violent_500_after", "nonviolent_500_before", "nonviolent_500_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/500_meters_ggplot.jpg")


# --- VACANT LOTS DATA ANALYSIS ---#
vacant_data = read.csv("data/processed_data/vacant_lots_crimes_final.csv")

# Box and whisker plot for 100m radius data
data_100_meters = vacant_data[,c("violent_100_before", "violent_100_after", "nonviolent_100_before", "nonviolent_100_after")]
stacked_data = stack(data_100_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_100_before", "violent_100_after", "nonviolent_100_before", "nonviolent_100_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/vacant_100_meters_ggplot.jpg")

# Box and whisker plot for 200m radius data
data_200_meters = vacant_data[,c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after")]
stacked_data = stack(data_200_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_200_before", "violent_200_after", "nonviolent_200_before", "nonviolent_200_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/vacant_200_meters_ggplot.jpg")


# Box and whisker plot for 500m radius data
data_500_meters = vacant_data[,c("violent_500_before", "violent_500_after", "nonviolent_500_before", "nonviolent_500_after")]
stacked_data = stack(data_500_meters)
stacked_data$ind <- factor(stacked_data$ind, levels = c("violent_500_before", "violent_500_after", "nonviolent_500_before", "nonviolent_500_after"), ordered = TRUE)

p <- ggplot(stacked_data, aes(x=reorder(ind, desc(ind)), y=values, fill=ind)) + 
        geom_boxplot() +
        scale_fill_manual(values=c("chartreuse", "firebrick1", "chartreuse", "firebrick1")) +
        theme(legend.position="none") +
        labs(x="Crime Type",y = "Crime Count") +
        scale_x_discrete(labels=c("Non-Violent After", "Non-Violent Before", "Violent After", "Violent Before"))
p + coord_flip()
ggsave("img/crimes/vacant_500_meters_ggplot.jpg")







# 100m radius data
jpeg('img/crime_100_meters.jpg', width = 800, height = 600)
par(mar=c(5,8,4,1)+.1)
boxplot(greened_data$violent_100_before,
        greened_data$violent_100_after,
        greened_data$nonviolent_100_before,
        greened_data$nonviolent_100_after,
        main = "100m Radius Crime Count in Greened Lots Interventions",
        las = 2,
        names = c("Violent Before", "Violent After", "Nonviolent Before", "Nonviolent After"),
        col = c("red", "green"),
        horizontal = TRUE,
        notch = TRUE)
dev.off()

# 200m radius data
jpeg('img/crime_200_meters.jpg', width = 800, height = 600)
par(mar=c(5,8,4,1)+.1)
boxplot(greened_data$violent_200_before,
        greened_data$violent_200_after,
        greened_data$nonviolent_200_before,
        greened_data$nonviolent_200_after,
        main = "100m Radius Crime Count in Greened Lots Interventions",
        las = 2,
        names = c("Violent Before", "Violent After", "Nonviolent Before", "Nonviolent After"),
        col = c("red", "green"),
        horizontal = TRUE,
        notch = TRUE)
dev.off()

# 500m radius data
jpeg('img/crime_500_meters.jpg', width = 800, height = 600)
par(mar=c(5,8,4,1)+.1)
boxplot(greened_data$violent_500_before,
        greened_data$violent_500_after,
        greened_data$nonviolent_500_before,
        greened_data$nonviolent_500_after,
        main = "100m Radius Crime Count in Greened Lots Interventions",
        las = 2,
        names = c("Violent Before", "Violent After", "Nonviolent Before", "Nonviolent After"),
        col = c("red", "green"),
        horizontal = TRUE,
        notch = TRUE)
dev.off()