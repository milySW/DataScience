player_data <-read.csv("player_data.csv", sep = ",", header = FALSE, fill = TRUE)
players_data <-read.csv("Players.csv", sep = ",", header = FALSE, fill = TRUE)
View(player_data)
View(players_data)

# Tworzymy tabelê na dane o wzroœcie i pozcyji graczy
mergedHeightAndPosition <- merge(player_data[ , c("V1", "V4")], players_data[ , c("V2", "V3", "V4")], by.x="V1", by.y="V2")
colnames(mergedHeightAndPosition) <- c("Player", "Position", "Height", "Weight")
View(mergedHeightAndPosition)

# Wczytujemy dane.
height <- mergedHeightAndPosition$Height
position <- mergedHeightAndPosition$Position
weight <- mergedHeightAndPosition$Weight


# Sprawdzamy w jaki sposób zapisane s¹ nasze dane.
summary(height)
summary(position)
summary(weight)

# Zmieniamy dane w wektor liczb.
height <- gsub(",", "", height)
height <- gsub("-", "", height)
height <- as.numeric(height, na.rm = TRUE)

weight <- gsub(",", "", weight)
weight <- gsub("-", "", weight)
weight <- as.numeric(weight, na.rm = TRUE)

# Z summary wynika, ¿e nie mamy pustych pól
# gdyby by³y height <- height[!is.na(height)]

# Wartoœci oczekiwane funkcj¹.
mean(height, na.rm = TRUE)
mean(weight, na.rm = TRUE)

# Wartoœci oczekiwane z definicji.
hMean_teo <- 0
wMean_teo <- 0
for(i in height){hMean_teo = hMean_teo + i}
for(i in weight){wMean_teo = wMean_teo + i}
hMean_teo <- hMean_teo/length(height)
wMean_teo <- wMean_teo/length(weight)

# Odchylenia standardowe funkcj¹.
sqrt(var(height, na.rm = TRUE))
sqrt(var(weight, na.rm = TRUE))

# Odchylenia standardowe z definicji.
hDeviation_teo <- 0
wDeviation_teo <- 0
for(i in height){hDeviation_teo = hDeviation_teo + i**2}
for(i in weight){wDeviation_teo = wDeviation_teo + i**2}
hDeviation_teo <- sqrt(hDeviation_teo/length(height) - hMean_teo**2)
wDeviation_teo <- sqrt(wDeviation_teo/length(weight) - wMean_teo**2)

# Wspó³czynnik zmiennoœci
coefficientHeight <- hDeviation_teo/hMean_teo * 100
coefficientWeight <- wDeviation_teo/wMean_teo * 100

# Mediany
hMedian <- median(height)
wMedian <- median(weight)

#Unikalne wartoœci
uniqueHeight <- length(unique(height))
uniqueWeight <- length(unique(weight))

# Najmniejsze wartoœci
min(height)
min(weight)

# Najwiêksze wartoœci
max(height)
max(weight)

# Kurtozy
install.packages("propagate")
library("propagate")
kurtosis(height)
kurtosis(weight)

# Wspó³czynniki skoœnoœci
skewness(height)
skewness(weight)

# Tworzymy listê pozycji.
uniquePositions <- unique(position)[1:7]

# Sprawdzamy jaka pozycja jest najpopularniejsza dla danego wzrostu.
listOfNames <- list()
listOfValues <- list()
for (heightValue in seq(from = 160, to = 230, by = 5))
{
  loopValue <- table(position[heightValue < height & height <= heightValue + 5])
  maxLoopValue <- max(loopValue)
  listOfValues <- c(listOfValues, maxLoopValue)
  for (name in uniquePositions)
  {
    if (loopValue[name] == maxLoopValue)
    {
      listOfNames <- c(listOfNames, name)
    }
    
  }
}

# Zmieniamy dane w wektor liczb.
listOfValues <- as.numeric(listOfValues, na.rm = TRUE)

# przygotowujemy wektor kolorów
listOfColors <- c("#88FF00", "#88FF00", "#88FF00", "#88FF00", 
                  "#6DFF00", "#88FF00", "#88FF00", "#88FF00", "#6DFF99", 
                  "#6DFF99", "#ECFF00", "#ECFF00", "#ECFF00", "#ECFF00", 
                  "#ECFF00")
# Przygotowujemy pole dla dwóch wykresów.
par(mfrow = c(1:2), mar=c(4.6,4.6,6,2.1))

# Histogram.
hist(height, main = "Histogram wzrostu graczy", xlab = "Wzrost [cm]", ylab = "Czêstotliwoœæ", col = "cyan", font = 2)

