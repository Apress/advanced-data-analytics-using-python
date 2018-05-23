asm_weekwise<-read.csv("F:/souravda/New ASM Weekwise.csv",header=TRUE)

asm_weekwise$Week <- NULL

library(MASS, lib.loc="F:/souravda/lib/")
library(tseries, lib.loc="F:/souravda/lib/")
library(forecast, lib.loc="F:/souravda/lib/")

#asm_weekwise[is.na(asm_weekwise)] <- 0
#asm_weekwise[asm_weekwise <= 0] <- mean(as.matrix(asm_weekwise))




weekjoyforecastvalues <- data.frame( "asm" = integer(), "value" = integer(), stringsAsFactors=FALSE)

for(i in 1:ncol(asm_weekwise))
{
  asmname<-names(asm_weekwise)[i]
  temparimadata<-asm_weekwise[,i]
  temparimadata[is.na(temparimadata)] <- 0
  temparimadata[temparimadata <=0] <- mean(as.matrix(temparimadata))
  m <- mean(as.matrix(temparimadata))
  #print(m)
  s <- sd(temparimadata)
  #print(s)
  temparimadata <- (temparimadata - m)
  temparimadata <- (temparimadata / s)
  temparima<-auto.arima(temparimadata, stationary = FALSE, seasonal = TRUE, allowdrift = TRUE, allowmean = FALSE, biasadj = FALSE)
  tempforecast<-forecast(temparima,h=12)
  #tempforecast <- (tempforecast * s)
  #print(tempforecast)
  temp_forecasted_data<-sum(data.frame(tempforecast$upper[,1])*s + m)
  weekjoyforecastvalues[nrow(weekjoyforecastvalues) + 1, ] <- c( asmname, temp_forecasted_data)
}

weekjoyforecastvalues$value<-as.integer(weekjoyforecastvalues$value)

cat(weekjoyforecastvalues$value,sep="\n")

(sum(weekjoyforecastvalues$value)- 103000000)/103000000 #53782605)/53782605