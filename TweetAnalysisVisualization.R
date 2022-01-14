# Generates a basic pie chart visualizing the sentiment of tweets
# related to the refugee crisis

percentages <- read.csv("sentiment_percentages.csv",sep = ",")

attach(percentages)

library(RColorBrewer)
myPalette <- brewer.pal(5, "Set2") 
slices <- c(Percent.Positive, Percent.Negative, Percent.Neutral)
labels <- c("Positive", "Negative", "Neutral")
percent <- round(slices / sum(slices) * 100)
labels <- paste(labels, percent) 
labels <- paste(labels, "%" ,sep="")
pie(slices,labels = lbls, col = myPalette, border = "white",
    main="Sentiments of Tweets Related to the US Refugee Crisis")

detach(percentages)