# Wykres wskazuj¹cy iloœæ graczy na najpoularniejszej pozycji dla danego wzrostu.
positionsPlot <- barplot(listOfValues, main = "Najpopularniejsza pozycja wzglêdem wzrostu", ylim=c(0,600), xlab = "Pozycja wzglêdem wzrostu", ylab = "Czêstotliwoœæ", names.arg = listOfNames, space = 0, cex.names = 1, font = 2, col = listOfColors)
legend("topright", 
       legend = c("Point Guard", "Shooting Guard", "Small Forward", "Center"), 
       fill = c("#88FF00", "#88FF00", "#6DFF99", "#ECFF00"))
text(x= positionsPlot, y= listOfValues + 25, labels=as.character(listOfValues),cex=0.8)


# Sprawdzamy jaka pozycja jest najpopularniejsza dla danej wagi.
listOfNames2 <- list()
listOfValues2 <- list()
for (weightValue in seq(from = 59, to = 160, by = 11))
{
  loopValue2 <- table(position[weightValue < weight & weight <= weightValue + 10])
  maxLoopValue2 <- max(loopValue2)
  listOfValues2 <- c(listOfValues2, maxLoopValue2)
  for (name in uniquePositions)
  {
    if (loopValue2[name] == maxLoopValue2)
    {
      listOfNames2 <- c(listOfNames2, name)
      break
    }
    
  }
}


# Zmieniamy dane w wektor liczb.
listOfValues2 <- as.numeric(listOfValues2, na.rm = TRUE)
listOfNames2 <- gsub("F-C", "", listOfNames2)


# przygotowujemy wektor kolorów
listOfColors2 <- c("#88FF00", "#88FF00", "#88FF00", "#6DFF99", 
                  "#6DFF99", "#ECFF00", "#ECFF00", "#ECFF00", "#ECFF00")
# Przygotowujemy pole dla dwóch wykresów.
par(mfrow = c(1:2), mar=c(4.6,4.6,6,2.1))

# Histogram.
hist(weight, main = "Histogram wagi graczy", xlab = "Waga [kg]", ylab = "Czêstotliwoœæ", col = "cyan", font = 2)

# Wykres wskazuj¹cy iloœæ graczy na najpoularniejszej pozycji dla danego wzrostu.
positionsPlot2 <- barplot(listOfValues2, main = "Najpopularniejsza pozycja wzglêdem wagi", ylim = c(0, 1300), xlab = "Pozycja wzglêdem wagi", ylab = "Czêstotliwoœæ", names.arg = listOfNames2, space = 0, cex.names = 0.8, font = 2, col = listOfColors2)
legend("topright", 
       legend = c("Point Guard", "Shooting Guard", "Small Forward", "Center"), 
       fill = c("#88FF00", "#88FF00", "#6DFF99", "#ECFF00"))
text(x = positionsPlot2, y= listOfValues2 + 35, labels=as.character(listOfValues2),cex=0.6)

# Sprawdzamy jaka jest proporcja wagi do wzrostu
listOfNames3 <- list()
listOfValues3 <- list()
for (propValue in seq(from = 0.35, to = 0.70, by = 0.05))
  
{
  loopValue3 <- table(position[propValue < weight/height & weight/height <= propValue + 0.05])
  maxLoopValue3 <- max(loopValue3)
  listOfValues3 <- c(listOfValues3, maxLoopValue3)
  for (name in uniquePositions)
  {
    if (loopValue3[name] == maxLoopValue3)
    {
      listOfNames3 <- c(listOfNames3, name)
      break
    }
    
  }
}

# Zmieniamy dane w wektor liczb.
listOfValues3 <- as.numeric(listOfValues3, na.rm = TRUE)
listOfNames3 <- gsub("F-C", "", listOfNames3)

# przygotowujemy wektor kolorów
listOfColors3 <- c("#88FF00", "#88FF00", "#6DFF99", "#6DFF99", 
                   "#ECFF00", "#ECFF00", "#ECFF00", "#ECFF00")
# Przygotowujemy pole dla dwóch wykresów.
par(mfrow = c(1:2), mar=c(4.6,4.6,6,2.1))

# Histogram.
hist(weight/height, main = "Histogram proporcji wagi do wzrostu", xlab = "Proporcja wagi do wzrostu", ylab = "Czêstotliwoœæ", col = "cyan", font = 2)

# Wykres wskazuj¹cy iloœæ graczy na najpoularniejszej pozycji dla danej proporcji.
positionsPlot3 <- barplot(listOfValues3, main = "Najpopularniejsza pozycja wzglêdem proporcji wagi do wzrostu", ylim = c(0, 1600), xlab = "Pozycja wzglêdem proporcji", ylab = "Czêstotliwoœæ", names.arg = listOfNames3, space = 0, cex.names = 0.8, font = 2, col = listOfColors3)
legend("topright", 
       legend = c("Point Guard", "Shooting Guard", "Small Forward", "Center"), 
       fill = c("#88FF00", "#88FF00", "#6DFF99", "#ECFF00"))
text(x = positionsPlot3, y= listOfValues3 + 35, labels=as.character(listOfValues3),cex=0.6)

# Dok³adne histogramy
par(mfrow = c(2,2))

hist(height, prob = TRUE, main = "Histogram wzrostu graczy(1)", ylim = c(0, 0.045), xlab = "Wzrost [cm]", ylab = "Gêstoœæ", col = "cyan", font = 2)
abline(v=hMean_teo,col="red")
abline(v=hMedian,col="purple")
lines(density(height), # density plot
      lwd = 2, # thickness of line
      col = "chocolate3")
legend(x = "topright", # location of legend within plot area
       c("Gêstoœæ", "Œrednia", "Mediana"),
       col = c("chocolate3", "red", "purple"),
       lwd = c(2, 2, 2))

hist(height, prob = TRUE, main = "Histogram wzrostu graczy(2)", xlab = "Wzrost [cm]", ylab = "Gêstoœæ", col = "cyan", font = 2, breaks = uniqueHeight)
abline(v=hMean_teo,col="red")
abline(v=hMedian,col="purple")
lines(density(height), # density plot
      lwd = 2, # thickness of line
      col = "chocolate3")
legend(x = "topright", # location of legend within plot area
       c("Gêstoœæ", "Œrednia", "Mediana"),
       col = c("chocolate3", "red", "purple"),
       lwd = c(2, 2, 2))


hist(weight,prob = TRUE, main = "Histogram wagi graczy(1)", xlab = "Waga [kg]", ylab = "Gêstoœæ", col = "cyan", font = 2)
abline(v=wMean_teo,col="red")
abline(v=wMedian,col="purple")
lines(density(weight), # density plot
      lwd = 2, # thickness of line
      col = "chocolate3")
legend(x = "topright", # location of legend within plot area
       c("Gêstoœæ", "Œrednia", "Mediana"),
       col = c("chocolate3", "red", "purple"),
       lwd = c(2, 2, 2))

hist(weight,prob = TRUE, main = "Histogram wagi graczy(2)", xlab = "Waga [kg]", ylab = "Gêstoœæ", col = "cyan", font = 2, breaks = uniqueWeight)
abline(v=wMean_teo,col="red")
abline(v=wMedian,col="purple")
lines(density(weight), # density plot
      lwd = 2, # thickness of line
      col = "chocolate3")
legend(x = "topright", # location of legend within plot area
       c("Gêstoœæ", "Œrednia", "Mediana"),
       col = c("chocolate3", "red", "purple"),
       lwd = c(2, 2, 2))

# Dystrybuanty
plot(ecdf(height), main = "Dystrybuanta wzrostu")
plot(ecdf(weight), main = "Dystrybuanta gêsoœci")

# Wspó³czynniki skoœnoœci dla wykresóW zwi¹zanych z pozycjami graczy.
skewness(listOfValues)
skewness(listOfValues2)
skewness(listOfValues3)

# Kurtoza dla wykresóW zwi¹zanych z pozycjami graczy.
kurtosis(listOfValues)
kurtosis(listOfValues2)
kurtosis(listOfValues3)

# Kwartyle
par(mfrow = c(1,2))

qh1 <- quantile(height, 0.25)
qh2 <- quantile(height, 0.5)
qh3 <- quantile(height, 0.75)
qplot1 <- cut(height, c(min(height) - 1, qh1, qh3, max(height)))
levels(qplot1) = c("160-190[cm]", "191-206[cm]", "207-231[cm]")
plot(qplot1, main = "Kwartyle wzrostu", col = "cyan", ylab = "Czêstotliwoœæ")

qw1 <- quantile(weight, 0.25)
qw2 <- quantile(weight, 0.5)
qw3 <- quantile(weight, 0.75)
qplot2 <- cut(weight, c(min(weight) - 1, qw1, qw3, max(weight)))
levels(qplot2) = c("60-86[kg]", "87-102[kg]", "103-163[kg]")
plot(qplot2, main = "Kwartyle wagi", col = "darkmagenta", ylab = "Czêstotliwoœæ")

par(mfrow = c(1,2))

boxplot(height, main = "Wykres pude³kowy wzrostu", ylab = "Wzrost [cm]", col=rgb(0.3,0.2,0.5,0.6))
boxplot(weight, main = "Wykres pude³kowy wagi", ylab = "Waga [kg]", col=rgb(0.3,0.2,0.5,0.6))

# Wykres rozrzutu
par(mfrow = c(1,2))

x <- height
y <- weight
z <- weight/height

plot(y, x, main = "Wykres wagi od wzrostu",
     xlab = "Wzrost [cm]", ylab = "Waga [kg]",
     pch = 19, frame = FALSE)
abline(lm(x ~ y, data = mergedHeightAndPosition), col = "magenta", lwd = 2)


plot(y, z, main = "Wykres proporcji od wzrostu",
     xlab = "Wzrost [cm]", ylab = "Proporcja wzrostu do wagi",
     pch = 19, frame = FALSE)
abline(lm(z ~ y, data = mergedHeightAndPosition), col = "magenta", lwd = 2)


